#!/usr/bin/env python3
# coding=utf-8

import codecs

lua_path = "/Users/bzx/Documents/sango/skill2.lua"
db_path = "/Users/bzx/Documents/sango/skill2.db"
file_path = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出CSV表/skill.csv"


fp = codecs.open(file_path, 'r', 'gbk')

fp.readline()
key_line = fp.readline()

lua_fp = open(lua_path, 'w')
db_fp = open(db_path, 'w')
lua_fp.write("module(\"skill2\", package.seeall)\n")
lua_fp.write("local keys={")
keys = key_line.split(',')
filtered_column = {}
offset = fp.tell()
for i in range(0, len(keys) - 1):
	key = keys[i]
	if key == '':
		filtered_column[i] = True
	else:
		lua_fp.write("\"%s\","%(key))
	pass
lua_fp.write("}\n")

lua_fp.write("local id_datas = {\n")
fp_position = 0
while True:
	text = fp.readline()
	#while True:
	#	pass
	db_fp.write(text)
	if text:
		data_id = text[:text.find(',')]
		lua_fp.write("    [%s] = %s,\n"%(data_id, fp_position))
		fuck = text.encode("utf-8")
		fp_position = fp_position + len(fuck)
		# print(data_id, fp_position)
		# print(text)
	else:
		break
fp.close()
lua_fp.write("}\n")
lua_fp.write("local db_path = \"%s\"\n"%(db_path))
lua_fp.write("""local mt = {}
mt.__index = function (t,key)
	for i=1, #keys do
		if keys[i] == key then
			return t[i]
		end
	end
end
local fp = nil
local datas = {}
function getDataById(id)
	local data = datas[id]
	if data == nil then
		if fp == nil then
			fp = io.open(db_path)
		end
		local id_data = id_datas[id]
		fp:seek("set", id_data)
		local data_line = fp:read()
		datas[id] = data_line
		data = data_line 
		print(data)
	end
	-- setmetatable(data, mt)
	return data
end
function getDataByField(fieldName,fieldValue)
	local result = {}
	for key, val in  pairs( data ) do
		setmetatable(val, skill_mt)
		if val[fieldName] == fieldValue then
			result[#result+1] = val
        end
	end
	return result
end""")
lua_fp.close()
db_fp.close()