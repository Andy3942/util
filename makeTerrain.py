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
import struct

file_path = None
if len(sys.argv) > 1:
	file_path = sys.argv[1]
mapName = "map"
if file_path:
	save_path = file_path[:-4] + "_terrain" + ".dat"
	mapName = "lay_1"
else:
	file_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_src.tmx"
	save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/script/ui/map/terrain.dat"

# file_path = file_path + ".tmx"
# save_path = save_path + ".dat"

class MapUtil(object):
	_map_data = {}
	_terrain_data = {}
	_width = 0
	_height = 0
	_tree = None
	_landid_datas = {}
	
	def __init__(self):
		pass

	def initLandId(self):
		self._landid_datas = {"1":"7002", "2":"2"} 

	def makeMap(self):	
		self._tree = et.parse(file_path)
		if mapName != "map":
			self.initLandId()
		layers = self._tree.findall("layer")
		for layer in layers:
			if layer.get("name") == mapName:
				self._width = int(layer.get("width"))
				self._height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')
		for y in range(self._height):
			for x in range(self._width):
				gid = self._map_data[self.getTileIndex(x, y)]
				if self._landid_datas.get(gid, None):
					gid = self._landid_datas.get(gid, None)
					self._map_data[self.getTileIndex(x, y)] = str(gid)
				if (int(gid) % 100000 >= 4005 and int(gid) % 100000 <= 4008):
					self._map_data[self.getTileIndex(x, y)] = "7002"
		pass
	def getTileIndex(self, x, y):
		return y * self._width + x
		pass

	def getMapGid(self, x, y):
		gid = self._map_data[self.getTileIndex(x, y)]
		return gid
		pass

	def initTerrainData(self):
		for y in range(self._height):
			for x in range(self._width):
				gid = self.getMapGid(x, y)
				if gid == "7002" or gid == "2":
					for xx in [x * 2, x * 2 + 1]:
						for yy in [y * 2, y * 2 + 1]:
							spaceCount = 0
							for xTemp in [xx - 1, xx, xx + 1]:
								for yTemp in [yy - 1, yy, yy + 1]:
									fuckX = math.floor(xTemp * 0.5)
									fuckY = math.floor(yTemp * 0.5)
									if fuckX >= 0 and fuckX < self._width and fuckY >= 0 and fuckY < self._height:
										if self.getMapGid(fuckX, fuckY) != gid:
											spaceCount += 1
									else:
										spaceCount += 1
							if spaceCount == 0:
								self._terrain_data[yy * self._width * 2 + xx] = 1
							elif spaceCount == 3:
								if math.floor((yy - 1) * 0.5) < 0 or self.getMapGid(math.floor(xx * 0.5), math.floor((yy - 1) * 0.5)) != gid:
									subGid = 1 + (xx + yy) % 2 + 1
								elif math.floor((yy + 1) * 0.5) >= self._height or self.getMapGid(math.floor(xx * 0.5), math.floor((yy + 1) * 0.5)) != gid:
									subGid = 3 + (xx + yy) % 2 + 1
								elif math.floor((xx - 1) * 0.5) < 0 or self.getMapGid(math.floor((xx - 1) * 0.5), math.floor(yy * 0.5)) != gid:
									subGid = 5 + (xx + yy) % 2 + 1
								elif math.floor((xx + 1) * 0.5) >= self._width or self.getMapGid(math.floor((xx + 1) * 0.5), math.floor(yy * 0.5)) != gid:
									subGid = 7 + (xx + yy) % 2 + 1
								self._terrain_data[yy * self._width * 2 + xx] = subGid
							elif spaceCount == 4:
								imageValue = xx % 2 * 2 + yy % 2 + 1
								if imageValue == 3 or imageValue == 4:
									self._terrain_data[yy * self._width * 2 + xx] = 20 +imageValue
								else:
									self._terrain_data[yy * self._width * 2 + xx] = 0

							elif spaceCount == 5:
								imageValue = xx % 2 * 2 + yy % 2 + 1
								self._terrain_data[yy * self._width * 2 + xx] = 30 + imageValue
							elif spaceCount == 1:
								imageValue = xx % 2 * 2 + yy % 2 + 1
								positionDatas = [
									[[-1, 0], [0, 0], [0, -1]],
									[[-1, 0], [0, 0], [0, 1]],
									[[0, -1], [0, 0], [1, 0]],
									[[0, 1], [0, 0], [1, 0]]
								]
								for i in range(3):
									positionData = positionDatas[imageValue - 1]
									subGid = (imageValue + 3) * 10 + i + 1
									self._terrain_data[(yy + positionData[i][1]) * self._width * 2 + xx + positionData[i][0]] = subGid
		pass
	def save(self):
		strData = ""
		with open(save_path, "wb") as fp:
			for y in range(self._height):
				for x in range(self._width):
					gid = self._map_data[self.getTileIndex(x, y)]
					byte1 = 0
					byte2 = 0
					byte3 = 0
					byte4 = 0
					if gid == "7002":
						byte4 = self._terrain_data.get((y * 2) * self._width * 2 + x * 2, 0)
						byte3 = self._terrain_data.get((y * 2) * self._width * 2 + x * 2 + 1, 0)
						byte2 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2, 0)
						byte1 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2 + 1, 0)
					elif gid == "2":
						if self._terrain_data.get((y * 2 ) * self._width * 2 + x * 2) != None: 
							byte4 = self._terrain_data.get((y * 2 ) * self._width * 2 + x * 2) + 100
						if self._terrain_data.get((y * 2 ) * self._width * 2 + x * 2 + 1) != None:
							byte3 = self._terrain_data.get((y * 2 ) * self._width * 2 + x * 2 + 1) + 100
						if self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2) != None:
							byte2 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2) + 100
						if self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2 + 1) != None:
							byte1 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2 + 1) + 100
					elif int(gid) % 100000 == 7001 and math.floor(int(gid) / 100000) >= 1:
						gidTemp = math.floor(int(gid) / 100000) + 200
						byte1 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte2 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte3 = gidTemp
						byte4 = 0
					#if x == 0 and y == 0:
					# print("haha==",gid, x, y, byte4, byte3, byte2, byte1)
					# fp.write(str(byte4) + ",")
					# fp.write(str(byte3) + ",")
					# fp.write(str(byte2) + ",")
					# fp.write(str(byte1) + ",")
					fp.write(struct.pack('>B', byte4))
					fp.write(struct.pack('>B', byte3))
					fp.write(struct.pack('>B', byte2))
					fp.write(struct.pack('>B', byte1))
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
mapUtil.initTerrainData()
mapUtil.save()