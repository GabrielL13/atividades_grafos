from bibgrafo.grafo_lista_adj_dir import GrafoListaAdjacenciaDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoListaAdjacenciaDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''
        nao_adj = set()
        for i, v1 in enumerate(self.vertices):
            for v2 in self.vertices[i + 1:]:
                extremos = {v1.rotulo, v2.rotulo}
                existe_aresta = any({a.v1.rotulo, a.v2.rotulo} == extremos for a in self.arestas.values())
                if not existe_aresta:
                    nao_adj.add(f"{v1.rotulo}-{v2.rotulo}")
        return nao_adj

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        return any(a.v1 == a.v2 for a in self.arestas.values())

    def grau_entrada(self, V=''):
        '''
        Provê o grau de entrada do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()
        grau = 0
        for aresta in self.arestas.values():
            if aresta.v2.rotulo == V :
                grau += aresta.peso
        return grau

    def grau_saida(self, V=''):
        '''
        Provê o grau de saída do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()
        grau = 0
        for aresta in self.arestas.values():
            if aresta.v1.rotulo == V :
                grau += aresta.peso
        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        pares = []
        for aresta in self.arestas.values():
            if aresta.v1.rotulo+aresta.v2.rotulo in pares: 
                return True
            else:
                pares.append(aresta.v1.rotulo+aresta.v2.rotulo)
        return False
        
    
    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()

        return {rotulo for rotulo, aresta in self.arestas.items()
                if aresta.v1.rotulo == V or aresta.v2.rotulo == V}

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco():
            return False
        for i, v1 in enumerate(self.vertices):
            for v2 in self.vertices[i + 1:]:
                extremos = {v1.rotulo, v2.rotulo}
                existe_aresta = any({a.v1.rotulo, a.v2.rotulo} == extremos for a in self.arestas.values())
                if not existe_aresta:
                    return False
        return True
    
    def menor_caminho(self, V, X):
        if not self.existe_rotulo_vertice(V) or not self.existe_rotulo_vertice(X):
            raise VerticeInvalidoError()

        for aresta in self.arestas.values():
            if aresta.peso < 0:
                print("O grafo possui peso negativos > ",aresta.rotulo)
                return False

        dist = {v.rotulo: 10000000000000 for v in self.vertices}
        visitado = {v.rotulo: False for v in self.vertices}
        anterior = {v.rotulo: None for v in self.vertices}
        dist[V] = 0

        while True:
            u = None
            menor_dist = 10000000000000
            for v in self.vertices:
                r = v.rotulo
                if not visitado[r] and dist[r] < menor_dist:
                    menor_dist = dist[r]
                    u = r

            if u is None:
                break
            visitado[u] = True

            for aresta in self.arestas.values():
                if aresta.v1.rotulo == u:
                    v = aresta.v2.rotulo
                    peso = aresta.peso
                    if not visitado[v]:
                        if dist[u] + peso < dist[v]:
                            dist[v] = dist[u] + peso
                            anterior[v] = u

        if dist[X] == 10000000000000:
            return False

        caminho = []
        atual = X
        while atual is not None:
            caminho.insert(0, atual)
            atual = anterior[atual]

        return [' -> '.join(caminho),dist[X]]

    def bellman_ford(self, V, X):
        if not self.existe_rotulo_vertice(V) or not self.existe_rotulo_vertice(X):
            raise VerticeInvalidoError()
        
        distancias = {v: 10000000000000 for v in self.vertices}
        predecessores = {v: None for v in self.vertices}
        distancias[V] = 0

        for i in range(len(self.vertices) - 1):
            for aresta in self.arestas:
                u = aresta.origem
                v = aresta.destino
                peso = aresta.peso
                if distancias[u] != float('inf') and distancias[u] + peso < distancias[v]:
                    distancias[v] = distancias[u] + peso
                    predecessores[v] = u

        for aresta in self.arestas:
            u = aresta.origem
            v = aresta.destino
            peso = aresta.peso
            if distancias[u] != 10000000000000 and distancias[u] + peso < distancias[v]:
                print("Ciclo negativo detectado. Não é possível calcular o menor caminho.")
                return False

        if distancias[X] == 10000000000000:
            return False

        caminho = []
        atual = X
        while atual is not None:
            caminho.insert(0, atual)
            atual = predecessores[atual]

        return [caminho,distancias[X]]