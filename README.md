# Módulo de Agendamento Inteligente (MVP)

Este projeto é o núcleo (Core Domain) de uma API de agendamentos para clínicas. O objetivo principal é automatizar a validação de disponibilidade médica, reduzindo o tempo de marcação e eliminando completamente os conflitos de horários.

## 🏗️ Arquitetura e Padrões de Projeto

O desenvolvimento deste módulo segue rigorosos padrões de qualidade de engenharia de software:

* **Domain-Driven Design (DDD):** Isolamento completo das regras de negócio em um modelo de domínio rico. A classe `Medico` é a guardiã de suas próprias regras (Invariantes).
* **Test-Driven Development (TDD):** Todo o código de produção foi guiado por testes automatizados, garantindo cobertura total das regras de negócio antes da implementação.
* **Design by Contract (DbC):** As interações ocorrem através de contratos estritos (Pré-condições e Pós-condições). Se um contrato for quebrado, o sistema falha rapidamente (Fail-Fast) lançando exceções de domínio específicas.

## 📂 Estrutura do Projeto

O projeto adota uma estrutura limpa, separando o código de produção do código de testes:

```text
agendamentos/
├── api/
│   ├── agendamento.py      # Domínio rico e contratos (Médico, Agendamento)
│   └── exceptions.py       # Exceções de domínio
├── tests/
│   └── test_agendamento.py # Suíte de testes unitários (Cenários de Aceitação)
├── main.py                 # Script de demonstração do sistema (MVP)
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Regras de Negócio Implementadas (Contratos)

As seguintes regras foram blindadas no domínio através de testes unitários:

*   **RF01 - Configuração de Grade:** Permite definir o horário de início, fim do turno do médico e o intervalo padrão de atendimento.
*   **RF02 - Validação de Horário (Pré-condição):** O sistema rejeita o agendamento (`ForaDoHorarioError`) se o horário solicitado estiver fora do turno de trabalho do médico.
*   **RF03 - Prevenção de Sobreposição (Pré-condição):** O sistema impede (`ConflitoHorarioError`) dois agendamentos no mesmo horário ou sobrepostos para o mesmo médico.
*   **RF04 - Duração Fixa:** Cada consulta possui uma duração padrão em minutos, parametrizável na criação do médico.

## 📝 Observações para Code Review

Esta seção detalha as escolhas arquiteturais feitas neste MVP para facilitar o processo de revisão de código:

### 1. Uso de Imutabilidade (Tuplas)
*   **Decisão:** O método `medico.agendamentos` retorna uma `tuple` em vez de uma `list`.
*   **Porquê:** Para garantir o encapsulamento. Como as tuplas são imutáveis em Python, impedimos que códigos externos modifiquem a agenda do médico (ex: `medico.agendamentos.append(...)`) sem passar pelas regras de negócio e validações do método `agendar()`.

### 2. Design by Contract (DbC)
*   **Decisão:** Uso do padrão *Fail-Fast* com exceções personalizadas (`ForaDoHorarioError`, `ConflitoHorarioError`).
*   **Porquê:** O código valida as pré-condições antes de alterar o estado do objeto. Isso garante que o sistema nunca entre em um estado inválido e fornece erros claros para as camadas superiores.

### 3. Dados Derivados
*   **Decisão:** A propriedade `fim` do agendamento não é armazenada no banco/memória, mas calculada dinamicamente.
*   **Porquê:** Evita a inconsistência de dados. Ao armazenar apenas `inicio` e `duracao`, garantimos que o horário de término seja sempre a "fonte única da verdade" baseada no intervalo de atendimento do médico.

### 4. Tipagem Estática (Type Hinting)
*   **Decisão:** Uso rigoroso de tipos em todos os métodos e atributos.
*   **Porquê:** Melhora a legibilidade, facilita o suporte de ferramentas de análise estática (como o **MyPy**) e previne erros comuns de passagem de parâmetros durante o desenvolvimento.

### 5. Separação de Exceções
*   **Decisão:** Exceções movidas para `api/exceptions.py`.
*   **Porquê:** Centralização de erros de domínio, facilitando futuras integrações com APIs (mapeamento de status HTTP) e evitando problemas de importação circular.
