import flet as ft
from src.controllers.auth_controller import autenticar_usuario
from src.views.principal_view import view as principal_view

def view(page: ft.Page):
    """Tela de login."""
    texto_erro = ft.Text("", color="red")

    def logar(e):
        """Função para autenticar o usuário."""
        nome = campo_nome.value.strip()
        senha = campo_senha.value.strip()

        if not nome or not senha:
            texto_erro.value = "Nome e senha são obrigatórios."
        else:
            usuario = autenticar_usuario(nome, senha)
            if usuario:
                texto_erro.value = "Login realizado com sucesso!"
                page.session.set("usuario_logado", usuario)  # Armazena o usuário logado na sessão
                page.go("/principal")  # Redireciona para a tela principal
            else:
                texto_erro.value = "Usuário ou senha incorretos."
        
        page.update()

    campo_nome = ft.TextField(label="Nome", width=300)
    campo_senha = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)

    return ft.View(
        "/login",
        [
            ft.Text("Tela de Login", size=20),
            campo_nome,
            campo_senha,
            ft.ElevatedButton("Entrar", on_click=logar),
            ft.ElevatedButton("Criar Conta", on_click=lambda e: page.go("/cadastro")),
            texto_erro,
        ]
    )