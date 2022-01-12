from unittest import TestCase

import CrawlerGoogleScholar


class TestJoke(TestCase):
    def test_is_string(self):
        s = funniest.joke()
        self.assertTrue(isinstance(s, basestring))