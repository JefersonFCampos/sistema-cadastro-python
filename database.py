import secrets
import hashlib
import sqlite3
import os

# --- Configuração de Caminho e Ambiente ---

# Define o caminho base como a pasta onde este script está localizado
current_dir = os.path.dirname(__file__)

# Define e cria a subpasta 'data' para isolar o banco de dados do código-fonte
data_dir = os.path.join(current_dir, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Caminho absoluto final para o banco de dados (garante portabilidade entre sistemas)
db_path = os.path.join(data_dir, "singusers.db")

SECRET_PEPPER = "MakEstoque_ChaveSecreta_9x8f7g6h5j4k3m2n1p_2026!"

# --- Operações de Banco de Dados ---

def save_user(name, email, phone, password, role):
    """
    Estabelece conexão com o SQLite, garante a tabela com tratamento de restrições
    e realiza a inserção da senha criptografada em formato Hash SHA-256.
    """
    password_salt = secrets.token_hex(8) 
    salted_password = password + password_salt + SECRET_PEPPER
    hashed_password = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Garante que a tabela exista antes da inserção
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS tb_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                V_NAME VARCHAR (30),
                V_EMAIL VARCHAR (30) UNIQUE,
                C_PHONE CHAR (11),
                V_PASSWORD_HASH VARCHAR (64),
                V_SALT VARCHAR (16),
                C_ROLE CHAR (01)
            ) 
        """)

        # Insere os dados validados no banco
        cursor.execute(
            """ 
            INSERT INTO tb_users (V_NAME, V_EMAIL, C_PHONE, V_PASSWORD_HASH, V_SALT, C_ROLE)
            VALUES (?, ?, ?, ?, ?, ?) 
            """,
            (name, email, phone, hashed_password, password_salt, role)
        )

        conn.commit()
        return True, "Dados salvos com sucesso!"
    
    except sqlite3.IntegrityError:
        return False, "Erro: Este e-mail já está cadastrado no sistema"
    
    except sqlite3.Error as error:
        return False, f"Erro interno no banco de dados: {error}"

    finally:
        if conn:
            conn.close()



def confirm_access(email_input, password_input):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
                    """
                    SELECT V_EMAIL, V_PASSWORD_HASH, V_SALT, C_ROLE
                    FROM tb_users
                    WHERE V_EMAIL = ? 
                    
                    """,
                    (email_input,)
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False, "Usuário não encontrado!", None

    check_password = password_input + result[2] + SECRET_PEPPER
    hash_calculada = hashlib.sha256(check_password.encode("utf-8")).hexdigest()
    
    if hash_calculada == result[1]:
        conn.close()
        return True, "Acesso concedido!", result[3]
    else:
        conn.close()
        return False, "Acesso negado!", None
    