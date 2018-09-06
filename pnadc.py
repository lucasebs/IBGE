import pandas as pd

def open_file(name):
	path = 'PNADC/' + name
	file = open(path, 'r')		
	return file

def open_txt(name):
	path = 'PNADC/saidas/' + name 
	
	file = open(path, 'a')

	return file

def write_txt(content, file):
	file.write(content+'\n')

def main():
	txt = open_txt('teste.txt')

	file = open_file('PNADC_012018.txt')

	for line in file.readlines():
		uf = line[0:11]
		capital = line[33]
		if (uf == '20181242424' and capital == '1' ):		
			write_txt(line,txt)
			break
	

if __name__ == "__main__":
    main()