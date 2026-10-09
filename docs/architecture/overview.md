# Visão Geral da Arquitetura

O MVP adota **monólito modular em Django**. A loja de e-commerce é o ambiente demonstrativo e a Engine de Conformidade é o artefato central.

Grandes contextos: `commerce`, `privacy` e `compliance`.

A aplicação possui um único deploy nesta etapa. A Engine deve permanecer suficientemente desacoplada para futura extração, se isso vier a ser necessário.
