import requests
from resources.lib.soundcloud.api_interface import ApiInterface


class ApiPublic(ApiInterface):
    """This class uses the official SoundCloud API."""

    api_host = "https://api.soundcloud.com/"

    def _do_request(self, path, payload):
        return requests.get(self.api_host + path, params=payload).json()

    def search(self, query, kind):
        pass

    def call(self, url):
        pass

    def discover(self):
        pass

    def resolve_url(self, url):
        pass
