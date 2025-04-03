import pandas as pd
import numpy as np
import os
import camelot
import zipfile
from io import BytesIO

# define o caminho dos arquivos
current_dir = os.path.dirname(os.path.abspath(__file__)) # diretorio atual
parent_dir = os.path.dirname(current_dir) # voltando um diretorio (documentation)
anexo_dir = os.path.join(parent_dir, "docs") # entrando no diretorio docs                
anexo_I = os.path.join(anexo_dir, "Anexo I.pdf") # encontrando o arquivo em docs

# verifica se o arquivo PDF existe
if not os.path.exists(anexo_I):
    print("Erro: Arquivo PDF não encontrado")
    exit()

try:
    # usando camelot para extrair tabelas do PDF
    tables = camelot.read_pdf(
        anexo_I,
        pages='3-181',              # verifica da página 3 até o final (não há tabelas na página 1 e 2)
        flavor='stream',            # método de extração
        row_tol=25,                 # tolerância para unir linhas
        strip_text='\n',            # remove quebras de linha
        suppress_stdout=True
    )

    print(f"Tabelas detectadas: {len(tables)}")

    # lista para armazenar dados processados
    dados = []
    processed_tables = 0
    error_report = {}

    # processa cada tabela individualmente
    for i, table in enumerate(tables):
        try:
            df = table.df.copy()

            # limpeza dos dados (colunas vazias)
            df = (df.replace('', np.nan)            # Converte vazio para NaN
                  .dropna(how='all', axis=1))       # Descarta colunas com todos valores NaN
            
            # correção de colunas GRUPO E SUBGRUPO
            if df.shape[1] == 14:
                # verifica qual coluna está vazia (12 ou 11)
                coluna_vazia = None
                if df.iloc[1:, 12].isna().all():   # verifica coluna 12 (GRUPO)
                    coluna_vazia = 12
                elif df.iloc[1:, 11].isna().all(): # verifica coluna 11 (SUBGRUPO)
                    coluna_vazia = 11
                
                if coluna_vazia is not None:
                    df = df.drop(df.columns[coluna_vazia], axis=1)
                else:
                    raise ValueError("Estrutura de 14 colunas não reconhecida")
                
            # padronizar cabeçalhos
            headers = [
                "PROCEDIMENTO", "RN (alteração)", "VIGÊNCIA",
                "Seg. Odontológica", "Seg. Ambulatorial", "HCO",
                "HSO", "REF", "PAC", "DUT", 
                "SUBGRUPO", "GRUPO", "CAPÍTULO"
            ]

            # aplica os novos cabeçalhos
            df.columns = headers
            
            # remove a primeira linha (cabeçalho do PDF)
            df = df.iloc[1:].reset_index(drop=True)
            
            # adiciona aos dados processados
            dados.append(df)
            processed_tables += 1

        except Exception as e:
            # registra erros indicando a página
            error_report.setdefault(table.page, []).append(str(e))
            continue

    print(f"\nTabelas processadas com sucesso: {processed_tables}/{len(tables)}")

     # relatório de erros
    print(f"\nProcessamento concluído: {processed_tables}/{len(tables)} tabelas")
    if error_report:
        print("\nERROS ENCONTRADOS:")
        for page, errors in error_report.items():
            print(f"Página {page}, erro:")
            for error in set(errors):
                print(f"{error}")

    # junta todas as tabelas
    full_df = pd.concat(dados, ignore_index=True)

    # armazena o .csv em zip
    zip_path = os.path.join(anexo_dir, 'Teste_Gabriel_Duarte.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        csv_buffer = BytesIO()
        full_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_buffer.seek(0)

    # adiciona ao ZIP sem criar arquivo físico
        zipf.writestr('dados_extraidos.csv', csv_buffer.getvalue())

    print(f"\nArquivo ZIP criado em: {zip_path}")

except Exception as erro:
    print(f"\nErro durante a extração: {str(erro)}")