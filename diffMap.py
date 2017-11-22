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
import csv
from pprint import pprint

file_path = sys.argv[1]
file_path2 = sys.argv[2]

class MapUtil(object):
	_map_data = {}
	_map_data2 = {}
	_width = 0
	_height = 0
	def __init__(self):
		pass

	def diffMap(self):
		tree = et.parse(file_path)
		maptree = tree.getroot()
		self._width = int(maptree.get("width"))
		self._height = int(maptree.get("height"))
		layers = maptree.findall("layer")
		for layer in layers:
			if layer.get("name") == "map":
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')
		tree = et.parse(file_path2)
		maptree = tree.getroot()
		layers = maptree.findall("layer")
		for layer in layers:
			if layer.get("name") == "map":
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data2 = text.split(',')
		for x in range(self._width):
			for y in range(self._height):
				index = self.getTileIndex(x, y)
				gid = self._map_data[index]
				gid2 = self._map_data2[index]
				if gid != gid2:
					print(x, y, gid, gid2)
		pass
	def getTileIndex(self, x, y):
		if x < 0 or x >= self._width or y < 0 or y >= self._height:
			return None
		return y * self._height + x
		pass
		
mapUtil = MapUtil()
mapUtil.diffMap()