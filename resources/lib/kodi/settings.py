class Settings:
    AUDIO_FORMATS = {
        "0": {
            "mime_type": "audio/ogg; codecs=\"opus\"",
            "protocol": "hls",
        },
        "1": {
            "mime_type": "audio/mpeg",
            "protocol": "hls",
        }
    }

    def __init__(self, addon):
        self.addon = addon

    def get(self, id):
        return self.addon.getSetting(id)
