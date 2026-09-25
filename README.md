# Filtro de livros da livraria

Implementação em Python de `filtrar_livros`, desenvolvida com TDD usando apenas a biblioteca padrão.

## Executar os testes

```bash
python -m unittest discover -s tests -v
```

## Exemplo

```python
from livraria import filtrar_livros

livros = [
    {"titulo": "A Casa das Marés", "autor": "L. Andrade",
     "genero": "Ficção", "preco": 49.90, "disponivel": True},
    {"titulo": "Python para Todos", "autor": "Ana Ribeiro",
     "genero": "Tecnologia", "preco": 79.90, "disponivel": False},
]

resultado = filtrar_livros(
    livros, genero="ficcao", preco_max=50, disponivel=True
)
print(resultado)  # Apenas A Casa das Marés
```

Os critérios `titulo`, `autor` e `genero` aceitam busca parcial sem distinção de maiúsculas ou acentos. `preco_min` e `preco_max` incluem os limites. Os critérios fornecidos são combinados com **E**; sem critérios, a função devolve todos os livros em uma nova lista, preservando a ordem.

## TDD

1. **Vermelho:** foram escritos sete testes antes de existir `livraria.py`; a execução falhou com `ModuleNotFoundError`.
2. **Verde:** a função foi implementada e os sete testes passaram.
3. **Refatoração:** a normalização do texto ficou em uma função auxiliar e a comparação de preços usa `Decimal`.

O histórico local separa o commit dos testes do commit da implementação.
