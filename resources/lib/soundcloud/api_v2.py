from future import standard_library
standard_library.install_aliases()

import logging
import requests
import urllib.parse

from resources.lib.models.playlist import Playlist
from resources.lib.models.track import Track
from resources.lib.models.selection import Selection
from resources.lib.models.user import User
from resources.lib.soundcloud.api_collection import ApiCollection
from resources.lib.soundcloud.api_interface import ApiInterface


class ApiV2(ApiInterface):
    """This class uses the unofficial API used by the SoundCloud website."""

    api_host = "https://api-v2.soundcloud.com"
    api_client_id = "FweeGBOOEOYJWLJN3oEyToGLKhmSz0I7"
    api_limit = 20  # This default value gets overridden in the constructor
    api_lang = "en"  # This default value gets overridden in the constructor

    def __init__(self, settings, lang):
        self.settings = settings
        self.api_lang = lang
        self.api_limit = int(self.settings.get("search.items.size"))

    def search(self, query, kind="tracks"):
        res = self._do_request("/search/" + kind, {"q": query, "limit": self.api_limit})
        return self._map_json_to_collection(res)

    def discover(self, selection_id=None):
        # TODO Cache response! (Also take a look at https://soundcloud.com/charts)
        res = self._do_request("/selections", {})

        if selection_id and "collection" in res:
            res = self._find_id_in_selection(res["collection"], selection_id)
            res = {"collection": res}

        return self._map_json_to_collection(res)

    def call(self, url):
        url = urllib.parse.urlparse(url)
        res = self._do_request(url.path, urllib.parse.parse_qs(url.query))
        return self._map_json_to_collection(res)

    def resolve_id(self, id):
        res = self._do_request("/tracks", {"ids": id})
        return self._map_json_to_collection({"collection": res})

    def resolve_url(self, url):
        res = self._do_request("/resolve", {"url": url})
        return self._map_json_to_collection(res)

    def resolve_media_url(self, url):
        url = urllib.parse.urlparse(url)
        res = self._do_request(url.path, urllib.parse.parse_qs(url.query))
        return res.get("url")

    def _do_request(self, path, payload):
        payload["client_id"] = self.api_client_id
        payload["app_locale"] = self.api_lang
        headers = {"Accept-Encoding": "gzip"}

        logging.info(
            "plugin.audio.soundcloud::ApiV2() Calling %s with header %s and payload %s",
            self.api_host + path, str(headers), str(payload)
        )

        return requests.get(self.api_host + path, headers=headers, params=payload).json()

    def _extract_media_url(self, transcodings):
        setting = self.settings.get("audio.format")
        for codec in transcodings:
            if self._is_preferred_codec(codec["format"], self.settings.AUDIO_FORMATS[setting]):
                return codec["url"]

        # Fallback
        logging.warning("plugin.audio.soundcloud::ApiV2() "
                        "Could not find a matching codec, falling back to first value...")
        return transcodings[0]["url"]

    def _find_id_in_selection(self, selection, selection_id):
        for category in selection:
            if category["id"] == selection_id:
                if "playlists" in category:
                    return category["playlists"]
                elif "system_playlists" in category:
                    return category["system_playlists"]
                elif "tracks" in category:
                    return category["tracks"]
            elif "system_playlists" in category:
                res = self._find_id_in_selection(category["system_playlists"], selection_id)
                if res:
                    return res

    def _map_json_to_collection(self, json):
        collection = ApiCollection()
        collection.items = []  # Reset list in order to resolve problems in unit tests.
        collection.load = []
        collection.next = json.get("next_href", None)

        if "kind" in json and json["kind"] == "track":
            # If we are dealing with a single track, pack it into a dict
            json = {"collection": [json]}

        if "collection" in json:

            for item in json["collection"]:
                kind = item.get("kind", None)

                if kind == "track":
                    if "title" not in item:
                        # Track not fully returned by API
                        collection.load.append(item["id"])
                        continue

                    track = self._build_track(item)
                    collection.items.append(track)

                elif kind == "user":
                    user = User()
                    user.id = item["id"]
                    user.label = item["username"]
                    user.label2 = item.get("full_name", "")
                    user.thumb = item.get("avatar_url", None)
                    user.info = {
                        "artist": item.get("description", None)
                    }
                    collection.items.append(user)

                elif kind == "playlist":
                    playlist = Playlist()
                    playlist.id = item["id"]
                    playlist.is_album = item.get("is_album", False)
                    playlist.label = item.get("title")
                    playlist.label2 = item.get("label_name", "")
                    playlist.thumb = item.get("artwork_url", None)
                    playlist.info = {
                        "artist": item["user"]["username"]
                    }
                    collection.items.append(playlist)

                elif kind == "system-playlist":
                    playlist = Selection()  # System playlists only appear inside selections
                    playlist.id = item["id"]
                    playlist.label = item.get("title")
                    playlist.thumb = item.get("calculated_artwork_url", None)
                    collection.items.append(playlist)

                elif kind == "selection":
                    selection = Selection()
                    selection.id = item["id"]
                    selection.label = item.get("title")
                    selection.label2 = item.get("description", "")
                    collection.items.append(selection)

                else:
                    logging.warning("plugin.audio.soundcloud::ApiV2() "
                                    "Could not convert JSON kind to model...")

        elif "tracks" in json:

            for item in json["tracks"]:
                if "title" not in item:
                    # Track not fully returned by API
                    collection.load.append(item["id"])
                    continue

                track = self._build_track(item)
                track.label2 = json["title"]
                collection.items.append(track)

        else:
            raise RuntimeError("ApiV2 JSON seems to be invalid")

        # Load unresolved tracks
        if collection.load:
            track_ids = ",".join(str(x) for x in collection.load)
            loaded_tracks = self._do_request("/tracks", {"ids": track_ids})
            # Because returned tracks are not sorted, we have to manually match them
            for track_id in collection.load:
                loaded_track = [lt for lt in loaded_tracks if lt["id"] == track_id]
                if len(loaded_track):  # Sometimes a track can not be resolved
                    track = self._build_track(loaded_track[0])
                    collection.items.append(track)

        return collection

    def _build_track(self, item):
        # TODO Check for country blocks. (policy: "BLOCK", no media transcodings)
        # Example blocked in Austria:
        # https://api-v2.soundcloud.com/playlists/327013762?client_id=FweeGBOOEOYJWLJN3oEyToGLKhmSz0I7

        if type(item.get("publisher_metadata")) is dict:
            artist = item["publisher_metadata"].get("artist", item["user"]["username"])
        else:
            artist = item["user"]["username"]

        track = Track()
        track.id = item["id"]
        track.label = item["title"]
        track.thumb = item.get("artwork_url", None)
        track.media = self._extract_media_url(item["media"]["transcodings"])
        track.info = {
            "artist": artist,
            "genre": item.get("genre", None),
            "date": item.get("display_date", None),
            "description": item.get("description", None),
            "duration": int(item["duration"]) / 1000
        }

        return track

    @staticmethod
    def _is_preferred_codec(codec, setting):
        if codec["mime_type"] == setting["mime_type"] and codec["protocol"] == setting["protocol"]:
            return True
