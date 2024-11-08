import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import os

# Carregar credenciais a partir do secret armazenado como uma variável de ambiente
credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")  # Nome do secret no GitHub
creds_dict = json.loads(credentials_json)
creds = Credentials.from_service_account_info(creds_dict)

# Autenticar com o Google Sheets
client = gspread.authorize(creds)

# ID da planilha do Google Sheets que queremos acessar
SPREADSHEET_ID = '1d0wUNVHnzEcdAdpnqnpAoogaLa0BNORaB5FkvGq-5PI'

# Abrir a planilha pelo ID
sheet = client.open_by_key(SPREADSHEET_ID)

# Selecionar a aba da planilha para atualização de notas e limpar conteúdo
worksheet = sheet.worksheet('SCRIPT-TURMA2')
worksheet.clear()

# Carregar o arquivo Excel com as notas para o pandas
df_local = pd.read_excel('turma2_planilha_notas.xlsx')  # Certifique-se de que o arquivo esteja no repositório ou em um local acessível

# Converter valores para strings para evitar problemas com JSON
df_local = df_local.astype(str)

# Transformar os dados do DataFrame em uma lista de listas
data = [df_local.columns.values.tolist()] + df_local.values.tolist()

# Escrever os dados no Google Sheets a partir da célula A1
worksheet.update(range_name='A1', values=data)

# Obter a data e horário atual formatados
data_atualizacao = datetime.now().strftime('Última Atualização: %Y-%m-%d %H:%M:%S')

# Selecionar a aba onde a data e hora serão atualizadas
status_worksheet = sheet.worksheet('turma2-status-alunos')

# Atualizar a célula W1 com a data e hora de atualização
status_worksheet.update('W1', [[data_atualizacao]])

print("Dados carregados com sucesso na aba 'NOTAS-TESTE' e data e hora de atualização adicionadas em 'turma2-status-alunos'!")
