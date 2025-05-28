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
            for v2 in self.vertices[i + 1:]:  # garante que não repete pares invertidos
                extremos = {v1.rotulo, v2.rotulo}
                existe_aresta = any({a.v1.rotulo, a.v2.rotulo} == extremos for a in self.arestas.values())
                if not existe_aresta:
                    par_formatado = f"{v1.rotulo}-{v2.rotulo}"
                    nao_adj.add(par_formatado)
        return nao_adj

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for a in self.arestas.values():
            if a.v1 == a.v2:
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
            raise VerticeInvalidoError()
        grau = 0
        for aresta in self.arestas.values():
            if aresta.v1.rotulo == V and aresta.v2.rotulo == V:
                grau += 2  
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

        resultado = set()
        for rotulo, aresta in self.arestas.items():
            if aresta.v1.rotulo == V or aresta.v2.rotulo == V:
                resultado.add(rotulo)
        return resultado

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco():
            return False

        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 != v2:
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
        
        arvore_dfs = MeuGrafo()
        visitados = set()

        def explorar(v):
            vertice = self.get_vertice(v) 
            visitados.add(vertice.rotulo)  
            for aresta in self.arestas.values():
                if aresta.eh_ponta(vertice):
                    outro_v = aresta.v1 if aresta.v2 == vertice else aresta.v2
                    
                    if outro_v.rotulo not in visitados:
                        arvore_dfs.adiciona_vertice(outro_v)
                        arvore_dfs.adiciona_aresta(aresta.rotulo, aresta.v1, aresta.v2, aresta.peso)
                        explorar(outro_v.rotulo)

        explorar(V)
        return arvore_dfs
        


    def bfs(self, V=''):
        '''
        Executa uma busca em largura (BFS) a partir do vértice V
        :param V: vértice raiz da busca
        :return: grafo representando a árvore de busca BFS
        '''
        pass
