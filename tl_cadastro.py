import flet as ft
import controle as cont
import funcoes_verificar_info as fvi

#-----------------------------------------------------------------------------------------------------------------------------------------

componentes = {
    "nome": ft.Ref[ft.TextField](),
    "senha": ft.Ref[ft.TextField](),
    "email": ft.Ref[ft.TextField](),
    "idade_ano": ft.Ref[ft.TextField](),
    "idade_mes": ft.Ref[ft.TextField](),
    "idade_dia": ft.Ref[ft.TextField](),
    "telefone": ft.Ref[ft.TextField](),
    "sexo": ft.Ref[ft.RadioGroup](),
}

def altera_erro(erro: str):
    """Muda a string de erro que aparece na tela de cadastro."""
    texto_erro.value = erro
    texto_erro.update()

#--------------------------------------------------------------------------------------------------------------------------------------

# Texto que mostra a mensagem de erro no cadastro
texto_erro = ft.Text("")

#-----------------------------------------------------------------------------------------------------------------------------------------

def cadastrar(e):
    """Adiciona um cadastro no banco de dados, validando os dados do usuário antes."""
    
    usuario = {
        'nome': componentes['nome'].current.value.strip(),
        'senha': componentes['senha'].current.value,
        'email': componentes['email'].current.value,
        'idade_ano': componentes['idade_ano'].current.value,
        'idade_mes': componentes['idade_mes'].current.value,
        'idade_dia': componentes['idade_dia'].current.value,
        'telefone': componentes['telefone'].current.value,
        'sexo': componentes['sexo'].current.value,
    }

    # Chamando funções de verificação e armazenando as mensagens de erro
    erro_nome = fvi.verifica_nome_correto(usuario["nome"])
    erro_email = fvi.verifica_email_correto(usuario["email"])
    erro_telefone = fvi.verifica_telefone_correto(usuario["telefone"])
    erro_idade = fvi.verifica_idade_correta(usuario["idade_ano"], usuario["idade_mes"], usuario["idade_dia"])
    erro_senha = fvi.verifica_senha_correta(usuario["senha"])

    # Verificando se há erros
    if usuario["nome"] in [cad["nome"] for cad in cont.carrega_bd()]:
        altera_erro("Usuário já cadastrado.")  
    elif erro_nome:
        altera_erro(erro_nome)  
    elif erro_email:
        altera_erro(erro_email)  
    elif erro_telefone:
        altera_erro(erro_telefone)  
    elif usuario['sexo'] is None:
        altera_erro("Sexo inválido.")  
    elif erro_idade:
        altera_erro(erro_idade)  
    elif erro_senha:
        altera_erro(erro_senha)  
    else:
        # Tudo certo para criar o cadastro
        cont.banco_cad = cont.criar_usuario_bd(usuario)
        altera_erro("Usuário cadastrado com sucesso, retorne para fazer o login.")

#-----------------------------------------------------------------------------------------------------------------------------------------

def view():
    """Gera a tela de cadastro de usuário"""
    return ft.View(
        "tela cadastro",
        [
            ft.Text('Tela cadastro', size=20),
            ft.Container(content=ft.Text("CADASTRO", size=20)),

            # NOME
            ft.TextField(label="Nome", ref=componentes["nome"], width=400, hint_text="Apenas letras maiúsculas e minúsculas"),

            # SENHA
            ft.TextField(label="Senha", ref=componentes["senha"], password=True, width=400, can_reveal_password=True, hint_text="Deve conter pelo menos 6 caracteres"),

            # EMAIL
            ft.TextField(label="E-mail", ref=componentes["email"], width=400),

            # IDADE
            ft.Row([
                ft.Dropdown(width=100, label='DIA', ref=componentes['idade_dia'], options=[ft.dropdown.Option(str(ano)) for ano in range(1, 32)]),
                ft.Dropdown(width=100, label='MÊS', ref=componentes['idade_mes'], options=[ft.dropdown.Option(str(ano)) for ano in range(1, 13)]),
                ft.Dropdown(width=100, label='ANO', ref=componentes['idade_ano'], options=[ft.dropdown.Option(str(ano)) for ano in range(2025, 1899, -1)]),
            ]),

            # TELEFONE
            ft.TextField(label="Telefone", ref=componentes["telefone"], width=400, max_length=11, hint_text="(__) _____-____", input_filter=ft.NumbersOnlyInputFilter()),

            # SEXO
            ft.Row([
                ft.Text("SEXO", width=40),
                ft.RadioGroup(
                    ref=componentes['sexo'],
                    content=ft.Row([
                        ft.Radio(value="M", label="M"),
                        ft.Radio(value="F", label="F"),
                        ft.Radio(value="OUTRO", label="OUTRO"),
                    ]),
                )
            ]),

            # BOTÕES
            ft.Row([
                ft.ElevatedButton('VOLTAR', icon=ft.Icons.ARROW_BACK, on_click=lambda e: cont.page.go("1")),
                ft.ElevatedButton('CADASTRAR', icon=ft.Icons.APP_REGISTRATION, on_click=cadastrar),
            ]),

            # MENSAGEM DE ERRO
            texto_erro,
        ],
    )
