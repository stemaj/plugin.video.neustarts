#!/usr/bin/python
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
    #req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5')
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

        #versuch über die frameUrl
        match = re.compile('frameUrl\":\"(.+?)",', re.DOTALL).findall(data[0])
        if len(match) == 0:
            return
        data = getUrl(match[0])
        match = re.compile('de.vid.web.acsta.net(.+?).mp4', re.DOTALL).findall(data[0])
    
    if len(match) == 0:
        return

    link = ""

    hasLow = False
    hasMed = False
    hasHigh = False
    for m in match:
        if "_ld_" in m:
            hasLow = True
        if "_sd_" in m or "_md_" in m:
            hasMed = True
        if "_hd_" in m:
            hasHigh = True

    returnLow = False
    returnMed = False
    returnHigh = False
    if quality == 0:
        if hasLow:
            returnLow = True
        elif hasMed:
            returnMed = True
        else:
            returnHigh = True
    elif quality == 1:
        if hasMed:
            returnMed = True
        elif hasLow:
            returnLow = True
        else:
            returnHigh = True
    else:
        if hasHigh:
            returnHigh = True
        elif hasMed:
            returnMed = True
        else:
            returnLow = True


    if returnLow:
        for m in match:
            if "_ld_" in m:
                m = m.replace("\/","/")
                m = "http://de.vid.web.acsta.net" + m + ".mp4"
                return m
    elif returnMed:
        for m in match:
            if "_sd_" in m or "_md_" in m:
                m = m.replace("\/","/")
                m = "http://de.vid.web.acsta.net" + m + ".mp4"
                return m
    else:
        for m in match:
            if "_hd_" in m:
                m = m.replace("\/","/")
                m = "http://de.vid.web.acsta.net" + m + ".mp4"
                return m


def listTrailers(url):

    data = getUrl(url)
    if len(data) == 0:
        return

    entries = re.compile('article data-block="" class="media-meta small(.+?)</article>', re.DOTALL).findall(data[0])
    urls = []
    names = []
    images = []
    for i in range(len(entries)): 
        urls.append(baseUrl + re.compile('a href=\"(.+?)\">', re.DOTALL).findall(entries[i])[0])
        nameObj = re.compile('<a href(.+?)</span>', re.DOTALL).findall(entries[i])[0]
        nameObj = re.compile('\">(.+?)</a>', re.DOTALL).findall(nameObj)[0]
        nameObj = nameObj.replace("<strong>","");
        nameObj = nameObj.replace("</strong>","");
        nameObj = nameObj.replace("\n","");
        names.append(nameObj)
        images.append(re.compile('src\":\"(.+?)\"}', re.DOTALL).findall(entries[i])[0])

    return (names,urls,images)


def listTrailersMovies(url):

    data = getUrl(url)
    if len(data) == 0:
        return

    data = data[0].split("er</h2></div>")
    if len(data) < 2:
        return
    data = data[1]

    data = data.split("aside class")
    if len(data) < 2:
        return
    data = data[0]

    entries = re.compile('card-video-col mdl(.+?)div class=\"meta-sub light\"', re.DOTALL).findall(data)
    urls = []
    names = []
    images = []
    for i in range(len(entries)):
        text = re.compile('meta-title-link\" href=\"(.+?)\" >', re.DOTALL).findall(entries[i])
        if len(text) > 0:
            urls.append(baseUrl + text[0])
        else:
            urls.append(baseUrl)
        names.append(re.compile(' alt=\"(.+?)\" width=', re.DOTALL).findall(entries[i])[0])
        images.append(re.compile('data-src=\"(.+?)\" alt', re.DOTALL).findall(entries[i])[0])

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
#url = 'http://www.filmstarts.de/kritiken/257832/trailers'
#daten = listTrailersMovies(url)
#url = 'http://www.filmstarts.de/serien/19992/videos/19553238/'
#url = 'http://www.filmstarts.de/kritiken/228322/trailer/19558055.html'
#videoUrl = getVideoUrl(url, 0)
#hhh = 6
