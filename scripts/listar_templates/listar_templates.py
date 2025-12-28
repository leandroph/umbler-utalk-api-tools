"""
Listagem de Templates uTalk (Console)

Este script conecta à API da Umbler uTalk para listar todos os templates
de mensagens do WhatsApp configurados. Ele exibe o ID, nome, conteúdo, status,
rodapé e variáveis de cada template diretamente no console/terminal.

Dependências:
    - requests (pip install requests)
    - config.py (arquivo de configuração local)
"""

import requests
import time
import sys
import os

# --- IMPORTAÇÃO DO CONFIG DA RAIZ ---
# Obtém o caminho absoluto do diretório atual do script
dir_atual = os.path.dirname(__file__)
# Calcula o diretório raiz subindo dois níveis (../../)
# Estrutura esperada: raiz/scripts/listar_templates/main.py
diretorio_raiz = os.path.abspath(os.path.join(dir_atual, '../../'))

# Adiciona a raiz ao 'sys.path' para permitir importar o config.py
sys.path.append(diretorio_raiz)

try:
    import config
except ImportError:
    print("❌ ERRO CRÍTICO: Arquivo 'config.py' não encontrado na raiz do projeto.")
    print(f"   O Python procurou em: {diretorio_raiz}")
    sys.exit(1)

# --- CARREGAMENTO DE CREDENCIAIS ---
# Variáveis carregadas do arquivo config.py para segurança
TOKEN = config.TOKEN
ORG_ID = config.ORG_ID
CHANNEL_ID = config.CHANNEL_ID

# --- CONFIGURAÇÃO DA API ---
# Endpoint v1 para templates
URL = "https://app-utalk.umbler.com/api/v1/templates/"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def listar_todos_templates():
    """
    Função principal que itera sobre a API de templates usando paginação.

    A API da uTalk retorna os dados em fatias (slices). Esta função usa
    um loop 'while' para solicitar 50 itens por vez (Take) incrementando
    o ponto de partida (Skip) até que não haja mais itens.
    """
    skip = 0    # Ponto de partida da lista (offset)
    take = 50   # Quantidade de itens por requisição (limit)
    total_encontrados = 0

    print("🚀 Iniciando a extração dos templates...")
    print(f"📁 Lendo configurações de: {diretorio_raiz}/config.py")

    # Loop de paginação
    while True:
        # Monta os parâmetros para a requisição GET
        params = {
            "organizationId": ORG_ID,
            "channelId": CHANNEL_ID,
            "Skip": skip,
            "Take": take,
            "Behavior": "GetSliceOnly" # Garante retorno apenas da fatia solicitada
        }

        try:
            print(f"   ... Buscando itens {skip} a {skip + take} ...")
            response = requests.get(URL, headers=headers, params=params)

            # Verificação de erros HTTP
            if response.status_code != 200:
                print(f"❌ Erro na API: {response.status_code} - {response.text}")
                break

            dados = response.json()

            # Tratamento para garantir que 'itens' seja sempre uma lista,
            # independente se a API retorna um dict com chave 'items' ou a lista direta.
            itens = dados.get('items', dados) if isinstance(dados, dict) else dados

            # Critério de parada: Se a lista vier vazia, acabaram os templates
            if not itens:
                print("🏁 Fim da lista. Nenhum template restante.")
                break

            # Processamento e exibição de cada item
            for item in itens:
                total_encontrados += 1

                # Extração segura de dados
                template_id = item.get('id', 'N/A')  # <--- NOVA LINHA: Extrai o ID
                nome = item.get('label', 'Sem Rótulo')
                mensagem = item.get('content', '')
                status = item.get('status', 'Unknown')
                footer = item.get('footer')
                variaveis = item.get('variables', [])

                # Output formatado no console
                print(f"🔹 [{total_encontrados}] {nome} ({status})")
                print(f"🆔 ID: {template_id}")       # <--- NOVA LINHA: Exibe o ID
                print(f"📝 MENSAGEM:\n{mensagem}")

                if footer:
                    print(f"🔻 Rodapé: {footer}")

                if variaveis:
                    # List comprehension para extrair apenas o nome das variáveis
                    vars_nomes = [v.get('name') for v in variaveis]
                    print(f"💡 Variáveis: {', '.join(vars_nomes)}")

                print("-" * 60)

            # Prepara o próximo lote (avança o cursor)
            skip += take

            # Pausa de segurança para evitar rate-limit da API
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Erro de execução ou conexão: {e}")
            break

    print(f"\n✅ Concluído! Total de templates listados: {total_encontrados}")

# Execução direta do script
if __name__ == "__main__":
    listar_todos_templates()