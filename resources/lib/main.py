import re
import datetime

class Film():
  def __init__(self, str1, str2, str3, str4, str5, str6, str7):
        self.film = str1
        self.link = str2
        self.genre = str3
        self.length = str4
        self.plotoutline = str5
        self.plot = str6
        self.poster = str7

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
  splits3 = split2.split('_1rtC2')
  splits4 = splits3[1:len(splits3)]
  filme1 = []
  for data in splits4:
      comp = re.compile("CUBOJ.+href=\"(.+)\" class=\"_2lnW0\" title=\"(.+)\" .+2hm9z.+srcset=\"(.+) 2x.+_2Ie5A.+[0-9]\">(.+)</div><div class=\"p7P3N.+<p>(.+)</p>.+3FIJo").findall(data)
      if len(comp) > 0:
        filme1.append(comp[0])
      else:
        comp = re.compile("CUBOJ.+href=\"(.+)\" class=\"_2lnW0\" title=\"(.+)\" .+2hm9z").findall(data)
        if len(comp) > 0:
          filme1.append(comp[0])
  filme = []
  for x in range(0, len(filme1)):
    link = 'http://m.moviepilot.de' + filme1[x][0] + '/trailer'
    if len(filme1[x]) > 2:
      filme.append(Film(filme1[x][1], link, '', '', filme1[x][3], filme1[x][4], filme1[x][2]))
    else:
      filme.append(Film(filme1[x][1], link, '', '', '', '', ''))
  return filme

def listOfMovieSearch(bytes):
  split1 = bytes.decode('utf-8').split('<!--{"results":')[1]
  split2 = split1.split('<div class=\'grid--row\'>\'')[0]
  splits3 = split2.split('Movie')
  splits4 = splits3[1:len(splits3)-1]
  filme1 = []
  for data in splits4:
    comp = re.compile("title\":\"(.+)\",\"dis.+path\":\"(.+)\".\"meta").findall(data)
    if len(comp) > 0:
          filme1.append(comp[0])
  filme = []
  for x in range(0, len(filme1)):
    link = 'http://m.moviepilot.de' + filme1[x][1] + '/trailer'
    filme.append(Film(filme1[x][0], link, '', '', '', '', ''))
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