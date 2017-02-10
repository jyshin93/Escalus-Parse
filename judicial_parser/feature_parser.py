# Author : Jin Yong Shin
# Date : 2017.02.09

# Purpose : First phase of parsing text file that is converted from PDF
# Might contains some unnecessary spacings

import sys
import os
import re

class text_converter():

	def __init__(self, path_to_file):
		self.path_to_file =  path_to_file

	def simple_read(self):
		data_to_store = []
		file_object = open(self.path_to_file, 'rb')
		for line in file_object:
			print(line)

	def parse_apellee(self):
		data_to_store = []
		file_object = open(self.path_to_file, 'rb')
		for line in file_object:
			lst = line.split('\n')
			line_data = lst[0].strip()
			if line_data == "______________________":
				data_to_store = []
			else:
				if line_data != '' and line_data != 'v.':
					data_to_store.append(line_data)

			if "Defendants-Appellants" in data_to_store:
				print data_to_store

	def parse_date(self):
		file_object = open(self.path_to_file, 'rb')
		text = file_object.read()
		match = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', text)
		print(match)

def main():
	convt = text_converter("sample.txt")
	convt.parse_apellee()
	convt.parse_date()

if __name__ == "__main__":
	main()
