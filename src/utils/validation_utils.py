import re
from datetime import datetime

def verifica_email_correto(email: str):
    """Valida o formato do e-mail."""
    email = email.lower().strip()
    if not re.fullmatch(r"[0-9a-z_\.]+@[a-z]+\.[a-z]+(\.[a-z]+)*", email):
        return "E-mail inválido."
    return ""

def verifica_telefone_correto(telefone: str):
    """Valida o formato do telefone."""
    telefone = telefone.strip()
    if not re.fullmatch(r"[1-9]{2}9[0-9]{8}", telefone):
        return "Telefone inválido."
    return ""

def verifica_nome_correto(nome: str):
    """Valida o formato do nome."""
    if re.findall(r"([^A-Za-z ]|[ ]{2,})", nome):
        return "Nome inválido. Apenas letras e espaços simples são permitidos."
    return ""

def verifica_idade_correta(ano: str, mes: str, dia: str):
    """Valida a data de nascimento."""
    agora = datetime.now()
    try:
        data_nasc = datetime(int(ano), int(mes), int(dia))
        if agora < data_nasc:
            return "Data de nascimento inválida."
    except ValueError:
        return "Data de nascimento inválida."
    return ""

def verifica_senha_correta(senha: str):
    """Valida a força da senha."""
    if len(senha) < 6:
        return "A senha deve ter pelo menos 6 caracteres."
    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r"[a-z]", senha):
        return "A senha deve conter pelo menos uma letra minúscula."
    if not re.search(r"\d", senha):
        return "A senha deve conter pelo menos um número."
    if not re.search(r"[!@#$%^&*()-+=]", senha):
        return "A senha deve conter pelo menos um caractere especial (!@#$%^&*()-+=)."
    return ""