import tabula
import pandas as pd
import os
import zipfile

# PDF
current_dir = os.path.dirname(os.path.abspath(__file__)) # Diretorio atual
parent_dir = os.path.dirname(current_dir) # Voltando um diretorio (documentation)
pasta_pdf = os.path.join(parent_dir, "docs", "Anexo I.pdf") # Encontrando o arquivo em docs

# Verifica o arquivo
if os.path.exists(pasta_pdf):
    print("Arquivo encontrado")
else:
    print("Arquivo nao encontrado")