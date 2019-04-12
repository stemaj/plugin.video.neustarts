# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import log
from resources.lib import main
from resources.lib import read


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_category, "one"), ListItem("Filme kommend nach Startdatum"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_category, "two"), ListItem("Filme bisher nach Startdatum"), True)
    endOfDirectory(plugin.handle)


@plugin.route('/category/<category_id>')
def show_category(category_id):
    if category_id == "one":
        #plugin.handle, "", ListItem("Hello category %s!" % category_id))
        for x in range(0, 15):
            date = main.getThursday(True, x)
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_filmlist, date), ListItem(date), True)
        endOfDirectory(plugin.handle)
    if category_id == "two":
        for x in range(0, 15):
            date = main.getThursday(False, x)
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_filmlist, date), ListItem(date), True)
        endOfDirectory(plugin.handle)


@plugin.route('/filmlist/<filmlist_id>')
def show_filmlist(filmlist_id):
    data = read.load_url('https://m.moviepilot.de/kino/kinoprogramm/demnaechst-im-kino?start_date='+filmlist_id)
    arr = main.listOfWeek(data)
    for x in arr:
        listItem = ListItem(x.film)
        listItem.setArt({'poster':x.poster})
        listItem.setInfo('video',infoLabels={ 'plot': x.plot, 'plotoutline': x.plotoutline })
        addDirectoryItem(plugin.handle, plugin.url_for(show_trailerList, x.link.replace('/','_')), listItem, True)
    endOfDirectory(plugin.handle)


@plugin.route('/trailerList/<trailerlist_id>')
def show_trailerList(trailerlist_id):
    data = read.load_url(trailerlist_id.replace('_','/'))
    arr = main.listOfTrailers(data)
    for x in arr:
        log('##########LINK##############'+x.link)
        data2 = read.load_url(x.link)
        xxx = main.getTrailerLink(data2).decode('utf-8')
        log('##########XXX##############'+xxx)
        listitem = ListItem(path=xxx , label=x.film)
        listitem.setInfo('video',infoLabels={ "Title": x.film })
        listitem.setLabel(x.film)
        listitem.setProperty('IsPlayable', 'true')
        addDirectoryItem(plugin.handle, xxx, listitem)
    endOfDirectory(plugin.handle)

def run():
    plugin.run()
