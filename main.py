import flet as ft
import controle as cont

def main(page: ft.Page):   
    cont.iniciar(page)

    page.title = "Sistema de Gerenciamento de Senhas"           
    page.on_route_change = cont.controle_mudar_view  
    page.theme_mode = "dark"
    page.go("1")  # Começando na tela de login

ft.app(target=main)
