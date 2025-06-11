from bibgrafo.grafo_matriz_adj_nao_dir import GrafoMatrizAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *
from bibgrafo.vertice import Vertice

class MeuGrafo(GrafoMatrizAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto (set) de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um conjunto (set) com os pares de vértices não adjacentes
        '''
        nao_adjacentes = set()
        num_vertices = len(self.vertices)

        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if not self.matriz[i][j]:
                    vertice_i_rotulo = self.vertices[i].rotulo
                    vertice_j_rotulo = self.vertices[j].rotulo
                    nao_adjacentes.add(f"{vertice_i_rotulo}-{vertice_j_rotulo}")
        return nao_adjacentes

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        # Sua lógica atual funciona, mas pode ser simplificada e otimizada
        # para a estrutura de matriz de adjacência não direcionada.
        # Em um grafo não direcionado, laços estão apenas na diagonal principal.
        for i in range(len(self.vertices)):
            if self.matriz[i][i]: 
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo.')
        
        grau = 0
        indice_V = self.indice_do_vertice(Vertice(V)) 

        for j in range(len(self.vertices)):
            arestas_na_celula = self.matriz[indice_V][j]
            
            if arestas_na_celula:
                if indice_V == j:
                    grau += 2 * len(arestas_na_celula)
                else:
                    grau += len(arestas_na_celula)
        return grau
        

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        for linha in self.matriz:
            for elemento in linha:
                if len(elemento) > 1:
                    return True
        return False
    
    def arestas_sobre_vertice(self, V):
        '''
        Provê um conjunto (set) que contém os rótulos das arestas que
        incidem sobre o vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um conjunto com os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo.')

        arestas_incidentes = set()
        indice_V = self.indice_do_vertice(Vertice(V))

        for j in range(len(self.vertices)):
            for rotulo_aresta in self.matriz[indice_V][j]:
                arestas_incidentes.add(rotulo_aresta)
        
        return arestas_incidentes

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        Um grafo não direcionado é completo se todos os pares de vértices distintos
        estão conectados por exatamente uma aresta, e não há laços.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco():
            return False

        num_vertices = len(self.vertices)
        
        if num_vertices == 0 or num_vertices == 1:
            return True

        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if len(self.matriz[i][j]) != 1:
                    return False
        return True
    
    def marshall(self):
        '''
        Use o grafo de matriz de adjacência para fazer uma função para encontrar a matriz de alcançabilidade de um grafo usando o algoritmo de Warshall.
        '''
        num_vertices = len(self.vertices)
        matriz_adj = list()
        for i in range(num_vertices):
            print(self.vertices[i].rotulo)
            linha = list()
            for j in range(num_vertices):
                if not self.matriz[i][j]:
                    linha.append(0)
                else:
                    linha.append(1)
            matriz_adj.append(linha)
        print(matriz_adj)
    