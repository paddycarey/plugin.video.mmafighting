#!/usr/bin/env python

import urllib
import sys

from BeautifulSoup import BeautifulSoup


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


def getVideoPages(pageNum):
    
    """Retrieve a list of video page urls for a given page number on mmafighting.com
    
    Arguments:  pageNum -- An integer containg the page number to process
    Returns:    vidPageList -- A list containg all the urls of the videos (html pages not direct links) on the page"""
    
    # initialise empty list to store video page urls
    vidPages = []
    
    # construct url to scrape
    url = 'http://www.mmafighting.com/videos/%s' % str(pageNum)
    
    # retrieve page and parse into BS object
    soup = BeautifulSoup(getHtml(url))
    
    # get link to video at top of page
    headerVidUrl = soup.find("div", {"class" : "media-gallery-hero"}).a['href']
    headerVid = getVideoDetails(headerVidUrl)
    headerVid['url'] = sys.argv[0] + "?videoURL=%s" % urllib.quote_plus(headerVidUrl)
    
    # add header video page to list
    vidPages.append(headerVid)
    
    # loop through all videos in rest of page
    for a in soup.findAll("a", {"class" : "media-gallery-grid-entry"}):
        
        gridVid = {}
        gridVid['url'] = sys.argv[0] + "?videoURL=%s" % urllib.quote_plus(a['href'])
        gridVid['title'] = a.find("div", {"class" : "media-gallery-grid-entry-title"}).string
        gridVid['thumb'] = a.find("div", {"class" : "image-window shadowbox"}).img['src']
        # add video page to list
        vidPages.append(gridVid)
    
    # return the list of video pages
    return vidPages


def getVideoDetails(url):
    videoDetails = {}
    mmafPage = BeautifulSoup(getHtml(url))
    videoDetails['date'] = parseDate(mmafPage.find("span", {"class" : "publish-date"}).string)
    vidioUrl = mmafPage.find("div", {"class" : "clearfix video-player"}).iframe['src']
    vidioPage = BeautifulSoup(getHtml(vidioUrl))
    videoDetails['title'] = vidioPage.html.head.title.string
    videoDetails['thumb'] = vidioPage.html.video['poster']
    videoDetails['url'] = vidioPage.html.video.source['src']
    return videoDetails

def parseDate(tempDate):
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
    retDate = "%s-%s-%s" % (tempYear, tempMonth, tempDay)
    return retDate
