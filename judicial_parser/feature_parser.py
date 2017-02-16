# Author : Jin Yong Shin
# Date : 2017.02.09

# Purpose : First phase of parsing text file that is converted from PDF
# Might contains some unnecessary spacings

import sys
import os
import re
import csv

class text_converter():

	def __init__(self, path_to_file):
		self.path_to_file =  path_to_file
		self.file_list = self.simple_read()

	def simple_read(self):
		file_lst = []
		file_object = open(self.path_to_file, 'rb')
		for pdf_file in file_object:
			pdf_file = pdf_file.split('\n')[0]
			file_lst.append(pdf_file + ".txt")
		return file_lst
			

	def parse_main(self):
		csv_file = open("phase1.csv", 'w')
		fieldnames = ['circuit_no', 'type', 'file_date', 'dates', 'company info']
		writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
		writer.writeheader()
		for file_path in self.file_list:
			file_object = open(file_path, 'rb')
			#parse date from txt
			judge_date = self.parse_date(file_object)
			#parse apelle
			file_object.seek(0)
			apelle_info = self.parse_apellee(file_object)
			#parse type of course appeals
			file_object.seek(0)
			court_type = self.parse_type(file_object)

			case_num = self.parse_case_no(file_path)

			#file date
			file_date = self.parse_filedate(file_path)

			writer.writerow({'circuit_no' : case_num, "type" : court_type, 'file_date' : file_date, "dates" : judge_date, "company info" : apelle_info})


	def parse_date(self, file_object):
		text = file_object.read()
		match = re.findall(r'Decided:\s{1,3}(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', text)
		if len(match) > 0:
			date = match[0].replace("Decided:", "").strip()
			return date
		else:
			match = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', text)
			date = match[-1].strip()
			return date
		# for line in file_object:
		# 	line_data = line.split('\n')[0].strip()
		# 	for element in match:
		# 		if element in line_data:

		return match			


	def parse_apellee(self, file_object):
		data_to_store = []
		for line in file_object:
			line_data = line.split('\n')[0].strip()
			if line_data == "______________________":
				data_to_store = []
			else:
				if line_data != '' and line_data != 'v.':
					data_to_store.append(line_data)
			if len(data_to_store) > 0:
				if re.match("Defendant", data_to_store[-1]):
					return data_to_store
				elif re.match("Appellee", data_to_store[-1]):
					return data_to_store
				elif re.match("Appellant", data_to_store[-1]):
					return data_to_store
					
	def parse_type(self, file_object):
		type_info = []
		for line in file_object:
			line_data = line.split('\n')[0].strip()
			if line_data == "______________________": 
				break;
			elif line_data != "":
				type_info.append(line_data)
		#detect court_info
		court_info = type_info[-1]
		court_info = court_info.split()
		#collect capital start
		return_val = ""
		for word in court_info:
			if re.match("^[A-Z]", word):
				return_val += word + " "
		return return_val

	def parse_case_no(self, file_name):
		match = re.findall(r'\d{2,4}-\d{4}', file_name)
		return match[0]

	def parse_filedate(self, file_name):
		match = re.findall(r'\d{1,2}-\d{2,4}-\d{4}', file_name)
		return match[0]


def main():
	convt = text_converter("Lists/list1.txt")
	# convt.parse_date()
	convt.parse_main()

if __name__ == "__main__":
	main()
