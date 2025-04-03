import pandas as pd
import os
import camelot
import zipfile

# PDF
current_dir = os.path.dirname(os.path.abspath(__file__)) # Diretorio atual
parent_dir = os.path.dirname(current_dir) # Voltando um diretorio (documentation)
anexo_dir = os.path.join(parent_dir, "docs") # Entrando no diretorio docs                
anexo_I = os.path.join(anexo_dir, "Anexo I.pdf") # Encontrando o arquivo em docs

# Verifica o arquivo
if not os.path.exists(anexo_I):
    print("Arquivo nao encontrado")

# Extração das tabelas
try:
    tables = camelot.read_pdf(
        anexo_I,
        pages='3-13', # Extraindo apenas da página 3 até 13 para exemplo (1 e 2 não há tabelas)
        flavor='stream',
        row_tol=25, # Tolerância para unir textos de duas linhas em apenas uma
        strip_text='\n',
        suppress_stdout=True
    )

    print(f"Total de tabelas detectadas: {len(tables)}")
   
   
    # Mostrando informações das tabelas extraidas
    for i, table in enumerate(tables[:1]): # Mostrando a primeira tabela extraida
        print(f"\nTabela {i+1}:")
        print(f"- Página: {table.page}")
        print(f"- Dimensões: {table.shape}")
        print("Primeiras linhas:")
        print(table.df.head(6).to_string())

    print(f"Total de tabelas detectadas: {len(tables)}")

    # Cria lista para armazenar dados
    dados = []

    # Processa as tabelas encontradas
    for i, table in enumerate(tables):
        df = table.df

        # Limpa os dados e remove colunas vazias
        df = df.replace('', pd.NA)  # Converte strings vazias em NA
        df = df.dropna(how='all', axis=1)  # Remove colunas vazias

        # Garante que há pelo menos 13 colunas antes de tentar a correção
        if df.shape[1] >= 13:
            # Verifica se a coluna 10 está vazia e a coluna 11 tem "SUBGRUPO"
            if pd.isna(df.iloc[0, 10]) and df.iloc[0, 11] == "SUBGRUPO":
                print(f"Ajustando cabeçalho da tabela {i+1} (página {table.page})...")

                # Corrige a posição do cabeçalho
                df.iloc[0, 10] = "SUBGRUPO"  # Define o cabeçalho correto na coluna 10

                # Remove a coluna 11, fazendo as demais colunas se ajustarem
                df.drop(columns=[11], axis=1, inplace=True)

            # Atualiza os cabeçalhos
            df.columns = list(df.iloc[0])  
            df = df[1:].reset_index(drop=True)  

            # Renomeia para garantir consistência
            df.columns = [
                "Coluna0", "Coluna1", "Coluna2", "Coluna3", "Coluna4",
                "Coluna5", "Coluna6", "Coluna7", "Coluna8", "Coluna9",
                "SUBGRUPO", "GRUPO", "CAPÍTULO"
            ][:df.shape[1]]  # Garante que só renomeamos colunas existentes

        # Adiciona ao conjunto de dados
        dados.append(df)


    # Junta todas as tabelas
    full_df = pd.concat(dados, ignore_index=True)

    # Salvar em .CSV
    csv_path = os.path.join(anexo_dir, 'dados_extraidos.csv')
    full_df.to_csv(csv_path, index=False, encoding='utf-8-sig')

    print(f"Dados salvos em: {csv_path}")

except Exception as erro:
    print(f"Erro durante a extração: {str(erro)}")