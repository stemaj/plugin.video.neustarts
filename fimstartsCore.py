#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import httplib
import socket

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
    
    if response:
        response.close()

    return (link, error)

socket.setdefaulttimeout(5) # timeout in seconds


def getmatches(url):
    site = getUrl(url)
    if not site[0]:
        return site[1]

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
        info = info.replace('.html','/trailers')
        trailerUrls.append(info)
        bilderUrls.append(re.compile("<img src='(.+?)'", re.DOTALL).findall(box)[0])

    return (titles,trailerUrls,bilderUrls)

#Test
#baseUrl = "http://www.filmstarts.de"
#url = baseUrl + '/filme-vorschau/de/'
##url = baseUrl + '/filme-vorschau/usa/'

#matches = getmatches(url)
#for i in range(len(matches[0])): 
#    ee = matches[0][i]
#    ff = matches[1][i]
#    gg = matches[2][i]
#    hh = 5


