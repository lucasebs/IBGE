import requests as rq
# import json
import pandas as pd
from social import *

def open_file(dado, resultado):
	path = 'CSV/'
	if resultado:
		path += 'resultados/'
	path += dado
	path += '.csv'

	file = open(path, 'a')
		
	file.write('pesquisa_id;pesquisa_nome;id;posicao;nome\n')
	return file

def close_file(file):
	file.close()	

def get_url(pesquisa, source):
	url = source
	url += str(pesquisa)
	url += '/indicadores/'
	return url

def get_url_resultados(pesquisa, indicador, municipio, source):
	url = get_url(pesquisa, source)
	url += indicador
	url += '/resultados/'
	url += municipio
	return url

# def get_pesquisas():
# 	df = pd.read_csv('CSV/pesquisas.csv', error_bad_lines=False, sep=';')
# 	df = df['id']	
# 	return df

def get_df(dado):
	path = 'CSV/'
	path += dado
	path += '.csv'
	df = pd.read_csv(path, error_bad_lines=False, sep=';')
	return df

def write_indicadores(pesquisa, pesquisa_nome, id, posicao, indicador, file):		
	file.write(pesquisa + ';' + pesquisa_nome + ';' + id + ';' + posicao + ';' + indicador + '\n')

def set_indicadores(pesquisa, pesquisa_nome, indicadores, file):
	for indicador in indicadores:	
		# print(indicador['id'],indicador['posicao'],indicador['indicador'])
		write_indicadores(str(pesquisa), pesquisa_nome, str(indicador['id']),str(indicador['posicao']),indicador['indicador'], file)		
		if indicador['children'] is not None:
			set_indicadores(pesquisa, pesquisa_nome, indicador['children'], file)

def crawl(source,file):
	cont = 0
	pesquisas = get_df('pesquisas')
	# pesquisas = 
	print(pesquisas)
	for pesquisa in pesquisas['id']:
		if pesquisa is not 'id':
			print(pesquisa)
			response = rq.get(get_url(pesquisa, source))
			indicadores = response.json()
			# print(indicadores)
			# print(cont)
		set_indicadores(pesquisa, pesquisas['nome'][cont], indicadores, file)
		cont += 1

def compare(file, list):
	indicadores = get_df('indicadores')
	for re in list:
		# if len(re) > 1:
		# 	for re_i in re:
		# else:
		
		print(re)
		if len(re[0]) > 1:
			compare(file,re)

		cont = 0
		n_existe = True
		for indicador in indicadores['nome']:
			print(indicador)
			if re in indicador:
				write_indicadores(str(indicadores['pesquisa_id'][cont]),
								indicadores['pesquisa_nome'][cont],
								str(indicadores['id'][cont]),
								str(indicadores['posicao'][cont]),
								indicador, file)
				ausente = False
				cont += 1

		if n_existe:
			write_indicadores(" "," "," "," "," ", file)
		

def write_resultados(resultado, municipio, file):
	file.write(municipio + ';' + resultado + '\n')	

def set_resultados(resultados, municipio, file, cont):
	result = 0
	for resultado in resultados:
		if resultado["res"][0]["res"]["2010"] == '99999999999992':
			result += 0
		else:
			result += int(resultado["res"][0]["res"]["2010"])

		if cont == 9:
			write_resultados(str(result), str(municipio), file)			
			cont = 0
		


	

def crawl_resultados(source, file):
	df = get_df('indicadores_filtro')
	municipios = get_df('municipios')
	municipios = municipios['id']
	indicadores = df['posicao']
	pesquisas = df['pesquisa_id']
	print(df)


	for municipio in municipios:
		print(municipio)	
		# print(type(indicador))
		cont = 0			
		cont1 = 0
		# for pesquisa in df['pesquisa_id']:
		for indicador in indicadores:
			print(indicador)

			# indicador = df['posicao'][cont]
			pesquisa = pesquisas[cont]
			
			url = get_url_resultados(str(pesquisa), str(indicador), str(municipio), source)

			response = rq.get(url)
			resultados = response.json()

			set_resultados(resultados, municipio, file, cont1)
			cont += 1
			cont1 += 1
			if cont1 == 10:
				cont1 = 0
		

def main():
	source = 'https://servicodados.ibge.gov.br/api/v1/pesquisas/'

	# file = open_file('indicadores')
	# crawl(source,file)	

	# file = open_file('indicadores_filtro')
	# compare(file, social)
	
	file = open_file('resultados_', True)
	crawl_resultados(source,file)		
	
	close_file(file)    

if __name__ == "__main__":
    main()