import unittest
import datetime
from pyStemaj import downloadFile
from pyStemaj import byteStream
from pyStemaj import bytesExtractor
from resources.lib import main
from resources.lib import stringops
import six

# class Test_ReadComparing(unittest.TestCase):

#   def test_compareReading(self):
#     a = read.load_file('000').decode('utf8')
#     b = read.load_url('https://m.moviepilot.de/kino/kinoprogramm/demnaechst-im-kino?start_date=2019-04-04').decode('utf8')
#     self.assertEqual(a, b)


class Test_ParseFiles(unittest.TestCase):

  def test_file000(self):
    a = byteStream.fromFile('tests/file.000')
    arr = main.listOfWeek(a)
    self.assertEqual(7, len(arr))
    self.assertEqual('Scream', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/movies/scream-5/trailer', arr[0].link)
    self.assertEqual('<p&gt;In <b&gt;Scream </b&gt;kehrt nach jahrelanger Abwesenheit das Grauen unter der Maske des Ghostface-Killers nach Woodsboro zurück.</p&gt;', arr[0].plot)
    self.assertEqual('https://assets.cdn.moviepilot.de/files/3e22c6ed08b4ded5d6cb10db21a6cc285afbc63c0b83c56f580006cf74c4/fill/348/500/SCM_INTL_DIGITAL_MONTAGE_TEASER_1_SHEET_GER.jpg', arr[0].poster)


  def test_file001(self):
    a = byteStream.fromFile('tests/file.001')
    arr = main.listOfTrailers(a)
    self.assertEqual(12, len(arr))
    self.assertEqual('Shazam - Trailer 2 (Deutsch) HD', arr[2].film)
    self.assertEqual('https://m.moviepilot.de/movies/shazam--2/trailer/115992', arr[2].link)
    self.assertEqual('Der neue Joker, Shazam und Wonder Woman | So geht es bei DC weiter!', arr[11].film)
    self.assertEqual('https://m.moviepilot.de/movies/shazam--2/trailer/112351', arr[11].link)


  def test_file002(self):
    a = byteStream.fromFile('tests/file.002')
    link = main.getTrailerLink(a)
    self.assertEqual(b'plugin://plugin.video.dailymotion_com/?url=x7xj52f&mode=playVideo', link)

  
  def test_file003(self):
    a = byteStream.fromFile('tests/file.003')
    arr = main.listOfSearch(a)
    self.assertEqual(7, len(arr))
    self.assertEqual('Cold War', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/movies/cold-war/trailer', arr[0].link)
    self.assertEqual('Cold Warriors', arr[5].film)
    self.assertEqual('http://m.moviepilot.de/movies/cold-warriors/trailer', arr[5].link)

  
  def test_file004(self):
    a = byteStream.fromFile('tests/file.004')
    arr = main.listOfSearch(a)
    self.assertEqual(2, len(arr))
    self.assertEqual('Orphan Black', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/serie/orphan-black/trailer', arr[0].link)
    self.assertEqual('Orphan Black - 7 Genes', arr[1].film)
    self.assertEqual('http://m.moviepilot.de/serie/orphan-black-7-genes/trailer', arr[1].link)

  def test_file005(self):
    a = byteStream.fromFile('tests/file.005')
    arr = main.listOfStreaming(a)
    self.assertEqual(25, len(arr))
    self.assertEqual('Bo Burnham: Inside', arr[0].film)
    self.assertEqual('http://m.moviepilot.de/movies/bo-burnham-inside/trailer', arr[0].link)
    
  def test_file007(self):
    a = byteStream.fromFile('tests/file.007')
    arr = main.listOfTrailers(a)
    self.assertEqual(12, len(arr))

  def test_stringops(self):
    bla = "Bla bla blubs tattaaa toll"
    val = stringops.extract_inner_part(bla, "bla ", " toll")
    self.assertEqual(val, "blubs tattaaa")

  def test_jahr(self):
    startjahr = int(datetime.date.today().year)
    self.assertEqual(startjahr, 2022)

  def test_2(self):
    a = bytesExtractor.extractInnerPart(b'":"deutsch-werden","showtimesCount":1,"', b'":"', b'","')
    self.assertTrue(isinstance(a, bytes))
    self.assertEqual(a, b'deutsch-werden')
    a = bytesExtractor.extractInnerPart(b'":"deutsch-werden","', b'":"', b'","')
    self.assertTrue(isinstance(a, bytes))
    self.assertEqual(a, b'deutsch-werden')
    



if __name__ == '__main__':
    unittest.main()
