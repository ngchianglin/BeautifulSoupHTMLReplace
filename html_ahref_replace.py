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
#
#
# Simple python3 script to 
# add rel="noopener noreferrer" attribute to link <a> tag
# that opens the target in a new window (target="_blank")
# This is to protect against security vulnerability that can
# cause phishing or private information leakage. 
# 
# The script modifies all html files in a directory recursively. 
# The script doesn't follow symlinks.  
# It uses BeautifulSoup 4 library with the lxml parser. 
# The html files are assumed to be utf-8 encoded and well formed.  
# 
# Warning: The script replaces/modifies existing files. 
#          To prevent data corruption of data loss. 
#          Always backup your files first ! 
#
# 
# Ng Chiang Lin
# Jan 2019
#

import os
from bs4 import BeautifulSoup

# Text to match
matchtext = "_blank"

# Attribute and its content to be added
relattr = {'rel':'noopener noreferrer'}

# Directory containing the html files
homepagedir = "HomePage"

def processDir(dir):
    print("Processing ", dir)
    dirlist = os.listdir(path=dir)

    for f in dirlist:
        f = dir + os.sep + f

        if (os.path.isfile(f) and 
        (f.endswith(".html") or f.endswith(".htm")) and not 
        os.path.islink(f)) : 
            print("file: " , f)
            updateFile(f)
        elif os.path.isdir(f) and not os.path.islink(f): 
            print("Directory: ", f)   
            processDir(f)



def updateFile(infile):
    fp = open(infile, mode='r', encoding='utf-8')

    try:

        try:
            fp = open(infile,mode='r', encoding='utf-8')
            soup = BeautifulSoup(fp, "lxml", from_encoding="utf-8")
            alist = soup.find_all('a')
           
            for ahref in alist:
                if ahref.has_attr('target'):
                    if matchtext in ahref['target']:        
                        appendAttr(ahref)

            output = soup.encode(formatter="html5")
            #quick hack to replace async="" with async
            #in javascript tag
            #for my use case this works but for complicated
            #html may require other solutions
            output = output.decode("utf-8")
            output = output.replace('async=""','async')
            writeOutput(infile, output)
            os.replace(infile + ".new", infile)

        finally:    
            fp.close()

    except err:
           print("Warning: Exception occurred: ", infile, " : " , err)  



def appendAttr(ahref):
    for key, val in relattr.items(): 

        if ahref.has_attr(key):
            # Handle the case where rel attribute already present
            # and contains "license" as  value
            # Any other value will be overwritten
            oldval = ahref[key]
          
            if "license" in oldval:
                ahref[key] = "license " + val
            else:
                ahref[key] = val
        else:
            ahref[key] = val




def writeOutput(infile, output):
    tempname = infile + ".new"

    try:
        
        try:
            of = open(tempname, mode='w', encoding='utf-8') 
            of.write(output)
        finally:
            of.close()
    
    except err:
        print("Warning: Exception occurred: ", infile, " : ", err)




if __name__ == "__main__" :
    processDir(homepagedir)




