from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import telegram_msg
import asyncio

# Configuração Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa o Chrome em segundo plano

# Inicializa o WebDriver com as opções headless
driver = webdriver.Chrome(options=chrome_options)

# Acessa a página
driver.get("https://sigaa.unb.br/sigaa/public/turmas/listar.jsf")

# Aguarda o carregamento da página
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "formTurma:inputNivel")))

# Seleciona "GRADUAÇÃO" no campo "Nível de ensino"
nivel_ensino_select = Select(driver.find_element(By.NAME, "formTurma:inputNivel"))
nivel_ensino_select.select_by_visible_text("GRADUAÇÃO")

# Seleciona "DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA" no campo "Unidade"
unidade_select = Select(driver.find_element(By.NAME, "formTurma:inputDepto"))
unidade_select.select_by_visible_text("DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA")

turmas_quero = {'CIC0234 - MÉTODOS DE PROGRAMAÇÃO',
                'CIC0135 - INTRODUCAO A INTELIGENCIA ARTIFICIAL',
                'CIC0182 - LÓGICA COMPUTACIONAL 1',
                }
turma_atual = []

while (True):
    # Clica no botão "Buscar"
    buscar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Buscar']"))
    )
    buscar_button.click()

    # Aguarda o carregamento da página de resultados
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "listagem"))
    )

    # Coleta as informações da tabela de turmas
    tabela = driver.find_element(By.CLASS_NAME, "listagem")
    linhas = tabela.find_elements(By.TAG_NAME, "tr")

    # Extrai as informações de cada linha da tabela
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        dados_linha = [coluna.text for coluna in colunas]

        if len(dados_linha) == 1:
            turma_atual = dados_linha

        if turma_atual and turma_atual[0] in turmas_quero:
            print(dados_linha)
            if len(dados_linha) > 1 and int(dados_linha[6]) < int(dados_linha[5]):
                print(f'{("LIBEROU VAGA " + turma_atual[0]+ "\n")*5}')
                asyncio.run(telegram_msg.send_message(f'{("LIBEROU VAGA " + turma_atual[0])}'))


# Fecha o navegador
driver.quit()