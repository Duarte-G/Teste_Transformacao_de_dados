import pandas as pd
import os
import camelot
import zipfile

# PDF
current_dir = os.path.dirname(os.path.abspath(__file__)) # Diretorio atual
parent_dir = os.path.dirname(current_dir) # Voltando um diretorio (documentation)
pasta_pdf = os.path.join(parent_dir, "docs", "Anexo I.pdf") # Encontrando o arquivo em docs

# Verifica o arquivo
if not os.path.exists(pasta_pdf):
    print("Arquivo nao encontrado")

# Extração das tabelas
try:
    tables = camelot.read_pdf(
        pasta_pdf,
        pages='5',
        flavor='stream',
        strip_text='\n',
        suppress_stdout=False
    )

    print(f"Total de tabelas detectadas: {len(tables)}")

    # Mostrando informações das tabelas extraidas
    for i, table in enumerate(tables[:1]): # Mostrando a primeira tabela extraida
        print(f"\nTabela {i+1}:")
        print(f"- Página: {table.page}")
        print(f"- Dimensões: {table.shape}")
        print("Primeiras linhas:")
        print(table.df.head(6).to_string())

except Exception as erro:
    print(f"Erro durante a extração: {str(erro)}")