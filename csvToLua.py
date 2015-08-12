#!/usr/bin/env python3
# coding=utf-8

import codecs

lua_path = "/Users/bzx/Documents/sango/skill.lua"
db_path = "/Users/bzx/Documents/sango/skill.db"
file_path = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出CSV表/skill.csv"


fp = codecs.open(file_path, 'r', 'gbk')

fp.readline()
fp.readline()

lua_fp = open(lua_path, 'w')
db_fp = open(db_path, 'w')
lua_fp.write("module(\"skill\", package.seeall)\n")
lua_fp.write("local data = {\n")
while True:
	fp_position = fp.tell()
	text = fp.readline()
	db_fp.write(text)
	if text:
		data_id = text[:text.find(',')]
		lua_fp.write("    [%s] = %s,\n"%(data_id, fp_position))
		# print(data_id, fp_position)
		# print(text)
	else:
		break
fp.close()
lua_fp.write("}")
lua_fp.close()
db_fp.close()