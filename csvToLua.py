#!/usr/bin/env python3
# coding=utf-8

import codecs
import re
import csv
import os

to_folder = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/db/"
cfg_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出XML表/"
csv_folder = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出CSV表/"
	
def findCsv(path):
	if os.path.isdir(path):
		for sub_dir in os.listdir(path):
			findCsv(path + sub_dir)
	elif path.endswith(".csv"):
		parse(os.path.splitext(os.path.basename(path))[0])
	pass
def parse(filename):				
	lua_path = "%sDB_%s.lua"%(to_folder, filename.capitalize())
	db_path = "%sDB_%s_data.lua"%(to_folder, filename.capitalize())
	cfg_path = "%s%s.cfg"%(cfg_folder, filename)
	csv_path = "%s%s.csv"%(csv_folder, filename)
	if filename == "skill":
		lua_path = "%s%s.lua"%(to_folder, filename)
		db_path = "%s%s_data.lua"%(to_folder, filename)
	if not os.path.exists(cfg_path):
		print(cfg_path)
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
	if filename == "skill":
		lua_fp.write("module(\"%s\", package.seeall)\n"%(filename))
		lua_fp.write("local db_path = \"db/%s_data.lua\"\n"%(filename))
	else:
		lua_fp.write("module(\"DB_%s\", package.seeall)\n"%(filename.capitalize()))
		lua_fp.write("local db_path = \"db/DB_%s_data.lua\"\n"%(filename.capitalize()))
	lua_fp.write("local keys={")

	db_fp = open(db_path, 'w')
	db_fp.write("local data = {\n")
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
			lua_fp.write("local id_datas = {\n")
		else:
			if line_fields[0] != "":
				data_count = data_count + 1
				data_id = None
				fp_position = db_fp.tell()
				db_fp.write("{")
				for i in range(0, len(line_fields)):
					field = line_fields[i]
					field_type = cfg_data.get(keys.get(i))
					if field_type != None:
						if field == "":
							db_fp.write("nil")
						else:
							if field[len(field) - 1] == '\n':
								field = field[:len(field) - 1]
							if field_type == "number":
								db_fp.write(field)
								if data_id == None:
									data_id = field
							elif field_type == "string":
								db_fp.write("\"" + field + "\"")
						db_fp.write(",")
				db_fp.write("},\n")
				lua_fp.write("[%s]=%s,\n"%(data_id or "nil", fp_position))
	db_fp.write("}\n")
	db_fp.write("return data")
	lua_fp.write("}\n")
	lua_fp.write("local data_count = %s\n"%(data_count))
	lua_fp.write("""
local mt = {}
mt.__index = function (t,key)
	local index = keys[key]
	local value = rawget(t, index)
	rawset(t, key, value)
	return value
end
local fp = nil
local datas = {}
function getDataById(id)
	id = tonumber(id)
	local data = datas[id]
	if data == nil then
		if fp == nil then
			local path = CCFileUtils:sharedFileUtils():fullPathForFilename(db_path)
			fp = io.open(path)
		end
		local id_data = id_datas[id]
		if id_data == nil then
			return
		end
		fp:seek("set", id_data)
		local data_line = fp:read()
		local statement = string.format("return %s", string.sub(data_line, 1, -2))
		data = loadstring(statement)()
		datas[id] = data
	end
	setmetatable(data, mt)
	return data
end
function getArrDataByField(fieldName, fieldValue)
	local arrData = {}
	local fieldNo = keys[fieldName]
	local datas = getDatas()
	for k, v in pairs(datas) do
		if v[fieldNo] == fieldValue then
			setmetatable (v, mt)
			arrData[#arrData+1] = v
		end
	end
	return arrData
end
function getDatas()
	datas = require(db_path)
	return datas
end
function getDataCount()
	return data_count
end
""")
	lua_fp.close()
	db_fp.close()
findCsv(csv_folder)