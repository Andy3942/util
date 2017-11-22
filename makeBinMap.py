#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import math
import string
import xml.etree.ElementTree as et
import re
import pprint
import random
import struct

file_path = None
if len(sys.argv) > 1:
	file_path = sys.argv[1]
fillData = False
if file_path != None:
	fillData = True
	save_path = file_path[:-4] + ".dat"
else:
	file_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_src.tmx"
	save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/script/ui/map/map.dat"
print(file_path, save_path)

class MapUtil(object):
	_map_data = {}
	_map_data2 = {}
	_terrain_data = {}
	_width = 0
	_height = 0
	_tree = None
	_landid_datas = {}
	def __init__(self):
		pass

	def initLandId(self):
		maptree = self._tree.getroot()
		tilesets = maptree.findall("tileset")
		for tileset in tilesets:
			firstgid = tileset.get("firstgid")
			tile = tileset.find("tile")
			if tile:
				properties = tile.findall("properties")
				for propertyTemp in properties:
					propertyElement = propertyTemp.find("property")
					name = propertyElement.get("name")
					if name == "landId":
						value = int(propertyElement.get("value"))
						self._landid_datas[firstgid] = value
		print("landIdDatas = ", self._landid_datas)

	def getTileIndex(self, x, y):
		if x < 0 or x >= self._width or y < 0 or y >= self._height:
			return None
		return y * self._height + x
		pass

	def makeMap(self):	
		self._tree = et.parse(file_path)
		self.initLandId()
		layers = self._tree.findall("layer")
		for layer in layers:
			if layer.get("name") == "块层 1" or layer.get("name") == "map":
				self._width = int(layer.get("width"))
				self._height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')
			elif layer.get("name") == "块层 2":
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data2 = text.split(',')
		pass

	def save(self):
		strData = ""
		with open(save_path, "wb") as fp:
			for y in range(self._height):
				for x in range(self._width):
					gid = self._map_data[self.getTileIndex(x, y)]
					if self._landid_datas.get(gid, None):
						gid = self._landid_datas.get(gid, None)
					gidTemp = int(gid)
					byte1 = gidTemp % 255
					gidTemp = math.floor(gidTemp / 255)
					byte2 = gidTemp % 255
					gidTemp = math.floor(gidTemp / 255)
					byte3 = gidTemp % 255
					gidTemp = math.floor(gidTemp / 255)
					byte4 = gidTemp
					fp.write(struct.pack('>B', byte4))
					fp.write(struct.pack('>B', byte3))
					fp.write(struct.pack('>B', byte2))
					fp.write(struct.pack('>B', byte1))
			
			# for y in range(self._height):
			# 	for x in range(self._width):
			# 		gid = self._map_data2[self.getTileIndex(x, y)]
			# 		if self._landid_datas.get(gid, None):
			# 			gid = self._landid_datas.get(gid, None)
			# 		gidTemp = int(gid)
			# 		byte1 = gidTemp % 255
			# 		gidTemp = math.floor(gidTemp / 255)
			# 		byte2 = gidTemp % 255
			# 		gidTemp = math.floor(gidTemp / 255)
			# 		byte3 = gidTemp % 255
			# 		gidTemp = math.floor(gidTemp / 255)
			# 		byte4 = gidTemp
			# 		fp.write(struct.pack('>B', byte4))
			# 		fp.write(struct.pack('>B', byte3))
			# 		fp.write(struct.pack('>B', byte2))
			# 		fp.write(struct.pack('>B', byte1))	
			fp.close()
		pass

	def xmlObjectToString(root):
		xmlString = ""
		
		pass
		
mapUtil = MapUtil()
mapUtil.makeMap()
mapUtil.save()