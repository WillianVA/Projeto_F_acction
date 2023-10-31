# Melhores Empresas Para Trabalhar™ - 2023

O certificado Great Place to Work (GPTW) é crucial para a gestão de pessoas em um negócio, destacando-se como um dos mais reconhecidos e importantes. Além de aprimorar a reputação da marca empregadora, atrai profissionais qualificados e sinaliza aos clientes um comprometimento com o bem-estar dos colaboradores. 
Além disso, o GPTW revela pontos fortes e fracos na gestão de pessoas, permitindo a identificação de áreas para melhoria contínua, e também destaca publicamente as empresas que se destacam na criação de um ambiente de trabalho saudável, aumentando a conscientização sobre sua importância.

## Requirements

*projeto-final-equipe-2\SQL:* 

- Criar arquivo acessoBD.py com os dados de acesso ao banco de dados e salvar na pasta SQL

![image](https://github.com/acction-alunos/projeto-final-equipe-2/assets/30813578/0674f7ba-f126-4401-85d4-c14f864daa99)

*projeto-final-equipe-2\Python:*

- Criar arquivo acesso_bd.py com os dados de acesso ao banco de dados e salvar na pasta Python

![image](https://github.com/acction-alunos/projeto-final-equipe-2/assets/30813578/7f55bd61-f7a4-4eed-bfa8-c73b3ade8d69)

*Acesso ao banco de dados MySQL*

*Power BI Desktop ou Power BI Online*

## Usage

*Cronograma do Projeto*

![image](https://github.com/acction-alunos/projeto-final-equipe-2/assets/30813578/4f5a10e6-b1f8-4485-bb0f-b2761d5fe1e5)

*Modelagem dos dados*

![image](https://github.com/acction-alunos/projeto-final-equipe-2/assets/30813578/096dc4b4-2a75-4e69-87b0-f07fcda5cc65)

*Criação da tabela no banco de dados*

```Python
import pymysql
import acessoBD

connection = pymysql.connect(host = acessoBD.host,
                             user = acessoBD.user,
                             password = acessoBD.password,
                             database = acessoBD.database,
                             port= acessoBD.port,
                             )

cursor = connection.cursor()

cursor.execute  ("CREATE TABLE empresa \
                (id int PRIMARY KEY AUTO_INCREMENT,\
                numposicao varchar(255),\
                nmempresa varchar(255),\
                qtdFuncionarios varchar(255),\
                segmentoIndustria varchar(255),\
                localidade varchar(255),\
                ano int,\
                tiporanking varchar(255),\
                ranking varchar(255),\
                corte varchar(255)\
                );")

connection.commit()
connection.close()
```

*Web Scraping GPTW (https://gptw.com.br/ranking/melhores-empresas-para-trabalhar/)*

```Python
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
```

*Dashboard -  Power BI*

[Link para o relatório](https://app.powerbi.com/view?r=eyJrIjoiODhmYzNkY2QtOTFlNy00Y2QyLTg4ZDgtMzc5MmU1Yzk1OWQxIiwidCI6IjAxYTRlMjVhLWY1NDUtNGRlMi04ZjAxLTU4MjUxMzE1ZTk5OCJ9)

![image](https://github.com/acction-alunos/projeto-final-equipe-2/assets/30813578/3adfb1a6-c20d-441b-b873-2ae71a22f1c2)
![image](https://github.com/acction-alunos/projeto-final-equipe-2/assets/30813578/1a0bfc72-b287-4209-b1c8-8cc39e8a467c)


## Contributors

Gabriel Diniz: [linkedin.com/in/gabriel-d-11816bb4/](https://www.linkedin.com/in/gabriel-d-11816bb4/)

Leidi Torquato: [linkedin.com/in/leidianatorquato/](https://www.linkedin.com/in/leidianatorquato/)

Thais Diniz: [linkedin.com/in/thais-leticia-do-amaral-diniz/](https://www.linkedin.com/in/thais-leticia-do-amaral-diniz/)

Willian Ramos: [linkedin.com/in/willianrsramos/](https://www.linkedin.com/in/willianrsramos/)





