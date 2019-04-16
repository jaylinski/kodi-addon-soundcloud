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
    api_limit = 20  # This value gets overridden in the constructor

    def __init__(self, settings):
        self.settings = settings
        self.api_limit = int(self.settings.get("search.items.size"))

    def search(self, query, kind="tracks"):
        res = self._do_request("/search/" + kind, {"q": query, "limit": self.api_limit})
        return self._map_json_to_collection(res)

    def discover(self, selection=None):
        res = self._do_request("/selections", {})

        if selection and "collection" in res:
            for category in res["collection"]:
                if category["id"] == selection:
                    res = {"collection": category["playlists"]}
                    break

        return self._map_json_to_collection(res)

    def call(self, url):
        url = urllib.parse.urlparse(url)
        res = self._do_request(url.path, urllib.parse.parse_qs(url.query))
        return self._map_json_to_collection(res)

    def resolve_url(self, url):
        url = urllib.parse.urlparse(url)
        res = self._do_request(url.path, urllib.parse.parse_qs(url.query))
        return res.get("url")

    def _do_request(self, path, payload):
        payload["client_id"] = self.api_client_id
        headers = {"Accept-Encoding": "gzip"}

        logging.info(
            "Calling %s with header %s and payload %s",
            self.api_host + path, str(headers), str(payload)
        )

        return requests.get(self.api_host + path, headers=headers, params=payload).json()

    def _extract_media_url(self, transcodings):
        setting = self.settings.get("audio.format")
        for codec in transcodings:
            if self._is_preferred_codec(codec["format"], self.settings.AUDIO_FORMATS[setting]):
                return codec["url"]

        # Fallback
        logging.warning("Could not find a matching codec, falling back to first value...")
        return transcodings[0]["url"]

    def _map_json_to_collection(self, json_obj):
        collection = ApiCollection()
        collection.next = json_obj.get("next_href", None)

        if "collection" in json_obj:

            for item in json_obj["collection"]:
                kind = item.get("kind", None)

                if kind == "track":
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

                elif kind == "selection" and "playlists" in item:  # TODO Implement system playlists
                    selection = Selection()
                    selection.id = item["id"]
                    selection.label = item.get("title")
                    selection.label2 = item.get("description", "")
                    collection.items.append(selection)

                else:
                    logging.warning("Could not convert JSON kind to model...")

        elif "tracks" in json_obj:

            artist = json_obj["user"]["username"]

            for item in json_obj["tracks"]:
                if "title" not in item:  # TODO Only the first 5 items are fully returned from the API.
                    break

                track = Track()
                track.id = item["id"]
                track.label = item["title"]
                track.label2 = json_obj["title"]
                track.thumb = item.get("artwork_url", None)
                track.media = self._extract_media_url(item["media"]["transcodings"])
                track.info = {
                    "artist": artist,
                    "genre": item.get("genre", None),
                    "date": item.get("display_date", None),
                    "description": item.get("description", None),
                    "duration": int(item["duration"]) / 1000
                }
                collection.items.append(track)

        else:
            raise RuntimeError("ApiV2 JSON seems to be invalid")

        return collection

    @staticmethod
    def _is_preferred_codec(codec, setting):
        if codec["mime_type"] == setting["mime_type"] and codec["protocol"] == setting["protocol"]:
            return True
