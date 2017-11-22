#!/usr/bin/env python3
# coding=utf-8

import math
import struct

save_path = "/Users/apple/Documents/workspace/MyGame/res/area.dat"

cell_width = math.floor(1000/13.7)
cell_height = cell_width
class AreaUtil(object):
	_map_data = {}
	_width = 1500
	_height = 1500

	def makeArea(self):
		area = 1
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
						if area <= 189 and cell_y == (cell_height - 1) or cell_x == (cell_width - 1):
							self._map_data[index] = 255
						else:
							self._map_data[index] = area
				area += 1
				if area > 189:
					area = 189

	def getTileIndex(self, x, y):
		return y * self._height + x
		pass

	def save(self):
		strData = ""
		with open(save_path, "wb") as fp:
			for y in range(self._height):
				for x in range(self._width):
					fp.write(struct.pack('>B',self._map_data[self.getTileIndex(x, y)]))
					#strData += chr(self._map_data[self.getTileIndex(x, y)])
				#strData = strData[:-1] + '\n'
			#print(len(strData))	
			fp.close()
		pass
areaUtil = AreaUtil()
areaUtil.makeArea()
areaUtil.save()