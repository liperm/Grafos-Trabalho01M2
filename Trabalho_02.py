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
