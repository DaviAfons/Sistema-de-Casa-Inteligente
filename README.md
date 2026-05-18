# SISTEMA DE CASA INTELIGENTE - DOCUMENTAÇÃO TÉCNICA

## 1. Visão Geral do Sistema

O **Sistema de Casa Inteligente** é uma aplicação monolítica desenvolvida em Python, baseada no paradigma de Programação Orientada a Objetos (POO). Seu objetivo principal é unificar e automatizar a gestão doméstica, oferecendo controle sobre moradores, tarefas rotineiras, inventário, manutenções preventivas e controle financeiro. A aplicação opera via interface de linha de comando (CLI) e utiliza persistência local de dados.

## 2. Autoria

Projeto desenvolvido por **Davi Afonso**, estudante universitário do curso de Sistemas de Informação na UNIUBE.

---

## 3. Estrutura e Árvore de Arquivos

O sistema está modularizado para garantir o princípio de responsabilidade única (SRP) e facilitar a manutenção estrutural do código.

```text
sistema_casa_inteligente/
│
├── Casa.py                       # Arquivo principal (Main) e orquestrador do sistema.
├── Compras.py                    # Gerenciador de listas e categorias de compras.
├── Conta.py                      # Módulo financeiro para controle de despesas e vencimentos.
├── ItemEstoque.py                # Controle de inventário, alertas de quantidade e validade.
├── Manutencao.py                 # Módulo de agendamento e periodicidade de manutenções.
├── Morador.py                    # Entidade base para gestão de usuários da residência.
├── RelatoriosEstatisticas.py     # Motor de consolidação de dados e geração de estatísticas.
├── Tarefas.py                    # Gestão de atividades recorrentes atreladas aos moradores.
├── test_casa_inteligente.py      # Suíte completa de testes automatizados (Unitários e Integração).
├── README_SISTEMA.md             # Documentação do projeto.
└── dados_casa.json               # Arquivo de persistência (Gerado automaticamente em tempo de execução).

```

---

## 4. Explicações Técnicas e Arquitetura

### 4.1 Paradigma e Design

A arquitetura baseia-se em classes independentes cujas instâncias e estados globais (listas estáticas) são orquestrados pela classe central `Casa`. Cada módulo define seus próprios métodos de validação, formatação de saída e regras de negócio.

### 4.2 Persistência de Dados e Gerenciamento Granular

O sistema abandona o uso de bancos de dados relacionais complexos em favor da persistência local em arquivos `JSON`. A serialização e desserialização ocorrem de forma centralizada na classe `Casa`. O código aplica um **gerenciamento granular** no acesso e manipulação das estruturas de dados (dicionários e listas), permitindo que a escrita no disco aconteça de forma estruturada e controlada, minimizando corrupções no estado da aplicação.

### 4.3 Gestão de Tempo e Alertas

O sistema faz uso intenso da biblioteca nativa `datetime` e do pacote `dateutil` para cálculos de relatividade temporal. Isso permite o cálculo autônomo de:

- Dias restantes para o vencimento de boletos.
- Prazos de manutenções baseados em periodicidade mensal.
- Rastreamento de itens de consumo próximos da data de validade.

---

## 5. Detalhamento dos Módulos

- **`Casa.py`:** Atua como o _Controller_ principal. Carrega os dados do `dados_casa.json` na inicialização, gerencia os submenus interativos e centraliza a rotina de salvamento global.
- **`Morador.py`:** Mantém o registro (nome, idade, quarto, telefone). Serve como entidade de relacionamento para o módulo de tarefas.
- **`Tarefas.py`:** Permite registrar atividades com recorrência (em dias) e associá-las a moradores específicos. Calcula automaticamente a próxima revisão com base na data de conclusão.
- **`Manutencao.py`:** Focado na gestão patrimonial. Avalia ativos físicos (ex: ar-condicionado, filtros) e dispara alertas quando a revisão programada expira.
- **`Compras.py` e `ItemEstoque.py`:** Trabalham em sinergia logística. O módulo de compras atua como demanda (lista de desejos financeira com preços estimados), enquanto o estoque atua como inventário real, monitorando níveis críticos (< 3 unidades) e validades.
- **`Conta.py`:** Motor financeiro simples que categoriza despesas e emite alertas de atraso cruzando a data de vencimento com a data do sistema operacional.
- **`RelatoriosEstatisticas.py`:** Agrega dados de todos os módulos para fornecer visões analíticas, cruzando gastos mensais, volume de tarefas pendentes por morador e inventário crítico, com capacidade de exportação em `.txt`.
- **`test_casa_inteligente.py`:** Suíte de testes automatizados utilizando `unittest` e `mock`. Possui um runner customizado que testa validações matemáticas, cruzamento de datas e integridade das regras de negócio.

---

## 6. Problemas e Desafios Enfrentados

Durante o ciclo de desenvolvimento e integração contínua, desafios técnicos foram identificados e mapeados pela suíte de testes automatizados (`test_casa_inteligente.py`):

1. **Incompatibilidade de Tipos no Motor de Relatórios (Bugs #1 e #2):**

- **O Problema:** Durante o desenvolvimento do módulo `RelatoriosEstatisticas.py`, o motor tentou acessar os atributos de tarefas e itens de estoque utilizando a função nativa `getattr()`. Contudo, devido à serialização em memória implementada pelo sistema principal, as tarefas e os itens de estoque estavam operando como estruturas de dicionários (dict), não como objetos instanciados tradicionais.
- **O Impacto:** O sistema de geração de relatórios falhava silenciosamente, pois o `getattr` não acessava as chaves do dicionário e retornava sistematicamente a string de fallback `"Desconhecido"`, invalidando a geração analítica de moradores com mais tarefas e itens mais comprados.
- **A Solução Técnica:** O código do relatório foi refatorado para realizar uma verificação de tipo (Type Checking) utilizando `isinstance()`. Se o elemento for um dicionário, o sistema utiliza o método estrito `.get()`; caso seja um objeto instanciado na memória durante o _runtime_, ele recua para o método `getattr()`. Isso restaurou a confiabilidade dos relatórios gerados.

2. **Manutenção de Estado Global nos Testes:**

- **O Problema:** Como a arquitetura inicializou listas estáticas dentro das classes (`Morador.moradores`, `Tarefas.tarefas`, etc.), os testes unitários sofriam de vazamento de estado (State Leak), onde um teste influenciava o resultado do outro.
- **A Solução Técnica:** Implementação rigorosa do método `limpar_estado_global()` chamado implicitamente no `setUp()` de cada classe de teste, garantindo o esvaziamento das listas antes de cada asserção de unidade.

---

## 7. Instruções de Execução

### Pré-requisitos

- Python 3.8 ou superior.
- Biblioteca externa `python-dateutil` (necessária para cálculos complexos no módulo de Manutenção).

```bash
pip install python-dateutil
```

### Executando o Sistema Principal

Para iniciar a interface de linha de comando:

```bash
python Casa.py
```

_O sistema verificará automaticamente a existência do arquivo `dados_casa.json` e o criará caso seja a primeira execução._

### Executando a Suíte de Testes

Para garantir a integridade da aplicação ou verificar novos desenvolvimentos, execute o runner customizado:

```bash
python test_casa_inteligente.py
```

Para um relatório verboso, utilize a flag `-v`:

```bash
python test_casa_inteligente.py -v
```
