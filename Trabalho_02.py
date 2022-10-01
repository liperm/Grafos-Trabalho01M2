from cProfile import label
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Grafo:
    def __init__(self, n_vertices):
        self.n_vertices = n_vertices
        self.matriz = np.zeros((n_vertices, n_vertices), dtype = int)

    def verificar_coordenada_valida(self, coordenada):
        if(ord(coordenada) - 65 > self.n_vertices - 1):
            print('Conexão inválida!!')
            return False
        
        return True

    def preencher_grafo(self):
        i = 0
        vertice = 'A'

        while i < self.n_vertices:
            self.adicionar_conexao(vertice)

            vertice = chr(ord(vertice) + 1)
            i += 1

    def adicionar_conexao(self, vertice):
        valido = False
    
        while valido == False:
            conexoes = input(f'Conexoes do vértice {vertice}: ').upper()

            for conexao in conexoes:
                if(not self.verificar_coordenada_valida(conexao) or not self.verificar_coordenada_valida(vertice)):
                    valido = False

                else:
                    coluna = ord(conexao) - 65
                    linha = ord(vertice) - 65
                    valido = True
                    self.matriz[linha][coluna] = 1

    def remover_vertice(self):
        vertices = input('Vértice a ser excluido: ').upper()

        for vertice in vertices:
            if(not self.verificar_coordenada_valida(vertice)):
                return

            self.matriz = np.delete(self.matriz, (ord(vertice) - 65), 0)
            self.matriz =  np.delete(self.matriz, (ord(vertice) - 65), 1)

    def remover_aresta(self):
        conexao = input('Conexão a ser removida: ').upper()

        if(len(conexao) > 2):
            print('Insira somente uma conexão')
        
        elif(self.verificar_coordenada_valida(conexao[0]) and self.verificar_coordenada_valida(conexao[1])):
            self.matriz[ord(conexao[0]) - 65][ord(conexao[1]) - 65] = 0

            bidirecional = input('\tRemoção bidirecional?[s/n]: ').upper()
            if(bidirecional == 'S'):
                self.matriz[ord(conexao[1]) - 65][ord(conexao[0]) - 65] = 0

        return        
    
    def printar_grafo(self):
        grafo = nx.Graph()

        for i in range(0, self.n_vertices):
            grafo.add_node(chr(i + 65))

        result = np.where(self.matriz == 1)
        coordenadas = list(zip(result[0], result[1]))
        
        arestas_dirigidas = []
        arestas_nao_dirigidas = []

        for coordenada in coordenadas:
            if((coordenada[1], coordenada[0]) in coordenadas):
                arestas_nao_dirigidas.append(coordenada)
            else:
                arestas_dirigidas.append(coordenada)

        
        for i in range(len(arestas_nao_dirigidas)):
            arestas_nao_dirigidas[i] = (chr(arestas_nao_dirigidas[i][0] + 65), chr(arestas_nao_dirigidas[i][1] + 65))
        
        for i in range(len(arestas_dirigidas)):
            arestas_dirigidas[i] = (chr(arestas_dirigidas[i][0] + 65), chr(arestas_dirigidas[i][1] + 65))

        arrow_options = {
            'arrowstyle' : '-|>',
            'arrowsize' : 12,
            'width' : 1
            }

        node_options = {
            'node_size' : 500,
        }

        pos = nx.spring_layout(grafo)
        nx.draw_networkx_nodes(grafo, pos, **node_options)
        nx.draw_networkx_labels(grafo, pos)
        nx.draw_networkx_edges(grafo, pos, **arrow_options, edgelist = arestas_dirigidas, arrows = True)
        nx.draw_networkx_edges(grafo, pos, **arrow_options, edgelist = arestas_nao_dirigidas, arrows = False)
        plt.show()

    def encontrar_ciclo(self):
        #Escolhe-se o vértice de referência (o primeiro nesse caso)(v0)
        vertice = 0
        
        #Percorre todos os vertices em busca de um caminho 3
        while vertice < self.n_vertices:
            for i in range(self.n_vertices): #busca o primeiro vértice em que a referência se conecta (v1)
                if self.matriz[vertice, i] == int(1):
                    for j in range(self.n_vertices): #busca o vertice em que a adjacencia do primeiro se conecta(v2)
                        if self.matriz[i, j] == int(1):
                            if self.matriz[j, vertice] == int(1): #se este segundo vértice (v2) se conectar a referencia(v0), existe um caminho de comprimento 3 (v0 -> v1 -> v2 -> v0)
                                return True
            vertice += 1


        return False

    def get_n_arestas(self):
        arestas = []
        n_arestas = 0

        for i in range(self.n_vertices):
            for j in range(self.n_vertices):
                if self.matriz[i, j] == 1 and (not [j, i] in arestas):
                    arestas.append([i, j])
                    n_arestas += 1
        
        return n_arestas

    def is_planar(self):
        e = self.get_n_arestas()

        if self.n_vertices >= 3:
            if not self.encontrar_ciclo():
                if ((2 * self.n_vertices - 4) >= e):
                    return True, (2 - self.n_vertices + e)
                return False, -1
            else:
                if ((3 * self.n_vertices - 6) >= e):
                    return True, (2 - self.n_vertices + e)
                return False, -1
        else:
            return True, (2 - self.n_vertices + e)

g = Grafo(5)
g.matriz = np.matrix([[0, 1, 1, 1, 0],
                      [1, 0, 0, 0, 1],
                      [1, 0, 0, 1, 1],
                      [1, 0, 1, 0, 1],
                      [0, 1, 1, 1, 0]], dtype = int)

g.printar_grafo()
print(g.is_planar())