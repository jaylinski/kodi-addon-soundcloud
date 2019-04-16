from future import standard_library
standard_library.install_aliases()

from resources.lib.models.list_item import ListItem
import urllib.parse
import xbmcgui


class Track(ListItem):
    thumb = ""
    media = ""
    info = {}

    def to_list_item(self, addon_base):
        list_item = xbmcgui.ListItem(label=self.label)
        url = addon_base + "/play/?" + urllib.parse.urlencode({"media_url": self.media})
        list_item.setArt({"thumb": self.thumb})
        list_item.setInfo("music", {
            "artist": self.info.get("artist"),
            "duration": self.info.get("duration"),
            "genre": self.info.get("genre"),
            "title": self.label,
            "year": self.info.get("date")[:4]
            # "title": item.info.get("description") TODO Add desc
        })
        list_item.setProperty("isPlayable", "true")

        return url, list_item, False
