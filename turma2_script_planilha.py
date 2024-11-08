import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime  # Para obter a data e horário atual

# Caminho para o arquivo de credenciais (JSON) 
CREDENTIALS_FILE = 'C:/Users/gabyb/Downloads/script-indata-d96fd3a627eb.json'

# Definir o escopo necessário para acessar o Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

# Autenticação com a conta de serviço
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPE)
client = gspread.authorize(creds)

# ID da planilha do Google Sheets que queremos acessar
SPREADSHEET_ID = '1d0wUNVHnzEcdAdpnqnpAoogaLa0BNORaB5FkvGq-5PI'

# Abrir a planilha pelo ID
sheet = client.open_by_key(SPREADSHEET_ID)

# Selecionar a aba da planilha para atualização de notas e limpar conteúdo
worksheet = sheet.worksheet('SCRIPT-TURMA2')
worksheet.clear()

# Carregar o arquivo Excel com as notas para o pandas
df_local = pd.read_excel('C:/Users/gabyb/Downloads/turma2_planilha_notas.xlsx')

# Converter valores para strings para evitar problemas com JSON
df_local = df_local.astype(str)

# Transformar os dados do DataFrame em uma lista de listas
data = [df_local.columns.values.tolist()] + df_local.values.tolist()

# Escrever os dados no Google Sheets a partir da célula A1 (ajustando a ordem dos argumentos)
worksheet.update(range_name='A1', values=data)

# Obter a data e horário atual formatados
data_atualizacao = datetime.now().strftime('Última Atualização: %Y-%m-%d %H:%M:%S')

# Selecionar a aba onde a data e hora serão atualizadas
status_worksheet = sheet.worksheet('turma2-status-alunos')

# Atualizar a célula W1 com a data e hora de atualização
status_worksheet.update('W1', [[data_atualizacao]])

print("Dados carregados com sucesso na aba 'NOTAS-TESTE' e data e hora de atualização adicionadas em 'turma2-status-alunos'!")
