import unittest
from meu_grafo_lista_adj_nao_dir import *
import gerar_grafos_teste
from bibgrafo.aresta import Aresta
from bibgrafo.vertice import Vertice
from bibgrafo.grafo_errors import *
from bibgrafo.grafo_json import GrafoJSON
from bibgrafo.grafo_builder import GrafoBuilder


class TestGrafo(unittest.TestCase):

    def setUp(self):
        # Grafo da Paraíba
        self.g_p = GrafoJSON.json_to_grafo('test_json/grafo_pb.json', MeuGrafo())

        # Clone do Grafo da Paraíba para ver se o método equals está funcionando
        self.g_p2 = GrafoJSON.json_to_grafo('test_json/grafo_pb2.json', MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o método equals está funcionando
        # Esse tem um pequena diferença na primeira aresta
        self.g_p3 = GrafoJSON.json_to_grafo('test_json/grafo_pb3.json', MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o método equals está funcionando
        # Esse tem um pequena diferença na segunda aresta
        self.g_p4 = GrafoJSON.json_to_grafo('test_json/grafo_pb4.json', MeuGrafo())

        # Grafo da Paraíba sem arestas paralelas
        self.g_p_sem_paralelas = MeuGrafo()
        self.g_p_sem_paralelas.adiciona_vertice("J")
        self.g_p_sem_paralelas.adiciona_vertice("C")
        self.g_p_sem_paralelas.adiciona_vertice("E")
        self.g_p_sem_paralelas.adiciona_vertice("P")
        self.g_p_sem_paralelas.adiciona_vertice("M")
        self.g_p_sem_paralelas.adiciona_vertice("T")
        self.g_p_sem_paralelas.adiciona_vertice("Z")
        self.g_p_sem_paralelas.adiciona_aresta('a1', 'J', 'C')
        self.g_p_sem_paralelas.adiciona_aresta('a2', 'C', 'E')
        self.g_p_sem_paralelas.adiciona_aresta('a3', 'P', 'C')
        self.g_p_sem_paralelas.adiciona_aresta('a4', 'T', 'C')
        self.g_p_sem_paralelas.adiciona_aresta('a5', 'M', 'C')
        self.g_p_sem_paralelas.adiciona_aresta('a6', 'M', 'T')
        self.g_p_sem_paralelas.adiciona_aresta('a7', 'T', 'Z')

        # Grafos completos
        self.g_c = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices(['J', 'C', 'E', 'P']).arestas(True).build()

        self.g_c2 = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices(3).arestas(True).build()

        self.g_c3 = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices(1).build()

        # Grafos com laco
        self.g_l1 = GrafoJSON.json_to_grafo('test_json/grafo_l1.json', MeuGrafo())

        self.g_l2 = GrafoJSON.json_to_grafo('test_json/grafo_l2.json', MeuGrafo())

        self.g_l3 = GrafoJSON.json_to_grafo('test_json/grafo_l3.json', MeuGrafo())

        self.g_l4 = GrafoBuilder().tipo(MeuGrafo()).vertices([v:=Vertice('D')]) \
            .arestas([Aresta('a1', v, v)]).build()

        self.g_l5 = GrafoBuilder().tipo(MeuGrafo()).vertices(3) \
            .arestas(3, lacos=1).build()

        # Grafos desconexos
        self.g_d = GrafoBuilder().tipo(MeuGrafo()) \
            .vertices([a:=Vertice('A'), b:=Vertice('B'), Vertice('C'), Vertice('D')]) \
            .arestas([Aresta('asd', a, b)]).build()

        self.g_d2 = GrafoBuilder().tipo(MeuGrafo()).vertices(4).build()

        # Grafo p\teste de remoção em casta
        self.g_r = GrafoBuilder().tipo(MeuGrafo()).vertices(2).arestas(1).build()


        # Árvore DFS do grafo da Paraíba
        self.g_p_dfs = MeuGrafo()
        self.g_p_dfs.adiciona_vertice("J")
        self.g_p_dfs.adiciona_vertice("C")
        self.g_p_dfs.adiciona_aresta("a1", "J", "C")
        self.g_p_dfs.adiciona_aresta("a2", "J", "C")


    def test_adiciona_aresta(self):
        self.assertTrue(self.g_p.adiciona_aresta('a10', 'J', 'C'))
        a = Aresta("zxc", self.g_p.get_vertice("C"), self.g_p.get_vertice("Z"))
        self.assertTrue(self.g_p.adiciona_aresta(a))
        with self.assertRaises(ArestaInvalidaError):
            self.assertTrue(self.g_p.adiciona_aresta(a))
        with self.assertRaises(VerticeInvalidoError):
            self.assertTrue(self.g_p.adiciona_aresta('b1', '', 'C'))
        with self.assertRaises(VerticeInvalidoError):
            self.assertTrue(self.g_p.adiciona_aresta('b1', 'A', 'C'))
        with self.assertRaises(TypeError):
            self.g_p.adiciona_aresta('')
        with self.assertRaises(TypeError):
            self.g_p.adiciona_aresta('aa-bb')
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.adiciona_aresta('x', 'J', 'V')
        with self.assertRaises(ArestaInvalidaError):
            self.g_p.adiciona_aresta('a1', 'J', 'C')

    def test_remove_vertice(self):
        self.assertIsNone(self.g_r.remove_vertice('A'))
        self.assertFalse(self.g_r.existe_rotulo_vertice('A'))
        self.assertFalse(self.g_r.existe_rotulo_aresta('1'))
        with self.assertRaises(VerticeInvalidoError):
            self.g_r.get_vertice('A')
        self.assertFalse(self.g_r.get_aresta('1'))
        self.assertEqual(self.g_r.arestas_sobre_vertice('B'), set())

    def test_eq(self):
        self.assertEqual(self.g_p, self.g_p2)
        self.assertNotEqual(self.g_p, self.g_p3)
        self.assertNotEqual(self.g_p, self.g_p_sem_paralelas)
        self.assertNotEqual(self.g_p, self.g_p4)

    def test_vertices_nao_adjacentes(self):
        self.assertEqual(self.g_p.vertices_nao_adjacentes(),
                         {'J-E', 'J-P', 'J-M', 'J-T', 'J-Z', 'C-Z', 'E-P', 'E-M', 'E-T', 'E-Z', 'P-M', 'P-T', 'P-Z',
                          'M-Z'})
        self.assertEqual(self.g_d.vertices_nao_adjacentes(), {'A-C', 'A-D', 'B-C', 'B-D', 'C-D'})
        self.assertEqual(self.g_d2.vertices_nao_adjacentes(), {'A-B', 'A-C', 'A-D', 'B-C', 'B-D', 'C-D'})
        self.assertEqual(self.g_c.vertices_nao_adjacentes(), set())
        self.assertEqual(self.g_c3.vertices_nao_adjacentes(), set())

    def test_ha_laco(self):
        self.assertFalse(self.g_p.ha_laco())
        self.assertFalse(self.g_p2.ha_laco())
        self.assertFalse(self.g_p3.ha_laco())
        self.assertFalse(self.g_p4.ha_laco())
        self.assertFalse(self.g_p_sem_paralelas.ha_laco())
        self.assertFalse(self.g_d.ha_laco())
        self.assertFalse(self.g_c.ha_laco())
        self.assertFalse(self.g_c2.ha_laco())
        self.assertFalse(self.g_c3.ha_laco())
        self.assertTrue(self.g_l1.ha_laco())
        self.assertTrue(self.g_l2.ha_laco())
        self.assertTrue(self.g_l3.ha_laco())
        self.assertTrue(self.g_l4.ha_laco())
        self.assertTrue(self.g_l5.ha_laco())

    def test_grau(self):
        # Paraíba
        self.assertEqual(self.g_p, self.g_p2)

        self.assertEqual(self.g_p.grau('J'), 1)
        self.assertEqual(self.g_p.grau('C'), 7)
        self.assertEqual(self.g_p.grau('E'), 2)
        self.assertEqual(self.g_p.grau('P'), 2)
        self.assertEqual(self.g_p.grau('M'), 2)
        self.assertEqual(self.g_p.grau('T'), 3)
        self.assertEqual(self.g_p.grau('Z'), 1)
        with self.assertRaises(VerticeInvalidoError):
            self.assertEqual(self.g_p.grau('G'), 5)

        self.assertEqual(self.g_d.grau('A'), 1)
        self.assertEqual(self.g_d.grau('C'), 0)
        self.assertNotEqual(self.g_d.grau('D'), 2)
        self.assertEqual(self.g_d2.grau('A'), 0)

        # Completos
        self.assertEqual(self.g_c.grau('J'), 3)
        self.assertEqual(self.g_c.grau('C'), 3)
        self.assertEqual(self.g_c.grau('E'), 3)
        self.assertEqual(self.g_c.grau('P'), 3)

        # Com laço. Lembrando que cada laço conta 2 vezes por vértice para cálculo do grau
        self.assertEqual(self.g_l1.grau('A'), 5)
        self.assertEqual(self.g_l2.grau('B'), 4)
        self.assertEqual(self.g_l4.grau('D'), 2)

    def test_ha_paralelas(self):
        self.assertTrue(self.g_p.ha_paralelas())
        self.assertFalse(self.g_p_sem_paralelas.ha_paralelas())
        self.assertFalse(self.g_c.ha_paralelas())
        self.assertFalse(self.g_c2.ha_paralelas())
        self.assertFalse(self.g_c3.ha_paralelas())
        self.assertTrue(self.g_l1.ha_paralelas())

    def test_arestas_sobre_vertice(self):
        self.assertEqual(self.g_p.arestas_sobre_vertice('J'), {'a1'})
        self.assertEqual(self.g_p.arestas_sobre_vertice('C'), {'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'})
        self.assertEqual(self.g_p.arestas_sobre_vertice('M'), {'a7', 'a8'})
        self.assertEqual(self.g_l2.arestas_sobre_vertice('B'), {'a1', 'a2', 'a3'})
        self.assertEqual(self.g_d.arestas_sobre_vertice('C'), set())
        self.assertEqual(self.g_d.arestas_sobre_vertice('A'), {'asd'})
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.arestas_sobre_vertice('A')

    def test_eh_completo(self):
        self.assertFalse(self.g_p.eh_completo())
        self.assertFalse((self.g_p_sem_paralelas.eh_completo()))
        self.assertTrue((self.g_c.eh_completo()))
        self.assertTrue((self.g_c2.eh_completo()))
        self.assertTrue((self.g_c3.eh_completo()))
        self.assertFalse((self.g_l1.eh_completo()))
        self.assertFalse((self.g_l2.eh_completo()))
        self.assertFalse((self.g_l3.eh_completo()))
        self.assertFalse(self.g_l4.eh_completo())
        self.assertFalse(self.g_l5.eh_completo())
        self.assertFalse(self.g_d.eh_completo())
        self.assertFalse(self.g_d2.eh_completo())
        self.assertTrue(self.g_p_dfs.eh_completo())

    def test_dfs(self):
        dfs_resultado = self.g_p.dfs('J')
        esperado = MeuGrafo()
        esperado.adiciona_vertice("J")    
        esperado.adiciona_vertice("C")   
        esperado.adiciona_vertice("E")   
        esperado.adiciona_vertice("P")   
        esperado.adiciona_vertice("M")   
        esperado.adiciona_vertice("T")   
        esperado.adiciona_vertice("Z")   
        esperado.adiciona_aresta('a1', 'J', 'C')
        esperado.adiciona_aresta('a2', 'C', 'E')
        esperado.adiciona_aresta('a3', 'C', 'P')
        esperado.adiciona_aresta('a4', 'C', 'M')
        esperado.adiciona_aresta('a5', 'M', 'T')
        esperado.adiciona_aresta('a6', 'T', 'Z')

        # Obter as arestas como frozenset para comparar como conjunto (sem ordem)
        arestas_dfs = set(frozenset([a.v1.rotulo, a.v2.rotulo]) for a in dfs_resultado.arestas.values())
        arestas_esperadas = set(frozenset([a.v1.rotulo, a.v2.rotulo]) for a in esperado.arestas.values())
        
        self.assertEqual(
            set(v.rotulo for v in dfs_resultado.vertices),
            set(v.rotulo for v in esperado.vertices)
        )
        self.assertEqual(arestas_dfs, arestas_esperadas)

        grafo = MeuGrafo()
        grafo.adiciona_vertice('A')
        grafo.adiciona_vertice('B')
        grafo.adiciona_vertice('C')  # Desconexo
        grafo.adiciona_aresta('a1', 'A', 'B')

        resultado = grafo.dfs('A')
        visitados = set(v.rotulo for v in resultado.vertices)

        self.assertIn('A', visitados)
        self.assertIn('B', visitados)
        self.assertNotIn('C', visitados)


    def test_bfs(self):
        bfs_resultado = self.g_p.bfs('J')
        esperado = MeuGrafo()
        esperado.adiciona_vertice("J")    
        esperado.adiciona_vertice("C")   
        esperado.adiciona_vertice("E")   
        esperado.adiciona_vertice("P")   
        esperado.adiciona_vertice("M")   
        esperado.adiciona_vertice("T")   
        esperado.adiciona_vertice("Z")   
        esperado.adiciona_aresta('a1', 'J', 'C')
        esperado.adiciona_aresta('a2', 'C', 'E')
        esperado.adiciona_aresta('a4', 'C', 'P')
        esperado.adiciona_aresta('a7', 'C', 'M')
        esperado.adiciona_aresta('a6', 'C', 'T')  
        esperado.adiciona_aresta('a9', 'T', 'Z')
        arestas_bfs = set(frozenset([a.v1.rotulo, a.v2.rotulo]) for a in bfs_resultado.arestas.values())
        arestas_esperadas = set(frozenset([a.v1.rotulo, a.v2.rotulo]) for a in esperado.arestas.values())
        
        self.assertEqual(
            set(v.rotulo for v in bfs_resultado.vertices),
            set(v.rotulo for v in esperado.vertices)
        )
        self.assertEqual(arestas_bfs, arestas_esperadas)

        grafo = MeuGrafo()
        grafo.adiciona_vertice('X')
        grafo.adiciona_vertice('Y')
        grafo.adiciona_vertice('Z')  # Desconexo
        grafo.adiciona_aresta('a1', 'X', 'Y')
        resultado = grafo.bfs('X')
        visitados = set(v.rotulo for v in resultado.vertices)

        self.assertIn('X', visitados)
        self.assertIn('Y', visitados)
        self.assertNotIn('Z', visitados)


    def test_ha_ciclo(self):
        grafo_com_ciclo = MeuGrafo()
        grafo_com_ciclo.adiciona_vertice('A')
        grafo_com_ciclo.adiciona_vertice('B')
        grafo_com_ciclo.adiciona_vertice('C')
        grafo_com_ciclo.adiciona_aresta('a1', 'A', 'B')
        grafo_com_ciclo.adiciona_aresta('a2', 'B', 'C')
        grafo_com_ciclo.adiciona_aresta('a3', 'C', 'A')  # Forma ciclo A-B-C-A

        grafo_sem_ciclo = MeuGrafo()
        grafo_sem_ciclo.adiciona_vertice('A')
        grafo_sem_ciclo.adiciona_vertice('B')
        grafo_sem_ciclo.adiciona_vertice('C')
        grafo_sem_ciclo.adiciona_aresta('a1', 'A', 'B')
        grafo_sem_ciclo.adiciona_aresta('a2', 'B', 'C')

        self.assertTrue(grafo_com_ciclo.ha_ciclo())
        self.assertFalse(grafo_sem_ciclo.ha_ciclo())

        grafo = MeuGrafo()
        grafo.adiciona_vertice('A')
        grafo.adiciona_vertice('B')
        grafo.adiciona_vertice('C')
        grafo.adiciona_vertice('D')
        grafo.adiciona_aresta('a1', 'A', 'B')
        grafo.adiciona_aresta('a2', 'B', 'C')
        grafo.adiciona_aresta('a3', 'C', 'A')  # ciclo
        grafo.adiciona_vertice('E')  # componente desconexo

        self.assertTrue(grafo.ha_ciclo())


    def test_eh_arvore(self):
        grafo_arvore = MeuGrafo()
        grafo_arvore.adiciona_vertice('A')
        grafo_arvore.adiciona_vertice('B')
        grafo_arvore.adiciona_vertice('C')
        grafo_arvore.adiciona_aresta('a1', 'A', 'B')
        grafo_arvore.adiciona_aresta('a2', 'A', 'C')

        grafo_com_ciclo = MeuGrafo()
        grafo_com_ciclo.adiciona_vertice('A')
        grafo_com_ciclo.adiciona_vertice('B')
        grafo_com_ciclo.adiciona_vertice('C')
        grafo_com_ciclo.adiciona_aresta('a1', 'A', 'B')
        grafo_com_ciclo.adiciona_aresta('a2', 'B', 'C')
        grafo_com_ciclo.adiciona_aresta('a3', 'C', 'A')  # ciclo

        self.assertEqual(set(grafo_arvore.eh_arvore()), {'B', 'C'})  # folhas
        self.assertFalse(grafo_com_ciclo.eh_arvore())

        grafo = MeuGrafo()
        self.assertFalse(grafo.eh_arvore())  # Grafo vazio não é árvore

        grafo = MeuGrafo()
        grafo.adiciona_vertice('A')
        grafo.adiciona_vertice('B')  # Sem aresta

        self.assertFalse(grafo.eh_arvore())


    def test_eh_bipartido(self):
        grafo_bipartido = MeuGrafo()
        grafo_bipartido.adiciona_vertice('1')
        grafo_bipartido.adiciona_vertice('2')
        grafo_bipartido.adiciona_vertice('3')
        grafo_bipartido.adiciona_vertice('4')
        grafo_bipartido.adiciona_aresta('a1', '1', '2')
        grafo_bipartido.adiciona_aresta('a2', '2', '3')
        grafo_bipartido.adiciona_aresta('a3', '3', '4')

        grafo_nao_bipartido = MeuGrafo()
        grafo_nao_bipartido.adiciona_vertice('A')
        grafo_nao_bipartido.adiciona_vertice('B')
        grafo_nao_bipartido.adiciona_vertice('C')
        grafo_nao_bipartido.adiciona_aresta('a1', 'A', 'B')
        grafo_nao_bipartido.adiciona_aresta('a2', 'B', 'C')
        grafo_nao_bipartido.adiciona_aresta('a3', 'C', 'A')  # ciclo ímpar (3 vértices)

        self.assertTrue(grafo_bipartido.eh_bipartido())
        self.assertFalse(grafo_nao_bipartido.eh_bipartido())

        grafo = MeuGrafo()
        grafo.adiciona_vertice('A')
        grafo.adiciona_vertice('B')
        grafo.adiciona_vertice('C')
        grafo.adiciona_vertice('D')
        grafo.adiciona_aresta('a1', 'A', 'B')
        grafo.adiciona_aresta('a2', 'B', 'C')
        grafo.adiciona_aresta('a3', 'C', 'D')
        grafo.adiciona_aresta('a4', 'D', 'A')  # ciclo par (4 vértices)

        self.assertTrue(grafo.eh_bipartido())
        grafo = MeuGrafo()
        self.assertTrue(grafo.eh_bipartido())  # Grafo vazio é bipartido por definição
