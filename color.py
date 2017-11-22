#!/usr/bin/env python3
# coding=utf-8

import os,sys
from xml.etree import ElementTree
from PIL import Image

def getColor(png_filename, x, y):
    img = Image.open(png_filename).convert("RGBA")
    pixel = img.getpixel((x, y))
    print(pixel)
if __name__ == '__main__':
    png_filename = sys.argv[1]
    x = int(sys.argv[2])
    y = int(sys.argv[3])
    if os.path.exists(png_filename):
        getColor(png_filename, x, y)
    else:
        print("make sure you have boith plist and png files in the same directory")