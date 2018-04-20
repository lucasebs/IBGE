import requests as rq
# import json
import pandas as pd
from social import *

def open_file(i):
	if i:
		file = open('CSV/indicadores_filtro.csv', 'a')
	else:
		file = open('CSV/indicadores.csv', 'a')
		
	file.write('pesquisa_id;pesquisa_nome;id;posicao;nome\n')
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
	# df = df['id']	
	return df

def get_indicadores():
	df = pd.read_csv('CSV/indicadores.csv', error_bad_lines=False, sep=';')
	return df

def write_indicadores(pesquisa, pesquisa_nome, id, posicao, indicador, file):		
	file.write(pesquisa + ';' + pesquisa_nome + ';' + id + ';' + posicao + ';' + indicador + '\n')

def crawl(source,file):
	cont = 0
	pesquisas = get_pesquisas()
	# pesquisas = 
	print(pesquisas)
	for pesquisa in pesquisas['id']:
		if pesquisa is not 'id':
			print(pesquisa)
			response = rq.get(get_url(pesquisa, source))
			indicadores = response.json()
			# print(indicadores)
			cont += 1
			# print(cont)

		set_indicadores(pesquisa, pesquisas['nome'][cont], indicadores, file)

def set_indicadores(pesquisa, pesquisa_nome, indicadores, file):
	for indicador in indicadores:	
		# print(indicador['id'],indicador['posicao'],indicador['indicador'])
		write_indicadores(str(pesquisa), pesquisa_nome, str(indicador['id']),str(indicador['posicao']),indicador['indicador'], file)		
		if indicador['children'] is not None:
			set_indicadores(pesquisa, pesquisa_nome, indicador['children'], file)

def compare(file, list):
	indicadores = get_indicadores()
	for re in list:
		# if len(re) > 1:
		# 	for re_i in re:
		# else:
		# 
		if len(re[0]) > 1:
			compare(file,list)

		cont = 0
		n_existe = True
		for indicador in indicadores:
			if re in indicador['nome']:
				write_indicadores(str(indicadores['pesquisa_id'][cont]),
								indicadores['pesquisa_nome'][cont],
								str(indicadores['id'][cont]),
								str(indicadores['posicao'][cont]),
								indicador['nome'], file)
				ausente = False
				cont += 1

		if n_existe:
			write_indicadores(" "," "," "," "," ", file)
		

def main():
	# file = open_file(False)
	# source = 'https://servicodados.ibge.gov.br/api/v1/pesquisas/'
	# crawl(source,file)	

	file = open_file(True)
	compare(file, social)
	close_file(file)    

if __name__ == "__main__":
    main()