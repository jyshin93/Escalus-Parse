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
		csv_file = open("phase2.csv", 'w')
		fieldnames = ['circuit_no', 'type', 'Date of Fed. Cir. Argument', 'Date of Fed. Cir. Decision', 'Previous Fed. Cir. Appeal(Y/N)', 'Previous Prevailing Party (if Y)',
					 'Supreme Court remand (Y/N)', 'Supreme Court Prevailing Party (if Y)', 'company info']
		writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
		writer.writeheader()
		for file_path in self.file_list:
			file_object = open(file_path, 'rb')
			
			decision_date = self.parse_date(file_object)			#parse date from txt
			
			file_object.seek(0)
			apelle_info = self.parse_apellee(file_object)			#parse apelle

			file_object.seek(0)
			court_type = self.parse_type(file_object)				#parse type of course appeals
			
			case_num = self.parse_case_no(file_path)				#federal court case number
			argument_date = self.parse_filedate(file_path) 			#argument date

			file_object.seek(0)
			previous_fed = self.parse_previous_fed(file_object)

			file_object.seek(0)
			supreme_remand = self.parse_supreme_remand(file_object)
			
			file_object.seek(0)
			judge_info = self.parse_judges(file_object)

			writer.writerow({'circuit_no' : case_num, "type" : court_type, 'Date of Fed. Cir. Argument' : argument_date, 
				"Date of Fed. Cir. Decision" : decision_date, 'Previous Fed. Cir. Appeal(Y/N)' : previous_fed, 'Previous Prevailing Party (if Y)' : "", 
				'Supreme Court remand (Y/N)' : supreme_remand, 'Supreme Court Prevailing Party (if Y)' : "", "company info" : apelle_info})

	#Because of parsing error, some of the PER CURIAM is coming before PER CURIAN
	def parse_judges(self, file_object):
		text = file_object.read()
		match = re.findall(r'.{1,20}\s{1,4}PER\s{1,3}CURIAM\s{1,2}\(.{1,100}\s{1,2}.{1,10}', text)
		if len(match) > 0:  	#if PER CURIAM exists, then 1st if statement
			match = match[0].replace('\n', "").replace('AFFIRMED.', "")
			info_list = match.strip().split(" ")
			index = info_list.index("PER")
			result = ' '.join(info_list[index:]) + ' ' + ' '.join(info_list[0:index])
			result = result.replace('PER CURIAM', "").strip()
			return result
		else:
			file_object.seek(0)
			data_to_store = []
			for line in file_object:
				line_data = line.split('\n')[0].strip()
				if line_data == "______________________":
					data_to_store = []
				elif 'PER CURIAM.' == line_data or 'Judge.' == line_data or 'Judges' == line_data:
					break;
				else:
					data_to_store.append(line_data)
			print(data_to_store)
			

	#assumption : previous federal circuit is based on the fact that if they had previous court decision.
	def parse_previous_fed(self, file_object):
		text = file_object.read()
		match = re.findall(r'Appeals\s{1,3}from\s{1,3}the\s{1,3}United\s{1,3}States\s{1,3}.{1,10}\s{1,3}Court', text)
		match2 = re.findall(r'Appeal\s{1,3}from\s{1,3}the\s{1,3}United\s{1,3}States\s{1,3}.{1,10}\s{1,3}Court', text)
		if len(match) > 0:
			return 'Y'
		elif len(match2) > 0:
			return 'Y'
		else:
			return 'N'

	#algorithm : 
	def parse_supreme_remand(self, file_object):
		text = file_object.read()
		match = re.findall(r'.{1,30}\s{1,3}Supreme\s{1,4}Court', text)
		for string in match:
			string = string.replace('\n', "")
			if 'remand' in string and 'Supreme Court' in string:
				return 'Y'
		return 'N'


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
		match = re.findall(r'\d{1,2}-\d{1,4}-\d{4}', file_name)
		return match[0]


def main():
	convt = text_converter("Lists/list1.txt")
	# convt.parse_date()
	convt.parse_main()

if __name__ == "__main__":
	main()
