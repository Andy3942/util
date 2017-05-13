#!/usr/bin/env python3
# coding=utf-8

import os,sys,csv,math
import xml.etree.ElementTree as et

isCopyright = False

countyFilename = "/Users/apple/Documents/workspace/slg/三国SLG项目/系统功能/地图/county/county"
mapFilename = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/map"
cityFilename = "/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_city.csv"
positionFilename = "/Users/apple/Documents/workspace/git/sangoslg/SangoSLG/Resources/res/images/map/position"
countDbFilename = "/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_eparchy.csv"
stateDbFilename = "/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_state.csv"
distributionDbFilename = "/Users/apple/Documents/workspace/slg/三国SLG项目/正式策划案/导出工具表/导出csv表/land_distribution.csv"

if isCopyright:
	countyFilename = countyFilename + "_copyright.tmx"
	mapFilename = mapFilename + "_copyright.tmx"
	positionFilename = positionFilename + "_copyright.txt"
else:
	countyFilename = countyFilename + ".tmx"
	mapFilename = mapFilename + ".tmx"
	positionFilename = positionFilename + ".txt"

if __name__ == '__main__':
	width = 0
	height = 0
	# 州郡分布
	countyDatas = []
	tree = et.parse(countyFilename)
	countyRoot = tree.getroot()
	layers = countyRoot.findall("layer")
	for layer in layers:
		if layer.get("name") == "块层 1":
				width = int(layer.get("width"))
				height = int(layer.get("height"))
				data = layer.find("data")
				text = data.text.replace('\n', '')
				countyDatas = text.split(',')
	def getTileIndex(x, y):
		return y * height + x
	pass

	def isHaveGid(x, y, distance, gids):
		distanceTemp = math.ceil(distance)
		for xx in range(x - distanceTemp, x + distanceTemp):
			for yy in range(y - distanceTemp, y + distanceTemp):
				curDistance = math.sqrt(math.pow(xx - x, 2) + math.pow(yy - y, 2))
				if curDistance <= distance:
					for gid in gids:
						if xx < 0 or xx >= width or yy < 0 or yy >= height:
							if gid == -1:
								return True
						else:
							index = getTileIndex(xx, yy)
							curGid = int(mapDatas[index])
							if gid == -2:
								if curGid >= 2001 and curGid <= 2011:
									return True
							else:
								if gid == curGid:
									return True

	# 地图数据
	mapDatas = []
	mapTree = et.parse(mapFilename)
	mapRoot = mapTree.getroot()
	layers = mapRoot.findall("layer")
	for layer in layers:
		if layer.get("name") == "map":
			data = layer.find("data")
			text = data.text.replace('\n', '')
			mapDatas = text.split(',')
 	# 城池表
	cityDatas = []
	with open(cityFilename, newline='', encoding="gbk") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		i = 0
		for row in spamreader:
			i = i + 1
			if i <= 2 or row[0] == "255":
				continue
			x = int(row[4])
			y = int(row[5])
			size = int(row[8].split("|")[0])
			index = getTileIndex(x, y)
			cityDatas.append({"size":size, "x":x, "y":y})
	# 城池填充
	for cityData in cityDatas:
		centerDistance = math.floor(cityData.get("size") * 0.5)
		for x in range(x - centerDistance, x + centerDistance):
			for y in range(y - centerDistance, y + centerDistance):
				index = getTileIndex(x, y)
				mapDatas[index] = 1000
	# 州表
	stateDbDatas = {}
	with open(stateDbFilename, newline='', encoding="gbk") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		i = 0
		for row in spamreader:
			i = i + 1
			if i <= 2:
				continue
			born = int(row[4] or 0)
			stateDbDatas[int(row[0])] = {"born":born}
	# 州郡表
	countyDbDatas = {}
	with open(countDbFilename, newline='', encoding="gbk") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		i = 0
		for row in spamreader:
			i = i + 1
			if i <= 2:
				continue
			stateId = int(row[3])
			stateDb = stateDbDatas.get(stateId, None)
			if stateDb != None:
				countyDbDatas[int(row[0])] = {"born":stateDb["born"], "stateId":stateId}

	# 限制
	distributionDatas = {}
	with open(distributionDbFilename, newline='', encoding="gbk") as csvfile:
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
			distributionDatas[key] = value

	# 处理不能做为出生州的州郡
	for y in range(height):
		for x in range(width):
			index = getTileIndex(x, y)
			countyId = int(countyDatas[index])
			if countyId == 97:
				countyId = 255
			countyDbData = countyDbDatas[countyId]
			if countyDbData["born"] == 0:
				countyDatas[index] == 0

	with open(positionFilename, "w") as fp:
		for y in range(3, height - 3):
			for x in range(3, width - 3):
				base = True
				for yy in range(y - 1, y + 1):
					for xx in range(x - 1, x + 1):
						index = getTileIndex(xx, yy)
						countyId = int(countyDatas[index])
						if countyId == 97:
							countyId = 255
						mapGid = int(mapDatas[index]) % 100000
						ret = {}
						# 水
						ret[1] = mapGid == 91 
						# 山
						ret[2] = mapGid >= 200 and mapGid < 300
						# 要塞
						ret[3] = mapGid == 399
						# 码头
						ret[4] = mapGid >= 300 and mapGid <= 320
						# npc城池
						ret[5] = mapGid >= 2001 and mapGid <= 2011
						# 边界
						ret[6] = countyId == 255
						#  非出生州
						ret[7] = countyId == 0
						# 玩家城池
						ret[8] = mapGid == 1001
						if ret[1] or ret[2] or ret[3] or ret[4] or ret[4] or ret[5] or ret[6] or ret[7] or ret[8]:
							base = False
							break
					if base == False:
						break

				# 主城周围指定等级的资源地数量要求
				if base == True:
					resCondition = {}
					ret = distributionDatas["landNum"].split(',')
					for data in ret:
						retTemp = data.split('|')
						resCondition[int(retTemp[0])] = int(retTemp[1]) 
					resCountDatas = {}
					for yy in range(y - 2, y + 2):
						for xx in range(x - 2, x + 2):
							xDistance = abs(xx - x)
							yDistance = abs(yy - y)
							distance = max(xDistance, yDistance)
							if distance == 2:
								index = getTileIndex(xx, yy)
								mapGid = int(mapDatas[index])
								level = None
								if mapGid == 0:
									level = 1
								elif mapGid == 2 or mapGid == 8 or mapGid == 14:
									level = 2
								if level != None:
									resCountDatas[level] = resCountDatas.get(level, 0)
									resCountDatas[level] += 1
					for key in resCondition:
						level = key
						countCondition = resCondition[level]
						count = resCountDatas.get(level, 0)
						if count < countCondition:
							base = False
							break
						pass
				# 河流
				if base == True:
					base = not isHaveGid(x, y, float(distributionDatas["riverRange"]), [100])
				# 山
				if base == True:
					base = not isHaveGid(x, y, float(distributionDatas["mountainRange"]), [200, 201, 202])
				# npc城池
				if base == True:
					base = not isHaveGid(x, y, float(distributionDatas["cityRange"]), [-2])
				# 要塞
				if base == True:
					base = not isHaveGid(x, y, float(distributionDatas["fortressRange"]), [400])
				# 玩家城池
				if base == True:
					base = not isHaveGid(x, y, float(distributionDatas["playerRange"]), [1001])
				# 边缘
				if base == True:
					base = not isHaveGid(x, y, float(distributionDatas["edgeRange"]), [-1])
				if base == True:
					for yy in range(y - 1, y + 1):
						for xx in range(x - 1, x + 1):
							index = getTileIndex(xx, yy)
							mapDatas[index] = 1001
					index = getTileIndex(x, y)
					countyId = int(countyDatas[index])
					countyDbData = countyDbDatas[countyId]
					fp.write("{0},{1},{2}\n".format(countyDbData["stateId"], x, y))
				#strData += chr(self._map_data[self.getTileIndex(x, y)])
			#strData = strData[:-1] + '\n'
		#print(len(strData))	
		fp.close()