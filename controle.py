import flet as ft
import tl_cadastro, tl_login
from datetime import datetime
from hashlib import sha3_256
import time
import os

BANCO_DE_USUARIOS = "bd/banco_de_usuarios.txt"
BANCO_DE_SENHAS = "bd/banco_de_senhas.txt"

# Variáveis globais
senhas_usuario = []  # Armazena temporariamente as senhas do usuário logado
conta_logada = {}  # Usuário que está logado no momento

def iniciar(pagina):
    """Set inicial das paginas/views"""
    global page, telas, banco_cad, conta_logada
    
    import tl_principal 
    #To importando a tl_principal aqui porque causa um erro de import circular, a tl_principal importa essa e essa a tela principal
    
    if not conta_logada:
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
        with open(BANCO_DE_USUARIOS, mode='r') as bd:  # Arquivo já existe  
            return [eval(linha.strip()) for linha in bd.readlines()]  # Retornando o banco de dados como uma lista de dicionários
    except FileNotFoundError:
        with open(BANCO_DE_USUARIOS, mode="x") as bd:
            pass
        return []

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def criar_usuario_bd(usuario):
    """Adiciona um novo usuário ao banco de dados e cria o diretório para o usuário"""
    
    nome_usuario = usuario.get("nome")
    
    # Caminho do arquivo do banco de usuários
    caminho_usuarios = BANCO_DE_USUARIOS  # Banco de dados de usuários
    
    # Criar diretório para o usuário (se não existir)
    caminho_diretorio_usuario = f"bd/{nome_usuario}"  # Caminho do diretório do usuário
    if not os.path.exists(caminho_diretorio_usuario):
        os.makedirs(caminho_diretorio_usuario)  # Cria o diretório para o usuário
    
    # Caminho do arquivo de senhas dentro do diretório do usuário
    caminho_senhas = f"{caminho_diretorio_usuario}/senhas.txt"
    
    # Adiciona o novo usuário no banco de dados de usuários
    with open(caminho_usuarios, mode='a') as bd:
        bd.write(f"{usuario}\n")
    
    # Cria o arquivo de senhas se ele não existir
    with open(caminho_senhas, mode='a') as arquivo:
        pass  # Não precisamos fazer nada aqui além de garantir que o arquivo exista
    
    # Retorna a lista de usuários atualizada
    return carrega_bd()  # Atualiza a lista de usuários

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def atualizar_usuario_bd(lista):
    """Substitui todos os usuários do banco de dados pelo novo conteúdo"""
    with open(BANCO_DE_USUARIOS, mode='w') as bd:
        for usuario in lista:
            bd.write(f"{usuario}\n")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def carregar_senhas_usuario(usuario):
    
    """Carrega apenas as senhas do usuário logado na memória."""
    nome_usuario = usuario.get("nome")  # Pega o nome do usuário
    if not nome_usuario:
        return []  # Se o nome do usuário não existir, retorna uma lista vazia
    
    # Definindo o caminho do arquivo do usuário (supondo que seja um arquivo de texto)
    caminho_arquivo = f'bd/{nome_usuario}/senhas.txt'  # Ajuste o caminho conforme sua estrutura

    try:
        # Abre o arquivo que contém as senhas do usuário
        with open(caminho_arquivo, mode="r") as senhas:
            # Retorna todas as senhas armazenadas no arquivo
            return [linha.strip() for linha in senhas]  # Usa .strip() para remover quebras de linha extras
    except FileNotFoundError:
        # Se o arquivo não for encontrado, retorna uma lista vazia
        print(f"Arquivo de senhas para o usuário {nome_usuario} não encontrado.")
        return []



def salvar_senhas():
    """Salva apenas as senhas do usuário logado no banco, sem apagar as dos outros usuários."""
    try:
        with open(BANCO_DE_USUARIOS, mode="r") as bd:
            todas_senhas = [eval(linha.strip()) for linha in bd.readlines()]
    except FileNotFoundError:
        todas_senhas = []
    
    # Remover as senhas do usuário logado para sobrescrever corretamente
    todas_senhas = [s for s in todas_senhas if s['usuario'] != conta_logada.get('nome')]

    # Adicionar as novas senhas do usuário logado
    todas_senhas.extend(senhas_usuario)

    # Salvar no arquivo
    with open(BANCO_DE_USUARIOS, mode="w") as bd:
        for senha in todas_senhas:
            bd.write(f"{senha}\n")



def cadastrar_senha(programa, tamanho, senha):
    """Salva a senha do usuário logado diretamente no arquivo de senhas do usuário."""
    if not conta_logada:
        return "Erro: Nenhum usuário logado."

    nome_usuario = conta_logada.get("nome")
    if not nome_usuario:
        return "Erro: Usuário não encontrado."
    
    # Caminho para o arquivo de senhas do usuário
    caminho_arquivo = f'bd/{nome_usuario}/senhas.txt'

    # Verifica se já existe uma senha cadastrada para o programa
    if not os.path.exists(f"bd/{nome_usuario}"):  # Verifica se o diretório do usuário existe
        os.makedirs(f"bd/{nome_usuario}")  # Cria o diretório para o usuário, se não existir

    try:
        # Abre o arquivo para adicionar a nova senha
        with open(caminho_arquivo, mode="a") as arquivo:
            arquivo.write(f"Programa: {programa} | Senha: {senha} | Tamanho: {tamanho}\n")  # Adiciona a senha ao arquivo

        return "Senha cadastrada com sucesso!"  # Mensagem de sucesso
    
    except Exception as e:
        return f"Erro ao salvar a senha: {str(e)}"  # Caso ocorra um erro, retorna a mensagem de erro


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
