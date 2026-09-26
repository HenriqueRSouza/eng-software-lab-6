"""Jornada mínima da livraria: busca, detalhes, estoque e reserva."""

from copy import deepcopy

from livraria import filtrar_livros


class LivroIndisponivelError(ValueError):
    """Não há exemplar para reservar na unidade escolhida."""


class LivrariaApp:
    """Serviço em memória para demonstrar o MVP e seus comportamentos."""

    def __init__(self, livros, lojas, estoque):
        self._livros = {livro["id"]: deepcopy(livro) for livro in livros}
        self._lojas = {loja["id"]: deepcopy(loja) for loja in lojas}
        self._estoque = deepcopy(estoque)
        self._clientes = {}
        self._reservas = {}

    def buscar_livros(self, **criterios):
        """Pesquisa o catálogo pelos critérios aceitos por filtrar_livros."""
        return deepcopy(filtrar_livros(self._livros.values(), **criterios))

    def detalhar_livro(self, livro_id):
        """Exibe sinopse, edição e preço do livro."""
        return deepcopy(self._livros[livro_id])

    def consultar_disponibilidade(self, livro_id):
        """Exibe cada unidade e as informações necessárias para a visita."""
        if livro_id not in self._livros:
            raise KeyError(f"Livro não encontrado: {livro_id}")
        opcoes = []
        for loja in self._lojas.values():
            registro = self._estoque.get((livro_id, loja["id"]), {})
            opcoes.append(
                {
                    "loja_id": loja["id"],
                    "nome": loja["nome"],
                    "endereco": loja["endereco"],
                    "horario": loja["horario"],
                    "formas_pagamento": list(loja["formas_pagamento"]),
                    "quantidade": registro.get("quantidade", 0),
                    "secao": registro.get("secao"),
                }
            )
        return opcoes

    def cadastrar_cliente(self, nome, email):
        """Registra os dados mínimos para identificar uma reserva."""
        nome, email = nome.strip(), email.strip().casefold()
        if not nome or "@" not in email:
            raise ValueError("Informe nome e e-mail válidos")
        if email in self._clientes:
            raise ValueError("E-mail já cadastrado")
        self._clientes[email] = nome
        return {"nome": nome, "email": email}

    def reservar_livro(self, livro_id, loja_id, email):
        """Separa um exemplar e devolve o código para retirada em 24 horas."""
        email = email.strip().casefold()
        if email not in self._clientes:
            raise ValueError("Cadastre-se antes de reservar")
        if livro_id not in self._livros or loja_id not in self._lojas:
            raise KeyError("Livro ou loja não encontrado")
        registro = self._estoque.get((livro_id, loja_id))
        if registro is None or registro["quantidade"] < 1:
            raise LivroIndisponivelError("Livro indisponível nesta loja")

        registro["quantidade"] -= 1
        codigo = f"LIV-{len(self._reservas) + 1:04d}"
        reserva = {
            "codigo": codigo,
            "livro_id": livro_id,
            "loja_id": loja_id,
            "email": email,
            "secao": registro.get("secao"),
            "prazo_horas": 24,
        }
        self._reservas[codigo] = reserva
        return deepcopy(reserva)

    def consultar_reserva(self, codigo):
        """Recupera os dados que o cliente apresenta na retirada."""
        return deepcopy(self._reservas[codigo])
