#!/usr/bin/env python
# coding=utf-8

from xxtea import encrypt
from xxtea import decrypt
import os

find_path = "/Users/bzx/Documents/sango/FknSango/CardSango/Resources/db__/"
key = "1234567890123456"
class Encrypt():
	def findFilePath(self, path):
		if os.path.isdir(path):
			for sub_dir in os.listdir(path):
				sub_path = os.path.join(path, sub_dir)
				if sub_path.endswith(".lua"):
					self.encrypt(sub_path)
	def encrypt(self, path):
		fp = open(path, "rb+")
		text = fp.readline()
		encrypt_text = decrypt(text, key)
		print(encrypt_text)
		#fp.seek(0)
		#fp.write(encrypt_text)
		fp.close()
		pass
hehe = Encrypt()
hehe.findFilePath(find_path)