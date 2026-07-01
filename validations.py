import re

"""
Módulo de Validações: Contém a lógica de negócio para verificação de 
integridade dos dados inseridos no sistema utilizando Table-Driven Validation.
"""

# --- Constantes de Configuração de Limites (Regras de Negócio) ---
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 6
MAX_EMAIL_LENGTH = 60
PHONE_DIGIT_REQUIREMENT = 11
VALID_DDDS = (
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


def validate_name(name_input):
    """Valida o nome utilizando uma lista de regras."""
    clean_content = name_input.strip()

    rules = [
        (not clean_content, "Nome não pode estar vazio."),
        (len(clean_content) < MIN_NAME_LENGTH, "Nome muito curto."),
        (
            not clean_content.replace(" ", "").isalpha(),
            "Nome deve conter apenas letras.",
        ),
        (len(clean_content) > MAX_NAME_LENGTH, "Nome muito longo."),
    ]

    for error, message in rules:
        if error:
            return False, message
    return True, ""


def validate_phone(phone_input):
    """Valida o telefone completo removendo a máscara visual antes do teste."""
    # Remove os parênteses, hifens e espaços para validar apenas os 11 números puros
    clean_content = "".join(filter(str.isdigit, phone_input))
    
    extracted_ddd = clean_content[:2] if len(clean_content) >= 2 else ""

    rules = [
        (not clean_content, "Telefone não pode estar vazio."),
        (
            len(clean_content) != PHONE_DIGIT_REQUIREMENT, 
            f"O telefone deve conter exatamente {PHONE_DIGIT_REQUIREMENT} dígitos numéricos."
        ),
        (
            extracted_ddd not in VALID_DDDS, 
            "DDD inválido ou inexistente no Brasil."
        )
    ]

    for error, message in rules:
        if error:
            return False, message           
    return True, ""


def validate_email(email_input):
    """Valida o e-mail utilizando uma lista de regras."""
    clean_content = email_input.strip()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|com\.br|net|org)$"

    rules = [
        (len(clean_content) == 0, "O e-mail não pode estar vazio."),
        (" " in email_input, "O e-mail não pode conter espaços."),
        (
            len(clean_content) > MAX_EMAIL_LENGTH, f"O e-mail deve ter no máximo {MAX_EMAIL_LENGTH} caracteres."
        ),
        (
            not re.match(pattern, clean_content), "E-mail inválido. Ex: abc@gmail.com"
        )
    ]

    for error, message in rules:
        if error:
            return False, message
    return True, ""


def validate_password(password_input):
    """Valida se a senha atende aos requisitos mínimos de segurança."""
    rules = [
        (not password_input.strip(), "A senha não pode estar vazia."),
        (" " in password_input, "A senha não pode conter espaços."),
        (
            len(password_input) < MIN_PASSWORD_LENGTH, f"Mínimo de {MIN_PASSWORD_LENGTH} caracteres."
        ),
        (
            password_input in ["123456", "654321", "admin123"],
            "A senha é muito óbvia.",
        ),
        (
            password_input.isdigit() and password_input in "1234567890",
            "Não use sequências simples.",
        ),
    ]

    for error, message in rules:
        if error:
            return False, message
    return True, ""


def confirm_password_match(original_password, repeated_password):
    """Verifica se a segunda senha é exatamente igual à primeira."""
    if not repeated_password:
        return False, ""

    if original_password != repeated_password:
        return False, "As senhas não coincidem."
    return True, ""
