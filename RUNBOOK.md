# RUNBOOK — Projeto 5

Runbook operacional da base de desenvolvimento do **Projeto 5 — Engine de Conformidade Regulatória para E-Commerce e Consumidor Digital**.

Este documento descreve como iniciar, validar, manter, diagnosticar e desligar a stack atual. Ele cobre o ambiente de desenvolvimento do MVP; não representa um procedimento de produção.

## 1. Baseline operacional

A stack atual possui um único serviço Docker:

```text
web → Python 3.12 + Django 5.2 + SQLite
```

O banco `db.sqlite3` fica na raiz do repositório durante o desenvolvimento e está ignorado pelo Git. O Docker Compose monta o repositório em `/app`, portanto alterações de código ficam disponíveis ao servidor de desenvolvimento sem reconstruir a imagem, salvo quando as dependências ou o próprio Dockerfile mudarem.

Portas padrão:

```text
Host:      8000
Container: 8000
```

Endpoints operacionais:

```text
/         aplicação
/health/  healthcheck
/admin/   Django Admin
```

## 2. Pré-requisitos

Caminho recomendado: Docker Desktop no Windows ou Docker Engine + Docker Compose em Linux.

Verifique:

```bash
docker --version
docker compose version
```

Para desenvolvimento sem Docker, use Python 3.12. O projeto não declara compatibilidade oficial com Python 3.13 ou 3.14.

## 3. Primeira inicialização

Na raiz do repositório, crie o arquivo local de ambiente.

Linux/macOS:

```bash
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

O valor de `DJANGO_SECRET_KEY` fornecido no exemplo é somente demonstrativo. Para uso local persistente, substitua-o por um valor próprio e nunca versione `.env`.

Construa e suba a stack:

```bash
docker compose up --build -d
```

Confira o estado:

```bash
docker compose ps
```

O serviço deve chegar ao estado `healthy`.

Teste:

```text
http://localhost:8000/
http://localhost:8000/health/
```

Resposta esperada do healthcheck:

```json
{"status":"ok"}
```

## 4. Operação diária

### Iniciar

Se a imagem já estiver construída:

```bash
docker compose up -d
```

### Iniciar reconstruindo a imagem

Use após mudança em `Dockerfile`, `pyproject.toml` ou dependências:

```bash
docker compose up --build -d
```

### Ver estado

```bash
docker compose ps
```

### Ver logs

```bash
docker compose logs -f web
```

Últimas 100 linhas:

```bash
docker compose logs --tail=100 web
```

### Reiniciar o serviço

```bash
docker compose restart web
```

### Parar sem remover o container

```bash
docker compose stop
```

Retomar:

```bash
docker compose start
```

### Desligar a stack

```bash
docker compose down
```

Esse comando remove containers e rede do Compose, mas **não apaga `db.sqlite3`**, pois o banco está no diretório do projeto.

Para eliminar containers órfãos eventualmente deixados por alterações no Compose:

```bash
docker compose down --remove-orphans
```

## 5. Healthcheck e diagnóstico rápido

Estado do Docker:

```bash
docker compose ps
```

Healthcheck pelo navegador:

```text
http://localhost:8000/health/
```

Ou dentro do container:

```bash
docker compose exec web /bin/sh /app/infra/docker/healthcheck.sh
```

Se estiver `unhealthy`, consulte primeiro:

```bash
docker compose logs --tail=200 web
```

Depois valide o Django:

```bash
docker compose exec web python manage.py check
```

## 6. Comandos Django no container

Abrir shell Django:

```bash
docker compose exec web python manage.py shell
```

Listar migrations:

```bash
docker compose exec web python manage.py showmigrations
```

Aplicar migrations manualmente:

```bash
docker compose exec web python manage.py migrate
```

Verificar se alterações de models exigem migration:

```bash
docker compose exec web python manage.py makemigrations --check
```

Ao desenvolver um model e realmente precisar gerar nova migration:

```bash
docker compose exec web python manage.py makemigrations
```

Sempre revise o arquivo gerado antes do commit.

Criar superusuário somente quando necessário para desenvolvimento:

```bash
docker compose exec web python manage.py createsuperuser
```

Nenhuma conta administrativa deve ser criada automaticamente ou versionada.

## 7. Qualidade, testes e coverage

A imagem de runtime instala somente as dependências necessárias para executar a aplicação. As ferramentas `pytest`, `coverage` e `ruff` pertencem ao conjunto `dev`.

Para validação completa fora do container, use Python 3.12:

```bash
python -m venv .venv
pip install -e ".[dev]"
ruff check .
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
pytest
coverage run -m pytest
coverage report
```

Ou execute:

```bash
./scripts/quality.sh
```

No Windows, se você não tiver Python 3.12 local, use o CI para a validação completa ou crie uma imagem de desenvolvimento posteriormente. Não altere o baseline do projeto apenas para acomodar uma versão diferente do Python instalada no host.

## 8. Alteração de dependências

Edite `pyproject.toml`.

Depois reconstrua:

```bash
docker compose down
docker compose build --no-cache web
docker compose up -d
```

Verifique:

```bash
docker compose exec web pip check
```

Não recrie `requirements.txt` paralelamente sem uma decisão explícita de projeto; `pyproject.toml` é a fonte de dependências.

## 9. Banco SQLite

Arquivo:

```text
db.sqlite3
```

Ele não deve ser versionado.

### Backup manual seguro

Pare a stack para obter uma cópia consistente:

```bash
docker compose down
```

Crie `backups/` e copie o banco.

PowerShell:

```powershell
New-Item -ItemType Directory -Force backups | Out-Null
Copy-Item db.sqlite3 "backups/db.sqlite3.backup"
```

Linux/macOS:

```bash
mkdir -p backups
cp db.sqlite3 backups/db.sqlite3.backup
```

Depois:

```bash
docker compose up -d
```

O diretório `backups/` é ignorado pelo Git.

### Restaurar backup

Desligue primeiro:

```bash
docker compose down
```

PowerShell:

```powershell
Copy-Item backups/db.sqlite3.backup db.sqlite3 -Force
```

Linux/macOS:

```bash
cp backups/db.sqlite3.backup db.sqlite3
```

Suba e valide:

```bash
docker compose up -d
docker compose exec web python manage.py check
docker compose exec web python manage.py showmigrations
```

### Reset completo do banco de desenvolvimento

Use apenas quando você realmente quiser perder os dados locais.

```bash
docker compose down
```

PowerShell:

```powershell
Remove-Item db.sqlite3 -ErrorAction SilentlyContinue
```

Linux/macOS:

```bash
rm -f db.sqlite3
```

Depois:

```bash
docker compose up -d
```

O entrypoint recriará o banco aplicando as migrations.

## 10. Atualizar o repositório local

Antes de atualizar, confirme que suas alterações estão commitadas ou armazenadas.

```bash
git status
git pull
```

Se houve alteração apenas no código Python/templates/static, normalmente basta:

```bash
docker compose up -d
```

Se houve mudança em `pyproject.toml`, `Dockerfile` ou infraestrutura de build:

```bash
docker compose up --build -d
```

Depois:

```bash
docker compose ps
docker compose logs --tail=100 web
```

## 11. Problemas comuns

### Porta 8000 já em uso

Altere `DJANGO_PORT` no `.env`, por exemplo:

```text
DJANGO_PORT=8001
```

Recrie o serviço:

```bash
docker compose down
docker compose up -d
```

Acesse `http://localhost:8001/`.

### `DJANGO_SECRET_KEY must be defined`

Isso ocorre quando Django é executado diretamente no host sem a variável de ambiente. Crie `.env` para Docker ou exporte a variável no ambiente local antes de executar `manage.py`.

PowerShell:

```powershell
$env:DJANGO_SECRET_KEY="chave-local-de-desenvolvimento"
```

Linux/macOS:

```bash
export DJANGO_SECRET_KEY="chave-local-de-desenvolvimento"
```

### Mudança de model sem migration

Verifique:

```bash
docker compose exec web python manage.py makemigrations --check
```

Se a alteração foi intencional, gere e revise a migration antes de commitá-la.

### Container inicia e cai

```bash
docker compose ps -a
docker compose logs --tail=200 web
```

Como o entrypoint executa migrations antes do servidor, erros de migration também aparecem nesse log.

### Container permanece `unhealthy`

Valide:

```bash
docker compose exec web python manage.py check
docker compose exec web /bin/sh /app/infra/docker/healthcheck.sh
```

### Alteração de dependência não aparece no container

Reconstrua a imagem:

```bash
docker compose build --no-cache web
docker compose up -d
```

### Scripts `.sh` com erro de `CRLF`

O repositório contém `.gitattributes` forçando `LF` para scripts e arquivos de configuração. Em uma cópia antiga, normalize o Git e faça checkout novamente dos scripts antes de alterar a arquitetura para contornar o problema.

## 12. Limpeza segura do Docker

Ver imagens do projeto:

```bash
docker compose images
```

Remover a stack:

```bash
docker compose down --remove-orphans
```

Remover apenas imagens não utilizadas pelo Docker em geral:

```bash
docker image prune
```

Não use `docker system prune -a` como rotina do projeto; esse comando pode remover imagens, redes e caches utilizados por outros ambientes.

## 13. CI no GitHub

`ci.yml` executa:

```text
Python 3.12
→ instalação das dependências dev
→ Ruff
→ Django check
→ makemigrations --check
→ migrate
→ pytest
→ coverage
```

`docker.yml` executa:

```text
docker compose config
→ docker compose build
```

Falha do CI deve ser tratada antes do merge. Atualmente não existe CD/deploy automático.

## 14. Procedimento antes de commit/push

Verifique o estado:

```bash
git status
```

Execute, quando disponível:

```bash
ruff check .
python manage.py check
python manage.py makemigrations --check
pytest
```

Para mudanças que afetam Docker:

```bash
docker compose config
docker compose build
```

Não versione:

```text
.env
db.sqlite3
backups/
coverage local
caches
segredos
```

Migrations válidas e intencionais devem ser versionadas.

## 15. Encerramento seguro de uma sessão de desenvolvimento

Confira alterações pendentes:

```bash
git status
```

Se precisar preservar o banco, faça backup antes de operações destrutivas.

Desligue:

```bash
docker compose down
```

Confirme:

```bash
docker compose ps
```

Nenhum serviço do projeto deve permanecer ativo.

## 16. Regra operacional da arquitetura

Durante manutenção ou desenvolvimento, não mova responsabilidade de negócio para `compliance` apenas por ela estar relacionada a conformidade.

Pedido pertence a `commerce/orders`; checkout pertence a `commerce/checkout`; consentimentos e solicitações de titulares pertencem a `privacy`. A Engine deve receber contexto por contratos explícitos, avaliar regras, produzir avaliações/evidências e encaminhar revisão quando necessário.

Se uma alteração exigir quebra dessas fronteiras, registre e discuta a decisão arquitetural antes de implementá-la.
