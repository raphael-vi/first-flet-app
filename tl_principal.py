import flet as ft
import controle as cont

def view():
    """Gera a tela principal com a lista de senhas do usuário logado."""

    def carregar_senhas(e):
        """Função chamada ao abrir a tela para garantir que as senhas foram carregadas."""
        if not hasattr(cont, 'senhas_usuario'):
            cont.carregar_senhas_usuario()
        cont.page.update()

    # Verifica se há um usuário logado antes de acessar a chave 'nome'
    usuario_logado = cont.conta_logada.get('nome')

    # Criando a tabela de senhas
    tabela = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Programa")),
        ft.DataColumn(ft.Text("Senha")),
        ft.DataColumn(ft.Text("Data de Criação/Renovação")),
        ft.DataColumn(ft.Text("Tamanho")),
        ft.DataColumn(ft.Text("Ações")),
    ])

    for senha in cont.senhas_usuario:
        tabela.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(senha['programa'])),
                ft.DataCell(ft.Text(senha['senha'])),
                ft.DataCell(ft.Text(senha['data'])),
                ft.DataCell(ft.Text(str(senha['tamanho']))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, p=senha['programa']: cont.deletar_senha(p)),
                        ft.IconButton(icon=ft.icons.REFRESH, on_click=lambda e, p=senha['programa']: cont.renovar_senha(p)),
                    ])
                ),
            ])
        )

    return ft.View(
        "tela principal",
        [
            ft.Text(f"Gerenciamento de Senhas - Usuário: {usuario_logado}", size=20),
            ft.ElevatedButton("Carregar Senhas", on_click=carregar_senhas),
            tabela,
            ft.ElevatedButton("Cadastrar Nova Senha", on_click=lambda e: cont.page.go("3")),
        ]
    )
