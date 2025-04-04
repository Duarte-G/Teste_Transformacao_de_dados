# Extração de Tabelas de PDF com Camelot

Este projeto tem como objetivo extrair tabelas de um arquivo PDF utilizando a biblioteca Camelot, realizar o tratamento dos dados com Pandas e armazená-los em um arquivo CSV compactado (ZIP).

## Descrição

O script lê um arquivo PDF localizado na pasta `docs`, extrai as tabelas das páginas 3 a 181, realiza a limpeza dos dados (remoção de colunas vazias, padronização dos cabeçalhos, etc.) e salva o resultado final compactado em um arquivo `.zip`.

Durante o desenvolvimento, enfrentei um problema na importação de algumas tabelas. Apesar de ter tentado diversas abordagens, a solução final, que considero a mais satisfatória, não conseguiu importar 8 das 178 tabelas detectadas.

## Estrutura do Projeto

docs/ # Contém os arquivos de dados brutos
* Anexo I.pdf
* Teste_Gabriel_Duarte.zip

src/ # Contém o código
* Transformação de Dados.py

## Como Executar
Certifique-se de ter o Python 3 instalado. Em seguida, instale as dependências necessárias:

```bash
pip install pandas numpy camelot-py[cv]
