# Exercício 5 — MVP da livraria com BDD e desenvolvimento top-down

Projeto em Python que cobre a jornada mínima do cliente: buscar e avaliar um livro, consultar estoque e dados da loja, cadastrar-se e reservar um exemplar para retirada. Usa apenas a biblioteca padrão.

## Executar os testes

```bash
python -m unittest discover -s tests -v
```

## Escopo do MVP

- Busca por título, autor, gênero e faixa de preço; detalhes com sinopse, edição e preço.
- Disponibilidade por unidade, com seção, endereço, horário e formas de pagamento.
- Cadastro simples e reserva de um exemplar com código e prazo de retirada.
- Reserva recusada quando o estoque está zerado.

O serviço usa dados **em memória**: ao reiniciar, cadastros, estoque alterado e reservas voltam ao estado inicial. É uma implementação demonstrativa do comportamento, sem interface mobile, banco de dados ou controle de concorrência entre servidores.

## Exemplo do filtro

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

## BDD e top-down

Os critérios de aceitação estão em [features/mvp_livraria.feature](features/mvp_livraria.feature). Cada cenário é executado por um teste de ponta a ponta em [tests/test_comportamento_mvp.py](tests/test_comportamento_mvp.py), em formato Dado/Quando/Então. Os testes usam `unittest`, sem depender de um instalador externo de Gherkin.

O desenvolvimento foi **top-down**: os cenários exercitam primeiro as operações públicas de `LivrariaApp` (`buscar_livros`, `detalhar_livro`, `consultar_disponibilidade`, `cadastrar_cliente` e `reservar_livro`). A busca usa o método `filtrar_livros` como parte interna.

O histórico registra:

1. Testes unitários do filtro escritos antes da implementação (TDD vermelho).
2. Implementação do filtro e sete testes verdes.
3. Cenários BDD escritos antes de `mvp.py` (novo vermelho).
4. Implementação do MVP e doze testes verdes.

O comando acima executa todos os cenários de aceitação e os testes do filtro.
