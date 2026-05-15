import secrets
import hashlib
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

PIMENTA_SECRETA = "MakEstoque_ChaveSecreta_9x8f7g6h5j4k3m2n1p_2026!"

# --- Operações de Banco de Dados ---

def conexao_database(nome, email, telefone, senha_pura, cargo):
    """
    Estabelece conexão com o SQLite, garante a tabela com tratamento de restrições
    e realiza a inserção da senha criptografada em formato Hash SHA-256.
    """
    senha_tempero = secrets.token_hex(8) 
    senha_temperada = senha_pura + senha_tempero + PIMENTA_SECRETA
    senha_criptografada = hashlib.sha256(senha_temperada.encode("utf-8")).hexdigest()
    
    conn = None
    try:
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()

        # Garante que a tabela exista antes da inserção
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS tb_usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                V_NOME VARCHAR (30),
                V_EMAIL VARCHAR (30) UNIQUE,
                C_TELEFONE CHAR (11),
                V_SENHA VARCHAR (64),
                V_SAL VARCHAR (16),
                C_CARGO CHAR (01)
            ) 
        """)

        # Insere os dados validados no banco
        cursor.execute(
            """ 
            INSERT INTO tb_usuarios (V_NOME, V_EMAIL, C_TELEFONE, V_SENHA, V_SAL, C_CARGO)
            VALUES (?, ?, ?, ?, ?, ?) 
            """,
            (nome, email, telefone, senha_criptografada, senha_tempero, cargo)
        )

        conn.commit()
        return True, "Dados salvos com sucesso!"
    
    except sqlite3.IntegrityError:
        return False, "Erro: Este e-mail já está cadastrado no sistema"
    
    except sqlite3.Error as erro:
        return False, f"Erro interno no banco de dados: {erro}"

    finally:
        if conn:
            conn.close()



def confirmar_acesso(email_digitado, senha_digitada):

    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    cursor.execute(
                    """
                    SELECT V_EMAIL, V_SENHA, V_SAL, C_CARGO
                    FROM tb_usuarios
                    WHERE V_EMAIL = ? 
                    
                    """,
                    (email_digitado,)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return False, "Usuário não encontrado!", None

    verificar_senha = senha_digitada + resultado[2] + PIMENTA_SECRETA
    hash_calculada = hashlib.sha256(verificar_senha.encode("utf-8")).hexdigest()
    
    if hash_calculada == resultado[1]:
        conn.close()
        return True, "Acesso concedido!", resultado[3]
    else:
        conn.close()
        return False, "Acesso negado!", None