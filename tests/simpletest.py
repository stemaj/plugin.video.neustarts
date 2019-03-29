from resources.lib import simple
import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(simple.increment(3), 4)

class Test_TestMakeGet(unittest.TestCase):
    def test_makeGet1(self):
        self.assertIsNotNone(simple.load_url('https://www.technisat.com/'))

class Test_TestgetThursday(unittest.TestCase):
    def test_getThursday(self):
        self.assertEqual(simple.getThursday(True, 0), '2019-04-04')
    def test_getNextThursday(self):
        self.assertEqual(simple.getThursday(True, 1), '2019-04-11')
    def test_getPrevThursday(self):
        self.assertEqual(simple.getThursday(False, 0), '2019-03-28')
    def test_getPrevPrevThursday(self):
        self.assertEqual(simple.getThursday(False, 1), '2019-03-21')


class Test_TestgetFilmList(unittest.TestCase):
    def test_getFilmList(self):
        x = simple.filmList('2019-01-03')
        self.assertEqual(6, len(x))
        y = x[0]
        self.assertEqual(y.film, b'Colette')
        self.assertEqual(y.link, 'https://m.moviepilot.de/movies/colette--2/trailer/114318')
        y = x[1]
        self.assertEqual(y.film, b'Die Frau des Nobelpreistr\xc3\xa4gers')
        self.assertEqual(y.link, 'https://m.moviepilot.de/movies/die-frau-des-nobelpreistragers/trailer/114470')

    def test_loadTrailer(self):
        self.assertEqual(simple.trailerLink('https://m.moviepilot.de/movies/colette--2/trailer/114318'),
        b'https://cdnapisec.kaltura.com/p/1764171/sp/176417100/playManifest/entryId/1_u4ptlu9y/format/url/protocol/https/flavorParamId/0')



if __name__ == '__main__':
    unittest.main()