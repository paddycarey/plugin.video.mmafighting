#!/usr/bin/env python

import os
import sys
import traceback
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from BeautifulSoup import BeautifulSoup

from resources.lib.mmafighting import *
from resources.lib.utils import *

### get addon info
__addon__             = xbmcaddon.Addon()
__addonidint__        = int(sys.argv[1])
__addonname__         = __addon__.getAddonInfo('name')
__addonid__         = __addon__.getAddonInfo('id')
__addondir__          = xbmc.translatePath(__addon__.getAddonInfo('path'))


if __name__ == '__main__':

    # parse script arguments
    params = getParams()
    
    # get current page number
    try:
        
        # check if a page number was passed to script
        page = int(urllib.unquote_plus(params["page"]))
        
    except:
        
        # set page number to 1 if none passed
        page = 1

    # enable episode viewtypes in xbmc
    xbmcplugin.setContent(__addonidint__, 'episodes')

    # loop over all videos on page
    for vidPageUrl in getVideoPages(page):
        
        # extract video details
        video = getVideoDetails(vidPageUrl)
        
        # add video to directory list
        addVideo(linkName = video['title'], url = video['url'], thumbPath = video['thumb'], date = video['date'])
    
    # add next page listitem
    addNext(page + 1)
    
    ## finish adding items to list and display
    xbmcplugin.endOfDirectory(__addonidint__)
