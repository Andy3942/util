#!/usr/bin/env python3
# coding=utf-8

import codecs
import re
import csv
import os

resources_folder = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/"
db_folder = "db/"
cfg_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出XML表/"
csv_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出CSV表/"
to_folder = resources_folder + db_folder


def findCsv(path):
	if os.path.isdir(path):
		for sub_dir in os.listdir(path):
			findCsv(path + sub_dir)
	elif path.endswith(".csv"):
		parse(os.path.splitext(os.path.basename(path))[0])
	pass
def parse(filename):
	lua_module_name = None
	data_module_name = None
	if filename == "skill":
		lua_module_name = filename
		data_module_name = "skill_data"
	else:
		lua_module_name = "DB_%s" % (filename.capitalize())
		data_module_name = "DB_%s_data" % (filename.capitalize())

	lua_path = "%s%s.lua"%(to_folder, lua_module_name)
	data_path = "%s%s.lua"%(to_folder, data_module_name)
	cfg_path = "%s%s.cfg"%(cfg_folder, filename)
	csv_path = "%s%s.csv"%(csv_folder, filename)
	if filename == "skill":
		lua_path = "%s%s.lua"%(to_folder, filename)
		db_path = "%s%s_data.lua"%(to_folder, filename)
	if not os.path.exists(cfg_path):
		print("没有找到对应的cfg文件：", cfg_path)
		return
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
	lua_fp = open(lua_path, 'w')
	lua_fp.write("module(\"%s\", package.seeall)\n"%(lua_module_name))
	lua_fp.write("data_path = \"%s%s.lua\"\n"%(db_folder, data_module_name))
	lua_fp.write("keys={")

	data_fp = open(data_path, 'w')
	data_fp.write("data = {\n")
	csv_reader = csv.reader(codecs.open(csv_path, 'rb', "gbk"))
	keys = {}
	key_max_num = None
	fp_position = 0
	data_count = 0
	for line_fields in csv_reader:
		if csv_reader.line_num == 1:
			continue
		elif csv_reader.line_num == 2:
			key_max_num = len(line_fields)
			for i in range(0, key_max_num):
				field = line_fields[i]
				if cfg_data.get(field) != None:
					keys[i] = field
			key_index = 0
			for i in range(0, key_max_num):
				key = keys.get(i)
				if key != None:
					key_index = key_index + 1
					lua_fp.write("[\"%s\"]=%s,\n"%(key, key_index))
				pass
			lua_fp.write("}\n")
			lua_fp.write("id_datas = {\n")
		else:
			if line_fields[0] != "":
				data_count = data_count + 1
				data_id = None
				fp_position = data_fp.tell()
				data_fp.write("{")
				for i in range(0, len(line_fields)):
					field = line_fields[i]
					field_type = cfg_data.get(keys.get(i))
					if field_type != None:
						if field == "":
							data_fp.write("nil")
						else:
							if field[len(field) - 1] == '\n':
								field = field[:len(field) - 1]
							if field_type == "number":
								data_fp.write(field)
								if data_id == None:
									data_id = field
							elif field_type == "string":
								data_fp.write("\"" + field + "\"")
						data_fp.write(",")
				data_fp.write("},\n")
				lua_fp.write("[%s]=%s,\n"%(data_id or "nil", fp_position))
	data_fp.write("}\n")
	data_fp.write("return data")
	lua_fp.write("}\n")
	lua_fp.write("data_count = %s\n"%(data_count))
	lua_fp.write("DBCommon.addDBFunction(%s)" % (lua_module_name))
	lua_fp.close()
	data_fp.close()
findCsv(csv_folder)