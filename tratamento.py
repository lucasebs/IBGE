import pandas as pd


df = pd.read_csv('CSV/resultados/resultados_.csv', error_bad_lines=False, sep=';')
file = open('CSV/resultados/tratados/resultados_tratados_.csv', 'a')
# file.write(';Masculin;Feminino\n')
file.write('Urbana;Rural;Urbana;Rural;Urbana;Rural;45 a 48 horas;49 horas ou mais;6 a 14 anos de idade;Saúde;Taxa de mortalidade infantil;Escola pública municipal;Escola pública estadual;Escola pública federal;Escola pública municipal;Escola pública estadual;Escola pública federal;Escola pública municipal;Escola pública estadual;Escola pública federal;Urbana;Rural;Urbana;Rural;Urbana;Rural;Já quitado;Em aquisição\n')

cont = 0 
i = 0
result = ''
valor = 0

for municipio in df['municipio']:
	print(municipio)
		
	result += ";" + str(df['resultado'][i])

	if cont == 27:
		result += '\n'
		file.write(result)
		result = ''		
		cont = 0	
	else:
		cont += 1

	i += 1
