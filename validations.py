import re

"""
Módulo de Validações: Contém a lógica de negócio para verificação de 
integridade dos dados inseridos no sistema utilizando Table-Driven Validation.
"""

# --- Constantes de Configuração de Limites (Regras de Negócio) ---
NOME_MIN_CARACTERES = 3
NOME_MAX_CARACTERES = 50
SENHA_MIN_CARACTERES = 6
EMAIL_MAX_CARACTERES = 60
TELEFONE_REQUISITO_DIGITOS = 11
DDDS_VALIDOS = (
    # Região 1 (SP)
    "11", "12", "13", "14", "15", "16", "17", "18", "19",
    # Região 2 (RJ/ES)
    "21", "22", "24", "27", "28",
    # Região 3 (MG)
    "31", "32", "33", "34", "35", "37", "38",
    # Região 4 (PR/SC)
    "41", "42", "43", "44", "45", "46", "47", "48", "49",
    # Região 5 (RS)
    "51", "53", "54", "55",
    # Região 6 (CO)
    "61", "62", "64", "65", "66", "67",
    # Região 7 (Norte)
    "71", "73", "74", "75", "77", "79",
    # Região 8 (Nordeste)
    "81", "82", "83", "84", "85", "86", "87", "88", "89",
    # Região 9 (Norte/Nordeste)
    "91", "92", "93", "94", "95", "96", "97", "98", "99"
)


def validar_nome(nome_digitado):
    """Valida o nome utilizando uma lista de regras."""
    conteudo_limpo = nome_digitado.strip()

    regras = [
        (not conteudo_limpo, "Nome não pode estar vazio."),
        (len(conteudo_limpo) < NOME_MIN_CARACTERES, "Nome muito curto."),
        (
            not conteudo_limpo.replace(" ", "").isalpha(),
            "Nome deve conter apenas letras.",
        ),
        (len(conteudo_limpo) > NOME_MAX_CARACTERES, "Nome muito longo."),
    ]

    for erro, mensagem in regras:
        if erro:
            return False, mensagem
    return True, ""


def validar_telefone(telefone_digitado):
    """Valida o telefone completo removendo a máscara visual antes do teste."""
    # Remove os parênteses, hifens e espaços para validar apenas os 11 números puros
    conteudo_limpo = "".join(filter(str.isdigit, telefone_digitado))
    
    ddd_extraido = conteudo_limpo[:2] if len(conteudo_limpo) >= 2 else ""

    regras = [
        (not conteudo_limpo, "Telefone não pode estar vazio."),
        (
            len(conteudo_limpo) != TELEFONE_REQUISITO_DIGITOS, 
            f"O telefone deve conter exatamente {TELEFONE_REQUISITO_DIGITOS} dígitos numéricos."
        ),
        (
            ddd_extraido not in DDDS_VALIDOS, 
            "DDD inválido ou inexistente no Brasil."
        )
    ]

    for erro, mensagem in regras:
        if erro:
            return False, mensagem
            
    return True, ""


def validar_email(email_digitado):
    """Valida o e-mail utilizando uma lista de regras."""
    conteudo_limpo = email_digitado.strip()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|com\.br|net|org)$"

    regras = [
        (len(conteudo_limpo) == 0, "O e-mail não pode estar vazio."),
        (" " in email_digitado, "O e-mail não pode conter espaços."),
        (
            len(conteudo_limpo) > EMAIL_MAX_CARACTERES, f"O e-mail deve ter no máximo {EMAIL_MAX_CARACTERES} caracteres."
        ),
        (
            not re.match(pattern, conteudo_limpo), "E-mail inválido. Ex: abc@gmail.com"
        )
    ]

    for erro, mensagem in regras:
        if erro:
            return False, mensagem
    return True, ""


def validar_senha(senha_digitada):
    """Valida se a senha atende aos requisitos mínimos de segurança."""
    regras = [
        (not senha_digitada.strip(), "A senha não pode estar vazia."),
        (" " in senha_digitada, "A senha não pode conter espaços."),
        (
            len(senha_digitada) < SENHA_MIN_CARACTERES, f"Mínimo de {SENHA_MIN_CARACTERES} caracteres."
        ),
        (
            senha_digitada in ["123456", "654321", "admin123"],
            "A senha é muito óbvia.",
        ),
        (
            senha_digitada.isdigit() and senha_digitada in "1234567890",
            "Não use sequências simples.",
        ),
    ]

    for erro, mensagem in regras:
        if erro:
            return False, mensagem
    return True, ""


def validar_confirmacao_senha(senha_original, senha_repetida):
    """Verifica se a segunda senha é exatamente igual à primeira."""
    if not senha_repetida:
        return False, ""

    if senha_original != senha_repetida:
        return False, "As senhas não coincidem."
    return True, ""
