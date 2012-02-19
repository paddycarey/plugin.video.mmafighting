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

### get addon info
__addon__             = xbmcaddon.Addon()
__addonidint__        = int(sys.argv[1])
__addonname__         = __addon__.getAddonInfo('name')
__addonid__         = __addon__.getAddonInfo('id')
__addondir__          = xbmc.translatePath(__addon__.getAddonInfo('path'))

def getHtml(url):
    """Retrieve and return remote resource as string
    Arguments:  url -- A string containing the url of a remote page to retrieve
    Returns:    data -- A string containing the contents to the remote page"""
    # connect to url using urlopen
    client = urllib.urlopen(url)
    # read data from page
    data = client.read()
    # close connection to url
    client.close()
    # return the retrieved data
    return data

def log(txt, severity=xbmc.LOGDEBUG):
    """Log txt to xbmc.log at specified severity
    Arguments:  txt -- A string containing the text to be logged
                severity -- Logging level to log text at (Default to LOGDEBUG)"""
    # generate log message from addon name and txt
    message = ('%s: %s' % (__addonid__, txt))
    # write message to xbmc.log
    xbmc.log(msg=message, level=severity)

def addVideo(linkName = '', url = '', thumbPath = '', date = ''):
    li = xbmcgui.ListItem(linkName, iconImage = thumbPath, thumbnailImage = thumbPath)
    li.setProperty("IsPlayable", 'true')
    li.setInfo( type="Video", infoLabels={ "title": linkName, "date":date} )
    li.setProperty( "Fanart_Image", os.path.join(__addondir__, 'fanart.jpg'))
    xbmcplugin.addDirectoryItem(handle = __addonidint__, url = url, listitem = li, isFolder = False)

def getVideoPages():
    pageNum = 1
    vidPageList = []
    while pageNum < 6:
        url = 'http://www.mmafighting.com/videos/%s' % str(pageNum)
        log("Parsing page: %s" % url)
        soup = BeautifulSoup(getHtml(url))
        headerVid = soup.find("div", {"class" : "media-gallery-hero"}).a['href']
        vidPageList.append(headerVid)
        for a in soup.findAll("a", {"class" : "media-gallery-grid-entry"}):
            vidPageList.append(a['href'])
        pageNum = pageNum + 1
    return vidPageList

def getVideoDetails(url):
    videoDetails = {}
    mmafPage = BeautifulSoup(getHtml(url))
    tempDate = mmafPage.find("span", {"class" : "publish-date"}).string
    print tempDate.split(' ')
    months = {  'January': '01',
                'February': '02',
                'March': '03',
                'April': '04',
                'May': '05',
                'June': '06',
                'July': '07',
                'August': '08',
                'September': '09',
                'October': '10',
                'November': '11',
                'December': '12' }
    tempMonth = months[tempDate.split(' ')[1]]
    try:
        tempDay = "%.2d" % int(tempDate.split(' ')[3].rstrip(','))
        tempYear = tempDate.split(' ')[4]
    except ValueError:
        tempDay = "%.2d" % int(tempDate.split(' ')[4].rstrip(','))
        tempYear = tempDate.split(' ')[5]
    videoDetails['date'] = "%s-%s-%s" % (tempYear, tempMonth, tempDay)
    vidioUrl = mmafPage.find("div", {"class" : "clearfix video-player"}).iframe['src']
    vidioPage = BeautifulSoup(getHtml(vidioUrl))
    videoDetails['title'] = vidioPage.html.head.title.string
    videoDetails['thumb'] = vidioPage.html.video['poster']
    videoDetails['url'] = vidioPage.html.video.source['src']
    return videoDetails

if __name__ == '__main__':
    for vidPageUrl in getVideoPages():
        video = getVideoDetails(vidPageUrl)
        addVideo(linkName = video['title'], url = video['url'], thumbPath = video['thumb'], date = video['date'])
    xbmcplugin.setContent(__addonidint__, 'episodes')
    ## finish adding items to list and display
    xbmcplugin.endOfDirectory(__addonidint__)
