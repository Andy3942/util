#!/usr/bin/env python3
# coding=utf-8

import os
import sys

src_folder = "/Users/apple/Documents/workspace/sg/FknSango/CardSango/Resources--/db/"
cfg_folder = src_folder
dest_folder = "/Users/apple/Documents/workspace/git/sanguo_html/HSango/resource/db/"

config_datas = {
	"cxmlLua":{
		"dest_path":"copy",
		"key":"copy"
	},
	"drugCXml":{
		"dest_path":"drug",
		"key":"DrugPosition"
	},
	"heroCXml":{
		"dest_path":"hero",
		"key":"HeroCXml"
	},
	"moonCXml":{
		"dest_path":"moon",
		"key":"MoonPosition"
	},
	"teamCXml":{
		"dest_path":"team",
		"key":"TeamCity",
	},
	"city1.lua":{
		"dest_path":"city/",
		"key":"GuildCity"
	},
	# "talk.lua":{
	# 	"dest_path":"talk/",
	# 	"key":"talk"
	# }
}

config_data = None

def findFilePath(path, dest_path):
	global config_data
	if os.path.isdir(path):
		for sub_dir in os.listdir(path):
			if dest_folder == dest_path:
				config_data = config_datas.get(sub_dir, None)
			if config_data != None:
				if sub_dir.endswith(".lua"):
					args = ("""\"{
							is_cxml = true,
							dir = '%s',
							file_name = '%s',
							dest_folder = '%s',
							key = '%s',
						}
						\"""")%(path, sub_dir, dest_folder + config_data["dest_path"] + "/", config_data["key"])
					#print(args)
					os.system("lua %s/luaToJson.lua %s"%(sys.path[0], args))
				else:
					#print(path + sub_dir + "/", dest_path + config_data["dest_path"])
					findFilePath(path + sub_dir + "/", dest_path + config_data["dest_path"] + "/")
			elif sub_dir.startswith("DB_") or sub_dir == "skill.lua":
				if sub_dir == "skill.lua":
					fp = open(src_folder + "skill.lua", "r+")
					text = fp.read()
					text = text.replace("local skill_keys=", "keys=")
					text = text.replace("local skill=", "Skill=")
					fp.close()
					fp = open(src_folder + "DB_Skill.lua", "w")
					fp.write(text)
					fp.close()
					sub_dir = "DB_Skill.lua"
				args = ("""\"{
					dir = '%s',
					file_name = '%s',
					dest_folder = '%s',
				}
				\"""")%(path, sub_dir, dest_folder + "normal/")
				os.system("lua %s/luaToJson.lua %s"%(sys.path[0], args))
				if sub_dir == "DB_Skill.lua":
					os.system("rm " + src_folder + "DB_Skill.lua")
			else:
				findFilePath(path + sub_dir + "/", dest_folder)
	pass

findFilePath(src_folder, dest_folder)