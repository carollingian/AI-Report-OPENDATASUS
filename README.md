# AI-Report-OPENDATASUS

## Visão Geral

Este projeto automatiza a coleta, tratamento e análise de dados públicos do
OPENDATASUS, utilizando um pipeline de dados, notícias atuais e agente IA para gerar um 
relatório em PDF (e Markdown) sobre a Síndrome Respiratória Aguda Grave no Brasil.

---

# Getting Started

## Variáveis de Ambiente

Antes de executar o projeto, certifique-se de obter e configurar as seguintes **variáveis de ambiente pessoais**:

* **GROQ API KEY**
  Disponível em: [https://console.groq.com/home](https://console.groq.com/home)

* **NEWS API KEY**
  Disponível em: [https://newsapi.org](https://newsapi.org)

> **Importante:** crie um arquivo `.env` e preencha as variáveis exemplificadas em `.env.example`.

Exemplo:

```bash
export GROQ_API_KEY="sua_chave_aqui"
export NEWS_API_KEY="sua_chave_aqui"
```

---

## Requisitos do Sistema

Certifique-se de que os seguintes requisitos estejam instalados no sistema:

* Python **3.12**
* pip
* git
* pandoc
* texlive-xetex

### Instalação do pandoc e texlive-xetex

Execute os comandos abaixo em sistemas baseados em Debian/Ubuntu:

```bash
sudo apt update
sudo apt install pandoc texlive-xetex
```

---

## Configuração do Ambiente Virtual

Este projeto utiliza **Virtual Environment** para isolar as dependências.

### 1. Instalar suporte a venv

```bash
sudo apt install python3.12-venv
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

```bash
source venv/bin/activate
```

Após a ativação, seu terminal indicará que o ambiente virtual está ativo.

---

## Instalação das Dependências

Com o ambiente virtual ativado, instale os pacotes necessários executando:

```bash
pip install -r requirements.txt
```

---

## Execução do projeto

Após seguir os passos anteriores, já é possível executar o agente com o seguinte comando:

```bash
python3 main.py
```
A execução resultará na geração do relatório automatizado, localizado em **report/final_report.pdf**.

---

## Arquitetura

O projeto é dividido em três atividades principais:

- **Pipeline de Dados**: faz download, limpeza e processamento dos dados brutos.
- **Agentes de IA**: por meio de tools, gera métricas e gráficos baseados nos dados 
processados e interpreta-os junto a notícias externas e atuais.
- **Geração de Relatório**: consolida os resultados em Markdown e converte para PDF.

![Diagrama da Arquitetura](architecture_diagram.pdf)

# Agente de IA

O sistema utiliza dois componentes de IA com papéis distintos:

### Reader Agent
- Calcular métricas estatísticas a partir do dataset processado
- Gerar dados para visualização
- Buscar notícias recentes relacionadas ao tema

> Importante: o agente **não acessa dados brutos, não manipula dataset** e não realiza tarefas de ETL.

### Writer Chain
- Consolidar os dados fornecidos pelo Reader Agent
- Gerar um relatório final estruturado em Markdown
- Não realizar inferências externas ou coleta adicional

## Tools
O agente não possui acesso direto aos dados brutos nem executa
operações computacionais complexas. As ações de processamento,
cálculo ou acesso externo é realizada por meio das tools. São três:

### Rates Tool (Calcular Métricas Epidemiológicas)

Responsável por calcular métricas quantitativas a partir do dataset
processado, sendo:

- Taxa de aumento de casos
- Taxa de mortalidade
- Taxa de ocupação de UTI
- Taxa de vacinação

**Entradas**:
- Dataset OPENDATASUS processado

**Saídas**:
- Estrutura de dados contendo métricas numéricas prontas para análise

Essa tool garante que todas as métricas apresentadas no relatório sejam
determinísticas e baseadas exclusivamente em dados reais.

### Charts Tool (Gerar Gráficos Epidemiológicos)

Responsável pela geração de visualizações a partir de métricas calculadas dos dados OPENDATASUS,
sendo:

- Número diário de casos nos últimos 30 dias
- Número mensal de casos nos últimos 90 dias

Os gráficos são exportados em formato PNG e armazenados em um diretório
específico para posterior inclusão no relatório Markdown e PDF.

**Saídas**:
- Arquivos PNG contendo as visualizações
- Caminhos dos arquivos gerados

### News Tool (Buscar Notícias Epidemiológicas)

Responsável por consultar fontes jornalísticas externas para coletar
notícias recentes relacionadas à Síndrome Respiratória Aguda Grave (SRAG).

As notícias são utilizadas exclusivamente para contextualização e
interpretação dos dados epidemiológicos, não sendo usadas como fonte
quantitativa.

A coleta é feita por meio da News API.

**Critérios**:
- Notícias mais recentes
- Filtragem por palavra chave
- Remoção de fontes portuguesas para focar nas brasileiras

## Fluxo de Execução das Tools

1. Calcular Métricas Epidemiológicas
2. Gerar Gráficos Epidemiológicos
3. Buscar Notícias Epidemiológicas
4. Consolidação e interpretação pelo Writer Chain

## Regras de Uso das Tools

- O agente **não pode inventar métricas ou valores**
- Toda análise quantitativa deve obrigatoriamente derivar da tool
  *Calcular Métricas Epidemiológicas*
- Toda visualização deve ser gerada exclusivamente pela tool
  *Gerar Gráficos Epidemiológicos*
- Notícias são usadas apenas como suporte interpretativo
- O fluxo de execução das tools é fixo
