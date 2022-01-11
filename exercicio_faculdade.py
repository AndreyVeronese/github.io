# Considere um arquivo de texto contendo os dados dos funcionários de uma empresa. Cada linha do arquivo contém 
# informações sobre um funcionário, separados por ponto-e-virgula, no formato: nome;idade;salario. 

# Implemente um programa para realizar as seguintes operações:

# Realizar o mapeamento da tabela em uma classe, utilizando ORM e SQLAlchemy. Abrir o arquivo de texto e inserir os 
# dados contidos no arquivo na tabela do banco de dados. Realizar uma consulta no banco de dados e exibir no terminal
# todos os dados cadastrados na tabela do banco de dados. Gerar um novo arquivo de texto com os dados da tabela de 
# funcionários, organizados em ordem alfabética pelos nomes dos funcionários. O arquivo de texto deve utilizar o 
# formato: nome;idade;salario 


# IMPORTAR MÓDULOS
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# CONFIGURAR CONEXÃO COM BANCO DE DADOS SQLITE
engine = create_engine("sqlite:///server.db")
connection = engine.connect()

# INICIAR SESSÃO COM BANCO DE DADOS
session = Session()

# INSTANCIAR CLASSE BASE DO SQLALCHEMY
Base = declarative_base(engine)

connection.execute("""CREATE TABLE IF NOT EXISTS FUNCIONARIO (
                        ID INTEGER PRIMARY KEY,
                        NOME VARCHAR(255),
                        IDADE INTEGER,
                        SALARIO FLOAT)""")


# Classe que realiza o mapeamento da tabela de funcionários
class Funcionario(Base):
    __tablename__ = 'FUNCIONARIO'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('NOME', String(255))
    idade = Column('IDADE', Integer)
    salario = Column('SALARIO', Float)

    def __init__(self, nome, idade, salario):
        self.nome = nome
        self.idade = idade
        self.salario = salario


# Implemente o programa principal...

# Criar lista funcionarios

funcionarios = open('funcionarios.txt', 'r', encoding='UTF-8')
lista_func = []
dados_func = []
for linha in funcionarios:
    dados_fun = linha.split(';')
    nome = dados_fun[-3]
    idade = int(dados_fun[-2])
    salario = float(dados_fun[-1])
    func = Funcionario(nome, idade, salario)
    lista_func.append(func)

# Adicionar no BD

session.add_all(lista_func)
session.commit()

# Consultar BD

resultado = session.query(Funcionario)
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)

funcionarios.close()

funcionarios_ordenado = open('funcionarios.txt', 'w', encoding='UTF-8')
resultado2 = session.query(Funcionario).order_by(Funcionario.nome)
for obj in resultado2:
    funcionarios_ordenado.write(str(obj.nome) + ';' + str(obj.idade) + ';' + str(obj.salario) + '\n')

funcionarios_ordenado.close()
connection.close()
