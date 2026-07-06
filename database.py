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
    

# =====================================================================
# OPERAÇÕES DO ESTOQUE (PRODUTOS)
# =====================================================================
def initialize_products_table():
    """Cria a tabela de estoque flexível no banco caso ela ainda não exista."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            V_NAME VARCHAR(50) NOT NULL,
            I_QUANTIDADE INTEGER NOT NULL,
            D_PRICE_SALE REAL NOT NULL,
            
            -- Campos flexíveis/opcionais (Aceitam NULL)
            V_BARCODE VARCHAR(30) NULL UNIQUE,
            V_BATCH VARCHAR(30) NULL,
            V_EXPIRY_DATE VARCHAR(10) NULL,
            D_PRICE_COST REAL NULL
        )
    """)
    conn.commit()
    conn.close()


def db_save_new_product(name, qty, price_sale, barcode=None, batch=None, expiry=None, price_cost=None):
    """Insere um novo produto no banco. Trata valores opcionais vazios de forma limpa."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Garante a existência da tabela antes de qualquer inserção
        initialize_products_table()

        # Converte strings vazias vindas da interface em None (NULL no SQLite)
        final_barcode = barcode if barcode and barcode.strip() else None
        final_batch = batch if batch and batch.strip() else None
        final_expiry = expiry if expiry and expiry.strip() else None
        
        try:
            final_cost = float(price_cost.strip().replace(",", ".")) if price_cost else None
        except (ValueError, AttributeError):
            final_cost = None

        cursor.execute(
            """
            INSERT INTO tb_products (V_NAME, I_QUANTIDADE, D_PRICE_SALE, V_BARCODE, V_BATCH, V_EXPIRY_DATE, D_PRICE_COST)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, qty, price_sale, final_barcode, final_batch, final_expiry, final_cost)
        )
        
        # Estratégia de ID Inteligente: Se o lojista não informou código de barras, 
        # preenchemos a coluna automaticamente usando o ID sequencial que o banco acabou de gerar (Ex: "INT-1")
        product_id = cursor.lastrowid
        if not final_barcode:
            cursor.execute(
                "UPDATE tb_products SET V_BARCODE = ? WHERE id = ?",
                (f"INT-{product_id}", product_id)
            )

        conn.commit()
        return True, "Produto cadastrado com sucesso!"
        
    except sqlite3.IntegrityError:
        return False, "Erro: Este código de barras já está associado a outro produto."
    except sqlite3.Error as error:
        return False, f"Erro interno no banco de dados: {error}"
    finally:
        if conn:
            conn.close()


def db_list_products(search_term=""):
    """Busca produtos no banco aplicando um filtro parcial pelo nome ou pelo código de barras."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    initialize_products_table()

    # Busca inteligente: filtra se o termo bater com o nome OU com o código de barras
    if search_term and search_term.strip():
        query_filter = f"%{search_term.strip()}%"
        cursor.execute(
            """
            SELECT id, V_NAME, I_QUANTIDADE, D_PRICE_SALE, V_BARCODE 
            FROM tb_products 
            WHERE V_NAME LIKE ? OR V_BARCODE LIKE ?
            """,
            (query_filter, query_filter)
        )
    else:
        cursor.execute("SELECT id, V_NAME, I_QUANTIDADE, D_PRICE_SALE, V_BARCODE FROM tb_products")
        
    results = cursor.fetchall()
    conn.close()
    
    # Converte os registros do SQLite (tuplas) de volta para o formato de dicionário
    products_mapped = []
    for row in results:
        products_mapped.append({
            "id": str(row[0]),
            "name": row[1],
            "qty": row[2],
            "price": row[3],
            "barcode": row[4]
        })
        
    return products_mapped


def db_quick_increment_stock(product_id):
    """Localiza o produto pelo ID no SQLite e soma +10 unidades fisicamente no arquivo."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tb_products SET I_QUANTIDADE = I_QUANTIDADE + 10 WHERE id = ?",
            (product_id,)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def db_update_product(product_id, name, qty, price_sale, barcode, batch, expiry, price_cost):
    """Atualiza as informações de um produto existente no banco de dados."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Converte strings vazias em NULL para manter a integridade dos opcionais
        final_barcode = barcode if barcode and barcode.strip() else f"INT-{product_id}"
        final_batch = batch if batch and batch.strip() else None
        final_expiry = expiry if expiry and expiry.strip() else None
        
        try:
            final_cost = float(price_cost.strip().replace(",", ".")) if price_cost else None
        except (ValueError, AttributeError):
            final_cost = None

        cursor.execute(
            """
            UPDATE tb_products 
            SET V_NAME = ?, I_QUANTIDADE = ?, D_PRICE_SALE = ?, 
                V_BARCODE = ?, V_BATCH = ?, V_EXPIRY_DATE = ?, D_PRICE_COST = ?
            WHERE id = ?
            """,
            (name, qty, price_sale, final_barcode, final_batch, final_expiry, final_cost, product_id)
        )
        conn.commit()
        return True, "Produto atualizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Este código de barras já pertence a outro produto."
    except sqlite3.Error as error:
        return False, f"Erro interno no banco de dados: {error}"
    finally:
        conn.close()
