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
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice {V} não existe no grafo.")

        visitados = set()
        adicionados = set()
        pilha = [V]
        grafo_dfs = MeuGrafo()

        grafo_dfs.adiciona_vertice(V)
        visitados.add(V)
        adicionados.add(V)

        arestas_usadas = set()

        while pilha:
            atual = pilha[-1]
            vizinhos_nao_visitados = []

            # Encontrar vizinhos não visitados do vértice atual
            for aresta in self.arestas.values():
                if aresta.rotulo in arestas_usadas:
                    continue

                v1 = aresta.v1.rotulo
                v2 = aresta.v2.rotulo

                if v1 == atual and v2 not in visitados:
                    vizinhos_nao_visitados.append((v2, aresta))
                elif v2 == atual and v1 not in visitados:
                    vizinhos_nao_visitados.append((v1, aresta))

            # Ordenar vizinhos não visitados pelo rótulo
            vizinhos_nao_visitados.sort(key=lambda x: x[0])

            if vizinhos_nao_visitados:
                proximo, aresta = vizinhos_nao_visitados[0]
                visitados.add(proximo)
                pilha.append(proximo)
                arestas_usadas.add(aresta.rotulo)

                if proximo not in adicionados:
                    grafo_dfs.adiciona_vertice(proximo)
                    adicionados.add(proximo)

                grafo_dfs.adiciona_aresta(aresta.rotulo, atual, proximo)
            else:
                pilha.pop()

        return grafo_dfs


    def bfs(self, V=''):
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f"O vértice {V} não existe no grafo.")

        visitados = set()
        adicionados = set()
        fila = [V]
        grafo_bfs = MeuGrafo()

        grafo_bfs.adiciona_vertice(V)
        visitados.add(V)
        adicionados.add(V)

        arestas_usadas = set()

        while fila:
            atual = fila.pop(0)
            vizinhos_nao_visitados = []

            for aresta in self.arestas.values():
                if aresta.rotulo in arestas_usadas:
                    continue

                v1 = aresta.v1.rotulo
                v2 = aresta.v2.rotulo

                if v1 == atual and v2 not in visitados:
                    vizinhos_nao_visitados.append((v2, aresta, atual))
                elif v2 == atual and v1 not in visitados:
                    vizinhos_nao_visitados.append((v1, aresta, atual))

            vizinhos_nao_visitados.sort(key=lambda x: x[0])

            for proximo, aresta, origem in vizinhos_nao_visitados:
                visitados.add(proximo)
                fila.append(proximo)
                arestas_usadas.add(aresta.rotulo)

                if proximo not in adicionados:
                    grafo_bfs.adiciona_vertice(proximo)
                    adicionados.add(proximo)

                grafo_bfs.adiciona_aresta(aresta.rotulo, origem, proximo)

        return grafo_bfs
    
    def ha_ciclo(self):
        def dfs_ciclo(v, pai, visitados):
            visitados.add(v)
            for aresta in self.arestas.values():
                if aresta.v1.rotulo == v:
                    vizinho = aresta.v2.rotulo
                elif aresta.v2.rotulo == v:
                    vizinho = aresta.v1.rotulo
                else:
                    continue
                
                if vizinho not in visitados:
                    if dfs_ciclo(vizinho, v, visitados):
                        return True
                elif vizinho != pai:
                    # Encontrou um vértice visitado diferente do pai -> ciclo
                    return True
            return False

        visitados = set()
        for vertice in [v.rotulo for v in self.vertices]:
            if vertice not in visitados:
                if dfs_ciclo(vertice, None, visitados):
                    return True
        return False
    
    def eh_arvore(self):
        # Verifica ciclo
        if self.ha_ciclo():
            return False
        
        # Verifica conexão (usar BFS ou DFS)
        if not self.vertices:
            return False # grafo vazio não é árvore

        start = self.vertices[0].rotulo
        visitados = set()

        def dfs(v):
            visitados.add(v)
            for aresta in self.arestas.values():
                if aresta.v1.rotulo == v:
                    vizinho = aresta.v2.rotulo
                elif aresta.v2.rotulo == v:
                    vizinho = aresta.v1.rotulo
                else:
                    continue
                
                if vizinho not in visitados:
                    dfs(vizinho)

        dfs(start)

        if len(visitados) != len(self.vertices):
            return False # não conexo
        
        # Graus dos vértices
        graus = {v.rotulo: 0 for v in self.vertices}
        for a in self.arestas.values():
            graus[a.v1.rotulo] += 1
            graus[a.v2.rotulo] += 1
        
        folhas = [v for v, g in graus.items() if g == 1]
        return folhas
    
    def eh_bipartido(self):
        if not self.vertices:
            return True # Grafo vazio é bipartido

        cores = {}
        from collections import deque

        for vertice in [v.rotulo for v in self.vertices]:
            if vertice not in cores:
                cores[vertice] = 0
                fila = deque([vertice])

                while fila:
                    atual = fila.popleft()
                    for aresta in self.arestas.values():
                        if aresta.v1.rotulo == atual:
                            vizinho = aresta.v2.rotulo
                        elif aresta.v2.rotulo == atual:
                            vizinho = aresta.v1.rotulo
                        else:
                            continue

                        if vizinho not in cores:
                            cores[vizinho] = 1 - cores[atual]
                            fila.append(vizinho)
                        elif cores[vizinho] == cores[atual]:
                            # Vizinho com mesma cor -> não é bipartido
                            return False
        return True