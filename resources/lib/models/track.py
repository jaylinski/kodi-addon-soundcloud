from future import standard_library
standard_library.install_aliases()  # noqa: E402

from resources.lib.models.list_item import ListItem
import urllib.parse
import xbmcaddon
import xbmcgui


class Track(ListItem):
    blocked = False
    thumb = ""
    media = ""
    info = {}

    def to_list_item(self, addon_base):
        blocked = xbmcaddon.Addon().getLocalizedString(30902)
        list_item_label = "[%s] " % blocked + self.label if self.blocked else self.label
        list_item = xbmcgui.ListItem(label=list_item_label)
        url = addon_base + "/play/?" + urllib.parse.urlencode({"media_url": self.media})
        list_item.setArt({"thumb": self.thumb})
        list_item.setInfo("music", {
            "artist": self.info.get("artist"),
            "duration": self.info.get("duration"),
            "genre": self.info.get("genre"),
            "title": self.label,
            "year": self.info.get("date")[:4]
            # Is there a way to add the description?
            # "xxx": item.info.get("description")
        })
        list_item.setProperty("isPlayable", "true")

        return url, list_item, False
