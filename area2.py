#!/usr/bin/env python3
# coding=utf-8

import os
import math
import string
import xml.etree.ElementTree as et
import re
import pprint
import random
import struct

# file_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/county.tmx"
# save_path = "/Users/apple/Documents/workspace/MyGame/res/area_copyright.dat"
file_path = "/Users/apple/Documents/workspace/slg/三国SLG项目/系统功能/地图/county/county.tmx"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/script/ui/map/county.dat"

class MapUtil(object):
	_map_data = {}
	_width = 0
	_height = 0
	_tree = None
	def __init__(self):
		pass

	def makeMap(self):	
		self._tree = et.parse(file_path)
		layers = self._tree.findall("layer")
		for layer in layers:
			if layer.get("name") == "块层 1":
				self._width = int(layer.get("width"))
				self._height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')

		pass
	def getTileIndex(self, x, y):
		return y * self._height + x
		pass

	def save(self):
		strData = ""
		with open(save_path, "wb") as fp:
			for y in range(self._height):
				for x in range(self._width):
					gid = int(self._map_data[self.getTileIndex(x, y)])
					if gid == 97:
						gid = 255
					fp.write(struct.pack('>B', gid))
					#strData += chr(self._map_data[self.getTileIndex(x, y)])
				#strData = strData[:-1] + '\n'
			#print(len(strData))	
			fp.close()
		pass

	def xmlObjectToString(root):
		xmlString = ""
		
		pass
		
mapUtil = MapUtil()
mapUtil.makeMap()
mapUtil.save()