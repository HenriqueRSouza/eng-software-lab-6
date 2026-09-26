"""Cenários de aceitação escritos a partir de features/mvp_livraria.feature."""

import unittest

from mvp import LivrariaApp, LivroIndisponivelError


class ComportamentoMVPTest(unittest.TestCase):
    def setUp(self):
        # Dado um catálogo, duas unidades e um exemplar disponível no Centro.
        self.app = LivrariaApp(
            livros=[
                {
                    "id": "L1", "titulo": "A Casa das Marés",
                    "autor": "L. Andrade", "genero": "Ficção",
                    "sinopse": "Uma história à beira-mar.",
                    "edicao": "Brochura", "preco": 49.90,
                },
                {
                    "id": "L2", "titulo": "Python para Todos",
                    "autor": "Ana Ribeiro", "genero": "Tecnologia",
                    "sinopse": "Introdução à programação.",
                    "edicao": "2ª edição", "preco": 79.90,
                },
            ],
            lojas=[
                {
                    "id": "CENTRO", "nome": "Livraria Centro",
                    "endereco": "Rua da Consolação, 850",
                    "horario": "10h às 20h",
                    "formas_pagamento": ["Pix", "cartão", "dinheiro"],
                },
                {
                    "id": "PINHEIROS", "nome": "Livraria Pinheiros",
                    "endereco": "Rua dos Pinheiros, 420",
                    "horario": "10h às 19h",
                    "formas_pagamento": ["Pix", "cartão"],
                },
            ],
            estoque={
                ("L1", "CENTRO"): {"quantidade": 1, "secao": "Ficção, B4"},
                ("L1", "PINHEIROS"): {"quantidade": 0, "secao": "Ficção, A2"},
            },
        )

    def test_cenario_buscar_livro_e_conferir_detalhes(self):
        # Quando pesquiso pelo nome, então encontro detalhes suficientes.
        encontrados = self.app.buscar_livros(titulo="casa das mares")
        self.assertEqual([livro["id"] for livro in encontrados], ["L1"])
        detalhe = self.app.detalhar_livro("L1")
        self.assertEqual(detalhe["sinopse"], "Uma história à beira-mar.")
        self.assertEqual(detalhe["edicao"], "Brochura")
        self.assertEqual(detalhe["preco"], 49.90)

    def test_cenario_consultar_disponibilidade_por_loja(self):
        # Quando consulto o livro, então vejo estoque e dados da visita.
        opcoes = self.app.consultar_disponibilidade("L1")
        self.assertEqual([opcao["loja_id"] for opcao in opcoes], ["CENTRO", "PINHEIROS"])
        self.assertEqual(opcoes[0]["quantidade"], 1)
        self.assertEqual(opcoes[0]["secao"], "Ficção, B4")
        self.assertEqual(opcoes[0]["endereco"], "Rua da Consolação, 850")
        self.assertEqual(opcoes[0]["horario"], "10h às 20h")
        self.assertIn("Pix", opcoes[0]["formas_pagamento"])

    def test_cenario_cadastrar_e_reservar_ultimo_exemplar(self):
        # Dado um cliente cadastrado, quando reserva, então recebe um código.
        self.app.cadastrar_cliente("Ana", "ana@example.com")
        reserva = self.app.reservar_livro("L1", "CENTRO", "ana@example.com")
        self.assertTrue(reserva["codigo"])
        self.assertEqual(reserva["prazo_horas"], 24)
        self.assertEqual(reserva["secao"], "Ficção, B4")
        self.assertEqual(self.app.consultar_reserva(reserva["codigo"]), reserva)
        self.assertEqual(
            self.app.consultar_disponibilidade("L1")[0]["quantidade"], 0
        )

    def test_cenario_impedir_reserva_sem_estoque(self):
        # Quando não há exemplar, então a reserva não altera o estoque.
        self.app.cadastrar_cliente("Ana", "ana@example.com")
        with self.assertRaises(LivroIndisponivelError):
            self.app.reservar_livro("L1", "PINHEIROS", "ana@example.com")
        self.assertEqual(
            self.app.consultar_disponibilidade("L1")[1]["quantidade"], 0
        )

    def test_cenario_nao_reservar_duas_vezes_o_ultimo_exemplar(self):
        self.app.cadastrar_cliente("Ana", "ana@example.com")
        self.app.reservar_livro("L1", "CENTRO", "ana@example.com")
        with self.assertRaises(LivroIndisponivelError):
            self.app.reservar_livro("L1", "CENTRO", "ana@example.com")


if __name__ == "__main__":
    unittest.main()
