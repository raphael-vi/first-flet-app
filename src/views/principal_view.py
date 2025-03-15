import flet as ft
from src.controllers.password_controller import carregar_senhas_usuario, cadastrar_senha, deletar_senha, gerar_senha_aleatoria
from datetime import datetime

def view(page: ft.Page):
    """Tela principal."""
    usuario_logado = page.session.get("usuario_logado")
    if not usuario_logado:
        page.go("/login")  # Redireciona para o login se não houver usuário logado
        return

    # Variáveis para controlar o estado de edição
    editando = False
    programa_editando = None

    def carregar_senhas():
        """Carrega as senhas do usuário logado."""
        senhas = carregar_senhas_usuario(usuario_logado["nome"])
        tabela.rows.clear()
        for senha in senhas:
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(senha["programa"])),
                        ft.DataCell(
                            ft.TextField(
                                value=senha["senha"],
                                read_only=not (editando and senha["programa"] == programa_editando),
                                on_submit=lambda e, p=senha["programa"]: confirmar_edicao(p)
                            )
                            if editando and senha["programa"] == programa_editando
                            else ft.Text(senha["senha"])
                        ),
                        ft.DataCell(ft.Text(str(senha["tamanho"]))),
                        ft.DataCell(ft.Text(senha["data"])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, p=senha["programa"]: deletar_senha_click(p)),
                                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, p=senha["programa"]: editar_senha_click(p)),
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def deletar_senha_click(programa):
        """Deleta uma senha do usuário."""
        mensagem = deletar_senha(usuario_logado["nome"], programa)
        texto_erro.value = mensagem
        carregar_senhas()  # Recarrega as senhas após deletar

    def editar_senha_click(programa):
        """Habilita a edição da senha."""
        nonlocal editando, programa_editando
        editando = True
        programa_editando = programa
        carregar_senhas()  # Recarrega as senhas para atualizar a interface

    def confirmar_edicao(programa):
        """Confirma a edição da senha."""
        nonlocal editando, programa_editando
        senhas = carregar_senhas_usuario(usuario_logado["nome"])
        for senha in senhas:
            if senha["programa"] == programa:
                # Atualiza a senha com o valor do campo de texto
                senha["senha"] = next(cell.control.value for row in tabela.rows if row.cells[0].content.value == programa for cell in row.cells if isinstance(cell.control, ft.TextField))
                senha["data"] = datetime.now().strftime("%Y-%m-%d")
                break

        # Salva as senhas atualizadas
        arquivo_senhas = f"bd/{usuario_logado['nome']}/senhas.txt"
        with open(arquivo_senhas, mode='w') as arquivo:
            for senha in senhas:
                arquivo.write(f"{senha}\n")

        editando = False
        programa_editando = None
        carregar_senhas()  # Recarrega as senhas após editar

    def gerar_senha_click(e):
        """Gera uma senha aleatória e a preenche no campo de senha."""
        tamanho = campo_tamanho.value.strip()
        if not tamanho or not tamanho.isdigit():
            texto_erro.value = "Erro: O tamanho da senha deve ser um número."
        else:
            senha_aleatoria = gerar_senha_aleatoria(int(tamanho))
            campo_senha.value = senha_aleatoria
        page.update()

    def cadastrar_nova_senha(e):
        """Cadastra uma nova senha."""
        programa = campo_programa.value.strip()
        tamanho = campo_tamanho.value.strip()
        senha = campo_senha.value.strip()

        if not programa or not tamanho or not senha:
            texto_erro.value = "Todos os campos são obrigatórios."
        else:
            mensagem = cadastrar_senha(usuario_logado["nome"], programa, senha, int(tamanho))
            texto_erro.value = mensagem
            if "sucesso" in mensagem:
                campo_programa.value = ""
                campo_tamanho.value = ""
                campo_senha.value = ""
                carregar_senhas()  # Recarrega as senhas após cadastrar
        
        page.update()

    # Componentes da tela
    texto_erro = ft.Text("", color="red")
    campo_programa = ft.TextField(label="Programa", width=300)
    campo_tamanho = ft.TextField(label="Tamanho", width=100, input_filter=ft.NumbersOnlyInputFilter())
    campo_senha = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Programa")),
            ft.DataColumn(ft.Text("Senha")),
            ft.DataColumn(ft.Text("Tamanho")),
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )

    carregar_senhas()  # Carrega as senhas ao abrir a tela

    return ft.View(
        "/principal",
        [
            ft.Text(f"Bem-vindo, {usuario_logado['nome']}!", size=20),
            ft.Row([
                campo_programa,
                campo_tamanho,
                campo_senha,
                ft.IconButton(icon=ft.icons.CASINO, on_click=gerar_senha_click),
                ft.ElevatedButton("Cadastrar Senha", on_click=cadastrar_nova_senha),
            ]),
            tabela,
            texto_erro,
            ft.ElevatedButton("Sair", on_click=lambda e: page.go("/login")),
        ]
    )