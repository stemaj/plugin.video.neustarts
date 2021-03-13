import unittest
from resources.lib import read
from resources.lib import main

# class Test_ReadComparing(unittest.TestCase):

#   def test_compareReading(self):
#     a = read.load_file('000').decode('utf8')
#     b = read.load_url('https://m.moviepilot.de/kino/kinoprogramm/demnaechst-im-kino?start_date=2019-04-04').decode('utf8')
#     self.assertEqual(a, b)


class Test_ParseFiles(unittest.TestCase):

  def test_file000(self):
    a = read.load_file('000')
    arr = main.listOfWeek(a)
    self.assertEqual(14, len(arr))
    self.assertEqual('Shazam!', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/movies/shazam--2/trailer', arr[0].link)
    self.assertEqual('Mit <b>Shazam!</b> wird ein weiterer DC-Comic zu Leinwandleben erweckt: der erste Captain Marvel. Der Junge Billy Batson wird darin Kraft des Zauberwortes Shazam! zum erwachsenen Superhelden.', arr[0].plot)
    self.assertEqual('https://assets.cdn.moviepilot.de/files/92744d7b1a5163c2acf54a68fbe8f38c5afa4365ab424a1b46a7e88fc45d/fill/348/500/De_Artwork_SHZAM.jpg', arr[0].poster)


  def test_file001(self):
    a = read.load_file('001')
    arr = main.listOfTrailers(a)
    self.assertEqual(12, len(arr))
    self.assertEqual('Shazam - Trailer 2 (Deutsch) HD', arr[2].film)
    self.assertEqual('https://m.moviepilot.de/movies/shazam--2/trailer/115992', arr[2].link)
    self.assertEqual('Der neue Joker, Shazam und Wonder Woman | So geht es bei DC weiter!', arr[11].film)
    self.assertEqual('https://m.moviepilot.de/movies/shazam--2/trailer/112351', arr[11].link)


  def test_file002(self):
    a = read.load_file('002')
    link = main.getTrailerLink(a)
    self.assertEqual(b'plugin://plugin.video.dailymotion_com/?url=x7xj52f&mode=playVideo', link)

  
  def test_file003(self):
    a = read.load_file('003')
    arr = main.listOfSearch(a)
    self.assertEqual(7, len(arr))
    self.assertEqual('Cold War', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/movies/cold-war/trailer', arr[0].link)
    self.assertEqual('Cold Warriors', arr[5].film)
    self.assertEqual('http://m.moviepilot.de/movies/cold-warriors/trailer', arr[5].link)

  
  def test_file004(self):
    a = read.load_file('004')
    arr = main.listOfSearch(a)
    self.assertEqual(2, len(arr))
    self.assertEqual('Orphan Black', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/serie/orphan-black/trailer', arr[0].link)
    self.assertEqual('Orphan Black - 7 Genes', arr[1].film)
    self.assertEqual('http://m.moviepilot.de/serie/orphan-black-7-genes/trailer', arr[1].link)
    

  def test_file007(self):
    a = read.load_file('007')
    arr = main.listOfTrailers(a)
    self.assertEqual(12, len(arr))


if __name__ == '__main__':
    unittest.main()
