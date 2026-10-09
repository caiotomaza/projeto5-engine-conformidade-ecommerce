# Projeto 5 — Engine de Conformidade Regulatória para E-Commerce e Consumidor Digital

**Equipe Granito · Projeto Integrador: Informática e Legislação · UniFAP · 2026**

## Visão geral

Este repositório contém o MVP do **Projeto 5 — Engine de Conformidade Regulatória para E-Commerce e Consumidor Digital**.

O problema do projeto é transformar requisitos regulatórios aplicáveis ao comércio eletrônico em mecanismos técnicos rastreáveis, sem confundir obrigação jurídica com decisão de engenharia. A solução é demonstrada dentro de uma loja de e-commerce de teste, mas a loja não é o artefato principal: o núcleo do projeto é a **Engine de Conformidade**.

A Engine deve apoiar a relação entre fontes, regras, aplicabilidade, controles, avaliações, evidências e revisão humana. Um teste técnico aprovado demonstra apenas o comportamento verificado naquele controle e cenário; o sistema não deve produzir uma declaração jurídica global de conformidade por meio de um simples `compliant = true`.

## Estado atual

A base arquitetural está preparada para o início do desenvolvimento funcional. O repositório contém:

- Python 3.12 e Django 5.2;
- SQLite para o MVP;
- Docker e Docker Compose;
- monólito modular com fronteiras de domínio;
- usuário Django extensível em `accounts`;
- `commerce`, `privacy` e `compliance` como contextos principais;
- domínio de `compliance` separado de detalhes de Django;
- pytest, coverage e Ruff;
- healthcheck HTTP em `/health/`;
- CI no GitHub Actions;
- documentação arquitetural, requisitos e áreas para evidências acadêmicas.

O deploy de produção e CD ainda não estão definidos. Os workflows atuais fazem **integração contínua e validação da imagem Docker**, sem publicação ou deploy automático.

## Arquitetura planejada

A arquitetura do MVP é um **monólito modular Django**. Existe um único serviço durante esta etapa, mas os limites internos foram organizados para evitar acoplamento indevido e permitir uma futura extração da Engine, caso isso seja necessário.

```text
E-Commerce demonstrativo
        │
        ├── commerce
        │   ├── catalog
        │   ├── cart
        │   ├── checkout
        │   ├── orders
        │   ├── suppliers
        │   └── returns
        │
        ├── privacy
        │   ├── domain
        │   ├── application
        │   ├── infrastructure
        │   └── interfaces
        │
        └── compliance
            ├── domain
            ├── application
            ├── infrastructure
            └── interfaces
```

### `commerce`

Representa o fluxo transacional da loja demonstrativa. Os subdomínios planejados são catálogo, carrinho, checkout, pedidos, fornecedor e arrependimento/devolução. Eles serão implementados conforme os casos de uso do MVP forem fechados.

### `privacy`

Será responsável pelos fluxos ligados a proteção de dados pessoais, como consentimentos quando aplicáveis, revogação, operações de tratamento, direitos do titular e acompanhamento de solicitações.

### `compliance`

É a fronteira da Engine. O domínio não deve depender de Django, HTTP, templates ou ORM. A integração com banco, framework e interfaces deve ficar nas camadas externas.

Conceitos previstos para evolução da Engine incluem:

```text
RegulatorySource
Rule
RuleVersion
Applicability
Control
Evaluation
Evidence
Finding
HumanReview
Retest
```

Esses conceitos serão implementados incrementalmente, conforme os fluxos reais exigirem. A arquitetura não deve criar abstrações vazias apenas para preencher a estrutura.

## Rastreabilidade

A lógica de engenharia deve preservar, sempre que aplicável:

```text
fonte
  ↓
versão
  ↓
dispositivo / seção
  ↓
regra
  ↓
aplicabilidade
  ↓
controle
  ↓
teste / avaliação
  ↓
evidência
  ↓
finding
  ↓
correção
  ↓
reteste
  ↓
revisão humana
```

Essa cadeia é uma decisão de arquitetura e governança da solução; ela não constitui, por si só, certificação jurídica.

## Estrutura do repositório

```text
.
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── docker.yml
│   └── pull_request_template.md
├── src/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── test.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── apps/
│       ├── core/
│       ├── accounts/
│       ├── commerce/
│       ├── privacy/
│       └── compliance/
├── tests/
│   ├── integration/
│   ├── functional/
│   └── e2e/
├── docs/
│   ├── architecture/
│   ├── requirements/
│   ├── evidence/
│   └── diagrams/
├── infra/
│   ├── docker/
│   └── ci/
├── scripts/
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── manage.py
├── RUNBOOK.md
└── README.md
```

## Stack

| Área | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework | Django 5.2 |
| Banco do MVP | SQLite |
| Containers | Docker + Docker Compose |
| Testes | pytest + pytest-django |
| Cobertura | coverage.py |
| Qualidade | Ruff |
| CI | GitHub Actions |

O arquivo `pyproject.toml` fixa o projeto em `Python >=3.12,<3.13`. A intenção é manter **Python 3.12 como baseline reproduzível** no desenvolvimento, Docker e CI.

## Execução rápida

Com Docker instalado:

```bash
cp .env.example .env
# No PowerShell: Copy-Item .env.example .env

docker compose up --build -d
docker compose ps
```

A aplicação deve responder em:

- `http://localhost:8000/`
- `http://localhost:8000/health/`

O healthcheck esperado é:

```json
{"status":"ok"}
```

Para desligar:

```bash
docker compose down
```

As operações completas de execução, manutenção, migrations, testes, backup, restauração e diagnóstico estão em **[RUNBOOK.md](RUNBOOK.md)**.

## Qualidade e validação

No ambiente de desenvolvimento com as dependências `dev` instaladas:

```bash
ruff check .
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
pytest
coverage run -m pytest
coverage report
```

Também existe:

```bash
./scripts/quality.sh
```

Em Windows, quando o ambiente local não possuir Python 3.12 ou as ferramentas de desenvolvimento, prefira executar as validações pelo container ou pelo CI.

## Docker

A stack possui atualmente apenas o serviço `web`. Não existe PostgreSQL, Redis, broker de mensagens ou outro serviço de infraestrutura no MVP inicial.

O entrypoint executa as migrations antes de iniciar o processo Django. O healthcheck testa `/health/` dentro do container.

## CI

O workflow `.github/workflows/ci.yml` valida a aplicação com Python 3.12, Ruff, Django checks, migrations, testes e coverage.

O workflow `.github/workflows/docker.yml` valida `docker compose config` e a construção da imagem. Nenhuma imagem é publicada e nenhum ambiente é implantado automaticamente nesta fase.

## Próximo estágio de desenvolvimento

A fundação deve permanecer estável. O próximo desenvolvimento previsto é o primeiro fluxo vertical demonstrável:

```text
Supplier
  → Product
  → Cart
  → Checkout
  → Order
  → Compliance Engine
  → Evaluation
  → Evidence
```

As primeiras regras candidatas para esse recorte são `OF-01`, `OF-02`, `CH-01` e `CH-02`, já definidas no Framework técnico-regulatório do projeto. A implementação deve manter contratos explícitos entre o domínio transacional e a Engine, em vez de permitir que `compliance` assuma a propriedade das entidades de pedido ou checkout.

## Documentação

- `docs/architecture/`: arquitetura e decisões;
- `docs/requirements/`: requisitos derivados do Framework;
- `docs/evidence/`: evidências acadêmicas versionáveis;
- `docs/diagrams/`: diagramas de arquitetura, fluxos e modelagem;
- `RUNBOOK.md`: operação e manutenção do ambiente.

## Licença

Consulte o arquivo `LICENSE`.
