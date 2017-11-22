#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import re

dest_folder = "/Users/apple/Documents/workspace/git/sanguo_html/HSango/resource/db/"
config_datas = [
	{
		"paths":["/Users/apple/Documents/workspace/git/sanguo_html/HSango/resource/db/normal/"],
		"filename":"normal",
	}
]

def pack():
	for config_data in config_datas:
		pack_fp = open(dest_folder + config_data["filename"] + ".db.json", "w")
		pack_text = "{"
		for path in config_data["paths"]:
			for sub_dir in os.listdir(path):
				if sub_dir.endswith(".db.json"):
					single_fp = open(path + sub_dir, "r+")
					text = single_fp.read()
					single_fp.close()
					key = sub_dir[0:-5] + "_json" 
					pack_text += "\"" + key + "\"" + ":" + text + ",\n"
		pack_text = pack_text[0:-2] + "}"
		#pack_text = re.sub(r"\n", "", pack_text)
		pack_fp.write(pack_text)
		pack_fp.close()
	pass
pack()