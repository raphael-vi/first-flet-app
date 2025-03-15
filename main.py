import flet as ft
from src.views.login_view import view as login_view
from src.views.cadastro_view import view as cadastro_view
from src.views.principal_view import view as principal_view

def main(page: ft.Page):
    """Função principal que configura a aplicação."""
    # Configurações da página
    page.title = "Sistema de Gerenciamento de Senhas"
    page.theme_mode = "dark"  # Tema escuro
    page.padding = 20

    def route_change(route):
        """Gerencia a mudança de rotas (telas)."""
        page.views.clear()

        # Tela de Login
        if page.route == "/login" or page.route == "/":
            page.views.append(login_view(page))

        # Tela de Cadastro
        elif page.route == "/cadastro":
            page.views.append(cadastro_view(page))

        # Tela Principal
        elif page.route == "/principal":
            page.views.append(principal_view(page))

        # Atualiza a página para exibir a view correta
        page.update()

    # Configura o gerenciador de rotas
    page.on_route_change = route_change

    # Inicia a aplicação na tela de login
    page.go("/login")

# Inicia a aplicação
ft.app(target=main)