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

file_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_src.tmx"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/src/script/ui/map/map.dat"
gidModifyDatas = {
		"1":401,
		"2":402,
		"3":403,
		"4":404,
		"5":405,
		"6":406,
		"7":201,
		"8":202,
		"9":203,
		"10":204,
		"11":205,
		"12":206,
		"13":101,
		"14":102,
		"15":103,
		"16":104,
		"17":105,
		"18":106,
		"200":107001,
		"201":207001,
		"202":307001,
	}
class MapUtil(object):
	_map_data = {}
	_terrain_data = {}
	_width = 0
	_height = 0
	_tree = None
	def __init__(self):
		pass

	def makeMap(self):	
		self._tree = et.parse(file_path)
		layers = self._tree.findall("layer")
		for layer in layers:
			if layer.get("name") == "map":
				self._width = int(layer.get("width"))
				self._height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')

		pass
	def getTileIndex(self, x, y):
		return y * self._width + x
		pass
	def initTerrainData(self):
		for y in range(self._height):
			for x in range(self._width):
				gid = self._map_data[self.getTileIndex(x, y)]
				if gid == "99" or gid == "149":
					for xx in [x * 2, x * 2 + 1]:
						for yy in [y * 2, y * 2 + 1]:
							spaceCount = 0
							for xTemp in [xx - 1, xx, xx + 1]:
								for yTemp in [yy - 1, yy, yy + 1]:
									fuckX = math.floor(xTemp * 0.5)
									fuckY = math.floor(yTemp * 0.5)
									if fuckX >= 0 and fuckX < self._width and fuckY >= 0 and fuckY < self._height:
										if self._map_data[self.getTileIndex(fuckX, fuckY)] != gid:
											spaceCount += 1
									else:
										spaceCount += 1
							if spaceCount == 0:
								self._terrain_data[yy * self._width * 2 + xx] = 1
							elif spaceCount == 3:
								if self._map_data[self.getTileIndex(math.floor(xx * 0.5), math.floor((yy - 1) * 0.5))] != gid:
									subGid = 1 + (xx + yy) % 2 + 1
								elif self._map_data[self.getTileIndex(math.floor(xx * 0.5), math.floor((yy + 1) * 0.5))] != gid:
									subGid = 3 + (xx + yy) % 2 + 1
								elif self._map_data[self.getTileIndex(math.floor((xx - 1) * 0.5), math.floor(yy * 0.5))] != gid:
									subGid = 5 + (xx + yy) % 2 + 1
								elif self._map_data[self.getTileIndex(math.floor((xx + 1) * 0.5), math.floor(yy * 0.5))] != gid:
									subGid = 7 + (xx + yy) % 2 + 1
								self._terrain_data[yy * self._width * 2 + xx] = subGid
							elif spaceCount == 4:
								imageValue = xx % 2 * 2 + yy % 2 + 1
								self._terrain_data[yy * self._width * 2 + xx] = 20 +imageValue
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
					if gid == "99":
						byte4 = self._terrain_data.get((y * 2) * self._width * 2 + x * 2)
						byte3 = self._terrain_data.get((y * 2) * self._width * 2 + x * 2 + 1)
						byte2 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2)
						byte1 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2 + 1)
					elif gid == "149":
						byte4 = self._terrain_data.get((y * 2 ) * self._width * 2 + x * 2) + 100
						byte3 = self._terrain_data.get((y * 2 ) * self._width * 2 + x * 2 + 1) + 100
						byte2 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2) + 100
						byte1 = self._terrain_data.get((y * 2+1) * self._width * 2 + x * 2 + 1) + 100
					else:
						gidModify = gidModifyDatas.get(gid)
						gidTemp = None
						if gidModify != None:
							gid = gidModify
							gidTemp = gid
						else:
							gid = int(gid) 
							gidTemp = gid + 1
						byte1 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte2 = gidTemp % 255
						gidTemp = math.floor(gidTemp / 255)
						byte3 = gidTemp
						byte4 = 0
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