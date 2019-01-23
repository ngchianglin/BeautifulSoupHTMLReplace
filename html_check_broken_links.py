#!/usr/bin/python3
# The MIT License (MIT)
#
# Copyright (c) 2019 Ng Chiang Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Simple python3 script to check for broken links in a directory of html files
# It uses BeautifulSoup and Response and recursively check 
# html files in a directory. 
# The script only checks for absolute links (starting with http) and can be configured
# to ignore your own domain. i.e. checking only absolute links to external
# websites. The script considers http redirection as well as a non HTTP 200 status 
# as indicating that a link is broken. It spawns a number of threads to speed up
# the network check. 
# The results are written to a file brokenlinks.txt. Existing file with the same name
# will be overwritten. 
#  
#  
#
# Ng Chiang Lin
# Jan 2019



import os
import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

# domain to exclude from checks
exclude = "nighthour.sg"

# Directory containing the html files
homepagedir = "HomePage"

# A list holding all the html doc objects
htmldocs = []

# Number of threads to use for checking links
numthread = 10 

# User-Agent header string
useragent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"

# The results file
outputfile = "brokenlinks.txt"

class Link:
    """
    This class represents a link <a href=".."> in a html file
    It has the following variables
    url:  the url of the link  
    broken: a boolean indicating whether the link is broken
    number: the number of occurences in the html file

    """

    def __init__(self, url):
        self.url = url
        self.broken = False
        self.number = 1
 


class HTMLDoc:
    """
    This class represents a html file
    It has the following member variables. 
    name: filename of the html file
    path: file path of the html file
    broken_link: A boolean flag indicating whether the 
                html file contains broken links
    links: A dictionary holding the links in the html file. 
           It uses the url string of the link as the key. 
           The value is a Link object. 

    """

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.broken_link = False
        self.links = {}

    def addLink(self, url, link):
        ret = self.links.get(url)
        if ret :
            ret.number = ret.number + 1
            self.links[url] = ret
        else:
            self.links[url] = link

    def hasBroken(self):
        return self.broken_link 

    def setBroken(self):
        self.broken_link = True



def processDir(dir):
    print("Processing ", dir)
    dirlist = os.listdir(path=dir)

    for f in dirlist:
        filename = f
        f = dir + os.sep + f

        if (os.path.isfile(f) and 
        (f.endswith(".html") or f.endswith(".htm")) and not 
        os.path.islink(f)) : 
            print("file: " , f)
            processHTMLDoc(filename, f)
 
        elif os.path.isdir(f) and not os.path.islink(f): 
            print("Directory: ", f)   
            processDir(f)

def processHTMLDoc(filename, path):

    try:

        try:
            fp = open(path,mode='r', encoding='utf-8')
            soup = BeautifulSoup(fp, "lxml", from_encoding="utf-8")
            alist = soup.find_all('a')

            htmlobj = HTMLDoc(filename, path)          
 
            for link in alist:
                processDocLink(link, htmlobj)
           
            htmldocs.append(htmlobj) 

        finally:    
            fp.close()

    except err:
           print("Warning: Exception occurred: ", path, " : " , err)  




def processDocLink(link, htmlobj):
    if(link.has_attr('href')):
        location = link['href']

        if (location.startswith("http") and 
        exclude not in location) :
            linkobj = Link(location)
            htmlobj.addLink(location, linkobj)
        


def checkBrokenLink(htmlqueue, tnum):

    while True:
        htmlobj = htmlqueue.get()
        print("Thread ", tnum, " processing ", htmlobj.name)
        links = htmlobj.links
        
        try:
        
            for k, v in links.items():
                linkobj = v 
                try:
                    headers = {'User-Agent':useragent}
                    r = requests.get(linkobj.url, headers=headers, allow_redirects=False)

                    if r.status_code != 200:
                        print("Broken link : ", htmlobj.path ,
                               " : " , linkobj.url)
                        linkobj.broken = True
                        htmlobj.broken_link = True
                except:
                    print("Broken link : ", htmlobj.path ,
                               " : " , linkobj.url)
                    linkobj.broken = True
                    htmlobj.broken_link = True
                
        finally:
            htmlqueue.task_done()
            



def writeResults():

    with open(outputfile, mode='w', encoding='utf-8') as fp:
        fp.write("==================== Results =============================\n")
        fp.write("Html File Path ; Broken Link ; Number of links in file\n")
        fp.write("==========================================================\n\n")
        for html in htmldocs:
            if html.hasBroken():
                for k, v in html.links.items():
                    link = v
                    if link.broken:
                        output = html.path + " ; " + link.url  + " ; " + str(link.number) + "\n"
                        fp.write(output)
                           
    fp.close()

  
                                        


if __name__ == "__main__" :
     processDir(homepagedir)

     htmlqueue = Queue()

     for i in range(numthread):
         worker = Thread(target=checkBrokenLink,args=(htmlqueue,i,))
         worker.setDaemon(True)
         worker.start()


     for html in htmldocs:
         htmlqueue.put(html)


     htmlqueue.join()
     print("\n\n\n")
     print("Checking done, writing results to ", outputfile)
     writeResults()
     print("Completed. Check the results in ", outputfile)
      

