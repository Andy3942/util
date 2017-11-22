#!/usr/bin/env python3
# coding=utf-8

import os
import math
import string
import xml.etree.ElementTree as et
import re
import pprint
import random
import csv
import io
from pprint import pprint

isCopyright = False

county_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/script/ui/map/county.dat"
map_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_src.tmx"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/check.txt"

class MapUtil(object):
	_map_data = {}
	_width = 0
	_height = 0
	_tree = None
	_countyDbDatas = {}
	_countyDatas = None
	_distributeDatas = {}
	def __init__(self):
		pass
	# 州郡表
	def initCountyDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_eparchy.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
					continue
				self._countyDbDatas[int(row[0])] = {"stateId":row[3]}
		fp = io.open(county_path, "rb")
		self._countyDatas = fp.read()
		fp.close()

	def checkMap(self):
		self._tree = et.parse(map_path)
		maptree = self._tree.getroot()
		self._width = int(maptree.get("width"))
		self._height = int(maptree.get("height"))
		self.initCountyDatas()
		layers = maptree.findall("layer")
		for layer in layers:
			if layer.get("name") == "map":
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')
				for x in range(self._width):
					for y in range(self._height):
						index = self.getTileIndex(x, y)
						gid = self._map_data[index]
						countyId = self._countyDatas[index]
						stateId = self._countyDbDatas[countyId].get("stateId")
						distributeData = self._distributeDatas.get(stateId)
						if distributeData == None:
							distributeData = {}
							self._distributeDatas[stateId] = distributeData
						landData = distributeData.get(gid)
						if landData == None:
							landData = {"gid":-1, "count":0}
							distributeData[gid] = landData
						landData["gid"] = gid
						landData["count"] = landData["count"] + 1
		pprint(self._distributeDatas)
		pass
	def getTileIndex(self, x, y):
		if x < 0 or x >= self._width or y < 0 or y >= self._height:
			return None
		return y * self._height + x
		pass

	def save(self):
		# tilesets = self._tree.getroot().findall("tileset")
		# for tileset in tilesets:
		# 	print(tileset.get("firstgid"))
		# pass
		# self._tree.write(save_path, encoding="UTF-8", xml_declaration=True)
		pass
		
mapUtil = MapUtil()
mapUtil.checkMap()
mapUtil.save()