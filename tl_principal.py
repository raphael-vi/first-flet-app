import flet as ft
import controle as cont

def view():
    """Gera a tela principal com a lista de senhas do usuário logado."""

    def carregar_senhas(e):
        """Função chamada ao abrir a tela para garantir que as senhas foram carregadas."""
        if not hasattr(cont, 'senhas_usuario'):
            cont.carregar_senhas_usuario()
        cont.page.update()

    def abrir_dialogo_cadastro(e):
        """Abre o pop-up de cadastro de senha"""
        cont.page.dialog = dialogo_cadastro  # Agora usamos cont.page.dialog corretamente
        dialogo_cadastro.open = True
        cont.page.update()  # Atualiza a interface para exibir o pop-up

    def confirmar_cadastro(e):
        """Executa o cadastro de senha"""
        programa = campo_programa.value.strip()
        tamanho = campo_tamanho.value.strip()
        senha = campo_senha.value.strip()  # Captura o valor da senha inserida

        if not programa:
            resultado_erro.value = "Erro: O nome do programa não pode ser vazio."
        elif not tamanho.isdigit() or int(tamanho) < 4:
            resultado_erro.value = "Erro: O tamanho da senha deve ser um número maior que 3."
        elif not senha:
            resultado_erro.value = "Erro: A senha não pode ser vazia."  # Verificação se a senha não é vazia
        else:
            # Chama a função de cadastro de senha passando o programa, tamanho e a senha
            mensagem = cont.cadastrar_senha(programa, int(tamanho), senha)
            resultado_erro.value = mensagem
            if "sucesso" in mensagem:
                campo_programa.value = ""
                campo_tamanho.value = ""
                campo_senha.value = ""  # Limpa o campo de senha após o cadastro
                dialogo_cadastro.open = False
                cont.carregar_senhas_usuario()
        
        cont.page.update()  # Atualiza a interface após o cadastro

    # Criando o pop-up globalmente
    campo_programa = ft.TextField(label="Nome do Programa", width=300)
    campo_tamanho = ft.TextField(label="Tamanho da Senha", width=150, input_filter=ft.NumbersOnlyInputFilter())
    campo_senha = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)  # Campo para a senha
    resultado_erro = ft.Text("", color="red")

    dialogo_cadastro = ft.AlertDialog(
        title=ft.Text("Cadastrar Nova Senha"),
        content=ft.Column([
            campo_programa,
            campo_tamanho,
            campo_senha,
            resultado_erro
        ]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dialogo_cadastro, "open", False)),
            ft.TextButton("Confirmar", on_click=confirmar_cadastro)
        ]
    )

    # Verifica se há um usuário logado antes de acessar a chave 'nome'
    usuario_logado = cont.conta_logada.get('nome', 'Usuário Desconhecido')

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
            tabela,
            ft.ElevatedButton("Cadastrar Nova Senha", on_click=abrir_dialogo_cadastro),
            ft.ElevatedButton("Carregar Senhas", on_click=carregar_senhas),
            ft.ElevatedButton("Sair", on_click=lambda e: cont.deslogar())
        ]
    )
