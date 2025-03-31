import pdfplumber
import pandas as pd
import zipfile
import os

# Caminho do arquivo PDF
caminho_pdf = "Anexo I.pdf"

# Número da página inicial onde a primeira tabela está (começando de 0)
numero_pagina = 2  # Por exemplo, a terceira página (índice 2)

# Lista para armazenar todas as tabelas extraídas
tabelas_extraidas = []

# Abrir o PDF e processar da página especificada até a última
# Esta levando em torno de 60 segundos
with pdfplumber.open(caminho_pdf) as pdf:
    for i in range(numero_pagina, len(pdf.pages)):
        pagina = pdf.pages[i]
        tabelas = pagina.extract_tables()
        
        for tabela in tabelas:
            df_temp = pd.DataFrame(tabela)
            
            # Se for a primeira tabela, manter o cabeçalho
            if not tabelas_extraidas:
                tabelas_extraidas.append(df_temp)
            else:
                # Remover a primeira linha (cabeçalho) das tabelas seguintes 
                tabelas_extraidas.append(df_temp.iloc[1:].reset_index(drop=True))

# Concatenar todas as tabelas extraídas em um único DataFrame
if tabelas_extraidas:
    df_final = pd.concat(tabelas_extraidas, ignore_index=True)
    print("Tabela extraída com sucesso")
else:
    print("⚠ Nenhuma tabela encontrada no PDF.")


df_final.columns = df_final.iloc[0]  # Usa a primeira linha como cabeçalho
df_final = df_final.drop(0).reset_index(drop=True)
df_final['OD'] = df_final['OD'].replace('OD', 'Seg. Odontológica')
df_final['AMB'] = df_final['AMB'].replace('AMB', 'Seg. Ambulatorial')

# Salvando o DataFrame como CSV
df_final.to_csv('tabela.csv', index=False)

# Nome do arquivo zip
nome_zip = 'Teste_Felipe.zip'

# Criando o arquivo zip
with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('tabela.csv', os.path.basename('tabela.csv'))  # Adiciona o CSV ao ZIP

print(f"Arquivo {nome_zip} criado com sucesso!")