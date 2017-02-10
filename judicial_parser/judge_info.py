import csv

class Judge_info_reader():

	def __init__(self, file_loc):
		self.file = file_loc
		self.header = []
		self.emp_index = 0
		self.chief_index = 0
		self.chief_YN = 0
		self.write_file = 'sample.csv'

	def judge_info(self):
		emp_index = 0
		#find index of employment history and chief judge date
		with open(self.file) as rfile2:
			cf = csv.reader(rfile2)
			for row in cf:
				self.emp_index = row.index('Employment text field')
				self.chief_index = row.index('Date of Service as Chief Judge (begin)')
				break;
		#read csv and find header
		with open(self.file) as f:
			has_header = csv.Sniffer().has_header(f.read(1024))
			f.seek(0)
			incsv = csv.reader(f)
			#skip first line of csv if header exits
			if has_header:
				for line in incsv:
					self.header = line
					break;
				next(incsv)
			#organize order of header
			emp = self.header.pop()
			self.header.append('Chief Judge(Y/N)')
			self.header.append(emp)
			self.chief_YN = self.emp_index
			self.emp_index += 1			
			#csv writer imported
			ofile = open(self.write_file, 'wb')
			writer = csv.writer(ofile, delimiter = ',')
			writer.writerow(self.header)
			#read csv 'file_loc'
			for line in incsv:	
				emp_hist = line[self.emp_index - 1:]
				line = line[:self.emp_index - 1]
				#check chief or not
				if line[self.chief_index] != '':
					line.append('1')
				else:
					line.append('0')
				#Eliminate <BR> tags
				string = ' '.join(emp_hist)
				string = string.split('<BR>')
				for hist in string:
					if ';' in hist:
						hist = hist.split(';')
						for h in hist:
							line.append(h)
					else:
						line.append(hist)
				writer.writerow(line)		


def main():
	reader = Judge_info_reader('jb.csv')
	reader.judge_info()


if __name__ == '__main__':
	main()