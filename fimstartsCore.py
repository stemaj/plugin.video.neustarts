﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import httplib
import socket
import datetime

def getUrl(url):
    error = ''
    link = ''
    req = urllib2.Request(url, headers={'accept': '*/*'})
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
    try:
        response = urllib2.urlopen(req)
        if not response:
            error = 'No response - Please try again'
    except urllib2.HTTPError as e:
        error = 'Error code: ', e.code
    except urllib2.URLError as e:
        error = 'Reason: ', e.reason
    except Exception as e:
        if e.message:
            error = e.message
        else:
            error = 'Other reason'
    if not error:
        try:
            link = response.read()
            if not link:
                error = 'No data - Please try again'
        except httplib.IncompleteRead as e:
            error = e.message
        except Exception as e:
            error = e.message
    
    if not error:
        if response:
            response.close()

    return (link, error)


socket.setdefaulttimeout(5) # timeout in seconds
prev = datetime.datetime.now()
next = datetime.datetime.now()

baseUrl = "http://www.filmstarts.de"

def getVideoUrl(url, quality):

    data = getUrl(url)
    match = re.compile('de.vid.web.acsta.net(.+?).mp4', re.DOTALL).findall(data[0])
    if len(match) == 0:
        return

    link = ""

    for m in match:
        m = m.replace("\/","/")
        m = "http://de.vid.web.acsta.net" + m + ".mp4"
        if len(link) == 0:
            link = m
        if quality == 0:
            if "_ld_" in m:
                link = m
        elif quality == 1:
            if "_sd_" in m or "_md_" in m:
                link = m
        else:
            if "_hd_" in m:
                link = m

    return link


def listTrailers(url):

    data = getUrl(url)
    if len(data) == 0:
        return

    splits = data[0].split('section class=\"section section-trailer')
    splits = splits[1]
    splits = splits.split('div class=\"rc-fb-widget')[0]
    spl = splits.split('<div class=\"card card-video mdl row row-col-padded-10')
    spl.pop(0)

    urls = []
    names = []
    images = []
    for i in range(len(spl)): 
        match = re.compile('href="(.+?)"', re.DOTALL).findall(spl[i])
        if match:
            urls.append(baseUrl + match[0])
            names.append(re.compile('alt="(.+?)"', re.DOTALL).findall(spl[i])[0])
            images.append(re.compile('data-src="(.+?)"', re.DOTALL).findall(spl[i])[0])

    return (names,urls,images)

def getmatches(url, filmByDateSite):
    global prev
    global next

    site = getUrl(url)
    if not site[0]:
        return site[1]

    boxesSplitter = 'data_box">'
    titelSearch = ".html\">\n(.+?)\n</a>"
    linkSearch = "href=\"(.+?)\">"
    replaceStr = '.html'

    if filmByDateSite:
        # findout the "current" donnerstag
        a = site[0].split('calendar_picker\">\n')

        if len(a) > 1:
            b = a[1].split('breaker')
            c = re.compile("(.+?) <a>", re.DOTALL).findall(b[0])[0]
            day, month, year = (int(x) for x in c.split('.'))
            current = datetime.date(year, month, day)
            prev = current - datetime.timedelta(days=7)

        else:
            a = re.compile("week=(.+?)'>", re.DOTALL).findall(site[0])
            year, month, day = (int(x) for x in a[0].split('-'))
            prev = datetime.date(year, month, day)
            current = prev + datetime.timedelta(days=7)

            boxesSplitter = 'datablock vpadding10t'
            titelSearch = "/dvd-bluray/'>\n(.+?)\n</a>"
            linkSearch = "href=\'(.+?)\'>"
            replaceStr = '/dvd-bluray/'

        next = current + datetime.timedelta(days=7)


    data = []
    data2 = []

    boxes = site[0].split(boxesSplitter)
    boxes.pop(0)
    for i in range(len(boxes)): 
        data.append(boxes[i].split('</h2>')[0])
        data2.append(boxes[i].split('</h2>')[1])

    titles = []
    trailerUrls = []
    bilderUrls = []
    startTerminLaenge = []
    von = []
    mit = []
    genre = []
    beschreibung = [] 
    for box in data:
        title = re.compile(titelSearch, re.DOTALL).findall(box)
        titles.append(title[0])
        info = str(re.compile(linkSearch, re.DOTALL).findall(box)[0])
        if filmByDateSite:
            info = info.replace(replaceStr,'/trailers')
        else:
            info = info.replace(replaceStr,'/videos')
        trailerUrls.append(info)
        bilderUrls.append(re.compile("src='(.+?)'", re.DOTALL).findall(box)[0])
    for box in data2:

        cnt = 0

        boxx = box.split("</li>");

        if filmByDateSite and len(boxx) > 3:

            startTerminLaeng = re.compile("<div class=\"oflow_a\">\n(.+?)</div>", re.DOTALL).findall(boxx[cnt])[0]
            startTerminLaenge.append(startTerminLaeng)
            cnt = cnt+1

            vonn = re.compile(" >(.+?)</a>", re.DOTALL).findall(boxx[cnt])
            if len(vonn) == 0:
                vonn = re.compile(" >(.+?)</span>", re.DOTALL).findall(boxx[cnt])
            von.append(vonn[0])
            cnt = cnt+1

            tupp = re.compile(" >(.+?)</a>", re.DOTALL).findall(boxx[cnt])
            if len(tupp) == 0:
                tupp = re.compile(" >(.+?)</span>", re.DOTALL).findall(boxx[cnt])
            tup = ()
            for t in tupp:
                tup = tup + (t,)
            mit.append(tup)
            if len(tup) > 0:
                cnt = cnt+1

            genr = re.compile("genre\">(.+?)</span>", re.DOTALL).findall(boxx[cnt])[0]
            genre.append(genr)
            cnt = cnt+1

            beschr = re.compile("<p>\n(.+?)</p>", re.DOTALL).findall(boxx[cnt])[0]
            beschreibung.append(beschr)

        else:
            startTerminLaenge.append('')
            von.append('')
            mit.append(())
            genre.append('')
            beschreibung.append('')


    return (titles,trailerUrls,bilderUrls,startTerminLaenge,von,mit,genre,beschreibung)


def getUrlSuffixWeek(previous):

    global prev
    global next

    if (previous):
        datum = prev
    else:
        datum = next

    mon = str(datum.month)
    day = str(datum.day)

    if (len(mon) == 1):
        mon = '0' + mon
    if (len(day) == 1):
        day = '0' + day

    return "?week=" + str(datum.year) + "-" + mon + "-" + day


##Test
#url = 'http://www.filmstarts.de/filme-vorschau/de/'
#url = 'http://www.filmstarts.de//dvd/vorschau/deutschland/'
#url = 'http://www.filmstarts.de/filme-vorschau/usa/'
#url = 'http://www.filmstarts.de/serien/top/produktionsland-5002/'
#film = True
#matches = getmatches(url, film)
#for i in range(len(matches[0])):
    #e = matches[0][i]
    #f = listTrailers('http://www.filmstarts.de' + matches[1][i])
#    f = matches[1][i]
#    g = matches[2][i]
#    h = matches[3][i]
#    ii = matches[4][i]
#    j = matches[5][i]
#    k = matches[6][i]
#    l = matches[7][i]
    #hh = 5

#dat = getUrl("http://www.filmstarts.de/kritiken/243648/trailer/19557821.html")

#videoUrl = getVideoUrl("http://www.filmstarts.de/kritiken/243648/trailer/19557821.html", 0)


#hhh = 6


#baseUrl = 'http://www.filmstarts.de'
#url = 'http://www.filmstarts.de/kritiken/195350/trailer/19549723.html'
#content = getUrl(url)[0]
#quality = '\"html5PathHD\"'
#match = re.compile(quality + ':"(.*?)"', re.DOTALL).findall(content)
#finalUrl=match[0]
#match = re.compile('"refmedia":(.+?),', re.DOTALL).findall(content)
#media = match[0]
#match = re.compile('"relatedEntityId":(.+?),', re.DOTALL).findall(content)
#ref = match[0]
#match = re.compile('"relatedEntityType":"(.+?)"', re.DOTALL).findall(content)
#typeRef = match[0]
#content = getUrl(baseUrl + '/ws/AcVisiondataV4.ashx?media='+media+'&ref='+ref+'&typeref='+typeRef)[0]
#finalUrl = ""
#match = re.compile('md_path="(.+?)"', re.DOTALL).findall(content)
#finalUrl = match[0]

#content = getUrl('http://www.filmstarts.de/kritiken/238194/trailers/')[0]
#content = content[:content.find('<div class="social">')]
#spl = content.split('<figure class="media-meta-fig">')
#for i in range(1, len(spl), 1):
#    entry = spl[i]
#    match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
#    if match:
#        match = re.compile('"src":"(.+?)"', re.DOTALL).findall(entry)
#        thumb = ""
#        if match:
#            thumb = match[0]
#        match = re.compile('<span >.+?>(.+?)</span>', re.DOTALL).findall(entry)
#        title = match[0].replace("<b>","").replace("</b>"," -").replace("</a>","").replace("<strong>","").replace("</strong>","")
#        title = title.replace("\n","")
#        title = title.replace(" DF", " - "+str(translation(30009))).replace(" OV", " - "+str(translation(30010)))
#        title = cleanTitle(title)

#urlFull = baseUrl + '/filme-vorschau/de/'
#matches = getmatches(urlFull, True)
#data = listTrailers(baseUrl + matches[1][0])
#titles = data[0]
#urls = data[1]
#thumbs = data[2]
#for i in range(len(titles)): 
#    title = titles[i]
#    url = urls[i]
#    thumb = thumbs[i]

#j = 6