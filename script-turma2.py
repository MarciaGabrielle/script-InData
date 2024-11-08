# script-turma2.py

import chromedriver_autoinstaller
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Instala automaticamente a versão correta do ChromeDriver
chromedriver_autoinstaller.install()

# Diretório de download temporário usando a variável de ambiente do GitHub Actions
download_dir = os.getenv("GITHUB_WORKSPACE")  # Usa o diretório de trabalho correto

# Configurações para o Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Inicializar o WebDriver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Acessar a página de login
driver.get('https://ensino.nead.ufrr.br/ava/login/index.php')

# Aguardar a página carregar completamente
wait = WebDriverWait(driver, 10)
username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))

# Preencher os campos de login com variáveis de ambiente
username_field.send_keys(os.getenv("USERNAME"))
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(os.getenv("PASSWORD"))

# Submeter o formulário de login
password_field.send_keys(Keys.RETURN)

# Aguardar o carregamento da página após login
wait.until(EC.presence_of_element_located((By.ID, 'page-footer')))

# Navegar para a página de download
driver.get('https://ensino.nead.ufrr.br/ava/grade/export/xls/index.php?id=1735')

# Aguardar até que o botão de download esteja clicável e clique nele
download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'id_submitbutton')))
download_button.click()
print("Botão de download clicado, aguardando o download do arquivo.")

# Aumentar o tempo de espera para o download
download_wait_time = 60  # tempo de espera aumentado para 60 segundos
download_file_path = os.path.join(download_dir, "InData - Turma02 Notas.xlsx")

# Verificar se o arquivo foi baixado, repetindo a verificação até o tempo limite
for _ in range(download_wait_time):
    if os.path.exists(download_file_path):
        print("Arquivo de download encontrado.")
        break
    time.sleep(1)
else:
    # Se o arquivo não for encontrado, listar todos os arquivos no diretório de download
    print("Erro: Arquivo de download não encontrado. Listando arquivos no diretório de downloads:")
    print(os.listdir(download_dir))
    driver.quit()
    exit()

# Renomear o arquivo baixado para "turma2_planilha_notas.xlsx"
new_file = os.path.join(download_dir, "turma2_planilha_notas.xlsx")
if os.path.exists(download_file_path):
    os.rename(download_file_path, new_file)
    print(f"Arquivo renomeado para: {new_file}")
else:
    print(f"Arquivo {download_file_path} não encontrado para renomear.")

# Fechar o navegador após a execução
driver.quit()
