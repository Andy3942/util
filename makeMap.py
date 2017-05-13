#!/usr/bin/env python3
# coding=utf-8

import os
import math
import string
import xml.etree.ElementTree as et
import re
import pprint
import random

file_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_copyright_src.tmx"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_copyright.tmx"

cell_width = 10
cell_height = 10

gids = [1,2,3,4,5,6,7]

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
			if layer.get("name") == "resource":
				self._width = int(layer.get("width"))
				self._height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				map_data = text.split(',')
				for i in range(math.ceil(self._height / cell_height)):
					for j in range(math.ceil(self._width / cell_width)):
						for cell_y in range(cell_height):
							y = i * cell_height + cell_y
							if y >= self._height:
								break
							for cell_x in range(cell_width):
								x = j * cell_width + cell_x
								if x >= self._width:
									break
								index = self.getTileIndex(x, y)
								gidIndex = random.randint(0, 10)
								gid = 0
								if gidIndex < len(gids):
									gid = gids[gidIndex]
								map_data[index] = gid
				newStrData = ""
				for y in range(self._height):
					newStrData += "\n"
					for x in range(self._width):
						newStrData += str(map_data[self.getTileIndex(x, y)]) + ","
				newStrData = newStrData[:-1] + '\n'
				data.text = newStrData
		pass
	def getTileIndex(self, x, y):
		return y * self._height + x
		pass

	def save(self):
		self._tree.write(save_path, encoding="UTF-8", xml_declaration=True)
		pass

	def xmlObjectToString(root):
		xmlString = ""
		
		pass
		
mapUtil = MapUtil()
mapUtil.makeMap()
mapUtil.save()