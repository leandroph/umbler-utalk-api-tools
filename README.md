# Umbler uTalk API Tools (Python)

Este repositório contém scripts em Python para interagir de forma eficiente com a API oficial da **Umbler uTalk** (WhatsApp Business API).

O foco principal é resolver problemas comuns de integração, como a paginação automática de dados e a formatação correta dos templates (WABA), convertendo os campos técnicos da API para um formato legível.

## 🚀 Funcionalidades

- **Autenticação Segura:** Gerenciamento de cabeçalhos Bearer Token via arquivo de configuração separado.
- **Extração de Templates:** Script otimizado que percorre todas as páginas da API (Loop/Paginação) para baixar *todos* os templates, e não apenas os primeiros 50.
- **Leitura Inteligente:** Identifica automaticamente os campos corretos (`label`, `content`), exibe variáveis (`{{1}}`) e status de aprovação.

## 🛠️ Pré-requisitos

- Python 3.8 ou superior.
- Conta na Umbler uTalk com acesso à API.

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/leandroph/umbler-utalk-api-tools.git
   cd umbler-utalk-api-tools
