# Compliance Engine

O domínio de compliance não deve depender de Django, HTTP, templates ou ORM.

Conceitos futuros: RegulatorySource, Rule, RuleVersion, Applicability, Control, Evaluation, Evidence, Finding, HumanReview e Retest.

Um teste aprovado demonstra somente o resultado daquele controle no cenário avaliado. Não existe `compliant = true` global para a organização.
