# 📱 Listagem de Templates uTalk (CLI)

Este é um script em **Python** desenvolvido para conectar à API da **Umbler uTalk** e extrair todos os templates de mensagens do **WhatsApp** cadastrados na sua organização.

O script percorre todas as páginas da API e exibe os resultados formatados diretamente no terminal, sendo ideal para **conferência rápida de IDs, status e conteúdo das mensagens**.

---

## 🚀 Funcionalidades

- 🔄 **Paginação Automática**  
  Percorre todos os registros da API sem necessidade de configurar limites manuais.

- 📋 **Exibição Detalhada**  
  Exibe:
  - Nome do template  
  - **ID** (essencial para integrações)  
  - Conteúdo da mensagem  
  - Status (Aprovado / Reprovado)  
  - Rodapé  
  - Variáveis utilizadas  

- 🛡️ **Tratamento de Erros**  
  Identifica falhas de autenticação, problemas de conexão ou respostas inválidas da API.

- ⏱️ **Rate Limit Safe**  
  Inclui pausas automáticas entre requisições para evitar bloqueios pela API.

---

## 📂 Estrutura de Pastas Obrigatória

O script busca o arquivo `config.py` **dois níveis acima** do arquivo `main.py`.  
A estrutura do projeto **deve ser exatamente esta**:

```text
MEU_PROJETO/                ← Raiz do projeto
│
├── config.py               ← ⚠️ AS CREDENCIAIS FICAM AQUI
│
└── scripts/
    └── listar_templates/
        └── main.py         ← Script principal
```

## 🛠️ Pré-requisitos

Python 3.**x** instalado

Biblioteca **requests**

### Instalação da dependência
```bash
pip install requests
```

## ⚙️ Configuração

Crie um arquivo chamado config.py na raiz do projeto e adicione suas credenciais da API:

```python

# config.py

# Token de acesso (Bearer Token)
TOKEN = "SEU_TOKEN_AQUI"

# ID da Organização na Umbler uTalk
ORG_ID = "SEU_ORGANIZATION_ID"

# ID do Canal do WhatsApp
CHANNEL_ID = "SEU_CHANNEL_ID"
```

> 🔐 **Nota de Segurança**  
> Nunca envie o arquivo `config.py` para repositórios públicos.  
> Adicione-o ao `.gitignore`.


## ▶️ Como Executar

1. Abra o terminal

2. Navegue até a pasta do script:

```bash
cd scripts/listar_templates
```

3. Execute o script:

```bash
python main.py
```

## 📄 Exemplo de Saída
```text
Copy code
🚀 Iniciando a extração dos templates...
📁 Lendo configurações de: .../MEU_PROJETO/config.py
   ... Buscando itens 0 a 50 ...

🔹 [1] Boas Vindas (APPROVED)
🆔 ID: 812390123
📝 MENSAGEM:
Olá {{name}}, seja bem-vindo à nossa loja! Como podemos ajudar?
💡 Variáveis: name
------------------------------------------------------------
🔹 [2] Promoção Relâmpago (REJECTED)
🆔 ID: 812390124
📝 MENSAGEM:
Aproveite 50% de desconto hoje!
🔻 Rodapé: Oferta limitada
------------------------------------------------------------

✅ Concluído! Total de templates listados: 2
```

## ⚠️ Solução de Problemas
### ❌ **Erro:** ModuleNotFoundError: No module named 'config'

**Causa:**
O script não encontrou o arquivo config.py.

**Solução:**
Verifique se o arquivo está exatamente na raiz do projeto, dois níveis acima do main.py.

### ❌ Erro: 401 Unauthorized
**Causa:**
Token inválido ou expirado.

**Solução:**
Gere um novo token no painel da Umbler uTalk e atualize o arquivo config.py.
