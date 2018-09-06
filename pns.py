import pandas as pd

def open_file(name):
	path = 'PNS/' + name
	file = open(path, 'r')		
	return file

def open_txt(name):
	path = 'PNS/saidas/' + name 
	
	file = open(path, 'a')

	return file

def write_txt(content, file):
	file.write(content+'\n')

def main():
	txt = open_txt('teste.txt')

	file = open_file('PNS_012018.txt')

	for line in file.readlines():
		uf = line[0:2]
		capital = line[33]
		if (uf == '24'):		
			write_txt(line,txt)
			break
	

if __name__ == "__main__":
    main()