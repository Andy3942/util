#!/usr/bin/env python3
#encoding: UTF-8
#
import re
import os
import pprint
print("\n\n\n\n\n\n\n\n\n\n\n")
oldConfigPath = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/script/localized/LocalizedStrings_cn.lua"
scriptPath = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/script/"
function = "GetLocalizeStringBy"
filterDirs = [".svn", "localized", "db", "platform", "libs", "model", "utils", "consoleExe"]
#path = input("请输入要转换的路径：")
key_tag = "key_"
class Internationalization():
	_cur_id = ""
	_key_values = []
	_config_data = {}
	_new_config_data_map = {}
	_new_config_data = []
	_file_datas = []
	_old_config_data_map = {}
	_old_config_data = []
	def initTranslateData(self, filepath):
		with open(filepath) as fp:
			text = fp.read()
			fp.close()
		new_text = text
		#去掉注释和日志
		new_text = re.sub(r"--\[\[[\S\s]*?\]\]", "", new_text)
		new_text = re.sub(r"--[^\n]*", "", new_text)
		new_text = re.sub(r"print\(.*", "", new_text)
		new_text = re.sub(r"error\(.*", "", new_text)
		new_text = re.sub(r"Logger\.trace\(.*", "", new_text)

		pattern = re.compile(r"\"[^\"]*[\u4e00-\u9fa5][^\"]*\"")
		strs = pattern.findall(new_text)
		if len(strs) == 0:
			return
		print(filepath)
		no_repeat_strs = []
		for i in range(len(strs)):
			content = strs[i]
			if not content in no_repeat_strs:
				no_repeat_strs.append(content)
			key = self._config_data.get(content, None)
			if key is None:
				key = self._new_config_data_map.get(content, None)
			else:
				data = {"key":key, "content":content}
				self._old_config_data.append(data)
				self._old_config_data_map[content] = key
			if key is None:
				key = key_tag + str(self._cur_id)
				self._cur_id = self._cur_id + 1
				data = {"key":key, "content":content}
				self._new_config_data.append(data)
				self._new_config_data_map[content] = key
			print(key + " = " + content)
			file_data = {"path":filepath, "contents":no_repeat_strs}
		self._file_datas.append(file_data)
	def findFilePath(self, path):
		if os.path.isdir(path):
			for sub_dir in os.listdir(path):
				if self.isFiltered(sub_dir):
					continue
				sub_path = os.path.join(path, sub_dir)
				self.findFilePath(sub_path)
		elif path.endswith(".lua"):
			self.initTranslateData(path)
	def isFiltered(self, dir_name):
		for filterDir in filterDirs:
			if filterDir == dir_name:
				return True
		return False
	def printKeyValue(self):
		print("--------------------------旧数据----------------------------")
		for data in self._old_config_data:
			print("%s = %s,"%(data["key"], data["content"]))
		print("--------------------------新数据----------------------------")
		for data in self._new_config_data:
			print("%s = %s,"%(data["key"], data["content"]))
	def initConfigData(self):
		with open(oldConfigPath) as fp:
			configText = fp.read()
			fp.close()
		data = configText.split(",\n")
		for i in range(len(data)):
			if i == 0:
				continue
			if i == len(data) - 1:
				return
			text = data[i]
			space_position = text.find(" = ")
			key = text[0:space_position]
			content = text[space_position + 3:]
			self._config_data[content] = key
			if i == len(data) - 2:
				self._cur_id = int(key[key.find("_") + 1:]) + 1
		pass
	def translateAlert(self):
		translate = input("是否替换(y/n)：")
		if translate == "y":
			self.translate()
	def translate(self):
		for file_data in self._file_datas:
			filepath = file_data["path"]
			print(filepath, "=================")
			contents = file_data["contents"]
			with open(filepath) as fp:
				text = fp.read()
				fp.close()
			ret_text = text
			for content in contents:
				key = self._old_config_data_map.get(content, None)
				if key is None:
					key = self._new_config_data_map.get(content, None)
				replace_content = "%s(\"%s\")"%(function, key)
				ret_text = ret_text.replace(content, replace_content)
			with open(filepath, "w+") as fp2:
				fp2.write(ret_text)
				fp2.close()
		print("转换成功")
hehe = Internationalization()
hehe.initConfigData()
hehe.findFilePath(scriptPath)
hehe.printKeyValue()
hehe.translateAlert()
 #"\*.?+$^[](){}|/"