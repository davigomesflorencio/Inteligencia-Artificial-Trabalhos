import ia
import random
from random import randint
import time


# GERADOR DE ESTADOS ALEATORIOS
def gerar_estado_aleatorio(qt_enfer, turnos):
	novo = ""
	for x in range(qt_enfer*turnos):
		novo += str(randint(0, 1))
	return novo

#GERADOR DE UM ESTADO OBJETIVO


def exemplo_objetivo():
	st1 = "000100100000100100100"
	st2 = "000000010010010010010"
	st3 = "001001000000001001001"
	st4 = "100000000100100100100"
	st5 = "000000001001001001001"
	st6 = "100100100000100100000"
	st7 = "010010000010010010000"
	st8 = "001001000001000001001"
	st9 = "100100100100000000100"
	st10 = "010010010010000000010"
	return st1+st2+st3+st4+st5+st6+st7+st8+st9+st10

# GERADOR DE ESTADO COM 50 BITS 1


def gerar_estado_50bits(qt_enfer, turnos):
	"""
	Função que gera um estado que contem 50 bits 1
	@param qt_enfer : Quantidade de enfermeiros
	@param qt_turnos : Quantidade de turnos
	@return :Estado de um nó.
	"""
	novo = ""
	for x in range(50):
		novo += "1"
	for x in range(qt_enfer*turnos-50):
		novo += "0"
	return "".join(random.sample(novo, len(novo)))

# OPERADORES


def gera(estado):
    """
	Função que gera as configurações de estados a partir de um estado de um nó
	@param estado: estado de um nó
	@return : Lista da configurações de um estado do nó mudando apenas um bit por vez no estado
	"""
    filhos = []
    for x in range(len(estado)):
        aux = estado
        insere = ""
        if aux[x] == "1":
            insere += estado[0:x]+"0"+estado[x+1:len(estado)]
        else:
           insere += estado[0:x]+"1"+estado[x+1:len(estado)]
        filhos.append(insere)
    return filhos

# RESTRIÇÔES


def r1(estado, qt_enfer, qt_turnos):
	"""
	r1 : Deve haver ao menos 1 enfermeiro e no máximo 3 enfermeiros em cada turno.
	"""
	count = 0
	desempate = 0
	turnosvalidos = 0
	# x turnos range(x)
	for y in range(qt_turnos):
		count = 0
		for x in range(qt_enfer):
			# print(qt_turnos*x+y,end=" ")
			if(estado[qt_turnos*x+y] == "1"):
				count += 1
		# print("count",count)
		if(count >= 1 and count <= 3):
			turnosvalidos += 1
		desempate += count
	# print("turnos validos r1 ",turnosvalidos)
	if(turnosvalidos == qt_turnos):
		# print("valido r1")
		return (0, 0)
	else:
		# print("valido r1 nao")
		return (1, qt_turnos-turnosvalidos)


def r2(estado, qt_enfer, qt_turnos):
	"""
	r2 : Cada enfermeiro deve ser alocado em 5 turnos por semana.
	"""
	count = 0
	desempate = 0
	enfer_validos = 0
	# x funcio range(x)
	for y in range(qt_turnos, (qt_enfer+1)*qt_turnos, qt_turnos):
		count = 0
		count = estado[y-qt_turnos:y].count("1")
		# for x in range(qt_turnos):
		# 	#print("visit ",(y*21+x),"estado",estado[y*21+x])
		# 	if(estado[y*qt_turnos+x]=="1"):
		# 		count+=1
		if(count == 5):
			enfer_validos += 1
		desempate += count
	if(enfer_validos == qt_enfer):
		# print("valido r2")
		return (0, 0)
	else:
		# print("valido r2 nao")
		return (1, qt_enfer-enfer_validos)


def r3(estado, qt_enfer, qt_turnos):
	"""
	r3 : Nenhum enfermeiro pode trabalhar mais que 3 turnos seguidos sem folga.
	"""
	count = 0
	enfer_validos = 0
	# x funci range(x)
	for y in range(qt_enfer):
		count = 0
		for x in range(qt_turnos):
			#print("visit ",(y*21+x),"estado",estado[y*21+x])
			if((y*qt_turnos+x+4) % qt_turnos < qt_turnos and y*qt_turnos+x+4 < len(estado) and estado[y*qt_turnos+x:y*qt_turnos+x+4] == "1111"):
				count += 1
		if(count == 0):
			enfer_validos += 1
	if(enfer_validos == qt_enfer):
		# print("valido r3")
		return (0, 0)
	else:
		# print("valido r3 nao")
		return (1, qt_enfer-enfer_validos)


def r4(estado, qt_enfer, qt_turnos):
	"""
	r4 : Enfermeiros preferem consistência em seus horários, ou seja, eles preferem
	trabalhar todos os dias da semana no mesmo turno (dia, noite, ou madrugada)
	"""
	count = 0
	enfer_turno_validos = [[] for x in range(qt_enfer)]
	# x funci range(x)
	for y in range(qt_enfer):
		count = 0
		for x in range(0, qt_turnos, 3):
			# print("valor ",(y*21+x),"valor2 ",(y*21+x+3))
			if(enfer_turno_validos[y] == []):
				if(estado[y*qt_turnos+x:y*qt_turnos+x+3] == "100"):
					enfer_turno_validos[y] += ["100"]
				elif(estado[y*qt_turnos+x:y*qt_turnos+x+3] == "010"):
					enfer_turno_validos[y] += ["010"]
				elif(estado[y*qt_turnos+x:y*qt_turnos+x+3] == "001"):
					enfer_turno_validos[y] += ["001"]
			else:
				if(not(estado[y*qt_turnos+x:y*qt_turnos+x+3] == "000")):
					if(enfer_turno_validos[y] == ["100"] and estado[y*qt_turnos+x:y*qt_turnos+x+3] != "100"):
						enfer_turno_validos[y] += [estado[y*qt_turnos+x:y*qt_turnos+x+3]]
					elif(enfer_turno_validos[y] == ["010"] and estado[y*qt_turnos+x:y*qt_turnos+x+3] != "010"):
						enfer_turno_validos[y] += [estado[y*qt_turnos+x:y*qt_turnos+x+3]]
					elif(enfer_turno_validos[y] == ["001"] and estado[y*qt_turnos+x:y*qt_turnos+x+3] != "001"):
						enfer_turno_validos[y] += [estado[y*qt_turnos+x:y*qt_turnos+x+3]]
	for x in enfer_turno_validos:
		if len(x) == 1:
			count += 1
	# print("tu",turnosquant)
	if(count == qt_enfer):
		# print("valido r4")
		return (0, 0)
	else:
		# print("valido r4 nao")
		return (1, qt_enfer-count)

# FUNÇÃO QUE AVALIA UM ESTADO


def avaliar_estado(estado, qt_enfer, qt_turnos):
	"""
	Função que avalia o melhor nó dentre os outros pela sua avaliação de estado
	@param estado :Estado de um nó
	@param qt_enfer : Quantidade de enfermeiros
	@param qt_turnos : Quantidade de turnos 
	"""
	(c1, d1) = r1(estado, qt_enfer, qt_turnos)
	(c2, d2) = r2(estado, qt_enfer, qt_turnos)
	(c3, d3) = r3(estado, qt_enfer, qt_turnos)
	(c4, d4) = r4(estado, qt_enfer, qt_turnos)
	return ((c1+c2+c3+c4), (d1+d2+d3+d4))

# FUNÇÃO QUE AVALIA O MELHOR ESTADODE UM NÓ A PARTIR DO PARAMETRO RECEBIDO


def melhor_avaliado(nos):
	"""	
	Função que avalia o melhor nó dentre os outros pela sua avaliação de estado
	@param nos : Lista de nós 
	"""
	if(nos == []):
		return []
	melhor_no = nos[0]
	for no in nos:
		if(ia.compare(no, melhor_no) == True):
			melhor_no = no
	return [melhor_no]

# METODO PRINCIPAL


def main():
	num_func = 10
	num_turnos = 21
	metodo = -1
	gerador = -1
	while not (1 <= metodo <= 2):
		print("-------------------------------------------------")
		print("Digite qual o metodo de busca: ")
		print("	1. (Tempera simulada or Simulated Annealing)")
		print("	2. (Algoritmo Genetico)")
		metodo = int(input())
		if not(metodo == 1 or metodo == 2):
			print("Digite um numero valido ou 1 ou 2\n")

	# lista de operadores do problema
	operadores = [gera]

	# Verificando o metodo pra realizar as buscas
	if metodo == 1:
		# Instancia do problema
		teste = ""
		while not (1 <= gerador <= 3):
			print("Digite que tipo de estado a busca deve começar: ")
			print("	1. (Exemplo de estado objetivo")
			print("	2. (Estado aleatório com 50 bits 1)")
			print("	3. (Estado aleatório)")
			gerador = int(input())
			if (gerador == 1):
				teste = exemplo_objetivo()
			if (gerador == 2):
				teste = gerar_estado_50bits(num_func, num_turnos)
			if (gerador == 3):
				teste = gerar_estado_aleatorio(num_func, num_turnos)
			if not(gerador == 1 or gerador == 2 or gerador == 3):
				print("Digite um numero valido ou 1, 2 ou 3\n")

		print("Digite o valor da temperatura inicial: ")
		temperatura = int(input())

		problema = ia.ProblemaBuscaSimulatedAnnealing(
			teste, operadores, num_func, num_turnos, melhor_avaliado, avaliar_estado, temperatura)

		ini = time.time()
		resultado = ia.busca(problema)
		fim = time.time()
		print("Tempera simulada Finalizada")
		print("\nEstado Inicial:")
		ia.imprime_estado(problema, teste)
		print("\nSaida Busca Tempera simulada: ")
		ia.imprime_estado(problema, resultado)
		print("\nTempo: ", fim - ini)
		print("Numero de comparações: ", problema.comparacoes)
	if(metodo == 2):
		problema = ia.ProblemaBusca(
			"", operadores, num_func, num_turnos, melhor_avaliado, avaliar_estado)

		print("Digite o tamanho da populacao:")
		populacao = int(input())
		print("Digite o numero de gerações:")
		num_geracoes = int(input())
		print("Digite a taxa de mutacao: Exemplo : 0.1, ou 0.2 ")
		mutacao = float(input())
		print("Digite a taxa de elistimo: Exemplo : 0.1, ou 0.2 ")
		elitismo = float(input())	
		instanceAlgGenetico = ia.InstanceAlgoritmoGenetico(populacao,num_geracoes,mutacao,elitismo)

		ini = time.time()
		resultado = ia.algoritmoGenetico(instanceAlgGenetico, problema)
		fim = time.time()

		print("Algotitmo Genetico Finalizado")
		print("Melhor individuo encontrado: ")
		print(resultado)
		ia.imprimeCromossomo(problema,resultado.estado)
		print("\nTempo: ", fim - ini)
	return 0


# EXECUÇÃO DO METODO MAIN
print("O programa executou com saida %d" % (main()))
