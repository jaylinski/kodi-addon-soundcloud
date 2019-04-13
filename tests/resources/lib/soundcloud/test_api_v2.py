import json
from unittest import TestCase
from unittest.mock import Mock
from resources.lib.soundcloud.api_v2 import ApiV2


class ApiV2TestCase(TestCase):

    def setUp(self):
        self.api = ApiV2()

    def test_search(self):
        with open("./tests/mocks/api_v2_search.json") as f:
            mock_data = f.read()

        self.api._do_request = Mock()
        self.api._do_request.return_value = json.loads(mock_data)

        res = self.api.search("noisia")

        self.assertEqual(res.items[0].label, "xxxtentacion & wifisfuneral Dont Test Me (Remix)")
        self.assertEqual(res.items[0].info["artist"], "xxxtentacion")
        self.assertEqual(res.items[0].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:244920117/aeff90df-2358-4077-8d16-0891784ad52b/stream/hls")
        self.assertEqual(res.items[1].label, "Seekae - Test & Recognise (Flume Re-work)")
        self.assertEqual(res.items[1].info["artist"], "Flume")
        self.assertEqual(res.items[1].media, "https://api-v2.soundcloud.com/media/soundcloud:tracks:159723640/f332a3df-8dab-4cb5-be2d-4083aa044c85/stream/hls")
