import re
import datetime

class Film():
  def __init__(self, film_, link_, genre_, length_, plotout_, plot_, poster_):
        self.film = film_
        self.link = link_
        self.genre = genre_
        self.length = length_
        self.plotoutline = plotout_
        self.plot = plot_
        self.poster = poster_

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

def getMonday(next, number):
    if next:
        d = datetime.date.today() + datetime.timedelta(7)*number
        while d.weekday() != 0:
            d += datetime.timedelta(1)
        return str(d)
    else:
        d = datetime.date.today() - datetime.timedelta(7)*number
        while d.weekday() != 0:
            d -= datetime.timedelta(1)
        return str(d)

def listOfWeek(bytes):
  split1 = bytes.decode('utf-8').split('trackingCategory')[1]
  split2 = split1.split('</main>')[0]
  splits3 = split2.split('_1rtC2')
  splits4 = splits3[1:len(splits3)]
  filme1 = []
  for data in splits4:
      comp = re.compile("a href=\"(.+)\".+IN_3r\" title=\"(.+)\" da.+_2lnW0.+srcset=\"(.+) 2x.+p7P3N.+<p>(.+)</p>.+3FIJo").findall(data)
      if len(comp) > 0:
        filme1.append(comp[0])
      else:
        comp = re.compile("CUBOJ.+href=\"(.+)\" class=\"_2lnW0\" title=\"(.+)\" .+2hm9z").findall(data)
        if len(comp) > 0:
          filme1.append(comp[0])
        else:
          print("Nix found 2")
  filme = []
  for x in range(0, len(filme1)):
    link = 'http://m.moviepilot.de' + filme1[x][0] + '/trailer'
    if len(filme1[x]) > 2:
      #print("\nX1 " + filme1[x][1] + "\nX2 " + link + "\nX3 " + filme1[x][3] + "\nX4 " + filme1[x][2])
      filme.append(Film(filme1[x][1], link, '', '', '', filme1[x][3], filme1[x][2]))
    else:
      #print("X2 " + filme1[x][1] + link)
      filme.append(Film(filme1[x][1], link, '', '', '', '', ''))
  return filme

def listOfSearch(bytes):
  split1 = bytes.decode('utf-8').split('<!--{"results":')[1]
  split2 = split1.split('<div class=\'grid--row\'>\'')[0]
  splits3 = split2.split('itemClass')
  splits4 = splits3[1:len(splits3)]
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





def listOfStreaming(bytes):
  split1 = bytes.decode('utf-8').split('archive-content')[1]
  split2 = split1.split('clearfix js--pagination')[0]
  splits3 = split2.split('itemprop=\"url\"')
  splits4 = splits3[1:len(splits3)]
  filme1 = []
  filme2 = []
  #filme3 = []
  for data in splits4:
    compLink = re.compile("href=\"(.+)\"><link").findall(data)
    #compPic = re.compile("link\shref=(.+)\sitem.+poster--p").findall(data)
    compName = re.compile("<h3 class=.+'>(.+)<.+/h3>").findall(data)
    if len(compLink) > 0 and len(compName) > 0:# and len(compPic) > 0:
          filme1.append(compLink)
          filme2.append(compName)
          #filme3.append(compPic)
  filme = []
  for x in range(0, len(filme1)):
    link = 'http://m.moviepilot.de' + filme1[x][0] + '/trailer'
    filme.append(Film(filme2[x][0], link, '', '', '', '', ''))#filme3[x][0]))
  return filme

def listOfTrailers(bytes):

  data = bytes.decode('utf-8')
  if ('Top Serien-Videos' not in data):
    split1 = bytes.decode('utf-8').split('Neueste Trailer')[0]
  else:
    split1 = bytes.decode('utf-8').split('Top Serien-Videos')[0]
  split1 = split1.split('video--lightbox--playlists-wrapper')[1]
  data = re.compile("data-video-title='(.+)' href='(.+)'>").findall(split1)
  trailer = []
  for x in range(0, len(data)):
    trailer.append(Trailer(data[x][0], data[x][1]))
  return trailer

def getTrailerLink(bytes):
  res = re.compile(b"og:video\" content=\"(.+)\">").findall(bytes)[0]
  ddd = res.decode('utf-8')
  str = ddd.replace('https://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?url=')
  str = str + '&mode=playVideo'
  return str.encode()

#test()