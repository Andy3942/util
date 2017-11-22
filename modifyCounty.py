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
		"1":"3",
		"2":"4",
		"3":"1",
		"4":"2",
		"11":"13",
		"13":"11",
		"21":"22",
		"22":"21",
		"31":"33",
		"33":"31",
		"42":"43",
		"43":"42",
	}
	tree = et.parse(xmlFilename)
	maptree = tree.getroot()
	layers = maptree.findall("layer")
	for layer in layers:
		if layer.get("name") == "块层 1":
			data = layer.find("data")
			text = data.text.replace('\n', '')
			countyDatas = text.split(',')
			gidStrs = ["\n"]
			for y in range(yCount):
				for x in range(xCount):
					index = getTileIndex(x, y)
					gid = countyDatas[index]
					gidModifyData = gidModifyDatas.get(gid)
					if gidModifyData != None:
						countyDatas[index] = gidModifyData
					gidStrs.append(countyDatas[index] + ",")
				gidStrs.append("\n")
			newText = "".join(gidStrs)
			newText = newText[:-2] + "\n"
			data.text = newText
	tree.write(saveXmlFilename, encoding="UTF-8", xml_declaration=True)