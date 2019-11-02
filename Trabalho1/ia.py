# REPRESENTAÇÃO DO PROBLEMA 
class Problema:
	# tipo abstrato de dado problema definido 

	def __init__(self, estado_inicial, operadores, teste_meta,num_rainhas):
		"""
		Construtor de uma classe problema. O construtor recebe como parametros todos
		os componentes de um problema para construir um.
		@param estado_inicial: estado inicial que se encontra o problema
		@param operadores: operadores que executam sobre o problema
		@param teste_meta: funcao que testa para ver se alcancamos o estado desejado
		"""
		self.estado_inicial = estado_inicial
		self.operadores = operadores
		self.teste_meta = teste_meta
		self.comparacoes = 0
		self.num_rainhas = num_rainhas

	def __str__(self):
	 	return "Problema : Estado Inicial {0}, Numero de rainhas {1}".format(self.estado_inicial,self.num_rainhas) 

# REPRESENTACAO DE NÓ
class No:
	# para realizar o algoritmo de busca em arvore, devemos ter o tipo no. O tipo abstrato

	def __init__(self, estado, no_pai, operador, profundidade, custo_caminho,iteracao,filhos):
		"""
		Construtor de um no para busca em arvore.
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
		self.custo_caminho = custo_caminho
		self.indice_iteracao =iteracao
		self.filhos =filhos

	def __str__(self):
		return "[NO: estado {0}, profundidade {1}]".format(self.estado,self.profundidade)

# FIFO
def enfileira_fifo(lista_1, lista_2):
	"""
	Funcao que simula a estrutura de inserção em fila
	@param lista1: lista de nós
	@param lista2: lista de nós
	@return : Insercao dos elementos da lista 1 no final da lista 2, essa lista que é retornada simula a fila
	"""
	var = lista_2.copy()
	for x in lista_1:
		var.append(x)
		# print("FIFO: ",x)
	return var

# LIFO
def enfileira_lifo(lista_1,lista_2):
	"""
	Funcao que simula a estrutura de inserção em pilha
	@param lista1: lista de nós
	@param lista2: lista de nós
	@return : Insercao dos elementos da lista 2 no final da lista 1, essa lista que é retornada simula a pilha
	"""
	var=lista_1.copy()
	for x in lista_2:
		var.append(x)
		# print("LIFO: ",x)
	return var
	
# GERADOR DE ESTADOS
def expande(no, problema):
	"""
	Funcao que expande um no e gera um conjunto de filhos
	@param no: no atual a ser expandido
	@param problema: problema no qual o no se encontra, no qual apenas se utiliza os operadores do problemas
	"""
	filhos = [] # conjunto de filhos gerados por um determinado no
	for operacao in problema.operadores:
		resultado = operacao(no,no.indice_iteracao,problema.num_rainhas)
		# se o no produz algum filho, entao coloque ele no conjunto de filhos
		if not resultado is None:
			# criando um novo no a partir da expansao do no atual
			print("Novos estados gerados : ")
			for x in resultado:
				# if(not no.no_pai==None):
				o = No(x.copy(),no,operacao,no.profundidade+1,no.custo_caminho+1,no.indice_iteracao+1,None)
				filhos.append(o)
				print(o)
				# else:
				# 	o = No(x.copy(),no,operacao,no.profundidade+1,no.custo_caminho+1,1)
				# 	filhos.append(o)
	no.filhos=filhos	
	# retornando o conjunto resultante da expansao
	return filhos

def imprime_caminho(no):
	"""
	Funcao que imprime o caminho parcial do no
	@param no: no a ser imprimido
	"""
	if not no == None:
		imprime_caminho(no.no_pai)
	if (not no ==None):
		print(no)

def imprime_vizinhanca(no):
	"""
	Funcao que imprime a vizinhança do no com base no seu pai nó 
	OBS : Todo nó na estrutura que estou utilizando tem seus filhos,
	então sua vizinhança será imprimido atraves do nó pai do nó recebido como parametro
	@param no: no a ser imprimido sua vizinhança
	"""
	if(not no.no_pai==None):
		aux = no.no_pai.filhos
		for x in aux:
			if(not no.estado == x.estado):
				print(x)
	else:
		print([])

def busca(problema, enfileira):
	# Variavel utilizada para verificar quantos comparaçoes de estados de nó foram utilizadas
	c = 0
	"""
	Funcao que realiza um algoritmo de busca. A estrategia de busca depende da
	funcao enfileira passada como argumento.
	Ex:
	FIFO representa busca em largura
	LIFO representa busca em profundidade.
	@param problema: problema a ser resolvido
	@param enfileira: funcao de enfileiramento de nos
	"""
	# criando a estrutura de dados (fila ou pilha) com o estado inicial
	nos = []
	nos.append(No(problema.estado_inicial, None, None, 0, 0,0,[]))
	# criando estrutura que guarda os caminhos já visitados
	visitados = []
	while (True):
		if nos == []:
			return None # retorna fracasso caso a lista seja vazia
		# criando uma variavel que guarda o primeiro no de teste da estrutura utilizada
		no = nos[0]
		print("-----------------------------------------------------")
		print("\nNo atual da busca:",no)
		print("Vizinhança: ")
		imprime_vizinhanca(no)
		print("Caminho parcial do nó atual da busca: ")
		imprime_caminho(no)
		# Incrementando as comparações de estados até chegar no estado meta ou não
		c = c + 1
		problema.comparacoes = c
		# IF testa se o nó atual é o meta
		if problema.teste_meta(no.estado,problema.num_rainhas):
			print("NO encontrado: ",no)
			return no.estado
		# caso o nó nao seja a meta,ele é expandido e removido da estrutura utilizada
		del(nos[0])
		# teste de redundancia
		if not no.estado in visitados:
			# colocando elementos na estrutura
			nos = enfileira(expande(no, problema), nos)
			# Imprima o tamanho da estrutura atual
			print("Tamanho da estrutura de dados: ",len(nos))
			print("-----------------------------------------------------")
			# insere o no visitado na variavel visitados para evitar redundancias de visitas de estados
			visitados.append(no)	