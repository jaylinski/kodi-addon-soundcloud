from future import standard_library
standard_library.install_aliases()

from resources.lib.soundcloud.api_v2 import ApiV2
from resources.lib.kodi.items import Items
from resources.lib.kodi.settings import Settings
from resources.routes import *
import urllib.parse
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo("id")
addon_base = "plugin://" + addon_id
settings = Settings(addon)
api = ApiV2(settings)
listItems = Items(addon, addon_base)


def run():
    url = urllib.parse.urlparse(sys.argv[0])
    path = url.path
    handle = int(sys.argv[1])
    args = urllib.parse.parse_qs(sys.argv[2][1:])
    xbmcplugin.setContent(handle, 'songs')

    # TODO Remove debug output
    xbmc.log(str(sys.argv))
    xbmc.log(addon_base)
    xbmc.log(path)

    if path == PATH_ROOT:
        action = args.get("action", None)
        if action is None:
            items = listItems.root()
            xbmcplugin.addDirectoryItems(handle, items, len(items))
            xbmcplugin.endOfDirectory(handle)
        elif "call" in action:
            xbmc.log("plugin.audio.soundcloud::call()  " + args.get("call")[0], xbmc.LOGINFO)
            collection = listItems.from_collection(api.call(args.get("call")[0]))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        elif "settings" in action:
            addon.openSettings()
        else:
            xbmc.log("Invalid root action", xbmc.LOGERROR)

    elif path == PATH_DISCOVER:
        selection = args.get("selection", [None])[0]
        collection = listItems.from_collection(api.discover(selection))
        xbmcplugin.addDirectoryItems(handle, collection, len(collection))
        xbmcplugin.endOfDirectory(handle)

    elif path == PATH_PLAY:
        # Public params
        track_id = args.get("track_id", [None])[0]
        playlist_id = args.get("playlist_id", [None])[0]
        url = args.get("url", [None])[0]

        # Public legacy params (deprecated)
        audio_id_legacy = args.get("audio_id", [None])[0]
        track_id = audio_id_legacy if audio_id_legacy else track_id

        # Private params
        media_url = args.get("media_url", [None])[0]

        if media_url:
            resolved_url = api.resolve_media_url(media_url)
            item = xbmcgui.ListItem(path=resolved_url)
            xbmcplugin.setResolvedUrl(handle, succeeded=True, listitem=item)
        elif track_id:
            collection = listItems.from_collection(api.resolve_id(track_id))
            playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
            playlist.add(url=collection[0][0], listitem=collection[0][1])
        elif playlist_id:
            call = "/playlists/{id}".format(id=playlist_id)
            collection = listItems.from_collection(api.call(call))
            playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
            for item in collection:
                playlist.add(url=item[0], listitem=item[1])
        elif url:
            collection = listItems.from_collection(api.resolve_url(url))
            playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
            for item in collection:
                playlist.add(url=item[0], listitem=item[1])
        else:
            xbmc.log("Invalid play param", xbmc.LOGERROR)

    elif path == PATH_SEARCH:
        action = args.get("action", None)
        query = args.get("query", "")
        if action is None:
            items = listItems.search()
            xbmcplugin.addDirectoryItems(handle, items, len(items))
            xbmcplugin.endOfDirectory(handle)
        elif "new" in action:
            search = xbmcgui.Dialog().input(addon.getLocalizedString(30101))
            search_options = listItems.search_sub(search)
            collection = listItems.from_collection(api.search(search))
            xbmcplugin.addDirectoryItems(handle, search_options, len(collection))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        elif "people" in action:
            xbmcplugin.setContent(handle, 'artists')
            collection = listItems.from_collection(api.search(query, "users"))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        elif "albums" in action:
            xbmcplugin.setContent(handle, 'albums')
            collection = listItems.from_collection(api.search(query, "albums"))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        elif "playlists" in action:
            xbmcplugin.setContent(handle, 'albums')
            collection = listItems.from_collection(api.search(query, "playlists_without_albums"))
            xbmcplugin.addDirectoryItems(handle, collection, len(collection))
            xbmcplugin.endOfDirectory(handle)
        else:
            xbmc.log("Invalid search action", xbmc.LOGERROR)

    else:
        xbmc.log("Path not found", xbmc.LOGERROR)
