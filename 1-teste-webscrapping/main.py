import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

"""A ideia aqui foi acessar a pagina e apartir do texto do link desejado baixar os arquivos
nesse caso os links <a> que continham os anexos que precisavamos eram "Anexo I." e "Anexo II."""

# Configurações
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"  # Substitua pela URL real
ARQUIVOS_DESEJADOS = {"Anexo I.", "Anexo II."}
PASTA_DOWNLOADS = "downloads"
ZIP_FILENAME = "arquivos.zip"

# Criar pasta de downloads se não existir
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)

def baixar_arquivo(url, caminho_destino):
    """Baixa um arquivo da URL e salva no caminho especificado."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(caminho_destino, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Arquivo baixado: {caminho_destino}")
        return caminho_destino
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao baixar {url}: {e}")
        return None

def obter_links_da_pagina(url):
    """Obtém todos os links da página especificada."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [(link.get_text(strip=True), link.get("href")) for link in soup.find_all("a")]
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar a página: {e}")
        return []

def compactar_arquivos(lista_arquivos, nome_zip):
    """Compacta os arquivos em um ZIP."""
    if lista_arquivos:
        with ZipFile(nome_zip, "w") as zipf:
            for arquivo in lista_arquivos:
                zipf.write(arquivo, os.path.basename(arquivo))
        print(f"📦 Arquivos compactados: {nome_zip}")
    else:
        print("⚠ Nenhum arquivo para compactar.")

def main():
    """Fluxo principal do script."""
    print("🔍 Buscando arquivos na página...")
    links = obter_links_da_pagina(URL)
    
    arquivos_baixados = []
    for nome, href in links:
        if nome in ARQUIVOS_DESEJADOS and href:
            href = href if href.startswith("http") else f"{URL.rstrip('/')}/{href.lstrip('/')}"
            caminho_arquivo = os.path.join(PASTA_DOWNLOADS, f"{nome}.pdf")
            arquivo_baixado = baixar_arquivo(href, caminho_arquivo)
            if arquivo_baixado:
                arquivos_baixados.append(arquivo_baixado)
    
    if not arquivos_baixados:
        print("⚠ Nenhum arquivo desejado encontrado.")
    else:
        compactar_arquivos(arquivos_baixados, ZIP_FILENAME)

if __name__ == "__main__":
    main()
