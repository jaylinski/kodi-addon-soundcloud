import requests


class ApiMobile:
    """This class uses the unofficial API used by the SoundCloud mobile app."""

    api_host = "https://api-mobile.soundcloud.com"
    api_client_id = "dbdsA8b6V6Lw7wzu1x0T4CLxt58yd4Bf"
    api_client_secret = "aBK1xbehZvrBw0dtVYNY3BuJJOuDFrYs"
    api_user_agent = "SoundCloud/2021.06.02-release (Android 11; Google sdk_gphone_x86)"
    api_udid = "4787dcf7a801d396b5f3cfa654fd89ae"  # Unique Device Identifier

    def __init__(self, settings, lang, cache):
        self.cache = cache
        self.settings = settings
        self.lang = lang

    def authenticate(self, identifier, password):
        url = self.api_host + "/sign_in"

        params = {
            "client_id": self.api_client_id,
        }

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": self.api_user_agent,
            "UDID": self.api_udid,
        }

        payload = {
            "auth_method": "password",
            "captcha_pubkey": "6LfuZ08UAAAAAEzW09iSDSG5t4ygnyGNz5ZGfj5h",
            "captcha_solution": None,
            "client_id": self.api_client_id,
            "client_secret": self.api_client_secret,
            "create_if_not_found": False,
            "credentials": {
                "identifier": identifier,
                "password": password,
            },
            "flags": {},
            "signature": "2:f3b1d672",
        }

        response = requests.post(url, params=params, json=payload, headers=headers).json()

        return response.token.access_token

