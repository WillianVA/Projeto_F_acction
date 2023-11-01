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