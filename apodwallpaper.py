# APODWallpaper
#
# Copyright (c) 2013 Alexander Bock
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import time
import urllib
from ctypes import windll
from win32con import SPI_SETDESKWALLPAPER

wallpaperFileName = "background.jpg"
apodURLPrefix = "http://apod.nasa.gov/apod/"
indexURL = "astropix.html"

nArguments = len(sys.argv)
if (nArguments > 2):
    print "Wrong number of arguments. Call 'apodwallpaper.py' with exactly 0 or 1 argument. If specified with one argument, this path will used to store relevant data."

if (nArguments == 2):
    # The argument denotes the path where the wallpaper will be stored
    path = sys.argv[1]
    if (not os.path.isdir(path)):
        print "The path '" + path + "' is not a valid path"
        exit()
else:
    path = os.getcwd()
    
wallpaperPath = os.path.join(path, wallpaperFileName)

# Check if we have the current wallpaper in the path by checking the timestamp of that file
if (os.path.exists(wallpaperPath)):
    lastModifiedTime = time.localtime(os.path.getmtime(wallpaperPath))
    lastModifiedDay = lastModifiedTime[7]
    lastModifiedYear = lastModifiedTime[0]
    currentTime = time.localtime()
    currentDay = currentTime[7]
    currentYear = currentTime[0]
    
    if (lastModifiedDay == currentDay and lastModifiedYear == currentYear):
        exit()
    
# Download index file
indexFile = urllib.urlopen(apodURLPrefix + indexURL)
indexText = indexFile.read().split('\n')
indexFile.close()

# Parse image position
# TODO: proper parsing instead of assuming constant position
correctLine = indexText[28]
imageURL = correctLine[9:-2]
imageFile = open(wallpaperPath, 'wb')
imageFile.write(urllib.urlopen(apodURLPrefix + imageURL).read())
imageFile.close()

# Setting the wallpaper
# TODO: include support for Linux and Mac
windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, wallpaperPath, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)