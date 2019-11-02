import ia
import time

# ESTADOS
# A representação utilizada é a seguinte , basicamente é um vetor de tamanho igual a
# quantidade de rainhas a ser inserido no tabuleiro 
# A estrategia é que as rainhas não vão ser posicionadas aleatoriamente
# mas sim distribuidas nas colunas , então sempre vai ter apenas uma rainha numa coluna
# sendo assim indice i representa a coluna da tabuleiro  
# e tabuleiro[i] representa a linha da rainha na coluna i
# ESTADO INICIAL
def cria_tabuleiro(num_rainhas):
	"""
	Funcao que cria um tabuleiro novo sem nenhuma rainhas posicionada
	OBS: -1 indica que naquela coluna não foi posicionada nenhuma rainha
	@param num_rainhas: Numero de rainhas a ser inserido no tabuleiro
	@return : Estado do tabuleiro onde nenhuma rainhas foi posicionada
	"""
	tabuleiro = []
	for i in range(num_rainhas):
		tabuleiro.append(-1)
	return tabuleiro

# OPERADORES
# operacoes definidas em cima do tabuleiro. Todos devidamente testados
def gera(no,k,num_rainhas):
	"""
	Funcao que gera a nova posicao da linha da nova rainha no indice k que indica a coluna
	@param no: No que serve para gerar seus novos estados
	@param k : indice da coluna
	@param num_rainhas : Numero de rainhas do tabuleiro
	@return : Array das posicoes da rainhas até coluna k.
	"""
	filhos = []
	
	if k==0:
		for item in range(0,num_rainhas):
			aux = cria_tabuleiro(num_rainhas)
			aux[0]=item+1
			filhos.append(aux)
	if k>0 and k<=num_rainhas-1:
		aux = no.estado.copy()
		if (aux[k-1]==1):
			for item in range(2,num_rainhas):
				aux[k]=item+1
				filhos.append(aux.copy())
		if (aux[k-1]==num_rainhas):
			for item in range(0,num_rainhas-2):
				aux[k]=item+1
				filhos.append(aux.copy())
		if aux[k-1]>=2 and aux[k-1]<=num_rainhas-1:
			for item in range(0,num_rainhas):
				if item+1>aux[k-1]+1 or item+1<aux[k-1]-1:
					aux[k]=item+1
					filhos.append(aux.copy())
	# print("FILHOS: ",filhos)
	return filhos

# TESTE OBJETIVO
def teste_meta(t,num_rainhas):
	"""
	Funcao que testa se o estado do nó recebido é o um estado meta e retorna 1 se é verdadeiro 1 ou 0 se ele é falso
	@param t: Estado do tabuleiro
	@param num_rainhas: Numero de rainhas do tabuleiro
	@return : retorna 1 se é verdadeiro 1 ou 0 se ele é falso
	"""
	tabuleiro = t
	# print("tabuleiro ",tabuleiro)
	x,y,xx,yy = 0,0,0,0 
	for i in range(num_rainhas):
		#print("indice",i)
		x = i
		y = tabuleiro[i]
		if y==-1:
			return 0
		# print("\n Y: ",y)
		xx = x
		yy = y
		# Testando se existe na linha anteriores de acordos com as colunas
		while(1):
			xx -= 1
			# yy -= 1
			if(xx < 0 ):
				break
			if(yy == tabuleiro[xx]):
				return 0
		# Testando se existe na diagonal acima
		xx = x
		yy = y
		while(1):
			xx -= 1
			yy -= 1
			if(xx < 0 or yy < 0):
				break
			if(yy == tabuleiro[xx]):
				return 0
		# Testando se existe na diagonal abaixo
		xx = x
		yy = y
		while(1):
			xx -= 1
			yy += 1
			if(xx < 0 or yy > num_rainhas-1):
				break
			if(yy == tabuleiro[xx]):
				return 0
	return 1

# MAIN
def main():
	num =-1
	while(num<0):
		print ("-------------------------------------------------")
		num = int(input("Digite o numero de rainhas: "))
		print ("-------------------------------------------------")
		if num<0:
			print("Digite um numero valido de rainhas\n")
	metodo = -1
	while not (metodo==1 or metodo==2):		
		print ("-------------------------------------------------")
		print("Digite qual o metodo de busca: ")
		print("	1.BFS (Busca em profundidade)")
		print("	2.DFS (Busca em largura)")
		print("OBS: 1 para Busca em profundidade ou 2 para Busca em largura")
		metodo = int(input())
		print ("-------------------------------------------------")
		if not(metodo==1 or metodo==2):
			print("Digite um numero valido ou 1 ou 2\n")

	teste = cria_tabuleiro(num)
	# lista de operadores do problema
	operadores = [gera] 
	
	if metodo==2:
		#Problemas:
		# Busca em largura
		# intanciando o problema
		problema = ia.Problema(teste, operadores, teste_meta,num)
		ini = time.time()
		# Realizando a busca em profundidade
		resultado = ia.busca(problema, ia.enfileira_fifo)
		fim = time.time()
		print ("-------------------------------------------------")
		print ("\nBusca em Largura")
		print ("Estado Inicial:",teste)
		print ("Saida Busca em Largura: ", resultado)
		print ("Tempo: ", fim - ini)
		print ("Numero de comparacoes: ", problema.comparacoes)
		print ("-------------------------------------------------")
	if metodo==1:
		#Problemas:
		# Busca em profundidade
		# intanciando o problema
		problema1 = ia.Problema(teste, operadores, teste_meta,num)
		ini1 = time.time()
		# Realizando a busca em profundidade
		resultado1 = ia.busca(problema1, ia.enfileira_lifo)
		fim1 = time.time()
		print ("-------------------------------------------------")
		print ("Busca em Profundidade")
		print ("Estado Inicial:",teste)
		print ("Saida Busca em profundidade: ", resultado1)
		print ("Tempo: ", fim1 - ini1)
		print ("Numero de comparacoes: ", problema1.comparacoes)
		print ("-------------------------------------------------")
	return 0
# Execucao do metodo main
print ("O programa executou com saida %d" % (main()))