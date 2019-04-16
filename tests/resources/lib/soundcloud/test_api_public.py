from unittest import TestCase, skip
from resources.lib.soundcloud.api_public import ApiPublic


class ApiPublicTestCase(TestCase):

    def setUp(self):
        self.api = ApiPublic()

    @skip("Not implemented")
    def test_search(self):
        self.api.search("test", "tracks")

