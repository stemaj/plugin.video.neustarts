import re
import datetime

class Film():
  def __init__(self, str1, str2, str3, str4, str5, str6, str7):
        self.film = str1
        self.link = str2
        self.genre = str3
        self.length = str4
        self.short = str5
        self.long = str6
        self.pic = str7

class Trailer():
  def __init__(self, str1, str2):
        self.film = str1
        self.link = str2

def getThursday(next, number):
    if next:
        d = datetime.date.today() + datetime.timedelta(7)*number
        while d.weekday() != 3:
            d += datetime.timedelta(1)
        return str(d)
    else:
        d = datetime.date.today() - datetime.timedelta(7)*number
        while d.weekday() != 3:
            d -= datetime.timedelta(1)
        return str(d)

def listOfWeek(bytes):
  split1 = bytes.decode('utf-8').split('trackingCategory')[1]
  split2 = split1.split('</main>')[0]
  splits3 = split2.split('_2HBle')
  splits4 = splits3[:len(splits3)-1]
  filme1 = []
  for data in splits4:
      filme1.append(re.compile("IN_3r\" data-reactid=\"[0-9]+\"><a href=\"(.+)\" class=\"_2lnW0\" title=\"(.+)\"\\s.+</a></s").findall(data)[0])
  filme = []
  for x in range(0, len(filme1)):
    link = 'http://m.moviepilot.de' + filme1[x][0] + '/trailer'
    filme.append(Film(filme1[x][1], link, '', '', '', '', ''))
  return filme

def listOfTrailers(bytes):
  split1 = bytes.decode('utf-8').split('video--lightbox--playlists-wrapper')[1]
  split2 = split1.split('Top-Videos')[0]
  splits3 = split2.split('</li>')
  splits4 = splits3[:len(splits3)-1]
  trailer1 = []
  for data in splits4:
    trailer1.append(re.compile("data-video-title='(.+)'\\shref='(.+)'>\\n<").findall(data)[0])
  trailer = []
  for x in range(0, len(trailer1)):
    trailer.append(Trailer(trailer1[x][0], trailer1[x][1]))
  return trailer

def getTrailerLink(bytes):
  res = re.compile(b"og:video\" content=\"(.+)\">").findall(bytes)
  if len(res) > 0:
    return res[0]
  return ''

#test()