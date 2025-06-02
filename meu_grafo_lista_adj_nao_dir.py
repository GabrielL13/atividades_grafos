from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoListaAdjacenciaNaoDirecionado):

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

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()
        grau = 0
        for aresta in self.arestas.values():
            if aresta.v1.rotulo == V and aresta.v2.rotulo == V:
                grau += 2  # laço conta duas vezes
            elif aresta.v1.rotulo == V or aresta.v2.rotulo == V:
                grau += 1
        return grau


    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        pares = {}
        for a in self.arestas.values():
            extremos = frozenset([a.v1.rotulo, a.v2.rotulo])
            if extremos in pares:
                return True
            else:
                pares[extremos] = 1
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
    
    def dfs(self, V=''):
        '''
        Executa uma busca em profundidade (DFS) a partir do vértice V
        :param V: vértice raiz da busca
        :return: grafo representando a árvore de busca DFS
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice {V} não existe no grafo.")

        visitados = set()
        arestas_resultado = []
        pilha = [V]

        while pilha:
            atual = pilha.pop()
            if atual not in visitados:
                visitados.add(atual)
                for aresta in self.arestas.values():
                    v1 = aresta.v1.rotulo
                    v2 = aresta.v2.rotulo
                    if v1 == atual and v2 not in visitados:
                        pilha.append(v2)
                        arestas_resultado.append((aresta.rotulo, v1, v2))
                    elif v2 == atual and v1 not in visitados:
                        pilha.append(v1)
                        arestas_resultado.append((aresta.rotulo, v2, v1))

        
        grafo_dfs = MeuGrafo()
        for vertice in self.vertices:
            grafo_dfs.adiciona_vertice(vertice.rotulo)

        for rotulo, v1, v2 in arestas_resultado:
            if rotulo not in grafo_dfs.arestas:
                grafo_dfs.adiciona_aresta(rotulo, v1, v2)
        return grafo_dfs


    def bfs(self, V=''):
        '''
        Executa uma busca em largura (BFS) a partir do vértice V
        :param V: vértice raiz da busca
        :return: grafo representando a árvore de busca BFS
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice {V} não existe no grafo.")

        visitados = set()
        fila = [V]
        arestas_resultado = []

        while fila:
            atual = fila.pop(0)
            if atual not in visitados:
                visitados.add(atual)
                for aresta in self.arestas.values():
                    v1 = aresta.v1.rotulo
                    v2 = aresta.v2.rotulo
                    if v1 == atual and v2 not in visitados and v2 not in fila:
                        fila.append(v2)
                        arestas_resultado.append((aresta.rotulo, v1, v2))
                    elif v2 == atual and v1 not in visitados and v1 not in fila:
                        fila.append(v1)
                        arestas_resultado.append((aresta.rotulo, v2, v1))

        grafo_bfs = MeuGrafo([v.rotulo for v in self.vertices])
        for rotulo, v1, v2 in arestas_resultado:
            if rotulo not in grafo_bfs.arestas:
                grafo_bfs.adiciona_aresta(rotulo, v1, v2)
        return grafo_bfs

    def __eq__(self, other):
        
        if not isinstance(other, MeuGrafo):
            return False
        if len(self.vertices) != len(other.vertices):
            return False
        if len(self.arestas) != len(other.arestas):
            return False
        vertices_self = sorted([v.rotulo for v in self.vertices])
        vertices_other = sorted([v.rotulo for v in other.vertices])
        if vertices_self != vertices_other:
            return False

        arestas_self = sorted([(a.rotulo, frozenset([a.v1.rotulo, a.v2.rotulo])) for a in self.arestas.values()])
        arestas_other = sorted([(a.rotulo, frozenset([a.v1.rotulo, a.v2.rotulo])) for a in other.arestas.values()])
        return arestas_self == arestas_other
