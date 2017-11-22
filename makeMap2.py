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

random.seed(1504507633)
isCopyright = False

file_path = "/Users/apple/Documents/workspace/slg/三国SLG项目/系统功能/地图/county/county"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map_src"

gidFilllDatas = {}
gidModifyDatas = {}
if isCopyright:
	file_path = file_path + "_copyright.tmx"
	save_path = save_path + "_copyright.tmx"
	gidModifyDatas = {
		15:100,
		16:150,
	}
else:
	file_path = file_path + ".tmx"
	save_path = save_path + ".tmx"
	gidModifyDatas = {
		"91":7002,
		"92":2,
		"94":1,
		"95":1,
		"96":1,
		"97":1,
		"98":1,
		"99":1,
		"100":1,
	}
cell_width = 10
cell_height = 10

class MapUtil(object):
	_map_data = {}
	_width = 0
	_height = 0
	_tree = None
	_cityDatas = {}
	_checkPointDatas = {}
	_wharfDatas = {}
	_distributionDatas = {}
	_countyDbDatas = {}
	_countyDatas = {}
	_mountainDatas = {}
	_mountainArrayDatas = {}
	def __init__(self):
		pass
	def initWharfDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_wharf.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2 or row[0] == "":
					continue
				x = int(row[4])
				y = int(row[5])
				index = self.getTileIndex(x, y)
				self._wharfDatas[index] = row
		pass

	def initFillDatas(self):
		firstgids = {}
		maptree = self._tree.getroot()
		tilesets = maptree.findall("tileset")
		for tileset in tilesets:
			image = tileset.find("image")
			firstgids[image.get("source")] = int(tileset.get("firstgid"))
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_mountain.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
					continue
				if firstgids.get(row[2], 0) != 0: 
					offsetDataStrs = row[3].split(',')
					gidModifyDatas[str(firstgids.get(row[2]))] = int(row[0]) * 100000 + 7001
					gidFilllDatas[firstgids.get(row[2])] = {"coordinateDatas":[]}
					self._mountainDatas[row[0]] = {"coordinateDatas":[]}
					for offsetDataStr in offsetDataStrs:
						offsetData = offsetDataStr.split('|')
						gidFilllDatas[firstgids.get(row[2])].get("coordinateDatas").append([int(offsetData[0]), int(offsetData[1])])
						if int(offsetData[0]) == 0 and int(offsetData[1]) == 0:
							self._mountainDatas[row[0]].get("coordinateDatas").append([int(offsetData[0]), int(offsetData[1]), int(row[0]) * 100000 + 7001])
						else:
							self._mountainDatas[row[0]].get("coordinateDatas").append([int(offsetData[0]), int(offsetData[1]), 7001])
		print("gidModifyDatas=", gidModifyDatas)
		print("firstgids=", firstgids)
		print("gidFillDatas", gidFilllDatas)
		pass
	def initMountainDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_mountain_array.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
					continue
				mountainArryId = row[0]
				mountainsStr = row[2].split(',')
				self._mountainArrayDatas[row[0]] = {"coordinateDatas":[]}
				for mountainStr in mountainsStr:
					mountain = mountainStr.split('|')
					mountainId = mountain[0]
					mountainX = int(mountain[1])
					mountainY = int(mountain[2])
					mountainData = self._mountainDatas.get(mountainId)
					for coordinateData in mountainData.get("coordinateDatas"):
						self._mountainArrayDatas[row[0]].get("coordinateDatas").append([coordinateData[0] + mountainX, coordinateData[1] + mountainY, coordinateData[2]])
		print("mountainArrayDatas=", self._mountainArrayDatas)
	def initCityDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_city.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
					continue
				x = int(row[4])
				y = int(row[5])
				index = self.getTileIndex(x, y)
				self._cityDatas[index] = row
		pass

	def initCheckPoint(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_roadblocks.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
					continue
				if row[0] == '':
					break
				x = int(row[4])
				y = int(row[5])
				index = self.getTileIndex(x, y)
				landId = int(row[6])
				self._checkPointDatas[index] = row
		pass
		pass
	def initDistributionDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_distribution.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			keys = []
			values = []
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 1:
					continue
				if i == 2:
					keys = row
				if i == 3:
					values = row
			for i in range(1, len(keys)):
				key = keys[i]
				value = values[i]
				self._distributionDatas[key] = value
			pass
		print("distri==", self._distributionDatas)
	# 州郡表
	def initCountyDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_eparchy.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
					continue
				self._countyDbDatas[row[0]] = {"stateId":row[3]}

	def makeMap(self):
		self._tree = et.parse(file_path)
		maptree = self._tree.getroot()
		self._width = int(maptree.get("width"))
		self._height = int(maptree.get("height"))
		self.initFillDatas()
		self.initWharfDatas()
		self.initCityDatas()
		self.initCheckPoint()
		self.initDistributionDatas()
		self.initCountyDatas()
		self.initMountainDatas()
		maptree.set("tileheight", "200")
		maptree.set("tilewidth", "400")
		tilesets = maptree.findall("tileset")
		for tileset in tilesets:
			if tileset.get("firstgid") == "1":
				tileset.set("tilewidth", "400")
				tileset.set("tileheight", "200")
				tileset.set("columns", "5")
				image = tileset.find("image")
				image.set("source", "res2.png")
				image.set("width", "2000")
				image.set("height", "800")
			else:
				maptree.remove(tileset)
		pass
		layers = maptree.findall("layer")
		for layer in layers:
			if layer.get("name") == "块层 1":
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._countyDatas = text.split(',')
		for layer in layers:
			if layer.get("name") == "块层 2":
				layer.set("name", "map")
				data = layer.find("data")
				text = data.text.replace('\n', '')
				self._map_data = text.split(',')
				for x in range(self._width):
					for y in range(self._height):
						index = self.getTileIndex(x, y)
						gid = self._map_data[index]
						gidModifyData = gidModifyDatas.get(gid)
						if gidModifyData != None:
							self._map_data[index] = gidModifyData
						gidFilllData = gidFilllDatas.get(int(gid))
						if gidFilllData != None:
							for coordinateData in gidFilllData.get("coordinateDatas"):
								fillX = x + coordinateData[0]
								fillY = y + coordinateData[1]
								if fillX >= 0 and fillX < self._width and fillY >= 0 and fillY < self._height:
									tileIndex = self.getTileIndex(fillX, fillY)
									if self._map_data[tileIndex] == "0":
										self._map_data[tileIndex] = 7001#山
								pass
						wharfData = self._wharfDatas.get(index)
						wharfExtendDatas = {
							4001:[1, 0],
							4002:[-1, 0],
							4003:[0, -1],
							4004:[0, 1]
						}
						if wharfData != None:
							self._map_data[index] = int(wharfData[0]) * 100000 + int(wharfData[6])
							wharfExtendData = wharfExtendDatas.get(int(wharfData[6]))
							wharfExtendIndex = self.getTileIndex(x + wharfExtendData[0], y + wharfExtendData[1])
							self._map_data[wharfExtendIndex] = int(wharfData[0]) * 100000 + int(wharfData[6]) + 4

						cityData = self._cityDatas.get(index)
						if cityData != None:
							size = cityData[8].split('|')
							width = int(size[0])
							height = int(size[1])
							centerCityGid = int(cityData[0]) * 100000 + int(cityData[6])
							branchCityGid = int(cityData[0]) * 100000 + int(cityData[7])
							for xx in range(x - math.floor(width * 0.5), x + math.floor(width * 0.5) + 1):
								for yy in range(y - math.floor(height * 0.5), y + math.floor(height * 0.5) + 1):
									index = self.getTileIndex(xx, yy)
									if xx == x and yy == y:
										self._map_data[index] = centerCityGid
									else:
										self._map_data[index] = branchCityGid

						checkPointData = self._checkPointDatas.get(index)
						if checkPointData != None:
							self._map_data[index] = int(checkPointData[0]) * 100000 + int(checkPointData[6])

				numStr = self._distributionDatas["mountainNum"]
				numData = numStr.split('|')
				mountainCellWidth = int(numData[0])
				mountainCellXCount = math.ceil(self._width / mountainCellWidth)
				for cellX  in range(mountainCellXCount):
					for cellY in range(mountainCellXCount):
						x_start = mountainCellWidth * cellX
						x_end = x_start + mountainCellWidth
						if x_end > self._width:
							x_end = self._width
						y_start = mountainCellWidth * cellY
						y_end = y_start + mountainCellWidth
						if y_end > self._height:
							y_end = self._height
						mountainCount = int(numData[1])
						repeatCount = 0
						while mountainCount > 0 and repeatCount < 10000:
							repeatCount += 1;
							x = random.randint(x_start, x_end - 1)
							y = random.randint(y_start, y_end - 1)
							mountainArryId = random.randint(1, 10)
							mountainArrayData = self._mountainArrayDatas.get(str(mountainArryId))
							ret = True
							for coordinateData in mountainArrayData.get("coordinateDatas"):
								for xx in range(coordinateData[0] + x - 5, coordinateData[0] + x + 5 + 1):
									for yy in range(coordinateData[1] + y - 5, coordinateData[1] + y + 5 + 1):
										index = self.getTileIndex(xx, yy)
										if index == None or self._map_data[index] != "0":
											ret = False
											break
									if not ret:
										break
								if not ret:
									break
							if ret:
								for coordinateData in mountainArrayData.get("coordinateDatas"):
									xx = coordinateData[0] + x
									yy = coordinateData[1] + y
									if int(self._map_data[self.getTileIndex(xx, yy)]) <= 7001:
										self._map_data[self.getTileIndex(xx, yy)] = coordinateData[2]
								mountainCount -= 1

				cell_width = int(self._distributionDatas["range"])
				cell_height = cell_width
				cell_x_count = math.ceil(self._width / cell_width)
				cell_y_count = math.ceil(self._height / cell_height)
							# for stateBlockData in stateBlockDatas[stateId]:
							# 	keys = list(resDatas.keys())
							# 	keyIndex = random.randint(0, len(keys) - 1)
							# 	resIndex = keys[keyIndex]
							# 	ret = True
							# 	while (resDatas[resIndex] == 1001 or resDatas[resIndex] == 1002) and ret:
							# 		distance = math.floor(float(self._distributionDatas["fortressRange"]))
							# 		xx_start = stateBlockData["x"] - distance
							# 		xx_end = stateBlockData["x"] + distance
							# 		if xx_start < 0:
							# 			xx_start = 0
							# 		if xx_end > self._width:
							# 			xx_end = self._width
							# 		yy_start = stateBlockData["y"] - distance
							# 		yy_end = stateBlockData["y"] + distance
							# 		ret = False
							# 		if yy_start < 0:
							# 			yy_start = 0
							# 		if yy_end > self._width:
							# 			yy_end = self._width
							# 		for xx in range(xx_start, xx_end):
							# 			for yy in range(yy_start, yy_end):
							# 				index = self.getTileIndex(xx, yy)
							# 				if self._map_data[index] == 1001 or self._map_data[index] == 1002:
							# 					ret = True
							# 					break
							# 			if ret:
							# 				print("haha=======", stateId, len(stateBlockDatas[stateId]))
							# 				keyIndex = random.randint(0, len(keys) - 1)
							# 				resIndex = keys[keyIndex]
							# 				break
							# 	if resDatas[resIndex] == 1001 or resDatas[resIndex] == 1002:
							# 		index = self.getTileIndex(stateBlockData["x"], stateBlockData["y"])
							# 		self._map_data[index] = resDatas[resIndex]
							# 		resDatas.pop(resIndex)

				for cell_x  in range(cell_x_count):
					for cell_y in range(cell_y_count):
						print(cell_x, cell_y)
						x_start = cell_width * cell_x
						x_end = x_start + cell_width
						if x_end > self._width:
							x_end = self._width
						y_start = cell_height * cell_y
						y_end = y_start + cell_height
						if y_end > self._height:
							y_end = self._height
						stateBlockDatas = {}
						for x in range(x_start, x_end):
							for y in range(y_start, y_end):
								index = self.getTileIndex(x, y)
								countyId = self._countyDatas[index]
								if countyId == "97":
									continue
								if self._map_data[index] != "0":
									continue
								stateId = self._countyDbDatas[countyId].get("stateId")
								stateBlockDatas[stateId] = stateBlockDatas.get(stateId, [])
								stateBlockDatas[stateId].append({"x":x, "y":y})
						for stateId in stateBlockDatas:
							stateBlockCount = len(stateBlockDatas[stateId])
							resStr = self._distributionDatas["landType" + str(stateId)]
							resStr_1 = resStr.split(',')
							resDatas = {}
							maxCount = 0
							for ret in resStr_1:
								resStr_2 = ret.split('|')
								maxCount += int(resStr_2[1])
							curCount = 0
							for ret in resStr_1:
								resStr_2 = ret.split('|')
								gid = int(resStr_2[0])
								count = int(resStr_2[1])
								count = math.floor(stateBlockCount * count / maxCount)
								for i in range(curCount, curCount + count):
									resDatas[i] = gid
								curCount += count
							if curCount < stateBlockCount:
								for i in range(curCount, stateBlockCount):
									resDatas[i] = 1
							keys = list(resDatas.keys())
							fortressDatas = []
							for i in range(len(keys)):
								resIndex = keys[i]
								if resDatas[resIndex] == 1001 or resDatas[resIndex] == 1002:
									fortressDatas.append(resIndex)
							blockDatas = stateBlockDatas[stateId]
							for resIndex in fortressDatas:
								gid = None
								ret = True
								index = None
								blockDataIndex = None
								while ret:
									blockDataIndex = random.randint(0, len(blockDatas) - 1)
									blockData = blockDatas[blockDataIndex] 
									index = self.getTileIndex(blockData["x"], blockData["y"])
									gid = self._map_data[index]
									distance = math.floor(float(self._distributionDatas["fortressRange"]))
									xx_start = blockData["x"] - distance
									xx_end = blockData["x"] + distance
									if xx_start < 0:
										xx_start = 0
									if xx_end > self._width:
										xx_end = self._width
									yy_start = blockData["y"] - distance
									yy_end = blockData["y"] + distance
									ret = False
									if yy_start < 0:
										yy_start = 0
									if yy_end > self._width:
										yy_end = self._width
									for xx in range(xx_start, xx_end):
										for yy in range(yy_start, yy_end):
											indexTemp = self.getTileIndex(xx, yy)
											if  type(self._map_data[indexTemp]) == type(1) and self.isNpc(self._map_data[indexTemp]):
												ret = True
												break
										if ret:
											print("haha=======", stateId, len(stateBlockDatas[stateId]))
											break
								self._map_data[index] = resDatas[resIndex]
								resDatas.pop(resIndex)
								blockDatas.pop(blockDataIndex)
							for stateBlockData in stateBlockDatas[stateId]:
								keys = list(resDatas.keys())
								keyIndex = random.randint(0, len(keys) - 1)
								resIndex = keys[keyIndex]
								index = self.getTileIndex(stateBlockData["x"], stateBlockData["y"])
								self._map_data[index] = resDatas[resIndex]
								resDatas.pop(resIndex)
				newStrData = ""
				for y in range(self._height):
					newStrData += "\n"
					for x in range(self._width):
						countyId = self._countyDatas[self.getTileIndex(x, y)]
						if self._map_data[self.getTileIndex(x, y)] == "0":
						 	print("fuck=====", x, y)
						if countyId == "97":
							landId = int(self._map_data[self.getTileIndex(x, y)]) % 100000
							if landId != 7002 and landId != 7001 and not (landId >= 5001 and landId <= 5010) and not (landId >= 4001 and landId <= 4008):
								print("hehe==", self._map_data[self.getTileIndex(x, y)], x, y)
						newStrData += str(self._map_data[self.getTileIndex(x, y)]) + ","
				newStrData = newStrData[:-1] + '\n'
				data.text = newStrData
			else:
				maptree.remove(layer)
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
		self._tree.write(save_path, encoding="UTF-8", xml_declaration=True)
		pass
	def isNpc(self, id):
		landId = id % 100000
		return landId == 1001 or landId == 1002
		# return landId == 2011 or landId == 1001 or landId == 1002 or (landId >= 4001 and landId <= 4008)
		pass
	def xmlObjectToString(root):
		xmlString = ""
		
		pass
		
mapUtil = MapUtil()
mapUtil.makeMap()
mapUtil.save()