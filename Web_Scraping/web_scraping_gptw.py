# Importação das Bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import re
import pymysql
import acesso_bd

# Configuração Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.maximize_window()

# Conexão Banco De Dados
conexao = pymysql.connect(
    host=acesso_bd.host,
    user=acesso_bd.user,
    password=acesso_bd.password,
    database=acesso_bd.database,
    port=acesso_bd.port
)
# Cursor SQL
cursor = conexao.cursor()

# Abre o Site
driver.get('https://gptw.com.br/ranking/melhores-empresas/')
sleep(5)

# Levantando opções de ano
select_ano = driver.find_element(By.XPATH, "/html/body/div[3]/main/section[3]/div/div/div/div[1]/select")
opcoes_ano = select_ano.find_elements(By.TAG_NAME, "option")

for ano in opcoes_ano:
    if ano.text == "Selecione por Ano" or (2016 <= int(ano.text) <= 2022):
        continue

    # Enviar o select para o filtro
    select_ano.send_keys(ano.text)
    sleep(3)

    # Levantando opções de tipo de ranking
    select_tipo_ranking = driver.find_element(By.XPATH, "/html/body/div[3]/main/section[3]/div/div/div/div[2]/select")
    tipos_ranking = select_tipo_ranking.find_elements(By.TAG_NAME, "option")

    for tipo_ranking in tipos_ranking:
        if tipo_ranking.text == "Selecione por Tipo de Ranking":
            continue

        # Enviar o select para o filtro
        select_tipo_ranking.send_keys(tipo_ranking.text)
        sleep(3)

        # Levantando opções de ranking
        select_ranking = driver.find_element(By.XPATH, "/html/body/div[3]/main/section[3]/div/div/div/div[3]/select")
        rankings = select_ranking.find_elements(By.TAG_NAME, "option")

        for ranking in rankings:
            if ranking.text == "Selecione por Ranking":
                continue

            # Enviar o select para o filtro
            select_ranking.send_keys(ranking.text)
            sleep(3)

            # Levantando opções de corte
            select_corte = driver.find_element(By.XPATH,"/html/body/div[3]/main/section[3]/div/div/div/div[4]/select")
            cortes = select_corte.find_elements(By.TAG_NAME, "option")

            for corte in cortes:
                if corte.text == "Selecione por Corte":
                    continue

                # Enviar o select para o filtro
                select_corte.send_keys(corte.text)
                sleep(3)

                # Clicar no botão filtrar
                driver.find_element(By.XPATH, '//*[@id="filterRanking"]').click()
                sleep(20)

                # CARREGAR TABELA
                tabela = driver.find_element(By.XPATH, '//*[@id="filterResult"]')
                corpo_tabela = tabela.find_element(By.TAG_NAME, "tbody")

                # Encontra todas as linhas da tabela
                linhas_tabela = corpo_tabela.find_elements(By.TAG_NAME, "tr")

                for linha in linhas_tabela:
                    # Encontra todas as células em cada linha
                    celulas = linha.find_elements(By.TAG_NAME, "td")

                    # Encontra os valores das células e armazena nas colunas apropriadas
                    posicao = celulas[0].text.strip()
                    empresa = celulas[1].text.strip()
                    empresa_sem_caractere = re.sub(r'[^a-zA-Z0-9\s]', '', empresa)
                    funcionarios = celulas[2].text.strip()
                    industria = celulas[3].text.strip()
                    propriedade = celulas[4].text.strip()

                    print(f"{posicao},{empresa},{funcionarios},{industria},{propriedade}, {ano.text}, {tipo_ranking.text}, {ranking.text}, {corte.text}")

                    # INSERIR DADOS SQL
                    sql = f"INSERT INTO empresa (numposicao, nmempresa, qtdfuncionarios, segmentoindustria, localidade, ano, tiporanking, ranking, corte)" \
                          f"VALUES('{posicao}','{empresa_sem_caractere}','{funcionarios}','{industria}','{propriedade}', '{ano.text}', '{tipo_ranking.text}', '{ranking.text}', '{corte.text}');"

                    cursor.execute(sql)

conexao.commit()
conexao.close()

print("Dados inseridos com sucesso no SQL")