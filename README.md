# AI-Report-OPENDATASUS

## Visão Geral

Este projeto depende de chaves de API externas e de alguns requisitos de sistema para funcionar corretamente. Siga atentamente os passos abaixo para configurar o ambiente antes de executar a aplicação.

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
