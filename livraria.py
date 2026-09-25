"""Busca simples no catálogo de uma livraria."""

import unicodedata
from collections.abc import Iterable, Mapping
from decimal import Decimal
from typing import Any


def _texto_normalizado(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor)).casefold()
    return "".join(letra for letra in texto if not unicodedata.combining(letra))


def filtrar_livros(
    livros: Iterable[Mapping[str, Any]],
    *,
    titulo: str | None = None,
    autor: str | None = None,
    genero: str | None = None,
    preco_min: int | float | Decimal | None = None,
    preco_max: int | float | Decimal | None = None,
    disponivel: bool | None = None,
) -> list[Mapping[str, Any]]:
    """Devolve livros que atendem a todos os critérios informados.

    Os filtros de texto aceitam trechos e ignoram maiúsculas e acentos.
    Os limites de preço são inclusivos. A ordem original é preservada.
    """
    minimo = Decimal(str(preco_min)) if preco_min is not None else None
    maximo = Decimal(str(preco_max)) if preco_max is not None else None
    if minimo is not None and maximo is not None and minimo > maximo:
        raise ValueError("preco_min não pode ser maior que preco_max")

    resultado = []
    for livro in livros:
        if any(
            _texto_normalizado(termo) not in _texto_normalizado(livro.get(campo, ""))
            for campo, termo in (("titulo", titulo), ("autor", autor), ("genero", genero))
            if termo is not None
        ):
            continue

        if minimo is not None or maximo is not None:
            if "preco" not in livro:
                continue
            preco = Decimal(str(livro["preco"]))
            if (minimo is not None and preco < minimo) or (
                maximo is not None and preco > maximo
            ):
                continue

        if disponivel is not None and livro.get("disponivel") is not disponivel:
            continue

        resultado.append(livro)

    return resultado
