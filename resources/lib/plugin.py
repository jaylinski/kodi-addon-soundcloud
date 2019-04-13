from future import standard_library
standard_library.install_aliases()

from resources.lib.soundcloud.api_v2 import ApiV2
import urllib.parse
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo("name")
api = ApiV2()

PATH_ROOT = "/"
PATH_PLAY = "/play/"


def root_items():
    items = []
    li = xbmcgui.ListItem(label=addon.getLocalizedString(30101))
    url = sys.argv[0] + "?mode=search"
    items.append((url, li, True))
    return items


def create_items(collection):
    xbmc_items = []
    for item in collection.items:
        xbmc_item = xbmcgui.ListItem(label=item.label)
        xbmc_item.setArt({"thumb": item.thumb})
        xbmc_item.setInfo("music", {
            "artist": item.info.get("artist"),
            "comment": item.info.get("comment"),
            "duration": item.info.get("duration")
        })
        url = sys.argv[0] + "play/?" + urllib.parse.urlencode({"url": item.media})
        xbmc_items.append((url, xbmc_item, False))

    next_item = xbmcgui.ListItem(label=addon.getLocalizedString(30102))
    url = sys.argv[0] + "?" + urllib.parse.urlencode({"mode": "call", "call": collection.next})
    xbmc_items.append((url, next_item, True))

    return xbmc_items


def run():
    url = urllib.parse.urlparse(sys.argv[0])
    path = url.path
    handle = int(sys.argv[1])
    args = urllib.parse.parse_qs(sys.argv[2][1:])

    xbmcplugin.setContent(handle, 'songs')

    xbmc.log(sys.argv[0])
    xbmc.log(sys.argv[1])
    xbmc.log(sys.argv[2])
    xbmc.log(path)

    if path == PATH_ROOT:
        mode = args.get('mode', None)
        if mode is None:
            items = root_items()
            xbmcplugin.addDirectoryItems(handle, items, len(items))
            xbmcplugin.endOfDirectory(handle)
        elif "search" in mode:
            search = xbmcgui.Dialog().input(addon.getLocalizedString(30101))
            collection = create_items(api.search(search))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        elif "call" in mode:
            xbmc.log("url: " + args.get("call")[0], xbmc.LOGINFO)
            collection = create_items(api.call(args.get("call")[0]))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
    elif path == PATH_PLAY:
        url = args.get("url", [""])[0]
        if url:
            resolved_url = api.resolve_media_url(url)
            xbmc.Player().play(resolved_url)
        else:
            xbmc.log("Action not supported", xbmc.LOGERROR)
    else:
        xbmc.log("Path not found", xbmc.LOGERROR)
