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
	xCount = 300
	yCount = 300
	imageWidth = 1440
	imageHeight = 720
	scale = width * xCount / imageWidth
	centerMat4 = mat([[width * 0.5 / scale, -height * 0.5 / scale, 0, 0], 
		[-width * 0.5 / scale, -height * 0.5 / scale, 0, 0], 
		[0, 0, 1, 0], 
		[width * 0.5 * xCount / scale, height * (yCount - 0.5) / scale, 0, 1]])
	pngFilename = sys.argv[1]
	xmlFilename = sys.argv[2]
	img = Image.open(pngFilename).convert("RGB")
	data = list(img.getdata())
	colorDatas = {}
	gids = {}
	with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_eparchy.csv", newline='', encoding="gbk") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
		i = 0
		for row in spamreader:
			i = i + 1
			if i <= 2 or row[0] == "255":
				continue
			colorStr = row[4].split("|")
			color = (int(colorStr[0]), int(colorStr[1]), int(colorStr[2]))
			colorDatas[color] = row[0]
	pass
	print(colorDatas)
	gidStrs = []
	for y in range(yCount):
		if y % 100 == 0:
			print(y)
		gidStrs.append("\n")
		for x in range(xCount):
			colorPosition = mat([x, y, 0, 1]) * centerMat4
			colorPosition = colorPosition.tolist()[0]
			colorIndex = (imageHeight - math.floor(colorPosition[1]) - 1) * imageWidth + math.floor(colorPosition[0])
			index = y * xCount + x
			color = data[colorIndex]
			gid = colorDatas.get(color, 97)			
			gidStrs.append(str(gid) + ",")
	text = "".join(gidStrs)
	text = text[:-1] + "\n"
	tree = et.parse(xmlFilename)
	maptree = tree.getroot()
	layers = maptree.findall("layer")
	for layer in layers:
		if layer.get("name") == "块层 1":
			data = layer.find("data")
			data.text = text
	tree.write(xmlFilename, encoding="UTF-8", xml_declaration=True)