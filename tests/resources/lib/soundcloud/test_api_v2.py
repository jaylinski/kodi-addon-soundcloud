import json
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock, DEFAULT, ANY
sys.modules['xbmc'] = MagicMock()
sys.modules['xbmcaddon'] = MagicMock()
sys.modules['xbmcgui'] = MagicMock()
from resources.lib.soundcloud.api_v2 import ApiV2


class ApiV2TestCase(TestCase):
    def setUp(self):
        self.api = ApiV2(settings=MagicMock(), lang="en", cache=MagicMock())

    @staticmethod
    def _side_effect_do_request(*args):
        if args[0] == "/tracks":
            with open("./tests/mocks/api_v2_discover_tracks.json") as f:
                mock_data = f.read()
            return json.loads(mock_data)
        else:
            return DEFAULT

    def test_search(self):
        with open("./tests/mocks/api_v2_search_tracks.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo")

        self.assertEqual(res.items[0].label, "Deadmau5 - Raise Your Weapon (Noisia Remix)")
        self.assertEqual(res.items[0].info["artist"], "NOISIA")
        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:15784497/580ad806-b3ab-440f-adbe-c12a83258a37/stream/hls")
        self.assertEqual(res.items[1].label, "Labrinth ft. Tinie Tempah - Earthquake (Noisia Remix)")
        self.assertEqual(res.items[1].info["artist"], "NOISIA")
        self.assertEqual(res.items[1].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:23547065/e7846551-5c8e-4b93-b4f0-f94bfa7b1275/stream/hls")

    def test_discover(self):
        with open("./tests/mocks/api_v2_discover.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))
        self.api._do_request.side_effect = self._side_effect_do_request

        # Level 1
        res = self.api.discover()
        self.assertEqual(res.items[0].label, "Chill")
        self.assertEqual(res.items[1].label, "Party")
        self.assertEqual(res.items[2].label, "Charts: New & hot")
        self.assertEqual(res.items[3].label, "Charts: Top 50")

        # Level 2
        res = self.api.discover("soundcloud:selections:charts-top")
        self.assertEqual(res.items[0].label, "Top 50: All music genres")
        self.assertEqual(res.items[1].label, "Top 50: Alternative Rock")
        self.assertEqual(res.items[2].label, "Top 50: Ambient")

        # Level 3
        res = self.api.discover("soundcloud:system-playlists:charts-top:all-music:at")
        self.assertEqual(res.load[0], 539018871)
        self.assertEqual(res.load[1], 603185304)
        self.assertEqual(res.items[0].label, "Old Town Road (I Got The Horses In The Back) [Prod. YoungKio]")
        self.assertEqual(res.items[1].label, "Capital Bra ft. Summer Cem & KC Rebell - Rolex (Official Audio)")

    def test_charts(self):
        with open("./tests/mocks/api_v2_charts.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.charts({})
        self.assertEqual(res.items[0].label, "Stop Snitchin")
        self.assertEqual(res.items[0].preview, True)
        self.assertEqual(res.items[1].label, "Young Nudy X Playboi Carti - Pissy Pamper Aka KID CUDI (Slimerre Shit)")
        self.assertEqual(res.items[1].preview, False)

    def test_blocked(self):
        with open("./tests/mocks/api_v2_tracks_blocked.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id("country blocks suck")
        self.assertEqual(res.items[0].blocked, True)

    def test_resolve_url(self):
        with open("./tests/mocks/api_v2_resolve_track.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_url("https://m.soundcloud.com/user/foo")
        # The SoundCloud APIv2 can't resolve mobile links (m.soundcloud.com), so they have to
        # be fixed manually. The following assertion is testing this.
        self.api._do_request.assert_called_with(ANY, {"url": "https://soundcloud.com/user/foo"})
        self.assertEqual(res.items[0].label, "Thomas Hayden - Universe")
