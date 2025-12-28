import requests
import time
import sys
import os

# Biblioteca para gerar o PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors

# --- IMPORTAÇÃO DO CONFIG ---
# Sobe dois níveis para achar o config.py na raiz
diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(diretorio_raiz)

try:
    import config
except ImportError:
    print("❌ ERRO: 'config.py' não encontrado na raiz.")
    sys.exit(1)

# --- DADOS DO CONFIG ---
TOKEN = config.TOKEN
ORG_ID = config.ORG_ID
CHANNEL_ID = config.CHANNEL_ID

URL = "https://app-utalk.umbler.com/api/v1/templates/"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def obter_dados_api():
    """Conecta na API e retorna uma lista com todos os templates"""
    lista_final = []
    skip = 0
    take = 50

    print("🚀 Baixando templates da API...")

    while True:
        params = {
            "organizationId": ORG_ID,
            "channelId": CHANNEL_ID,
            "Skip": skip,
            "Take": take,
            "Behavior": "GetSliceOnly"
        }

        try:
            print(f"   ... Processando lote a partir de {skip}...")
            response = requests.get(URL, headers=headers, params=params)

            if response.status_code != 200:
                print(f"❌ Erro API: {response.status_code}")
                break

            dados = response.json()
            itens = dados.get('items', dados) if isinstance(dados, dict) else dados

            if not itens:
                break

            for item in itens:
                # Extraindo os dados conforme o JSON que você enviou
                template_data = {
                    "id": item.get('id', 'N/A'),  # <--- O ID QUE VOCÊ PEDIU
                    "nome": item.get('label', 'Sem Rótulo'),
                    "status": item.get('status', 'Unknown'),
                    "categoria": item.get('category', 'N/A'),
                    "mensagem": item.get('content', ''),
                    "footer": item.get('footer'),
                    "variaveis": [v.get('name') for v in item.get('variables', [])]
                }
                lista_final.append(template_data)

            skip += take
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Erro: {e}")
            break

    return lista_final


def gerar_pdf(templates):
    """Gera o arquivo PDF formatado"""
    nome_arquivo = "relatorio_templates.pdf"
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Estilo da caixa de mensagem (Cinza claro) com MAIS ESPAÇO
    style_msg = ParagraphStyle(
        'MensagemZap',
        parent=styles['BodyText'],
        backColor=colors.whitesmoke,
        borderColor=colors.lightgrey,
        borderPadding=10,
        borderWidth=1,
        spaceBefore=15,  # Aumentado de 8 para 15
        spaceAfter=15,  # Aumentado de 8 para 15
        leading=14
    )

    story.append(Paragraph(f"Relatório de Templates - Umbler uTalk - GIGIO", styles['Title']))
    story.append(Paragraph(f"Total de Templates: {len(templates)}", styles['Normal']))
    story.append(Spacer(1, 30))  # Aumentado espaçamento após título

    print(f"📄 Gerando PDF com {len(templates)} itens...")

    for i, tmpl in enumerate(templates):
        # 1. Título: Nome e Status
        titulo = f"<b>{i + 1}. {tmpl['nome']}</b> <font color='blue' size=8>({tmpl['status']} - {tmpl['categoria']})</font>"
        story.append(Paragraph(titulo, styles['Heading3']))

        # 2. ID do Template (Destaque técnico)
        # Usa fonte Courier (tipo código) para diferenciar o ID
        linha_id = f"<b>ID:</b> <font name='Courier' color='darkred'>{tmpl['id']}</font>"
        story.append(Paragraph(linha_id, styles['Normal']))

        # 3. Tratamento de quebras de linha para o PDF
        texto_msg = tmpl['mensagem'].replace('\n', '<br/>')
        if not texto_msg.strip():
            texto_msg = "<i>[Sem corpo de texto]</i>"

        story.append(Paragraph(texto_msg, style_msg))

        # 4. Rodapé e Variáveis
        info_extra = []
        if tmpl['footer']:
            info_extra.append(f"<b>Rodapé:</b> {tmpl['footer']}")
        if tmpl['variaveis']:
            info_extra.append(f"<b>Variáveis:</b> {', '.join(tmpl['variaveis'])}")

        if info_extra:
            texto_extra = "<br/>".join(info_extra)
            story.append(Paragraph(texto_extra, styles['Normal']))

        # Linha separadora com MAIS ESPAÇO
        story.append(Spacer(1, 20))  # Aumentado de 10 para 20
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
        story.append(Spacer(1, 20))  # Aumentado de 10 para 20

    try:
        doc.build(story)
        print(f"\n✅ SUCESSO! PDF salvo em: {os.path.abspath(nome_arquivo)}")
    except PermissionError:
        print("\n❌ ERRO: Feche o arquivo PDF se ele estiver aberto e tente novamente.")


if __name__ == "__main__":
    lista = obter_dados_api()
    if lista:
        gerar_pdf(lista)
    else:
        print("Nenhum template encontrado.")