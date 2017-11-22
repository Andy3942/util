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

file_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/grass.tmx"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/ui/map/grass.dat"

class MapUtil(object):
	_base_grass_map_data = {}
	_additional_grass_map_data = {}
	_width = 0
	_height = 0
	_tree = None
	def __init__(self):
		pass

	def makeMap(self):	
		self._tree = et.parse(file_path)
		layers = self._tree.findall("layer")
		for layer in layers:
			if layer.get("name") == "草":
				self._width = int(layer.get("width"))
				self._height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._base_grass_map_data = text.split(',')
			elif layer.get("name") == "浅草":
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._additional_grass_map_data = text.split(',')

		pass
	def getTileIndex(self, x, y):
		return y * self._height + x
		pass

	def save(self):
		strData = ""
		with open(save_path, "wb") as fp:
			for y in range(self._height):
				for x in range(self._width):
					base_grass_map_data_value = int(self._base_grass_map_data[self.getTileIndex(x, y)])
					additional_grass_map_data_value = int(self._additional_grass_map_data[self.getTileIndex(x, y)])
					fp.write(struct.pack('>B', base_grass_map_data_value * 10 + additional_grass_map_data_value))
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