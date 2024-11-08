# SCRIPT QUE USA O SELENIUM PARA FAZER O DOWNLOAD DA PLANILHA DE NOTAS DOS ALUNOS

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.edge.service import Service
import os

# Defina o caminho do WebDriver
service = Service('C:/Users/gabyb/Downloads/edgedriver_win64/msedgedriver.exe')

# Definir o diretório de download
download_dir = "C:/Users/gabyb/Downloads"

# Inicializar o WebDriver 
driver = webdriver.Edge(service=service)

# Acessar a página de login
driver.get('https://ensino.nead.ufrr.br/ava/login/index.php')

# Aguardar a página carregar completamente
wait = WebDriverWait(driver, 10)
username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))

# Agora preencher o campo de login
username_field.send_keys('marcia_gabrielle')

# Continuar com o resto do processo de login
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys('#281283#')

# Submeter o formulário de login
password_field.send_keys(Keys.RETURN)

# Aguardar o carregamento após login
wait.until(EC.presence_of_element_located((By.ID, 'page-footer')))  # Aguarda a página carregar completamente

# Após o login, ir diretamente para a página do download
driver.get('https://ensino.nead.ufrr.br/ava/grade/export/xls/index.php?id=1735')

# Aguardar até que o botão de download esteja clicável
download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))

# Clicar no botão "Download" para baixar a planilha
download_button.click()

# Verificar se o arquivo foi baixado, repetindo a verificação por até 30 segundos
download_wait_time = 10
download_file_path = os.path.join(download_dir, "InData - Turma02 Notas.xlsx")
for _ in range(download_wait_time):
    if os.path.exists(download_file_path):
        break
    time.sleep(1)
else:
    print("Erro: Arquivo de download não encontrado.")
    driver.quit()
    exit()

# Verificar se o arquivo "planilha_notas.xlsx" já existe e excluí-lo
new_file = os.path.join(download_dir, "turma2_planilha_notas.xlsx")
if os.path.exists(new_file):
    os.remove(new_file)

# Verificar se o arquivo original existe e renomear
if os.path.exists(download_file_path):
    os.rename(download_file_path, new_file)
    print(f"Arquivo renomeado para: {new_file}")
else:
    print(f"Arquivo {download_file_path} não encontrado para renomear.")

# Fechar o navegador após a execução
driver.quit()
