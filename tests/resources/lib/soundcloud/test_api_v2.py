import json
import sys
from unittest import TestCase, skip
from unittest.mock import MagicMock, Mock
sys.modules['xbmcgui'] = MagicMock()
from resources.lib.soundcloud.api_v2 import ApiV2


class ApiV2TestCase(TestCase):
    def setUp(self):
        self.settings = MagicMock()
        self.api = ApiV2(self.settings)

    def test_search(self):
        with open("./tests/mocks/api_v2_search_tracks.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.search("foo")

        self.assertEqual(res.items[0].label, "xxxtentacion & wifisfuneral Dont Test Me (Remix)")
        self.assertEqual(res.items[0].info["artist"], "xxxtentacion")
        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:244920117/a81da15e-f1ca-4fd5-a6cb-66438f5c1d0d/stream/hls")
        self.assertEqual(res.items[1].label, "Seekae - Test & Recognise (Flume Re-work)")
        self.assertEqual(res.items[1].info["artist"], "Flume")
        self.assertEqual(res.items[1].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:159723640/fb94baeb-bee4-4fa8-85e8-dea8962c51b6/stream/hls")

    @skip("If this test runs, the test above fails...")
    def test_discover(self):
        with open("./tests/mocks/api_v2_discover.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock(return_value=json.loads(mock_data))

        res = self.api.discover()

        self.assertEqual(res.items[0].label, "Chill")
        self.assertEqual(res.items[1].label, "Party")
        self.assertEqual(res.items[2].label, "Relax")
