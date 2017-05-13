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
from pprint import pprint

isCopyright = False

file_path = "/Users/apple/Documents/workspace/slg/三国SLG项目/系统功能/地图/county/county"
save_path = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map"

gidFilllDatas = {}
gidModifyDatas = {}
if isCopyright:
	file_path = file_path + "_copyright.tmx"
	save_path = save_path + "_copyright.tmx"
	gidModifyDatas = {
		15:99,
		16:149,
	}
else:
	file_path = file_path + ".tmx"
	save_path = save_path + ".tmx"
	gidModifyDatas = {
		"91":99,
		"92":149,
		"94":0,
		"95":0,
		"96":0,
		"97":0,
		"98":0,
		"99":0,
		"100":0,
	}
cell_width = 10
cell_height = 10


gids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,399]

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
	def __init__(self):
		pass
	def initWharfDatas(self):
		with open("/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_wharf.csv", newline='', encoding="gbk") as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				i = i + 1
				if i <= 2:
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
					gidModifyDatas[str(firstgids.get(row[2]))] = 199 + int(row[0])
					gidFilllDatas[firstgids.get(row[2])] = {"coordinateDatas":[]}
					for offsetDataStr in offsetDataStrs:
						offsetData = offsetDataStr.split('|')
						gidFilllDatas[firstgids.get(row[2])].get("coordinateDatas").append([int(offsetData[0]), int(offsetData[1])])
		print("gidModifyDatas=", gidModifyDatas, firstgids)
		pass

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
		maptree.set("tileheight", "200")
		maptree.set("tilewidth", "400")
		tilesets = maptree.findall("tileset")
		for tileset in tilesets:
			if tileset.get("firstgid") == "1":
				tileset.set("tilewidth", "400")
				tileset.set("tileheight", "200")
				tileset.set("columns", "5")
				image = tileset.find("image")
				image.set("source", "res.png")
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
										self._map_data[tileIndex] = 199#山
								pass
						wharfData = self._wharfDatas.get(index)
						wharfExtendDatas = {
							1:[1, 0],
							2:[-1, 0],
							3:[0, -1],
							4:[0, 1]
						}
						if wharfData != None:
							self._map_data[index] = 299 + int(wharfData[8])
							wharfExtendData = wharfExtendDatas.get(int(wharfData[8]))
							wharfExtendIndex = self.getTileIndex(x + wharfExtendData[0], y + wharfExtendData[1])
							self._map_data[wharfExtendIndex] = 309 + int(wharfData[8])

						cityData = self._cityDatas.get(index)
						if cityData != None:
							size = cityData[8].split('|')
							width = int(size[0])
							height = int(size[1])
							centerCityGid = int(cityData[0]) * 100000 + int(cityData[6]) - 1
							branchCityGid = int(cityData[0]) * 100000 + int(cityData[7]) - 1
							for xx in range(x - math.floor(width * 0.5), x + math.floor(width * 0.5) + 1):
								for yy in range(y - math.floor(height * 0.5), y + math.floor(height * 0.5) + 1):
									index = self.getTileIndex(xx, yy)
									if xx == x and yy == y:
										self._map_data[index] = centerCityGid
									else:
										self._map_data[index] = branchCityGid

						checkPointData = self._checkPointDatas.get(index)

						if checkPointData != None:
							self._map_data[index] = int(checkPointData[0]) * 100000 + int(checkPointData[6]) - 1
							# y = i * cell_height + cell_y
							# if y >= self._height:
							# 	break
							# for cell_x in range(cell_width):
							# 	x = j * cell_width + cell_x
							# 	if x >= self._width:
							# 		break
								
							# 	gidIndex = random.randint(0, 10)
							# 	gid = 0
							# 	if gidIndex < len(gids):
							# 		gid = gids[gidIndex]
							# 	map_data[index] = gid
				cell_width = int(self._distributionDatas["range"])
				cell_height = cell_width
				cell_x_count = math.ceil(self._width / cell_width)
				cell_y_count = math.ceil(self._height / cell_height)
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
						for x in range(x_start, x_end - 1):
							for y in range(y_start, y_end -1):
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
							curCount = 0
							for ret in resStr_1:
								resStr_2 = ret.split('|')
								gid = int(resStr_2[0]) - 1
								count = int(resStr_2[1])
								count = math.floor(stateBlockCount * count / (cell_width * cell_height))
								for i in range(curCount, curCount + count):
									resDatas[i] = gid
								curCount += count
							if curCount < stateBlockCount:
								for i in range(curCount, stateBlockCount):
									resDatas[i] = 0
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
						newStrData += str(self._map_data[self.getTileIndex(x, y)]) + ","
				newStrData = newStrData[:-1] + '\n'
				data.text = newStrData
			else:
				maptree.remove(layer)
		pass
	def getTileIndex(self, x, y):
		return y * self._height + x
		pass

	def save(self):
		# tilesets = self._tree.getroot().findall("tileset")
		# for tileset in tilesets:
		# 	print(tileset.get("firstgid"))
		# pass
		self._tree.write(save_path, encoding="UTF-8", xml_declaration=True)
		pass

	def xmlObjectToString(root):
		xmlString = ""
		
		pass
		
mapUtil = MapUtil()
mapUtil.makeMap()
mapUtil.save()