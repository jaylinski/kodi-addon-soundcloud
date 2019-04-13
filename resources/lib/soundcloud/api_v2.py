from future import standard_library
standard_library.install_aliases()

import logging
import requests
import urllib.parse

from resources.lib.models.track import Track
from resources.lib.soundcloud.api_collection import ApiCollection
from resources.lib.soundcloud.api_interface import ApiInterface


class ApiV2(ApiInterface):
    """This class uses the unofficial API used by the SoundCloud website."""

    api_host = "https://api-v2.soundcloud.com"
    api_client_id = "9yZSvlXAK7Wmu4xhb0hdMtjP9D2z351X"
    api_limit = 30

    def _do_request(self, path, payload):
        payload["client_id"] = self.api_client_id
        headers = {"Accept-Encoding": "gzip"}

        logging.info(
            "Calling %s with header %s and payload %s",
            self.api_host + path, str(headers), str(payload)
        )

        return requests.get(self.api_host + path, headers=headers, params=payload).json()

    def _extract_media_url(self, transcodings):
        for transcoding in transcodings:
            if transcoding["format"]["mime_type"] == "audio/ogg; codecs=\"opus\"":
                return transcoding["url"]

        # Fallback
        return transcodings[0]["url"]

    def _map_json_to_collection(self, json_obj):
        collection = ApiCollection()
        collection.next = json_obj.get("next_href", None)

        for item in json_obj["collection"]:
            if type(item.get("publisher_metadata")) is dict:
                artist = item["publisher_metadata"].get("artist", item["user"]["username"])
            else:
                artist = item["user"]["username"]

            track = Track()
            track.id = item["id"]
            track.label = item["title"]
            track.thumb = item["artwork_url"]
            track.media = self._extract_media_url(item["media"]["transcodings"])
            track.info = {
                "artist": artist,
                "genre": item["genre"],
                "date": item["display_date"],
                "comment": item["description"],
                "duration": int(item["duration"]) / 100
            }
            collection.items.append(track)

        return collection

    def search(self, query):
        res = self._do_request("/search/tracks", {"q": query, "limit": self.api_limit})
        return self._map_json_to_collection(res)

    def call(self, url):
        url = urllib.parse.urlparse(url)
        res = self._do_request(url.path, urllib.parse.parse_qs(url.query))
        return self._map_json_to_collection(res)

    def resolve_media_url(self, url):
        url = urllib.parse.urlparse(url)
        res = self._do_request(url.path, urllib.parse.parse_qs(url.query))
        return res.get("url")
