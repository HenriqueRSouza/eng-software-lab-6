# Critérios de aceitação do MVP, escritos antes da implementação.
Funcionalidade: Encontrar e reservar um livro para retirada
  Como cliente da livraria
  Quero encontrar um exemplar disponível e reservá-lo
  Para evitar uma viagem desnecessária

  Cenário: Buscar um livro e conferir seus detalhes
    Dado que existem livros cadastrados no catálogo
    Quando pesquiso pelo nome "casa das mares"
    Então encontro "A Casa das Marés"
    E vejo sinopse, edição e preço

  Cenário: Escolher uma loja com estoque
    Dado que "A Casa das Marés" está disponível na loja Centro
    Quando consulto a disponibilidade do livro
    Então vejo a quantidade, seção, endereço, horário e formas de pagamento

  Cenário: Reservar o último exemplar disponível
    Dado que tenho uma conta cadastrada
    E resta um exemplar de "A Casa das Marés" na loja Centro
    Quando reservo esse livro para retirada
    Então recebo um código e o prazo da reserva
    E o estoque da loja é reduzido a zero

  Cenário: Impedir reserva de livro indisponível
    Dado que não há exemplares na loja escolhida
    Quando tento reservar o livro
    Então a reserva é recusada sem alterar o estoque
