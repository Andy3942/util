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

file_path = sys.argv[1]
filename = os.path.basename(file_path)[:-4]
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/script/ui/copy/copyMap/" + filename + ".lua"
terrain_path = file_path[:-4] + "_terrain.dat"
map_path = save_path[:-4] + ".dat"

print(file_path, save_path)

class MapUtil(object):
	_layerCount = 0
	_map_data = {}
	_terrain_data = {}
	_width = 0
	_height = 0
	_tree = None
	_landid_datas = {}
	_luaStr = ""
	def __init__(self):
		pass
	def initLayerCount(self):
		layers = self._tree.findall("layer")
		self._layerCount = len(layers) - 1
		pass

	def getTileIndex(self, x, y):
		if x < 0 or x >= self._width or y < 0 or y >= self._height:
			return None
		return y * self._height + x
		pass
		
	def makeMap(self):	
		self._tree = et.parse(file_path)
		self.initLayerCount()
		self._luaStr = "module(\"{0}\", package.seeall)\n".format(filename)
		self._luaStr += "layerCount = {0}\n".format(self._layerCount - 1)
		self._luaStr += "tileDatas = {\n"
		tilesets = self._tree.findall("tileset")
		for i in range(len(tilesets)):
			if i == 0:
				continue
			tileset = tilesets[i]
			firstgid = tileset.get("firstgid")
			source = tileset.find("image").get("source")
			tileoffset = tileset.find("tileoffset")
			offsetX = 0
			offsetY = 0
			if tileoffset != None:
				offsetX = tileoffset.get("x")
				offsetY = tileoffset.get("y")
			self._luaStr += "[{0}] = {{gid = {0}, source = \"{1}\", offsetX = {2}, offsetY = {3}}},\n".format(firstgid, source, offsetX, offsetY)
		self._luaStr += "}\n"
		layers = self._tree.findall("layer")
		for i in range(self._layerCount):
			if i == 0:
				continue
			layer = layers[i]
			self._width = int(layer.get("width"))
			self._height = int(layer.get("height"))
			data = layer.find("data")
			text = data.text.replace('\n', '')
			self._map_data[i] = text.split(',')
		pass

	def save(self):
		with open(save_path, "w") as fp:
			fp.write(self._luaStr)
			fp.close()
		self._luaStr = ""
		with open(map_path, "wb") as fp:
			for i in range(self._layerCount):
				if i == 0:
					continue
				for y in range(self._height):
					for x in range(self._width):
						gid = self._map_data[i][self.getTileIndex(x, y)]
						gidTemp = int(gid)
						byte1 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte2 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte3 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte4 = gidTemp
						self._luaStr += chr(byte4)
						self._luaStr += chr(byte3)
						self._luaStr += chr(byte2)
						self._luaStr += chr(byte1)
			fp.write(bytes(self._luaStr, "latin1"))
			fp.close()
		self._luaStr = ""
		os.system('/Users/apple/Documents/workspace/git/util/makeTerrain.py ' + file_path)
		with open(terrain_path, "rb") as fp:
			text = fp.read()
			for c in text:
				self._luaStr += chr(c)
			fp.close()
		with open(save_path[:-4] + "_terrain.dat", "wb") as fp:
			fp.write(self._luaStr.encode("latin1"))
			fp.close()
	def xmlObjectToString(root):
		xmlString = ""
		
		pass
		
mapUtil = MapUtil()
mapUtil.makeMap()
mapUtil.save()