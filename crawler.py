import requests as rq
# import json
import pandas as pd

def open_file():
	file = open('CSV/indicadores.csv', 'a')
	file.write('id;nome;posicao\n')
	return file

def close_file(file):
	file.close()	

def get_url(pesquisa, source):
	url = source
	url += str(pesquisa)
	url += '/indicadores/'
	return url

def get_pesquisas():
	df = pd.read_csv('CSV/pesquisas.csv', error_bad_lines=False, sep=';')
	df = df['id']	
	return df

def write_indicadores(id, posicao, indicador, file):
	file.write(id + ';' + posicao + ';' + indicador + '\n')

def crawl(source,file):
	cont = 0
	pesquisas = get_pesquisas()
	# pesquisas = 
	print(pesquisas)
	for pesquisa in pesquisas:
		if pesquisa is not 'id':
			print(pesquisa)
			response = rq.get(get_url(pesquisa, source))
			indicadores = response.json()
			# print(indicadores)
			cont += 1
			# print(cont)

		set_indicadores(indicadores, file)


def set_indicadores(indicadores, file):
	for indicador in indicadores:	
		# print(indicador['id'],indicador['posicao'],indicador['indicador'])
		write_indicadores(str(indicador['id']),str(indicador['posicao']),indicador['indicador'], file)		
		if indicador['children'] is not None:
			set_indicadores(indicador['children'], file)

def main():
	file = open_file()
	source = 'https://servicodados.ibge.gov.br/api/v1/pesquisas/'
	crawl(source,file)
	close_file(file)    

	# print(get_pesquisas())

if __name__ == "__main__":
    main()