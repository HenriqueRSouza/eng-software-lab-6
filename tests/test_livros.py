import unittest

from livraria import filtrar_livros


LIVROS = [
    {"titulo": "A Casa das Marés", "autor": "L. Andrade", "genero": "Ficção",
     "preco": 49.90, "disponivel": True},
    {"titulo": "O Jardim das Possibilidades", "autor": "M. Costa",
     "genero": "Ficção", "preco": 42.90, "disponivel": False},
    {"titulo": "Python para Todos", "autor": "Ana Ribeiro",
     "genero": "Tecnologia", "preco": 79.90, "disponivel": True},
]


class FiltrarLivrosTest(unittest.TestCase):
    def test_sem_criterios_devolve_todos_em_ordem_sem_alterar_entrada(self):
        original = [livro.copy() for livro in LIVROS]
        self.assertEqual(filtrar_livros(LIVROS), LIVROS)
        self.assertIsNot(filtrar_livros(LIVROS), LIVROS)
        self.assertEqual(LIVROS, original)

    def test_pesquisa_parcial_por_titulo_ignora_maiusculas_e_acentos(self):
        self.assertEqual(filtrar_livros(LIVROS, titulo="casa das mares"), [LIVROS[0]])

    def test_filtra_por_autor_e_genero(self):
        self.assertEqual(
            filtrar_livros(LIVROS, autor="ANDRADE", genero="ficcao"), [LIVROS[0]]
        )

    def test_limites_de_preco_sao_inclusivos(self):
        self.assertEqual(
            filtrar_livros(LIVROS, preco_min=42.90, preco_max=49.90),
            LIVROS[:2],
        )

    def test_disponibilidade_falsa_e_combinada_com_genero(self):
        self.assertEqual(
            filtrar_livros(LIVROS, genero="ficção", disponivel=False), [LIVROS[1]]
        )

    def test_sem_resultado_devolve_lista_vazia(self):
        self.assertEqual(filtrar_livros(LIVROS, titulo="inexistente"), [])

    def test_intervalo_invertido_e_rejeitado(self):
        with self.assertRaises(ValueError):
            filtrar_livros(LIVROS, preco_min=100, preco_max=50)


if __name__ == "__main__":
    unittest.main()
