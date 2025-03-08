import flet as ft
import tl_cadastro, tl_login
from datetime import datetime
from hashlib import sha3_256
import time

# Variáveis globais
senhas_usuario = []  # Armazena temporariamente as senhas do usuário logado
conta_logada = {}  # Usuário que está logado no momento

def iniciar(pagina):
    """Set inicial das paginas/views"""
    global page, telas, banco_cad, conta_logada
    
    import tl_principal 
    #To importando a tl_principal aqui porque causa um erro de import circular, a tl_principal importa essa e essa a tela principal
    
    
    conta_logada = {}
    banco_cad = []
    page = pagina
    telas = {
        '1': tl_login.view(),
        '2': tl_cadastro.view(),
        '3': tl_principal.view(),  # Agora a tela principal é registrada corretamente
    }
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def controle_mudar_view(route_event):
    """Funcao que muda de view"""
    page.views.clear()    
    page.views.append(telas[route_event.route])          
    page.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def carrega_bd():
    try:
        with open('banco_de_dados', mode='r') as bd:  # Arquivo já existe  
            return [eval(linha.strip()) for linha in bd.readlines()]  # Retornando o banco de dados como uma lista de dicionários
    except FileNotFoundError:
        with open("banco_de_dados", mode="x") as bd:
            pass
        return []

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def criar_usuario_bd(usuario):
    """Adiciona um novo usuário ao banco de dados"""
    with open('banco_de_dados', mode='a') as bd:
        bd.write(f"{usuario}\n")
    return carrega_bd()  # Atualiza a lista de usuários

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def atualizar_usuario_bd(lista):
    """Substitui todos os usuários do banco de dados pelo novo conteúdo"""
    with open('banco_de_dados', mode='w') as bd:
        for usuario in lista:
            bd.write(f"{usuario}\n")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def carregar_senhas_usuario():
    """Carrega apenas as senhas do usuário logado na memória."""
    global senhas_usuario
    try:
        with open("banco_senhas", mode="r") as bd:
            todas_senhas = [eval(linha.strip()) for linha in bd.readlines()]
            senhas_usuario = [s for s in todas_senhas if s['usuario'] == conta_logada.get('nome')]
    except FileNotFoundError:
        senhas_usuario = []

def salvar_senhas():
    """Salva apenas as senhas do usuário logado no banco, sem apagar as dos outros usuários."""
    try:
        with open("banco_senhas", mode="r") as bd:
            todas_senhas = [eval(linha.strip()) for linha in bd.readlines()]
    except FileNotFoundError:
        todas_senhas = []

    # Remover as senhas do usuário logado para sobrescrever corretamente
    todas_senhas = [s for s in todas_senhas if s['usuario'] != conta_logada.get('nome')]

    # Adicionar as novas senhas do usuário logado
    todas_senhas.extend(senhas_usuario)

    # Salvar no arquivo
    with open("banco_senhas", mode="w") as bd:
        for senha in todas_senhas:
            bd.write(f"{senha}\n")

def deletar_senha(programa):
    """Remove uma senha do usuário logado."""
    global senhas_usuario
    senhas_usuario = [s for s in senhas_usuario if s['programa'].lower() != programa.lower()]
    salvar_senhas()

def renovar_senha(programa):
    """Gera uma nova senha para o programa do usuário logado usando SHA3."""
    for senha in senhas_usuario:
        if senha['programa'].lower() == programa.lower():
            entrada = senha['programa'] + conta_logada.get('nome', '') + str(time.time())
            senha['senha'] = sha3_256(entrada.encode()).hexdigest()[:senha['tamanho']]
            senha['data'] = datetime.now().strftime("%Y-%m-%d")
            break
    salvar_senhas()
