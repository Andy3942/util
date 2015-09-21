#!/usr/bin/env python3
# coding=utf-8

import os
import re
import math
import string
from xmltodict import parse
from xmltodict import unparse
import pprint


src_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出XML表/"
cfg_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出XML表/"
dest_folder = "/Users/bzx/Documents/sango/json/"

def findCsv(path):
	if os.path.isdir(path):
		for sub_dir in os.listdir(path):
			findCsv(path + sub_dir)
	elif path.endswith(".xml"):
		parseDB(os.path.splitext(os.path.basename(path))[0])
	pass
def parseDB(filename):				
	json_path = "%s%s.json"%(dest_folder, filename)
	cfg_path = "%s%s.cfg"%(cfg_folder, filename)
	xml_path = "%s%s.xml"%(src_folder, filename)
	if not os.path.exists(cfg_path):
		print(cfg_path)
		return
	print(xml_path)
	#cfg
	cfg_data = {}
	cfg_fp = open(cfg_path)
	cfg_lines = cfg_fp.readlines()
	for line in cfg_lines:
		pattern = re.compile(r"[a-zA-Z0-9_=]*")
		line = pattern.search(line).group(0)
		if line != "":
			line_data = line.split("=")
			cfg_data[line_data[0]] = line_data[1]
		pass
	#keys
	json_fp = open(json_path, 'w')
	json_fp.write("{\n\"keys\":[")
	#data
	xml_data = parseXml(xml_path)
	datas = xml_data["root"][filename]
	if isinstance(datas, dict):
		datas = [datas]
	for i in range(0, len(datas)):
		data = datas[i]
		if i == 0:
			for key in data.keys():
				json_fp.write("\"%s\","%(key))
				pass
			json_fp.seek(json_fp.tell() - 1, os.SEEK_SET) 
			json_fp.write("],\n")
			json_fp.write("\"datas\":{\n")
		json_fp.write("\"%s\":["%(data.get("id", i + 1)))
		for key in data:
			value = data[key]
			if value == "":
				value = "null"
			else:
				value_type = cfg_data.get(key, None)
				if value_type == None:
					continue
				if value_type == "string":
					value = "\"%s\""%(value)
			json_fp.write("%s,"%(value))
			pass
		json_fp.seek(json_fp.tell() - 1, os.SEEK_SET) 
		json_fp.write("],\n")
		# print(datas[i])
	json_fp.seek(json_fp.tell() - 2, os.SEEK_SET) 
	json_fp.write("\n}\n}")
	json_fp.close()
	
	#print(xml_data)
def parseXml(file_path):
	fp = open(file_path, 'r')
	data = parse(fp.read())
	fp.close()
	return data
findCsv(src_folder)
