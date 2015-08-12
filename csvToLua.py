#!/usr/bin/env python3
# coding=utf-8

import codecs

to_path = "/Users/bzx/Documents/sango/DB_Arena_shop.lua"
file_path = "/Users/bzx/Documents/sango/卡牌三国项目/正式策划案/导出工具表/导出CSV表/skill.csv"


fp = codecs.open(file_path, 'r', 'gbk')

fp.readline()
fp.readline()

to_fp = open(to_path, 'w')
to_fp.write("module(\"DB_Arena_shop\", package.seeall)\n")
to_fp.write("local data = {\n")
while True:
	fp_position = fp.tell()
	text = fp.readline()
	if text:
		data_id = text[:text.find(',')]
		to_fp.write("    [%s] = %s,\n"%(data_id, fp_position))
		# print(data_id, fp_position)
		# print(text)
	else:
		break
fp.close()
to_fp.write("}")
to_fp.close()