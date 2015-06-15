#!/usr/bin/env python3

import os

root_path = "/Users/bzx/Documents/git/mygame/src/"
path_star_index = len(root_path)

dirs = [
	"/Users/bzx/Documents/git/mygame/src/my/"
]

to_file_path = "/Users/bzx/Documents/git/mygame/src/my/classload/ClassPath.lua"

fileter_dirs = [".svn"]
class ClassPath:
	_data = ""
	def findFilePath(self, path):
		if os.path.isdir(path):
			for sub_dir in os.listdir(path):
				if self.isFiltered(sub_dir):
					continue
				sub_path = os.path.join(path, sub_dir)
				self.findFilePath(sub_path)
		elif path.endswith(".lua"):
			self._data = self._data + "\n    %s = \"%s\","%(os.path.basename(path)[:-4], path[path_star_index:-4])
		pass

	def initData(self):
		self._data = "local ClassPath = {"
		for dir_temp in dirs:
			self.findFilePath(dir_temp)
			pass
		self._data = self._data + "\n}"
		self._data = self._data + "\nreturn ClassPath"
		pass

	def isFiltered(self, dir_name):
		for fileter_dir in fileter_dirs:
			if fileter_dir == dir_name:
				return True
		return False
		pass

	def save(self):
		with open(to_file_path, "w") as fp:
			fp.write(self._data)
			fp.close()
		pass
class_path = ClassPath()
class_path.initData()
class_path.save()