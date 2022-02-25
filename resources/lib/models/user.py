from resources.lib.models.list_item import ListItem
from resources.routes import PATH_USER
import urllib
import xbmcgui
import xbmc


class User(ListItem):
    thumb = ""
    info = {}

    def to_list_item(self, addon_base, dataPath):
        list_item = xbmcgui.ListItem(label=self.label, label2=self.label2)
        list_item.setArt({"thumb": self.thumb})
        list_item.setInfo("music", {
            "title": self.info.get("description")
        })
        url = addon_base + PATH_USER + "?" + urllib.parse.urlencode({
            "id": self.id,
            "call": "/users/{id}/tracks".format(id=self.id)
        })
        list_item.addContextMenuItems([(
            "Add To My Favourites",
            "RunScript({0}/resources/manageFav.py,{1},{2},{3}:{4})".format(
                 xbmc.translatePath("special://home/addons/plugin.audio.soundcloud"),
                 dataPath,
                 "add:user",
                 self.label.encode('utf-8'),
                 self.id
                 )
             )])

        return url, list_item, True

    def sanitizedName(self):
        return self.label.replace(" ", "_")
