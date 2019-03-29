# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import log
import urllib3

from resources.lib import simple


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
            date = simple.getThursday(True, x)
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_film_list, date), ListItem(date), True)
        endOfDirectory(plugin.handle)
    if category_id == "two":
        for x in range(0, 15):
            date = simple.getThursday(False, x)
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_film_list, date), ListItem(date), True)
        endOfDirectory(plugin.handle)


@plugin.route('/film_list/<category_id>')
def show_film_list(category_id):
    for x in simple.filmList(category_id):
        addDirectoryItem(plugin.handle, plugin.url_for(
                show_trailer, x.link.replace('/','_')), ListItem(x.film))
    endOfDirectory(plugin.handle)

@plugin.route('/trailer/<category_id>')
def show_trailer(category_id):
    urllib3.disable_warnings()
    path = ""
    listitem = ListItem(path=simple.trailerLink(category_id.replace('_','/')))
    logger.log(0,path)
    logger.log(1,path)
    logger.log(2,path)
    listitem.setInfo('video',infoLabels={ "Title": "title" , "Plot" : "plot" })
    listitem.setProperty('IsPlayable', 'true')
    setResolvedUrl(plugin.handle, True, listitem)


def run():
    plugin.run()
