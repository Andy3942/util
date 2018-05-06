#!/usr/bin/env python
# coding=utf-8

import os
import sys

file_path = sys.argv[1]
file_path2 = sys.argv[2]


def findJs(path):
	if os.path.isdir(path):
		for sub_dir in os.listdir(path):
			findJs(path + "/"+ sub_dir)
	elif path.endswith(".js"):
		open(file_path2 + "/"+ os.path.basename(path), "wb").write(open(path, "rb").read())
		print(os.path.basename(path))
	pass

findJs(file_path)