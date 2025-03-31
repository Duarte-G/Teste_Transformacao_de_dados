import tabula
import pandas as pd
import os
import zipfile

# PDF
current_dir = os.path.dirname(os.path.abspath(__file__)) # Diretorio atual
parent_dir = os.path.dirname(current_dir) # Voltando um diretorio (documentation)
pasta_pdf = os.path.join(parent_dir, "docs", "Anexo I.pdf") # Encontrando o arquivo em docs

# Verifica o arquivo
if not os.path.exists(pasta_pdf):
    print("Arquivo nao encontrado")

print(f"Tentando extrair tabelas de: {pasta_pdf}")

# Extraindo todas as tabelas
try:
    tables = tabula.read_pdf(
        pasta_pdf,
        pages = 'all', # Extrai todas as páginas
        multiple_tables = True, # Pode haver mais de uma tabela por página
        guess = True, # Tenta advinhar a estrutura da tabela
        lattice = True # Se guia com as linhas da tabela
    )

    print(f"Número de tabelas encontradas: {len(tables)}")

    if len(tables) > 0:
        print("Visualizando a primeira tabela encontrada:")
        print(tables[0].head())

except Exception as erro:
    print(f"Erro ao extrair tabelas: {erro}")