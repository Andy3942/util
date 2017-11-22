#!/usr/bin/env python3
# coding=utf-8

import os,sys
from xml.etree import ElementTree
from PIL import Image
import csv
import xml.etree.ElementTree as et
from numpy import *
if __name__ == '__main__':
	width = 200
	height = 100
	xCount = 1200
	yCount = 1200
	def getTileIndex(x, y):
		if x < 0 or x >= xCount or y < 0 or y >= yCount:
			return None
		return y * xCount + x
	pass
	xmlFilename = sys.argv[1]
	saveXmlFilename = sys.argv[2]
	gidModifyDatas = {
	}
	tree = et.parse(xmlFilename)
	maptree = tree.getroot()
	layers = maptree.findall("layer")
	for layer in layers:
		if layer.get("name") == "map":
			data = layer.find("data")
			text = data.text.replace('\n', '')
			countyDatas = text.split(',')
			gidStrs = ["\n"]
			for y in range(yCount):
				for x in range(xCount):
					index = getTileIndex(x, y)
					# if x == 604 and y == 772:
					# 	countyDatas[index] = "102"
					if (x == 638 and y == 733)\
						or (x == 639 and y == 733)\
						or (x == 640 and y == 733)\
						or (x == 647 and y == 674)\
						or (x == 648 and y == 674)\
						or (x == 649 and y == 674):
						countyDatas[index] = "307001"
					gidStrs.append(countyDatas[index] + ",")
				gidStrs.append("\n")
			newText = "".join(gidStrs)
			newText = newText[:-2] + "\n"
			data.text = newText
	tree.write(saveXmlFilename, encoding="UTF-8", xml_declaration=True)