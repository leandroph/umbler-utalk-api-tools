import requests
import time
import sys
import os

# --- IMPORTAÇÃO DO CONFIG DA RAIZ ---
# Adiciona o diretório raiz (duas pastas acima) ao caminho de busca do Python
# Estrutura esperada: raiz/scripts/listar_templates/main.py
diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(diretorio_raiz)

try:
    import config
except ImportError:
    print("❌ ERRO CRÍTICO: Arquivo 'config.py' não encontrado na raiz do projeto.")
    print(f"   O Python procurou em: {diretorio_raiz}")
    print("   Verifique se o arquivo existe e se os nomes estão corretos.")
    sys.exit(1)

# --- DADOS CARREGADOS DO CONFIG ---
TOKEN = config.TOKEN
ORG_ID = config.ORG_ID
CHANNEL_ID = config.CHANNEL_ID

# --- CONFIGURAÇÃO DA API ---
URL = "https://app-utalk.umbler.com/api/v1/templates/"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def listar_todos_templates():
    skip = 0
    take = 50
    total_encontrados = 0

    print("🚀 Iniciando a extração dos templates...")
    print(f"📁 Lendo configurações de: {diretorio_raiz}/config.py")
    print(f"🔑 Usando campo 'label' para nome e 'content' para mensagem.\n")

    while True:
        # Monta os parâmetros para paginação
        params = {
            "organizationId": ORG_ID,
            "channelId": CHANNEL_ID,
            "Skip": skip,
            "Take": take,
            "Behavior": "GetSliceOnly"
        }

        try:
            print(f"   ... Buscando itens {skip} a {skip + take} ...")
            response = requests.get(URL, headers=headers, params=params)

            if response.status_code != 200:
                print(f"❌ Erro na API: {response.status_code} - {response.text}")
                break

            dados = response.json()
            # Garante que pega a lista correta
            itens = dados.get('items', dados) if isinstance(dados, dict) else dados

            if not itens:
                print("🏁 Fim da lista. Nenhum template restante.")
                break

            # Processa cada template desta página
            for item in itens:
                total_encontrados += 1

                nome = item.get('label', 'Sem Rótulo')
                mensagem = item.get('content', '')
                status = item.get('status', 'Unknown')
                footer = item.get('footer')
                variaveis = item.get('variables', [])

                print(f"🔹 [{total_encontrados}] {nome} ({status})")
                print(f"📝 MENSAGEM:\n{mensagem}")

                if footer:
                    print(f"🔻 Rodapé: {footer}")

                if variaveis:
                    vars_nomes = [v.get('name') for v in variaveis]
                    print(f"💡 Variáveis: {', '.join(vars_nomes)}")

                print("-" * 60)

            skip += take
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Erro de execução: {e}")
            break

    print(f"\n✅ Concluído! Total de templates listados: {total_encontrados}")

if __name__ == "__main__":
    listar_todos_templates()