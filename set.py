from municipios import *
from pesquisas import *

def set_pesquisas():
	file = open('CSV/pesquisas.csv', 'w')
		
	result = 'id;nome\n'
	for pesquisa in pesquisas:
		result += str(pesquisa['id']) +';'+ pesquisa['nome'] + '\n'

	file.write(result)
	
	file.close()

def set_municipios():
	file = open('CSV/municipios.csv', 'w')

	result = 'id;nome\n'
	for municipio in municipios:
		result += str(municipio['id']) +';'+ municipio['nome'] + '\n'

	file.write(result)
	
	file.close()


# set_pesquisas()

# set_municipios()


