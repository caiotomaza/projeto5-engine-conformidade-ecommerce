# ADR-001 — Monólito modular no MVP

## Status
Aceito.

## Contexto
Equipe pequena, prazo acadêmico e necessidade de demonstração, testes e evidências.

## Decisão
Usar um único projeto Django organizado como monólito modular, com fronteira forte da Engine.

## Alternativas consideradas
Microserviços desde o início; monólito sem fronteiras; arquitetura distribuída com mensageria.

## Consequências
Menor complexidade operacional, testes e demonstração mais simples, mantendo possibilidade de extração futura da Engine.
