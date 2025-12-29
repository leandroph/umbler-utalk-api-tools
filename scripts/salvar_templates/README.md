# 📄 Gerador de Relatório de Templates uTalk (PDF)

Este script em Python automatiza a extração de templates de mensagens do WhatsApp da plataforma **Umbler uTalk** e gera um relatório visual profissional em formato **PDF**.

É ideal para documentar, auditar ou compartilhar os modelos de mensagens cadastrados (aprovados ou não) com a equipe, sem precisar dar acesso ao painel administrativo.

## 🚀 Funcionalidades

- **Conexão via API:** Baixa todos os templates automaticamente, lidando com a paginação da API.
- **Relatório PDF Rico:** Gera um arquivo A4 formatado utilizando a biblioteca `ReportLab`.
- **Visualização Clara:**
  - Status do template e Categoria.
  - **ID Técnico** (útil para disparos via API).
  - Corpo da mensagem em caixas destacadas.
  - Exibição de variáveis e rodapés.

---

## 📂 Estrutura de Pastas Obrigatória

⚠️ **Atenção:** O script foi programado para buscar o arquivo de configuração (`config.py`) **dois níveis acima** da pasta onde ele está salvo.

A estrutura do seu projeto deve ser semelhante a esta:

```text
MEU_PROJETO/                <-- Raiz do projeto
│
├── config.py               <-- 🔑 AS CREDENCIAIS FICAM AQUI
│
└── scripts/
    └── relatorios/         <-- Pasta onde este script deve estar
        └── gerar_pdf.py    <-- Este script
```

## 🛠️ Pré-requisitos e Instalação
1. Python 3.**x** instalado.

2. Instale as bibliotecas necessárias executando o comando abaixo:

```Bash
pip install requests reportlab
```

## ⚙️ Configuração
Crie um arquivo chamado config.py na raiz do projeto e adicione suas credenciais da Umbler uTalk:

```python

# config.py

# Seu token de acesso (Bearer Token)
TOKEN = "SEU_TOKEN_AQUI"

# ID da Organização
ORG_ID = "SEU_ORGANIZATION_ID"

# ID do Canal do WhatsApp
CHANNEL_ID = "SEU_CHANNEL_ID"
```

> Nota de Segurança: Nunca envie o arquivo config.py para repositórios públicos (GitHub, GitLab). Adicione-o ao seu .gitignore.

## ▶️ Como Executar
1. Abra o terminal.

2. Navegue até a pasta onde o script está salvo:

```bash
cd scripts/relatorios
```

3. Execute o script:

```bash
python gerar_pdf.py
```

## 📄 Resultado
Após a execução, um arquivo chamado relatorio_templates.pdf será gerado na mesma pasta do script. O PDF conterá uma lista formatada como no exemplo abaixo:

```text
1. Boas Vindas (APPROVED - MARKETING) ID: 8129301

[Caixa Cinza] Olá {{1}}, seja bem-vindo à GIGIO!

Rodapé: Equipe Gigio Variáveis: name
```

## ⚠️ Solução de Problemas comum
### ❌ Erro: ModuleNotFoundError: No module named 'config'
**Causa:** O script não encontrou o arquivo config.py.

**Solução:** Verifique se o arquivo está exatamente na raiz do projeto, dois níveis acima do main.py.

### ❌ Erro: 401 Unauthorized
**Causa:** Token inválido ou expirado.

**Solução:** Gere um novo token no painel da Umbler uTalk e atualize o arquivo config.py.
