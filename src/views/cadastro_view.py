import flet as ft
from src.controllers.auth_controller import criar_usuario
from src.utils.validation_utils import verifica_nome_correto, verifica_senha_correta, verifica_email_correto

def view(page: ft.Page):
    """Tela de cadastro."""
    texto_erro = ft.Text("", color="red")

    def cadastrar(e):
        """Função para cadastrar um novo usuário."""
        nome = campo_nome.value.strip()
        senha = campo_senha.value.strip()
        email = campo_email.value.strip()

        # Validações
        erro_nome = verifica_nome_correto(nome)
        erro_senha = verifica_senha_correta(senha)
        erro_email = verifica_email_correto(email)

        if erro_nome:
            texto_erro.value = erro_nome
        elif erro_senha:
            texto_erro.value = erro_senha
        elif erro_email:
            texto_erro.value = erro_email
        else:
            mensagem = criar_usuario(nome, senha, email)
            texto_erro.value = mensagem
            if "sucesso" in mensagem:
                page.go("/login")  # Redireciona para a tela de login após o cadastro
        
        page.update()

    campo_nome = ft.TextField(label="Nome", width=300)
    campo_senha = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)
    campo_email = ft.TextField(label="E-mail", width=300)

    return ft.View(
        "/cadastro",
        [
            ft.Text("Tela de Cadastro", size=20),
            campo_nome,
            campo_senha,
            campo_email,
            ft.ElevatedButton("Cadastrar", on_click=cadastrar),
            ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/login")),
            texto_erro,
        ]
    )