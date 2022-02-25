from resources.lib.models.list_item import ListItem
import urllib.parse
import xbmcaddon
import xbmcgui
import xbmc

blocked = xbmcaddon.Addon().getLocalizedString(30902)
preview = xbmcaddon.Addon().getLocalizedString(30903)


class Track(ListItem):
    blocked = False
    preview = False
    thumb = ""
    media = ""
    info = {}

    def to_list_item(self, addon_base, dataPath=None):
        list_item_label = "[%s] " % blocked + self.label if self.blocked else self.label
        list_item_label = "[%s] " % preview + self.label if self.preview else list_item_label
        list_item = xbmcgui.ListItem(label=list_item_label)
        url = addon_base + "/play/?" + urllib.parse.urlencode({"media_url": self.media})
        list_item.setArt({"thumb": self.thumb})
        list_item.setInfo("music", {
            "artist": self.info.get("artist"),
            "duration": self.info.get("duration"),
            "genre": self.info.get("genre"),
            "title": self.label,
            "year": self.info.get("date")[:4],
            "comment": self.info.get("description")
        })
        list_item.setProperty("isPlayable", "true")
        list_item.setProperty("mediaUrl", self.media)
        if dataPath:
            list_item.addContextMenuItems([(
                "Add To My Favourites",
                "RunScript({0}/resources/manageFav.py,{1},{2},{3}:{4})".format(
                    xbmc.translatePath("special://home/addons/plugin.audio.soundcloud"),
                    dataPath,
                    "add:track",
                    list_item_label.encode('utf-8'),
                    self.id
                )
            )])

        return url, list_item, False
