# -*- coding: utf-8 -*-

import re
import datetime
import six
from resources.lib import stringops
from pyStemaj import bytesExtractor

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
    split2 = six.ensure_str(bytesExtractor.extractInnerPart(bytes, six.ensure_str("alle Filme auf einen Blick"), six.ensure_str("dialogue")))
    splits3 = split2.split('posterId')
    splits4 = splits3[1:len(splits3)]
    filme = []
    for data in splits4:
        name = bytesExtractor.fromRegex(data, r"title(.+)rating")
        if len(name) > 0:
            name = six.ensure_str(bytesExtractor.extractInnerPart(name, six.b(":\""), six.b("\",")))
        else:
            print('missing name')
        link = bytesExtractor.fromRegex(data, r"permalink(.+)teaser")
        if len(link) > 0:
            link = six.ensure_str('http://m.moviepilot.de/movies/') + six.ensure_str(bytesExtractor.extractInnerPart(link, six.b(":\""), six.b("\","))) + six.ensure_str('/trailer')
        else:
            print('missing link')
        desc = bytesExtractor.fromRegex(data, r"teaser(.+)shortTeaser")
        if len(desc) > 0:
            desc = six.ensure_str(bytesExtractor.extractInnerPart(desc, six.b(":\""), six.b("\",")))
        else:
            print('missing desc')
        bild = bytesExtractor.fromRegex(data, r"(.+)posterFilename")
        bild2 = bytesExtractor.fromRegex(data, r"posterFilename(.+)rated")
        if len(bild2) == 0:
            bild2 = bytesExtractor.fromRegex(data, r"posterFilename(.+)permalink")
        if len(bild) > 1 and len(bild2) > 1:
            bild = six.ensure_str(bytesExtractor.extractInnerPart(bild, six.b(":\""), six.b("\",")))
            bild2 = six.ensure_str(bytesExtractor.extractInnerPart(bild2, six.b(":\""), six.b("\",")))
            bild = 'https://assets.cdn.moviepilot.de/files/' + bild + '/fill/348/500/' + bild2
        else:
            print('missing bild')
        if len(name) > 0 and len(link) > 0:
            filme.append(Film(name, link, '', '', '', desc, bild))
    return filme

def listOfSearch(bytes):
    split1 = bytes.decode('utf-8').split('<!--{"results":')[1]
    split2 = split1.split('<div class=\'grid--row\'>\'')[0]
    splits3 = split2.split('itemClass')
    splits4 = splits3[1:len(splits3)]
    filme1 = []
    for data in splits4:
        comp = re.compile(
            "title\":\"(.+)\",\"dis.+path\":\"(.+)\".\"meta").findall(data)
        if len(comp) > 0:
            filme1.append(comp[0])
    filme = []
    for x in range(0, len(filme1)):
        link = 'http://m.moviepilot.de' + filme1[x][1] + '/trailer'
        filme.append(Film(filme1[x][0], link, '', '', '', '', ''))
    return filme


def listOfStreaming(bytes):
    val = six.ensure_str(bytesExtractor.extractInnerPart(bytes, six.ensure_str("Du sortierst nach"), six.ensure_str("Zur nächsten Seite")))
    liste = val.split("</div></div></div></li>")
    if len(liste) > 0:
        liste.pop()
    filme = []
    for x in liste:
        name = bytesExtractor.fromRegex(x, r"gpEclt\">(.+)</span.+coun")
        if len(name) > 0:
            name = six.ensure_str(name)
        else:
            print('missing name')
        link = bytesExtractor.fromRegex(x, r"a href=\"(.+)/trailer")
        if len(link) > 0:
            link = six.ensure_str("http://m.moviepilot.de" + link + "/trailer")
        else:
            print('missing link')
        bild = bytesExtractor.fromRegex(x, r"files/(.+)/fill/155")
        bild2 = bytesExtractor.fromRegex(x, r"fill/310/446/(.+).jpg\ ")
        if len(bild) > 1 and len(bild2) > 1:
            bild = six.ensure_str('https://assets.cdn.moviepilot.de/files/' + bild + '/fill/348/500/' + bild2 + ".jpg")
        elif len(bild2) == 0:
            bild2 = bytesExtractor.fromRegex(x, r"fill/310/446/(.+).jpeg\ ")
            bild = six.ensure_str('https://assets.cdn.moviepilot.de/files/' + bild + '/fill/348/500/' + bild2 + ".jpeg")
        else:
            print('missing bild')
        desc = bytesExtractor.fromRegex(x, r"<p>(.+)</p>")
        if len(desc) > 0:
            desc = six.ensure_str(desc)
        else:
            print('missing desc')
        filme.append(Film(name, link, "", "", "", desc, bild))
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
    str = ddd.replace('https://www.dailymotion.com/video/',
                      'plugin://plugin.video.dailymotion_com/?url=')
    str = str + '&mode=playVideo'
    return str.encode()

# test()
