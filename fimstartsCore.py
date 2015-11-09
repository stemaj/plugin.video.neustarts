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


def getmatches(url, filmByDateSite):
    global prev
    global next

    site = getUrl(url)
    if not site[0]:
        return site[1]

    if filmByDateSite:
        # findout the "current" donnerstag
        a = site[0].split('calendar_picker\">\n')
        b = a[1].split('breaker')
        c = re.compile("(.+?) <a>", re.DOTALL).findall(b[0])[0]
        day, month, year = (int(x) for x in c.split('.'))
        current = datetime.date(year, month, day)

        prev = current - datetime.timedelta(days=7)
        next = current + datetime.timedelta(days=7)

    data = []
    boxes = site[0].split('data_box">')
    boxes.pop(0)
    for i in range(len(boxes)): 
        data.append(boxes[i].split('</h2>')[0])

    titles = []
    trailerUrls = []
    bilderUrls = []
    for box in data:
        titles.append(re.compile("alt='(.+?)'", re.DOTALL).findall(box)[0])
        info = str(re.compile("href=\"(.+?)\">", re.DOTALL).findall(box)[0])
        if filmByDateSite:
            info = info.replace('.html','/trailers')
        else:
            info = info.replace('.html','/videos')
        trailerUrls.append(info)
        bilderUrls.append(re.compile("src='(.+?)'", re.DOTALL).findall(box)[0])

    return (titles,trailerUrls,bilderUrls)


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
#url = 'http://www.filmstarts.de/serien/beste/produktionsland-5002/?page=1'
#film = False

#matches = getmatches(url, film)
#for i in range(len(matches[0])): 
#    ee = matches[0][i]
#    ff = matches[1][i]
#    gg = matches[2][i]

#hh = 5