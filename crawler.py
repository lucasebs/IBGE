import requests as rq
import json
import pandas as pd

def open_file(dado, resultado):
	path = 'CSV/'
	if resultado:
		path += 'resultados/'
	path += dado
	path += '.csv'

	file = open(path, 'a')
		
	# file.write('pesquisa_id;pesquisa_nome;id;posicao;nome\n')
	file.write('indicador;municipio;ano;resultado\n')
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

			url = get_url(pesquisa, source)

			print(url)
			response = rq.get(str(url))

			print(response.encoding)
			
			print(response.text)

			try:
			    indicadores = response.json()
			except Exception as err:
				print("Erro: {0}".format(err))
			finally:
			    print(pesquisa)
			    break

			# indicadores = response.json()

			# indicadores = json.loads(response.text)
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
		

def write_resultados(indicador, resultado, ano, municipio, file):
	file.write(indicador + ';' + municipio + ';' + ano  + ';' + resultado + '\n')	

def set_resultados(indicador, resultados, municipio, file, ano):
	if resultados == '':
		write_resultados(indicador, "0", "0", str(municipio), file)
	else:
		if ano == '':
			for resultado in resultados:
				keys = resultado["res"][0]["res"].keys()
				for key in keys:
					result = str(resultado["res"][0]["res"][key])
					write_resultados(indicador, result, str(key), str(municipio), file)
		else:
			for resultado in resultados:
				result = str(resultado["res"][0]["res"][ano])
				write_resultados(indicador, result, str(ano), str(municipio), file)
	# result = 0
	# for resultado in resultados:

	# 	if resultado["res"][0]["res"]["2010"] == '99999999999992':
	# 		result += 0
	# 	else:
	# 		result += int(resultado["res"][0]["res"]["2010"])

	# 	if cont == 9:
	# 		write_resultados(str(result), str(municipio), file)			
	# 		cont = 0
		


	

def crawl_resultados(source, file):
	df = get_df('indicadores_filtro')
	municipios = get_df('municipios')
	municipios = municipios['id']
	indicadores = df['posicao']
	pesquisas = df['pesquisa_id']
	print(df)

	cont_m = 1
	ano = '2010'
	for municipio in municipios:
		print(cont_m, municipio)	
		# print(type(indicador))
		cont = 0			
		# for pesquisa in df['pesquisa_id']:
		for indicador in indicadores:
			print(indicador)

			# indicador = df['posicao'][cont]
			pesquisa = pesquisas[cont]
			print(pesquisa)
			# print(municipio)
			# print(source)

			url = get_url_resultados(str(pesquisa), str(indicador), str(municipio), source)
			print(url)

			# response = rq.get(url)
			# print(response)
			# resultados = response.json()
			# print(resultados)
			resultados = rq.get(url).json()
			print(resultados)


			if len(resultados) == 0:
				set_resultados(str(indicador), '', municipio, file, ano)

			if cont == 10:
				ano = '2013'
			elif cont == 11:
				ano = '2015'
			elif cont == 20:
				ano = '2010'
				
			set_resultados(str(indicador), resultados, municipio, file, ano)
			cont += 1


		cont_m += 1
		

def main():
	source = 'https://servicodados.ibge.gov.br/api/v1/pesquisas/'


	file = open_file('indicadores', False)
	crawl(source,file)	

	# file = open_file('indicadores_filtro')
	# compare(file, social)
	
	# dado = 'srv_bsc_saude'

	# file = open_file('resultados_', True)
	# crawl_resultados(source,file)		
	
	close_file(file)    

if __name__ == "__main__":
    main()