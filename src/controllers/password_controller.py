import os
import random
import string
from datetime import datetime

def carregar_senhas_usuario(nome_usuario):
    """Carrega as senhas do usuário."""
    arquivo_senhas = f"bd/{nome_usuario}/senhas.txt"
    if not os.path.exists(arquivo_senhas):
        return []
    
    with open(arquivo_senhas, mode='r') as arquivo:
        return [eval(linha.strip()) for linha in arquivo]

def cadastrar_senha(nome_usuario, programa, senha, tamanho):
    """Cadastra uma nova senha para o usuário."""
    arquivo_senhas = f"bd/{nome_usuario}/senhas.txt"
    diretorio_usuario = f"bd/{nome_usuario}"

    # Verifica se o diretório do usuário existe
    if not os.path.exists(diretorio_usuario):
        os.makedirs(diretorio_usuario)
        #o        

    nova_senha = {
        "programa": programa,
        "senha": senha,
        "tamanho": tamanho,
        "data": datetime.now().strftime("%Y-%m-%d")
    }
    
    with open(arquivo_senhas, mode='a') as arquivo:
        arquivo.write(f"{nova_senha}\n")
    
    return "Senha cadastrada com sucesso."

def deletar_senha(nome_usuario, programa):
    """Deleta uma senha do usuário."""
    senhas = carregar_senhas_usuario(nome_usuario)
    senhas = [senha for senha in senhas if senha["programa"].lower() != programa.lower()]
    
    arquivo_senhas = f"bd/{nome_usuario}/senhas.txt"
    with open(arquivo_senhas, mode='w') as arquivo:
        for senha in senhas:
            arquivo.write(f"{senha}\n")
    
    return "Senha deletada com sucesso."

def gerar_senha_aleatoria(tamanho):
    """Gera uma senha aleatória com o tamanho especificado."""
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-+="
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def renovar_senha_usuario(nome_usuario, programa):
    """Renova a senha de um programa específico."""
    diretorio_usuario = f"bd/{nome_usuario}"
    arquivo_senhas = f"{diretorio_usuario}/senhas.txt"

    # Verifica se o arquivo de senhas existe
    if not os.path.exists(arquivo_senhas):
        return "Erro: Nenhuma senha cadastrada para este usuário."

    # Carrega as senhas do usuário
    with open(arquivo_senhas, mode='r') as arquivo:
        senhas = [eval(linha.strip()) for linha in arquivo]

    # Encontra a senha correspondente ao programa
    senha_antiga = None
    for senha in senhas:
        if senha["programa"].lower() == programa.lower():
            senha_antiga = senha
            break

    if not senha_antiga:
        return f"Erro: Nenhuma senha cadastrada para o programa '{programa}'."

    # Gera uma nova senha com o mesmo tamanho da senha antiga
    nova_senha = gerar_senha_aleatoria(senha_antiga["tamanho"])

    # Atualiza a senha no arquivo
    senhas_atualizadas = []
    for senha in senhas:
        if senha["programa"].lower() == programa.lower():
            senha["senha"] = nova_senha
            senha["data"] = datetime.now().strftime("%Y-%m-%d")
        senhas_atualizadas.append(senha)

    # Salva as senhas atualizadas no arquivo
    with open(arquivo_senhas, mode='w') as arquivo:
        for senha in senhas_atualizadas:
            arquivo.write(f"{senha}\n")

    return f"Senha renovada com sucesso para o programa '{programa}'."