import pandas as pd


df = pd.read_csv('CSV/resultados/resultados_cor_raca.csv', error_bad_lines=False, sep=';')
file = open('CSV/resultados/moldado_resultados_cor_raca.csv', 'a')
file.write('municipio;amarela;branca;indigena;parda;preta;semdeclara\n')


cont = 0 
i = 0
result = ''
for municipio in df['municipio']:
	print(municipio)
	result += ";" + str(df['valor'][i])
	if cont == 5:
		result += '\n'
		cont = 0
		file.write(result)
		result = ''		
	else:
		cont += 1

	i += 1
