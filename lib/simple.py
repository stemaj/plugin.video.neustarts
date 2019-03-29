from __future__ import unicode_literals
import urllib3
import concurrent.futures
import datetime
import re
import io
from resources.lib import myRegex

def increment(i):
    return (i+1)

def load_url(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    if (r.status == 200):
        text = r.data#.decode("utf-8")
        with io.open('file.txt', 'wb') as fo:
            fo.write(text)
        return r.data#text

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

def makeGet(url):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(load_url, url)

def filmList(date):
    result = load_url("https://www.moviepilot.de/kino/kinoprogramm/demnaechst-im-kino?start_date=" + date)
    return myRegex.parseToFilmList(result)

def trailerLink(url):
    result2 = load_url(url)
    res = myRegex.parseLink(result2)
    return res


#"video":{
#"https://m.moviepilot.de/movies/colette--2/trailer/114318"
#data-reactid="25"><a href="/movies/colette--2" class="_2lnW0" title="Colette" data-reactid="26"
#"video":{"id":114318,"remoteId":"1_u4ptlu9y","title":"Colette - Trailer (Deutsch) HD","flavorParams":{"sd-large":{"format":"mp4","label":"SD","default":false,"id":"1_nhafl2wf","bitrate":"470"},"hd-full":{"format":"mp4","label":"HD 1080p","default":false,"id":"1_dk9wv7dx","bitrate":"2861"}},"dataLayerParams":{"clickedMovieId":["tt5437928"],"clickedMovieDistributor":["DCM"]},"category":"Contents&gt;Movie Copyright Owner&gt;Verleih Language&gt;German Video-Type&gt;Trailer&gt;Neue Trailer","thumbnail":{"id":"4b49b3535377acd1836e573caa5542c5f5601431f8de117418e9b7be3107","filename":"1.jpg"}}}