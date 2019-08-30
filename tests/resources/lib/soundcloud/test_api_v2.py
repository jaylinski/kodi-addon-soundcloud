import json
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock, DEFAULT, ANY
sys.modules['xbmc'] = MagicMock()
sys.modules['xbmcaddon'] = MagicMock()
sys.modules['xbmcgui'] = MagicMock()
from resources.lib.kodi.settings import Settings
from resources.lib.soundcloud.api_v2 import ApiV2


class ApiV2TestCase(TestCase):
    def setUp(self):
        self.api = ApiV2(settings=Settings(MagicMock()), lang="en", cache=MagicMock())
        self.api.settings.get = self._side_effect_settings_get

    @staticmethod
    def _side_effect_do_request(*args):
        if args[0] == "/tracks":
            with open("./tests/mocks/api_v2_discover_tracks.json") as f:
                mock_data = f.read()
            return json.loads(mock_data)
        else:
            return DEFAULT

    @staticmethod
    def _side_effect_settings_get(*args):
        if args[0] == "audio.format":
            return "2"  # Default in settings (mp3 progressive)
        else:
            return DEFAULT

    def test_search(self):
        with open("./tests/mocks/api_v2_search_tracks.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo")

        self.assertEqual(res.items[0].label, "Deadmau5 - Raise Your Weapon (Noisia Remix)")
        self.assertEqual(res.items[0].info["artist"], "NOISIA")
        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:15784497/580ad806-b3ab-440f-adbe-c12a83258a37/stream/progressive")
        self.assertEqual(res.items[0].thumb, "https://i1.sndcdn.com/artworks-000007527658-smjpzh-t500x500.jpg")

        self.assertEqual(res.items[1].label, "Labrinth ft. Tinie Tempah - Earthquake (Noisia Remix)")
        self.assertEqual(res.items[1].info["artist"], "NOISIA")
        self.assertEqual(res.items[1].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:23547065/e7846551-5c8e-4b93-b4f0-f94bfa7b1275/stream/progressive")
        self.assertEqual(res.items[1].thumb, "https://i1.sndcdn.com/artworks-000011681052-n1a6w6-t500x500.jpg")

    def test_search_playlists(self):
        with open("./tests/mocks/api_v2_search_playlists_without_albums.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo")

        self.assertEqual(res.items[0].label, "Noisia")
        self.assertEqual(res.items[0].info["artist"], "Sebastian Morad")
        self.assertEqual(res.items[0].thumb, "https://i1.sndcdn.com/artworks-000498621510-fk1ovg-t500x500.jpg")

        self.assertEqual(res.items[1].label, "NOISIA")
        self.assertEqual(res.items[1].info["artist"], "Samuel Harris")
        self.assertEqual(res.items[1].thumb, None)

    def test_search_users(self):
        with open("./tests/mocks/api_v2_search_users.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo")

        self.assertEqual(res.items[0].label, "NOISIA")
        self.assertEqual(res.items[0].label2, "Outer Edges")
        self.assertEqual(res.items[0].thumb, "https://i1.sndcdn.com/avatars-000451809714-n5njwk-t500x500.jpg")

        self.assertEqual(res.items[1].label, "Noisia Radio")
        self.assertEqual(res.items[1].label2, "Noisia  Radio")
        self.assertEqual(res.items[1].thumb, "https://i1.sndcdn.com/avatars-000559848966-7tof1c-t500x500.jpg")

    def test_resolve_id(self):
        with open("./tests/mocks/api_v2_tracks.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_id(273627408)

        self.assertEqual(res.items[0].label, "Voodoo (Outer Edges)")
        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:273627408/d35bd07a-3adb-4620-a876-7770f80ff48d/stream/progressive")

    def test_resolve_url(self):
        with open("./tests/mocks/api_v2_resolve_track.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.resolve_url("https://m.soundcloud.com/user/foo")
        # The SoundCloud APIv2 can't resolve mobile links (m.soundcloud.com), so they have to
        # be fixed manually. The following assertion is testing this.
        self.api._do_request.assert_called_with(ANY, {"url": "https://soundcloud.com/user/foo"})
        self.assertEqual(res.items[0].label, "Thomas Hayden - Universe")
        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:584959245/631cc995-e8f2-4a62-a212-5a5768046bc2/stream/progressive")

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

    def test_audio_format(self):
        with open("./tests/mocks/api_v2_tracks.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))
        self.api.settings.get = Mock(return_value="0")

        res = self.api.resolve_id(1)

        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:273627408/23d4e278-f8c0-4438-ace8-201dbd242a1c/stream/hls")

    def test_call(self):
        with open("./tests/mocks/api_v2_search_playlists_without_albums.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.call("/playlists/1")

        self.assertEqual(res.items[0].label, "Noisia")
        self.assertEqual(res.items[1].label, "NOISIA")
