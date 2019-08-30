from future import standard_library
standard_library.install_aliases()  # noqa: E402

from resources.lib.kodi.utils import format_bold
from resources.routes import *

import urllib.parse
import xbmcgui


class Items:
    def __init__(self, addon, addon_base, search_history):
        self.addon = addon
        self.addon_base = addon_base
        self.search_history = search_history

    def root(self):
        items = []

        # Search
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30101))
        url = self.addon_base + PATH_SEARCH
        items.append((url, list_item, True))

        # Charts
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30102))
        url = self.addon_base + PATH_CHARTS
        items.append((url, list_item, True))

        # Discover
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30103))
        url = self.addon_base + PATH_DISCOVER
        items.append((url, list_item, True))

        # Settings
        list_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30108))
        url = self.addon_base + "/?action=settings"
        items.append((url, list_item, False))

        # Sign in TODO
        # list_item = xbmcgui.ListItem(label=addon.getLocalizedString(30109))
        # url = addon_base + "/action=signin"
        # items.append((url, list_item, False))

        return items

    def search(self):
        items = []

        # New search
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30201)))
        url = self.addon_base + PATH_SEARCH + "?action=new"
        items.append((url, list_item, True))

        # Search history
        history = self.search_history.get()
        for k in sorted(list(history), reverse=True):
            list_item = xbmcgui.ListItem(label=history[k].get("query"))
            url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
                "query": history[k].get("query")
            })
            items.append((url, list_item, True))

        return items

    def search_sub(self, query):
        items = []

        # People
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30211)))
        url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "people",
            "query": query
        })
        items.append((url, list_item, True))

        # Albums
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30212)))
        url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "albums",
            "query": query
        })
        items.append((url, list_item, True))

        # Playlists
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30213)))
        url = self.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
            "action": "playlists",
            "query": query
        })
        items.append((url, list_item, True))

        return items

    def charts(self):
        items = []

        # Top 50
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30301)))
        url = self.addon_base + PATH_CHARTS + "?" + urllib.parse.urlencode({
            "action": "top"
        })
        items.append((url, list_item, True))

        # Trending
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30302)))
        url = self.addon_base + PATH_CHARTS + "?" + urllib.parse.urlencode({
            "action": "trending"
        })
        items.append((url, list_item, True))

        return items

    def charts_genres(self):
        items = []

        # Music genres
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30310)))
        url = self.addon_base + PATH_CHARTS + "?" + urllib.parse.urlencode({
            "action": "top"
        })
        items.append((url, list_item, True))

        # Audio genres
        list_item = xbmcgui.ListItem(label=format_bold(self.addon.getLocalizedString(30311)))
        url = self.addon_base + PATH_CHARTS + "?" + urllib.parse.urlencode({
            "action": "trending"
        })
        items.append((url, list_item, True))

        """
alternativerock: n(51).t('Alternative Rock'),
ambient: n(51).t('Ambient'),
classical: n(51).t('Classical'),
country: n(51).t('Country'),
danceedm: n(51).t('Dance &amp; EDM'),
dancehall: n(51).t('Dancehall'),
deephouse: n(51).t('Deep House'),
disco: n(51).t('Disco'),
drumbass: n(51).t('Drum &amp; Bass'),
dubstep: n(51).t('Dubstep'),
electronic: n(51).t('Electronic'),
folksingersongwriter: n(51).t('Folk &amp; Singer-Songwriter'),
hiphoprap: n(51).t('Hip-hop &amp; Rap'),
house: n(51).t('House'),
indie: n(51).t('Indie'),
jazzblues: n(51).t('Jazz &amp; Blues'),
latin: n(51).t('Latin'),
metal: n(51).t('Metal'),
piano: n(51).t('Piano'),
pop: n(51).t('Pop'),
rbsoul: n(51).t('R&B &amp; Soul'),
reggae: n(51).t('Reggae'),
reggaeton: n(51).t('Reggaeton'),
rock: n(51).t('Rock'),
soundtrack: n(51).t('Soundtrack'),
speech: n(51).t('Speech'),
techno: n(51).t('Techno'),
trance: n(51).t('Trance'),
trap: n(51).t('Trap'),
triphop: n(51).t('Triphop'),
world: n(51).t('World'),
audiobooks: n(51).t('Audiobooks'),
business: n(51).t('Business'),
comedy: n(51).t('Comedy'),
entertainment: n(51).t('Entertainment'),
learning: n(51).t('Learning'),
newspolitics: n(51).t('News &amp; Politics'),
religionspirituality: n(51).t('Religion &amp; Spirituality'),
science: n(51).t('Science'),
sports: n(51).t('Sports'),
storytelling: n(51).t('Storytelling'),
technology: n(51).t('Technology')
},
"""

        return items

    def from_collection(self, collection):
        items = []

        for item in collection.items:
            items.append(item.to_list_item(self.addon_base))

        if collection.next_href:
            next_item = xbmcgui.ListItem(label=self.addon.getLocalizedString(30901))
            url = self.addon_base + "/?" + urllib.parse.urlencode({
                "action": "call",
                "call": collection.next_href
            })
            items.append((url, next_item, True))

        return items
