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

def conexao_database(nome, ddd, fone, email):
    """
    Estabelece conexão com o SQLite, garante a existência da tabela e realiza a inserção.
    
    :param nome: String contendo o nome do usuário.
    :param ddd: String contendo o DDD (2 dígitos).
    :param fone: String contendo o telefone (9 dígitos).
    :param email: String contendo o e-mail validado.
    """
    # Abre a conexão com o arquivo de banco de dados
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    # DDL (Data Definition Language): Garante que a tabela exista antes da inserção
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tb_pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            T_NOME TEXT (30),
            T_DDD TEXT (2),
            T_TELEFONE TEXT (14),
            T_EMAIL TEXT (30)
        ) 
    """)

    # DML (Data Manipulation Language): Insere os dados validados no banco
    cursor.execute(""" 
        INSERT INTO tb_pessoas (T_NOME, T_DDD, T_TELEFONE, T_EMAIL) 
        VALUES (?, ?, ?, ?) 
    """, (nome, ddd, fone, email))

    # Confirma a transação e encerra a conexão para liberar o arquivo
    conn.commit()
    conn.close()
