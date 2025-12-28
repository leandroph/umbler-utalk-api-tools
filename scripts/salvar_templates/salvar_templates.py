"""
Relatório de Templates uTalk para PDF.

Este script realiza a extração de todos os templates de mensagens do WhatsApp
configurados na plataforma Umbler uTalk via API e gera um relatório visual
em formato PDF.

Dependências:
    - requests
    - reportlab
    - config.py (arquivo local com credenciais)
"""

import requests
import time
import sys
import os

# Biblioteca ReportLab para geração de arquivos PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors

# --- CONFIGURAÇÃO DE AMBIENTE E IMPORTAÇÃO DE CREDENCIAIS ---

# Define o diretório raiz subindo dois níveis a partir da localização deste script.
# Exemplo: Se o script está em /projeto/scripts/relatorios/main.py,
# ele buscará o config.py em /projeto/config.py
diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(diretorio_raiz)

try:
    import config
except ImportError:
    print("❌ ERRO CRÍTICO: O arquivo 'config.py' não foi encontrado no diretório raiz.")
    print(f"   Diretório esperado: {diretorio_raiz}")
    sys.exit(1)

# --- CONSTANTES E CABEÇALHOS ---
TOKEN = config.TOKEN
ORG_ID = config.ORG_ID
CHANNEL_ID = config.CHANNEL_ID

# Endpoint para listagem de templates (v1)
URL = "https://app-utalk.umbler.com/api/v1/templates/"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def obter_dados_api():
    """
    Conecta à API da Umbler uTalk e baixa todos os templates cadastrados.

    A função lida com a paginação da API (Skip/Take) automaticamente,
    realizando requisições em loop até que não haja mais itens.

    Returns:
        list[dict]: Uma lista de dicionários, onde cada dicionário contém
                    os dados tratados de um template (id, nome, mensagem, etc).
    """
    lista_final = []
    skip = 0
    take = 50  # Quantidade de itens por requisição

    print("🚀 Iniciando download dos templates via API...")

    while True:
        # Parâmetros de paginação e filtros
        params = {
            "organizationId": ORG_ID,
            "channelId": CHANNEL_ID,
            "Skip": skip,
            "Take": take,
            "Behavior": "GetSliceOnly"  # Garante que venha apenas a fatia solicitada
        }

        try:
            print(f"   ... Processando lote (Skip: {skip} | Take: {take})...")
            response = requests.get(URL, headers=headers, params=params)

            if response.status_code != 200:
                print(f"❌ Erro na API. Código HTTP: {response.status_code}")
                print(f"   Detalhe: {response.text}")
                break

            dados = response.json()
            # Garante compatibilidade caso a API retorne uma lista direta ou um dict com chave 'items'
            itens = dados.get('items', dados) if isinstance(dados, dict) else dados

            # Se a lista estiver vazia, encerra o loop (fim da paginação)
            if not itens:
                break

            for item in itens:
                # Extração e tratamento dos dados para um formato limpo
                template_data = {
                    "id": item.get('id', 'N/A'),
                    "nome": item.get('label', 'Sem Rótulo'),
                    "status": item.get('status', 'Unknown'),
                    "categoria": item.get('category', 'N/A'),
                    "mensagem": item.get('content', ''),
                    "footer": item.get('footer'),
                    # List comprehension para extrair apenas os nomes das variáveis
                    "variaveis": [v.get('name') for v in item.get('variables', [])]
                }
                lista_final.append(template_data)

            # Prepara o próximo lote
            skip += take
            # Pequena pausa para evitar Rate Limit da API
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Exceção ocorrida durante a requisição: {e}")
            break

    return lista_final


def gerar_pdf(templates):
    """
    Gera um arquivo PDF formatado com a lista de templates.

    Utiliza a biblioteca ReportLab para criar um documento estruturado com
    títulos, destaques de cor para status e caixas estilizadas para o
    conteúdo das mensagens.

    Args:
        templates (list): A lista de dados retornada pela função obter_dados_api().
    """
    nome_arquivo = "relatorio_templates.pdf"

    # Configuração do documento A4
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
    story = []  # Lista que armazena os elementos (parágrafos, espaços) do PDF
    styles = getSampleStyleSheet()

    # Definição de estilo personalizado para o corpo da mensagem (Box Cinza)
    style_msg = ParagraphStyle(
        'MensagemZap',
        parent=styles['BodyText'],
        backColor=colors.whitesmoke,  # Fundo cinza claro
        borderColor=colors.lightgrey,
        borderPadding=10,
        borderWidth=1,
        spaceBefore=15,  # Espaçamento externo superior
        spaceAfter=15,  # Espaçamento externo inferior
        leading=14  # Espaçamento entre linhas
    )

    # Cabeçalho do PDF
    story.append(Paragraph(f"Relatório de Templates - Umbler uTalk - GIGIO", styles['Title']))
    story.append(Paragraph(f"Total de Templates Extraídos: {len(templates)}", styles['Normal']))
    story.append(Spacer(1, 30))

    print(f"📄 Gerando arquivo PDF com {len(templates)} templates...")

    for i, tmpl in enumerate(templates):
        # 1. Título do Template
        # Uso de tags HTML básicas (<b>, <font>) permitidas pelo ReportLab
        titulo = f"<b>{i + 1}. {tmpl['nome']}</b> <font color='blue' size=8>({tmpl['status']} - {tmpl['categoria']})</font>"
        story.append(Paragraph(titulo, styles['Heading3']))

        # 2. ID Técnico
        # Fonte Courier (monoespaçada) para destacar que é um código
        linha_id = f"<b>ID:</b> <font name='Courier' color='darkred'>{tmpl['id']}</font>"
        story.append(Paragraph(linha_id, styles['Normal']))

        # 3. Corpo da Mensagem
        # Substitui quebra de linha Python (\n) por quebra HTML (<br/>) para o PDF renderizar
        texto_msg = tmpl['mensagem'].replace('\n', '<br/>')
        if not texto_msg.strip():
            texto_msg = "<i>[Sem conteúdo de texto]</i>"

        story.append(Paragraph(texto_msg, style_msg))

        # 4. Metadados (Rodapé e Variáveis)
        info_extra = []
        if tmpl['footer']:
            info_extra.append(f"<b>Rodapé:</b> {tmpl['footer']}")
        if tmpl['variaveis']:
            info_extra.append(f"<b>Variáveis:</b> {', '.join(tmpl['variaveis'])}")

        if info_extra:
            texto_extra = "<br/>".join(info_extra)
            story.append(Paragraph(texto_extra, styles['Normal']))

        # 5. Separador visual entre itens
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
        story.append(Spacer(1, 20))

    # Tenta salvar o arquivo físico
    try:
        doc.build(story)
        caminho_absoluto = os.path.abspath(nome_arquivo)
        print(f"\n✅ SUCESSO! PDF gerado em:\n   -> {caminho_absoluto}")
    except PermissionError:
        print("\n❌ ERRO DE PERMISSÃO: Não foi possível salvar o arquivo.")
        print("   Verifique se o arquivo 'relatorio_templates.pdf' já está aberto e feche-o.")


# --- BLOCO PRINCIPAL DE EXECUÇÃO ---
if __name__ == "__main__":
    lista_templates = obter_dados_api()

    if lista_templates:
        gerar_pdf(lista_templates)
    else:
        print("⚠️ Processo finalizado: Nenhum template foi encontrado ou houve erro na API.")