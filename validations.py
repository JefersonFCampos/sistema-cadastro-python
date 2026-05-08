import re

"""
Módulo de Validações:
Contém a lógica de negócio para verificação de integridade dos dados inseridos no sistema.
Utiliza o padrão de 'Early Return' para garantir que cada regra seja atendida.
"""

def validar_nome(nome_digitado):
    """
    Valida se o nome contém apenas caracteres alfabéticos e não está vazio.
    """
    nome_digitado = nome_digitado.strip()
    
    if not nome_digitado:
        return False, "Nome não pode estar vazio."
        
    # Remove espaços para verificar se o restante é apenas letra
    if not nome_digitado.replace(" ", "").isalpha():
        return False, "Nome pode conter apenas letras."
        
    return True, ""


def validar_ddd(ddd_digitado):
    """
    Valida se o DDD possui exatamente 2 caracteres numéricos e não está vazio.
    """
    ddd_digitado = ddd_digitado.strip()
    
    if not ddd_digitado:
        return False, "DDD não pode ficar vazio."
        
    if not ddd_digitado.isdigit():
        return False, "DDD deve conter apenas números."
        
    if len(ddd_digitado) != 2:
        return False, "DDD deve conter apenas 2 dígitos. Exemplo: 51"
        
    return True, ""


def validar_telefone(telefone_digitado):
    """
    Valida se o telefone possui exatamente 9 caracteres numéricos e não está vazio.
    """
    telefone_digitado = telefone_digitado.strip()
    
    if not telefone_digitado:
        return False, "Telefone não pode estar vazio."
        
    if not telefone_digitado.isdigit():
        return False, "Telefone deve conter apenas números."
        
    if len(telefone_digitado) != 9:
        return False, "Telefone deve conter 9 dígitos. Exemplo: 999999999"
        
    return True, ""


def validar_email(email_digitado):
    """
    Valida o formato do e-mail utilizando Expressões Regulares (Regex).
    Padrão: usuário@domínio.extensão
    """
    # Regex para validação de e-mail padrão RFC 5322
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not re.match(pattern, email_digitado.strip()):
        return False, "E-mail inválido. Exemplo: abc@gmail.com"
        
    return True, ""
