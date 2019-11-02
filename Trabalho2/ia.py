# REPRESENTAÇÃO DO PROBLEMA
class Problema:
	# tipo abstrato de dado do problema definido

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
	 	return "Problema : Estado Inicial {0}, Numero de funcionarios {1}".format(self.estado_inicial, self.num_funcionarios)


class ProblemaBusca(Problema):
	"""
	Representação do problema para as buscas
	@param melhor_avaliado : Função que avalia o melhor nó entre os nós que recebe   
	@param avaliar_estado : Função que avalia o estado do nó 
	"""

	def __init__(self, estado_inicial, operadores, qt_enfer, qt_turnos, melhor_avaliado, avaliar_estado, metodo):
	   super().__init__(estado_inicial, operadores, qt_enfer, qt_turnos)
	   self.melhor_avaliado = melhor_avaliado
	   self.avaliar_estado = avaliar_estado
	   self.metodo = metodo

# REPRESENTACAO DE NÓ


class No:
	# para realizar o algoritmo de busca em lista, devemos ter o tipo no. O tipo abstrato

	def __init__(self, estado, no_pai, operador, profundidade, restricoes, desempate):
		"""
		Construtor de um no para busca em lista.
		@param estado: estado associado ao no corrente
		@param no_pai: no que deu origem ao no atual. "None" caso ele seja raiz
		@param operador: operador associado ao no
		@param profundidade: profundidade que no se encontra
		@param iteracao: indice da coluna onde será posicionada a nova rainha
		@param filhos: lista de nós filhos gerados pelo operador sobre o estado do nó
		"""
		self.estado = estado
		self.no_pai = no_pai
		self.operador = operador
		self.profundidade = profundidade
		self.restricoes = restricoes
		self.desempate = desempate

	def __str__(self):
		return "[NO: profundidade {0}, Num. de restrições violadas {1}, 1º criterio de desempate (Soma de turnos violados) {2}]".format(self.profundidade, self.restricoes, self.desempate)

# FUNÇÃO QUE IMPRIME O ESTADO DO NÓ


def imprime_estado(problema, estado):
	if estado == None:
		print("Estado sem representação")
	else:
		print("")
		for x in range(problema.qt_turnos, len(estado)+problema.qt_turnos, problema.qt_turnos):
			print("\t"+estado[x-problema.qt_turnos:x])
		print("")

# FUNCAO QUE TESTA SE UM ESTADO É META


def teste_meta(no):
	"""
	Função que que verifica se um estado é meta 
	"""
	if(no.restricoes == 0):
		return True
	else:
		return False

# LIFO


def enfileira_lifo(lista_1, lista_2):
	"""
	Funcao que simula a estrutura de inserção em pilha
	@param lista1: lista de nós
	@param lista2: lista de nós
	@return : Insercao dos elementos da lista 2 no final da lista 1, essa lista que é retornada simula a pilha
	"""
	var = lista_1.copy()
	for x in lista_2:
		var.append(x)
		# print("LIFO: ",x)
	return var

# QUICK SORT
# METODO UTILIZADO SOMENTE NA BUSCA PELO MAIOR ACLIVE


def quick_sort(lista, esq, dir):
	pivo = esq
	ch = 0
	i = esq+1
	while(i <= dir):
		j = i
		if compare(lista[j], lista[pivo]) == False:
			ch = lista[j]
			while(j > pivo):
				lista[j] = lista[j-1]
				j -= 1
			lista[j] = ch
			pivo += 1
		i += 1
	if(pivo-1 >= esq):
		quick_sort(lista, esq, pivo-1)
	if(pivo+1 <= dir):
		quick_sort(lista, pivo+1, dir)

# GERADOR DE ESTADOS


def expande(no, problema):
	"""
	Funcao que expande um no e gera um conjunto de filhos
	@param no: no atual a ser expandido
	@param problema: problema no qual o no se encontra, no qual apenas se utiliza os operadores do problemas
	@return : Filhos gerados pela operação do problema
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
	# imprime_avaliação_filhos(filhos)
	best = problema.melhor_avaliado(filhos)
	return best, filhos

# FUNÇÃO QUE ORDENA OS ELEMENTOS GERADOS PELA INSERCAO UM POR UM EM NÓS


def ordena(gerados, nos):
	for x in gerados:
		nos = insert_no(x, nos.copy())
	return nos

# FUNÇÃO QUE INSERE UM NO NA LISTA DE NÓS BASEADO NO VALOR DE RESTR


def insert_no(no, lista):
	aux = lista.copy()
	if(aux == []):
		aux.append(no)
	else:
		for ind, valor in zip(range(len(aux)), aux):
			if compare(no, valor) == True:
				aux = aux[0:ind]+[no]+aux[ind:len(aux)]
				break
	return aux


# FUNCAO QUE COMPARA DOIS NÓ


def compare(no1, no2):
	if((no1.restricoes < no2.restricoes) or (no1.restricoes == no2.restricoes and no1.desempate < no2.desempate) or (no1.restricoes == no2.restricoes and no1.desempate < no2.desempate and no1.estado < no2.estado)):
		return True
	return False

# FUNÇÃO QUE IMPRIME AS AVALIAÇÃO DOS FILHOS


def imprime_avaliação_filhos(lista):
	print("--------------------------------------------")
	print("Nós gerados")
	for no in lista:
		print(no)
	print("--------------------------------------------")

# FUNÇÃO DE BUSCA DO PROBLEMA


def busca(problema):
	"""
	@param problema :Representação do problema
	@param enfileira :Função que define a ordenação de nós 
	@return : Melhor nó encontrado ou o nó objetivo
	"""
	c = 0
	nos = []
	visitados = []
	qt_enfer = problema.qt_enfer
	qt_turnos = problema.qt_turnos
	custo, desempate = problema.avaliar_estado(
		problema.estado_inicial, qt_enfer, qt_turnos)

	nos.append(No(problema.estado_inicial, None, None, 0, custo, desempate))
	melhor_no = nos[0]
	tam_anterior_nos = 0
	while True:
		if nos == []:
			print("Nó objetivo não encontrado: Fila Vazia")
			print("Melhor no encontrado na busca: ", melhor_no)
			return melhor_no.estado
		no = nos[0]
		print("-----------------------------------------------------")
		print("Melhor nó encontrado atualmente: ", melhor_no)
		print("No atual da busca:", no)
		imprime_estado(problema, no.estado)

		print("Numero de comparações já feitas: ", c, "\n")
		# Incrementando as comparações de estados até chegar no estado meta ou não
		c = c + 1
		problema.comparacoes = c
		# Testa se o nó atual é o meta
		if teste_meta(no):
			print("-----------------------------------------------------")
			print("\\\\\\\  Nó objetivo encontrado  ////////")
			return no.estado
		# caso o nó nao seja a meta,ele é expandido e removido da estrutura utilizada
		del(nos[0])
		if not no.estado in visitados:
			best, gerados = expande(no, problema)
			tam_anterior_nos = len(nos)

			if(problema.metodo == 1): 
			# Se o tipo de busca foi subida da encosta
				if (best != []):
					if(compare(melhor_no, best[0]) == False):
						melhor_no = best[0]
						# Insere o melhor na fila
						nos = enfileira_lifo(best, nos)
			elif(problema.metodo == 2):
				# Se o tipo de busca foi subida da encosta pelo maior aclive
				if (best != []):
					if(compare(melhor_no, best[0]) == False):
						melhor_no = best[0]
					# Ordena os filhos gerados com o quick sort , os filhos são comparados com a função compare
					quick_sort(gerados, 0, len(gerados)-1)
					# Insere os gerados na fila
					nos = enfileira_lifo(gerados, nos)
			elif(problema.metodo == 3):
				if (best != []):
					if(compare(melhor_no, best[0]) == False):
						melhor_no = best[0]
					# Insere os gerados na fila com a função ordena por inserção, o metodo compara os nós com a função compare
					nos = ordena(gerados, nos)
			# Insere o estado visitado na lista de visitados
			visitados.append(no.estado)
			# Imprima o tamanho da estrutura atual
			print("Tamanho da estrutura de dados anterior a inserção: ", tam_anterior_nos)
			print("Tamanho da estrutura de dados  depois da inserção: ",
                            len(nos), " --- Quantidade de estados gerados", len(gerados))

			print("-----------------------------------------------------")
