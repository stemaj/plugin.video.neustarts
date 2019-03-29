from resources.lib import myRegex
import unittest   # The test framework


class Test_Regex(unittest.TestCase):

    def test_lodfile(self):
        self.assertNotEqual(len(myRegex.loadFromFile()), 0)

    def test_regex(self):
        x = myRegex.parseToFilmList(myRegex.loadFromFile())
        self.assertEqual(6, len(x))
        y = x[0]
        self.assertEqual(y.film, b'Colette')
        self.assertEqual(y.link, 'https://m.moviepilot.de/movies/colette--2/trailer/114318')
        y = x[1]
        self.assertEqual(y.film, b'Die Frau des Nobelpreistr\xc3\xa4gers')
        self.assertEqual(y.link, 'https://m.moviepilot.de/movies/die-frau-des-nobelpreistragers/trailer/114470')

    def test_regex2(self):
        self.assertEqual(myRegex.parseLink(myRegex.loadFromFile()), b'https://cdnapisec.kaltura.com/p/1764171/sp/176417100/playManifest/entryId/1_u4ptlu9y/format/url/protocol/https/flavorParamId/0')



if __name__ == '__main__':
    unittest.main()
