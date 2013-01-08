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