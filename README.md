# vetinfo-ia

Serviço em Python que responde perguntas de veterinários com base em bulas
de medicamentos, sempre mostrando de onde tirou a resposta.

É o módulo de IA do VetInfo, um prontuário
veterinário com backend em Node e Express. O projeto é construído em fases,
e cada fase registra aqui as decisões tomadas e o motivo.

> **Status:** em construção. Fase 1 de 7 concluída. Ainda não há IA nem banco:
> hoje o projeto lê uma bula em texto e a divide em parágrafos.

## As três regras do projeto

1. Resposta sem fonte não existe.
2. Não achou nos documentos? Responde "não encontrei". O sistema nunca
   inventa uma resposta, muito menos uma dose.
3. O sistema mostra fatos e alertas. Quem decide é o veterinário.

## Como rodar

Requisitos: [uv](https://docs.astral.sh/uv/).

    uv sync
    uv run vetinfo-ia

## Arquitetura planejada

O VetInfo fica dividido em dois serviços que usam o mesmo Postgres:

- **vetinfo-backend** (Node, Express): o produto. Ganha uma rota que
  repassa a pergunta.
- **vetinfo-ia** (Python, FastAPI): o RAG, com arquitetura hexagonal.
  Não fica exposto na internet, só o backend fala com ele.

Dentro do vetinfo-ia, a regra de negócio não conhece banco, PDF nem modelo
de IA. Ela fala com o mundo por quatro portas, e cada porta tem um adaptador
que pode ser trocado sem mexer no resto:

| Porta | O que faz |
|---|---|
| `LeitorDocumento` | lê um documento e devolve o texto por página |
| `GeradorEmbedding` | transforma texto em vetor |
| `BuscaTrechos` | acha os trechos mais parecidos com a pergunta |
| `ModeloIA` | recebe o pedido montado e devolve a resposta |

## Roteiro

- [x] Fase 0: ambiente (uv, Python 3.14)
- [x] Fase 1: ler uma bula e dividir em parágrafos
- [ ] Fase 2: domínio com dataclasses, pytest e Ruff
- [ ] Fase 3: arquitetura hexagonal com adaptadores falsos, sem IA e sem banco
- [ ] Fase 4: importar bulas (PDF, embeddings, pgvector)
- [ ] Fase 5: responder com o Claude, via FastAPI
- [ ] Fase 6: produção, junto do vetinfo-backend

## Decisões de projeto

### Fase 1: ler uma bula e dividir em parágrafos

**Leitura, processamento e saída em funções separadas.**
`read_bula` só lê o arquivo, `split_paragraphs` só divide e limpa o texto, e
`main` junta as duas e imprime. A leitura fica isolada porque na Fase 3 ela
vira o adaptador da porta `LeitorDocumento`, e a divisão em parágrafos é o
ponto de partida do chunking da Fase 4.

**Erro tratado na borda, não na função de leitura.**
A primeira versão capturava o `FileNotFoundError` dentro do `read_bula` e
devolvia uma string vazia. O programa seguia rodando e informava que a bula
tinha 1 parágrafo com 0 caracteres, ou seja, um resultado inventado. Num
sistema que não pode inventar dose, esse é o tipo de falha que não pode
passar. Agora o `read_bula` deixa o erro subir e quem decide o que mostrar
é o `main()`. É o mesmo desenho do vetinfo-backend, onde o use case devolve
o erro e o controller decide a resposta.

## Stack

Hoje: Python 3.14 e uv.

Planejado: FastAPI, Pydantic, Postgres com pgvector, SDK da Anthropic, Docker.
