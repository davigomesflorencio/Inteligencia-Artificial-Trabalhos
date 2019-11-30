
import random
from random import randint
from math import floor
import math


class Problema:
	# REPRESENTAÇÃO DO PROBLEMA
	def __init__(self, estado_inicial, operadores, qt_enfer, qt_turnos):
		"""
		Construtor de uma classe problema. O construtor recebe como parametros todos
		os componentes de um problema para construir um.
		@param estado_inicial: estado inicial que se encontra o problema
		@param operadores: operadores que executam sobre o problema
		@param teste_meta: Funcao que testa para ver se alcancamos o estado desejado
		@param qt_enfer : Quantidade de enfermeiros
		@param qt_turnos : Quantidade de turnos
		"""
		self.estado_inicial = estado_inicial
		self.operadores = operadores
		self.comparacoes = 0
		self.qt_enfer = qt_enfer
		self.qt_turnos = qt_turnos

	def __str__(self):
	 	return "Problema : Estado Inicial {0}, Numero de funcionarios {1} , Numero de turnos {2}".format(self.estado_inicial, self.num_funcionarios, self.qt_turnos)


class ProblemaBusca(Problema):
	"""
	Representação do problema para as buscas
	@param melhor_avaliado : Função que avalia o melhor estado entre os estado que recebe   
	@param avaliar_estado : Função que avalia o estado  
	"""

	def __init__(self, estado_inicial, operadores, qt_enfer, qt_turnos, melhor_avaliado, avaliar_estado):
	   super().__init__(estado_inicial, operadores, qt_enfer, qt_turnos)
	   self.melhor_avaliado = melhor_avaliado
	   self.avaliar_estado = avaliar_estado


class ProblemaBuscaSimulatedAnnealing(ProblemaBusca):
	"""
	Representação do problema da busca de Simulated Annealing 
	@param melhor_avaliado : Função que avalia o melhor estado entre os estado que recebe   
	@param avaliar_estado : Função que avalia o estado 
	@param temperatura : Temperatura inicial da busca 
	"""

	def __init__(self, estado_inicial, operadores, qt_enfer, qt_turnos, melhor_avaliado, avaliar_estado, temperatura=350):
		super().__init__(estado_inicial, operadores, qt_enfer,
                   qt_turnos, melhor_avaliado, avaliar_estado)
		self.temperatura = temperatura


class No:
	# REPRESENTACAO DE NÓ
	# para realizar o algoritmo de busca em lista, devemos ter o tipo no. O tipo abstrato
	def __init__(self, estado, no_pai, operador, profundidade, restricoes, desempate):
		"""
		Construtor de um no para busca em lista.
		@param estado : estado associado ao no corrente
		@param no_pai : no que deu origem ao no atual. "None" caso ele seja raiz
		@param operador : operador associado ao no
		@param profundidade : profundidade que no se encontra
		@param restrições : Numero de restrições violadas
		@param desempate : Segundo criterio de desempate que é baseado na soma de turnos violados
		"""
		self.estado = estado
		self.no_pai = no_pai
		self.operador = operador
		self.profundidade = profundidade
		self.restricoes = restricoes
		self.desempate = desempate

	def __str__(self):
		return "[NO: profundidade {0}, Num. de restrições violadas {1}, 1º criterio de desempate (Soma de turnos violados) {2}]".format(self.profundidade, self.restricoes, self.desempate)


class InstanceAlgoritmoGenetico:
	# Representacao geral dos parametros do algoritmo genetico

	def __init__(self, tam_populacao=40, quant_geracoes=120, mutacao=0.05, elitismo=0.25):
		"""
		Construtor de um InstanceAlgoritmoGenetico para o algoritmo genetico
		@param tam_populacao : Tamanho da população 
		@param quant_geracoes : Quantidade de gerações
		@param mutacao : Probabilidade de mutação
		@param elitismo : Taxa de elitismo
		"""
		self.tam_populacao = tam_populacao
		self.quant_geracoes = quant_geracoes
		self.mutacao = mutacao
		self.elitismo = elitismo


"""

	Representação de um individuo para o algoritmo genetico

"""


class Individuo:

	def __init__(self, estado, restricoes, desempate):
		"""
		Construtor de um no para busca em lista.
		@param estado: estado associado ao indivuduo
		@param restricoes: numero de restricoes violadas pelo estado
		@param desempate: criterio de desempate do individuo
		"""
		self.estado = estado
		self.restricoes = restricoes
		self.desempate = desempate
		self.fitness = 1

	def __str__(self):
		return "[Individuo: Num. de restrições violadas {0}, 1º criterio de desempate (Soma de turnos violados) {1}, Fitness {2}]".format(self.restricoes, self.desempate, self.fitness)


def imprime_estado(problema, estado):
	# FUNÇÃO QUE IMPRIME O ESTADO DO NÓ
	if estado == None:
		print("Estado sem representação")
	else:
		print("")
		for x in range(problema.qt_turnos, len(estado)+problema.qt_turnos, problema.qt_turnos):
			print("\t"+estado[x-problema.qt_turnos:x])
		print("")


def teste_meta(no):
	# FUNCAO QUE TESTA SE UM ESTADO É META
	if(no.restricoes == 0):
		return True
	else:
		return False


"""

	GERADOR DE ESTADOS

"""


def expande(no, problema):
	"""
	Funcao que expande um no e gera um conjunto de filhos
	@param no: no atual a ser expandido
	@param problema: problema no qual o no se encontra, no qual apenas se utiliza os operadores do problemas
	@return : TUPLA( Melhor filho gerado, Filhos gerados pela operação do problema)
	"""
	filhos = []  # conjunto de filhos gerados por um determinado no
	for operacao in problema.operadores:
		resultado = operacao(no.estado)
		# se o no produz algum filho, entao coloque ele no conjunto de filhos
		if not resultado is None:
			# criando um novo no a partir da expansao do no atual
			for x in resultado:
				(custo, desempate) = problema.avaliar_estado(
					x, problema.qt_enfer, problema.qt_turnos)
				o = No(x, no, operacao, no.profundidade+1, custo, desempate)
				if(compare(o, no) == True):
					filhos.append(o)
	# retornando o conjunto resultante da expansao
	best = problema.melhor_avaliado(filhos)
	return best, filhos


def insert_no(no, lista):
	# FUNÇÃO QUE INSERE UM NO NA LISTA DE NÓS BASEADO NO FUNCAO COMPARE
	aux = lista.copy()
	if(aux == []):
		aux.append(no)
	else:
		for ind, valor in zip(range(len(aux)), aux):
			if compare(no, valor) == True:
				aux = aux[0:ind]+[no]+aux[ind:len(aux)]
				break
	return aux


def compare(no1, no2):
	# FUNCAO QUE COMPARA DOIS NÓ PARA SIMULATED ANNEALING OU DOIS INDIVIDUOS PARA ALGORITMOS GENETICOS
	if((no1.restricoes < no2.restricoes) or (no1.restricoes == no2.restricoes and no1.desempate < no2.desempate) or (no1.restricoes == no2.restricoes and no1.desempate < no2.desempate and no1.estado < no2.estado)):
		return True
	return False


"""
	
	TEMPERA SIMULADA

"""


def busca(problema):
	"""
	@param problema :Representação do problema
	@return : Melhor nó encontrado pelo criterio de parada ou o nó objetivo
	"""
	c = 0
	nos = []
	visitados = []
	qt_enfer = problema.qt_enfer
	qt_turnos = problema.qt_turnos
	custo, desempate = problema.avaliar_estado(
		problema.estado_inicial, qt_enfer, qt_turnos)

	nos.append(No(problema.estado_inicial, None, None, 0, custo, desempate))
	no_corrente = nos[0]
	while True:
		if nos == [] or (isinstance(problema, ProblemaBuscaSimulatedAnnealing) and problema.temperatura == 0):
			print("------------------------BUSCA FINALIZADA-----------------------------\n")
			print("Estado objetivo não encontrado: Fila Vazia")
			print("Melhor nó encontrado na busca: ", no_corrente)
			return no_corrente.estado
		no = nos[0]
		print("-------------------------INICIO DE UM ETAPA----------------------------")
		print("Nó atual da busca:", no)
		imprime_estado(problema, no.estado)
		print("Temperatura - ", problema.temperatura)
		# Incrementando as comparações de estados até chegar no estado meta ou não
		c = c + 1
		problema.comparacoes = c
		# Testa se o nó atual é o meta
		if teste_meta(no):
			print("-----------------------------------------------------")
			print("\\\\\\\  Nó objetivo encontrado  ////////")
			return no.estado
		del(nos[0])
		# caso o nó nao seja a meta,ele é expandido e removido da estrutura utilizada
		if not no.estado in visitados:
			best, gerados = expande(no, problema)

			if (best != []):
				ind = randint(0, len(gerados)-1)
				print("No gerado para comparação:", gerados[ind])
				imprime_estado(problema, gerados[ind].estado)

				delta = no.desempate - gerados[ind].desempate
				exp = math.exp((-delta)/problema.temperatura)

				print("Delta ou Variação de energia : ", delta)
				print("Exp ou a probabilidade de mudar para o estado corrente : ", exp)

				if(delta > 0 or random.uniform(0, 1) < exp):
					# Insere o aleatorio na fila baseado na probabilidade
					nos = insert_no(gerados[ind], nos.copy())
					no_corrente = gerados[ind]
					problema.temperatura = problema.temperatura-1
					print("Nó gerado foi escolhido para a proxima iteração\n")
				else:
					print("Nó gerado NÃO foi seleciondo para a proxima iteração\n")
			visitados.append(no.estado)

		print("------------------------FIM DE UM ETAPA-----------------------------\n")


"""

	ALGORITMO GENETICO

"""


def algoritmoGenetico(algGenetico, problema):
	"""
	@param algGenetico : Representação do algoritmo genetico
	@param problema : Representação do problema 
	@return : Melhor individuo da população
	"""
	num_geracoes = 0
	# Gerando a populacao inicial
	populacao = generatePopulacao(algGenetico.tam_populacao, problema)
	# 1º criterio de parada numero de gerações maximas do algGenetico
	while num_geracoes <= algGenetico.quant_geracoes:
		print("------------------------------------------------------------------------------------------------------------------------\n")
		print("GERAÇÃO : ", num_geracoes, "\n")

		# Laco que calcula o fitness de cada individuo da população
		for iteracao in range(len(populacao)):

			populacao[iteracao] = calculaFitness(problema, populacao[iteracao])

			# Imprima a informaçaõ de cada individuo da populacao
			print("INDICE -> ", iteracao, " , ", populacao[iteracao])
			imprimeCromossomo(problema, populacao[iteracao].estado)

			# 2º Criterio de parada fitness de um individuo é o fitness objetivo
			if(populacao[iteracao].fitness == getFitnessObjetivo()):
				print("Individuo com fitness objetivo encontrado")
				return populacao[iteracao]

		print("\n------------------------------------------------------------------------------------------------------------------------")
		# Seleciona os mais aptos baseado na taxa de elitismo
		nova_populacao = selecao(algGenetico.elitismo, populacao)
		# Realiza a reprodução da população por meio dos indivuduos selecionado
		nova_populacao = reproducao(algGenetico, problema, nova_populacao.copy())
		# População recebe a nova população
		populacao = nova_populacao
		# Incrementa o numero de gerações
		num_geracoes = num_geracoes+1

	# Retorna a o melhor individuo se o 1º criterio de parada finalizar
	print("Individuo com fitness objetivo não encontrado\n")

	return populacao[0]


"""

	REPRODUCÃO

"""


def reproducao(algGenetico, problema, populacao):
	"""
	FUNCAO QUE REALIZA A REPRODUCAO DA POPULAÇÃO
	@param algGenetico : Representação do algoritmo genetico
	@param problema : Representação do problema
	@param populacao: lista de individuos 
	@return : Nova populacao
	"""
	nova_populacao = populacao.copy()
	while(len(nova_populacao) < algGenetico.tam_populacao):
		i1, i2 = crossover(problema, populacao)
		if(random.uniform(0, 1) < algGenetico.mutacao):
			i1 = mutacao(i1)
		if(random.uniform(0, 1) < algGenetico.mutacao):
			i2 = mutacao(i2)
		nova_populacao.append(i1)
		nova_populacao.append(i2)
	return nova_populacao.copy()


def gerar_cromossomo_aleatorio(qt_enfer, turnos):
	"""
	FUNÇÃO QUE GERA UM CROMOSSOMO ALEATORIO
	@param qt_enfer : Quantidade de enfermeiros
	@param qt_turnos : Quantidade de turnos
	"""
	novo = ""
	for x in range(qt_enfer*turnos):
		novo += str(randint(0, 1))
	return novo


def generatePopulacao(tam, problema):
	"""
	FUNÇÃO QUE GERA A POPULAÇÃO INICIAL DO PROBLEMA
	@param tam : tamanho da população
	@param problema : Representação do problema
	@return : lista de individuos
	"""
	lista = []
	for n in range(0, tam):
		estado = gerar_cromossomo_aleatorio(problema.qt_enfer, problema.qt_turnos)
		o = Individuo(estado, -1, -1)
		lista.append(o)
	return lista


"""

	FITNESS

"""


def getFitnessObjetivo():
	# @return : fitness objetivo
	return 1


def calculaFitness(problema, individuo):
	# FUNÇÃO QUE CALCULA O FITNESS DE UM INDIVIDUO
	# @return : Individuo calculado com valor de seu fitness
	(restricoes, desempate) = problema.avaliar_estado(
		individuo.estado, problema.qt_enfer, problema.qt_turnos)
	new_individuo = Individuo(individuo.estado, restricoes, desempate)
	new_individuo.fitness = 1 - desempate/51
	return new_individuo


"""

	MUTAÇÃO E CROSSOVER

"""


def mutacao(individuo):
	# FUNÇÃO QUE VERIFICA SE O CROMOSSOMO DE UM INDIVIDUO DEVE SOFRER MUTAÇÃO
	indice = random.randint(0, len(individuo.estado)-1)
	estado = list(individuo.estado)
	if estado[indice] == "1":
		estado[indice] = "0"
	else:
		estado[indice] = "1"
	individuo.estado = "".join(estado)
	return individuo


def crossover(problema, populacao):
	# FUNÇÃO QUE REALIZA O CROSSOVER ENTRE 2 INDIVIDUOS DA POPULAÇÃO
	j = random.randint(0, len(populacao)-1)
	k = random.randint(0, len(populacao)-1)

	indice = random.randint(0, len(populacao[j].estado))
	estado1 = populacao[j].estado[0:indice] + \
		populacao[k].estado[indice:len(populacao[j].estado)]
	estado2 = populacao[k].estado[0:indice] + \
		populacao[j].estado[indice:len(populacao[j].estado)]

	i1 = Individuo(estado1, -1, -1)
	i2 = Individuo(estado2, -1, -1)

	return (i1, i2)


"""

	SELECAO

"""


def selecao(elitismo, populacao):
	# FUNÇÃO QUE SELECIONA O MELHORES INDIVIDUOS DA POPULAÇÃO
	nova_populacao = ordenaPopulacao(populacao)
	return nova_populacao[0:int(elitismo*len(populacao))]


def ordenaPopulacao(populacao):
	# FUNÇÃO QUE ORDENA A POPULAÇÃO
	nova_populacao = []
	for x in populacao:
		nova_populacao = insereIndividuo(x, nova_populacao.copy())
	return nova_populacao


def insereIndividuo(individuo, populacao):
	# FUNÇÃO QUE INSERE UM INDIVIDUO NA POPULAÇÃO
	nova_populacao = populacao.copy()
	if(nova_populacao == []):
		nova_populacao.append(individuo)
	else:
		for ind, valor in zip(range(len(nova_populacao)), nova_populacao):
			if(ind == len(nova_populacao)-1):
				nova_populacao.append(individuo)
				break
			if individuo.fitness >= valor.fitness:
				nova_populacao = nova_populacao[0:ind] + \
					[individuo]+nova_populacao[ind:len(nova_populacao)]
				break
	return nova_populacao.copy()


def exemplo_cromossomo_objetivo():
	# FUNCAO QUE RETORNA UM EXEMPLO DE CROMOSSOMO OBJETIVO
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


def imprimeCromossomo(problema, cromossomo):
	# FUNÇÃO QUE IMPRIME A REPRESENTAÇÃO OCTAL DE UM CROMOSSOMO
	if cromossomo == None:
		print("Cromossomo sem representação")
	else:
		print("CROMOSSOMO -> ", end="")
		for x in range(0, len(cromossomo), 3):
			# print("ola-> ",estado[x:x+3])
			if(cromossomo[x:x+3] == "000"):
				print("0", end="")
			if(cromossomo[x:x+3] == "001"):
				print("1", end="")
			if(cromossomo[x:x+3] == "010"):
				print("2", end="")
			if(cromossomo[x:x+3] == "011"):
				print("3", end="")
			if(cromossomo[x:x+3] == "100"):
				print("4", end="")
			if(cromossomo[x:x+3] == "101"):
				print("5", end="")
			if(cromossomo[x:x+3] == "110"):
				print("6", end="")
			if(cromossomo[x:x+3] == "111"):
				print("7", end="")
		print("\n")
