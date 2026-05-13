import sqlite3
import os

# --- Configuração de Caminho e Ambiente ---

# Define o caminho base como a pasta onde este script está localizado
pasta_atual = os.path.dirname(__file__)

# Define e cria a subpasta 'data' para isolar o banco de dados do código-fonte
pasta_data = os.path.join(pasta_atual, "data")
if not os.path.exists(pasta_data):
    os.makedirs(pasta_data)

# Caminho absoluto final para o banco de dados (garante portabilidade entre sistemas)
caminho_db = os.path.join(pasta_data, "cadastro.db")


# --- Operações de Banco de Dados ---

def conexao_database(nome, email, senha, cargo):
    # Abre a conexão com o arquivo de banco de dados
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    # DDL (Data Definition Language): Garante que a tabela exista antes da inserção
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tb_usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            V_NOME VARCHAR (30),
            V_EMAIL VARCHAR (30),
            V_SENHA VARCHAR (30),
            C_CARGO CHAR (01)
        ) 
    """)

    # DML (Data Manipulation Language): Insere os dados validados no banco
    cursor.execute(""" 
        INSERT INTO tb_usuarios (V_NOME, V_EMAIL, V_SENHA, C_CARGO)
        VALUES (?, ?, ?, ?) 
    """, (nome, email, senha, cargo))

    # Confirma a transação e encerra a conexão para liberar o arquivo
    conn.commit()
    conn.close()
