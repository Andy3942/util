# coding=utf-8

import os
import math
import string
from xml.etree import ElementTree as ET
from xml.dom import minidom
import sys

APP 		= r"/Users/bzx/Downloads/TexturePacker.app/Contents/MacOS"
root_path 	= r"/Users/bzx/Documents/TexturePackerTest"
to_path 	= "{0}/dest".format(root_path)
src_path 	= "{0}/src".format(root_path)

class ParseAnimation:
	_ccdd = 1
	_aabb = 0
	_layer_num = 0
	_count = 0
	@staticmethod
	def texturePacker(path, new_path, animation_name):
		data = "{0}/{1}.plist".format(new_path, animation_name)
		out_format = "cocos2d"
		sheet = "{0}/{1}.png".format(new_path, animation_name)
		asserts = "{0}/LIBRARY".format(path)
		command = "{0} --data {1} --format {2} --sheet {3} {4}".format("TexturePacker", data, out_format, sheet, asserts)
		print command
		os.chdir(APP)
		os.system(command)
	
	@staticmethod
	def ParseXml(path, new_path):
		file_path = "{0}/DOMDocument.xml".format(path)
		print file_path
		tree = ET.parse(file_path)
		ns = tree.getroot().tag.split("}")[0] + "}"
		tag = ns + "timelines/" + ns + "DOMTimeline/" + ns + "layers/" + ns + "DOMLayer" 
		layer_items = tree.findall(tag)
		frame_dict = {}
		for layer_item in layer_items:
			frame_dict = {}
			ParseAnimation._layer_num = 0
			frame_num = 0
			layer_name = layer_item.get("name", "")
			frame_elements = layer_item.findall(ns + "frames/" + ns + "DOMFrame")
			for frame_element in frame_elements:
				frame_num = frame_element.get("index", "")
				frame_name = frame_element.get("name", "")
				is_key_frame = "0"
				if frame_name != "":
					is_key_frame = "1"
				frame_time = string.atoi(frame_element.get("duration", "0"))
				frame_datas = frame_element.findall(ns + "elements/" + ns + "DOMSymbolInstance")
				element_dict = {}
				frame_arr = []
				for frame_data in frame_datas:
					png_name = frame_data.get("libraryItemName", "")
					element_dict["bitmapName"] = png_name
					scale_y = "1"
					scale_x = "1"
					rota = "0"
					tx = 0
					ty = 0
					matrix_data = frame_data.find(ns + "matrix/" + ns + "Matrix")
					if matrix_data != None:
						a = string.atof(matrix_data.get("a", "1"))
						if a == 0:
							a = 1
						b = string.atof(matrix_data.get("b", "0"))
						c = string.atof(matrix_data.get("c", "0"))
						d = string.atof(matrix_data.get("d", "1"))
						if d == 0:
							d = 1
						rota = ParseAnimation.getRotation(a, b, c, d)
						scale_x = ParseAnimation.getScaleX(a, b, c, d)
						scale_y = ParseAnimation.getScaleY(a, b, c, d)
						tx = string.atof(matrix_data.get("tx", "0"))
						ty = string.atof(matrix_data.get("ty", "0"))
					element_dict["position"] = {"x":tx, "y":ty}
					element_dict["scaleX"] = scale_x
					element_dict["scaleY"] = scale_y
					element_dict["rotationX"] = ParseAnimation.getSkewX(a, b, c, d)
					element_dict["rotationY"] = ParseAnimation.getSkewY(a, b, c, d)
					color_data = frame_data.find(ns + "color/" + ns + "Color")
					if color_data != None:
						element_dict["alpha"] = color_data.get("alphaMultiplier", "1")
					frame_arr.append(element_dict)
				frame_dict[frame_num] = frame_arr
				frame_dict["{0}_isKeyFrame".format(frame_num)] = is_key_frame
				if frame_time > 0:
					for i in xrange(frame_time):
						frame_index = string.atoi(frame_num) + i
						frame_dict["{0}".format(frame_index)] = frame_arr
						if frame_index > ParseAnimation._layer_num:
							ParseAnimation._layer_num = frame_index
				else:
					ParseAnimation._layer_num = string.atoi(frame_num)
			ParseAnimation.writeXml(layer_name, frame_dict, new_path)
	@staticmethod
	def writeXml(layer_name, frame_dict,file_path):
		total = "{0}".format(ParseAnimation._layer_num + 1)
		file_path = "{0}/{1}.xml".format(file_path, layer_name)
		fp = open(file_path, "w")
		doc = minidom.Document()
		comment = doc.createComment("动画帧信息表")
		doc.appendChild(comment)
		
		root = doc.createElement("animation")

		action = doc.createElement("action")
		action.setAttribute("actionName", layer_name)
		action.setAttribute("totalFrame", total)
		root.appendChild(action)

		for  i in xrange(ParseAnimation._layer_num + 1):
			frame_str = "{0}".format(i)
			is_key_frame = frame_dict.get("{0}_isKeyFrame".format(i))

			frame_info = doc.createElement("frameInfo")
			frame_info.setAttribute("frame", frame_str)
			if is_key_frame == "1":
				frame_info.setAttribute("isKeyFrame", is_key_frame)
			action.appendChild(frame_info)
			data_arr = frame_dict.get(frame_str, [])
			for dict_temp in data_arr:
				frame_data = doc.createElement("frameData")
				for key in dict_temp.keys():
					if key == "position":
						position = dict_temp[key]
						position_str = "{0},{1}".format(position["x"], position["y"])
						frame_data.setAttribute(key, position_str)
					else:
						value = dict_temp[key]
						frame_data.setAttribute(key, value)

				frame_info.appendChild(frame_data)
		doc.appendChild(root)
		doc.writexml(fp, "\t", "\t", "\n")
		fp.close()
		
	@staticmethod
	def getRotation(a, b, c, d):
		return "0"
	@staticmethod
	def getSkewX(a, b, c, d):
		degree = math.degrees(-math.atan(c / d))
		return "{0}".format(degree)

	@staticmethod
	def	getSkewY(a, b, c, d):
		degree = math.degrees(math.atan(b / a))
		return "{0}".format(degree)

	@staticmethod
	def getScaleX(a, b, c, d):
		sx = a / math.cos(math.radians(string.atof(ParseAnimation.getSkewY(a, b, c, d))))
		return "{0}".format(sx)

	@staticmethod
	def getScaleY(a, b, c, d):
		sy = d / math.cos(math.radians(string.atof(ParseAnimation.getSkewX(a, b, c, d))))
		return "{0}".format(sy)

	@staticmethod 
	def handle(path):
		print path
		if os.path.isdir(path):
			print r"{0}/DOMDocument.xml".format(path)
			if os.path.exists(r"{0}/DOMDocument.xml".format(path)):
				ParseAnimation._count += 1
				folders = path.split("/")
				animation_name = folders[len(folders) - 1]
				new_path = path.replace(src_path, to_path)
				if os.path.exists(new_path) == False:
					os.makedirs(new_path)
				ParseAnimation.texturePacker(path, new_path, animation_name)
				ParseAnimation.ParseXml(path, new_path)
			else:
				for sub_dir in os.listdir(path):
					ParseAnimation.handle(r"{0}/{1}".format(path, sub_dir))
				
print "===========开始转换..."
ParseAnimation.handle(src_path)
end_tip = "===========成功转换{0}个特效"
if sys.platform	== "win32":
        end_tip = end_tip.decode("utf-8").encode("gb2312")
print end_tip.format(ParseAnimation._count)
