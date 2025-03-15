import os

BANCO_DE_USUARIOS = "bd/banco_de_usuarios.txt"

def carrega_usuarios():
    """Carrega todos os usuários do banco de dados."""
    if not os.path.exists(BANCO_DE_USUARIOS):
        return []
    
    with open(BANCO_DE_USUARIOS, mode='r') as arquivo:
        return [eval(linha.strip()) for linha in arquivo]

def criar_usuario(nome, senha, email):
    """Cria um novo usuário e seu diretório."""
    usuarios = carrega_usuarios()
    
    # Verifica se o usuário já existe
    if any(usuario["nome"] == nome for usuario in usuarios):
        return "Usuário já cadastrado."
    
    # Adiciona o novo usuário ao banco de dados
    novo_usuario = {"nome": nome, "senha": senha, "email": email}
    with open(BANCO_DE_USUARIOS, mode='a') as arquivo:
        arquivo.write(f"{novo_usuario}\n")
    
    # Cria o diretório do usuário e o arquivo de senhas
    diretorio_usuario = f"bd/{nome}"
    if not os.path.exists(diretorio_usuario):
        os.makedirs(diretorio_usuario)
    
    arquivo_senhas = f"{diretorio_usuario}/senhas.txt"
    with open(arquivo_senhas, mode='a') as arquivo:
        pass  # Cria o arquivo vazio
    
    return "Usuário cadastrado com sucesso."

def autenticar_usuario(nome, senha):
    """Autentica um usuário."""
    usuarios = carrega_usuarios()
    for usuario in usuarios:
        if usuario["nome"] == nome and usuario["senha"] == senha:
            return usuario
    return None