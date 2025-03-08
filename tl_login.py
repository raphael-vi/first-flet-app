import flet as ft
import controle as cont
import funcoes_verificar_info as fvi

#-----------------------------------------------------------------------------------------------------------------------------------------

componentes = {
    "nome": ft.Ref[ft.TextField](),
    "senha": ft.Ref[ft.TextField](),
    "email": ft.Ref[ft.TextField](),
}

def altera_erro(erro: str):
    """Essa funcao vai mudar a string de erro que aparece na tela ao tentar cadastrar com valores invalidos ou usuario repetido"""
    texto_erro.value = erro
    texto_erro.update()

#--------------------------------------------------------------------------------------------------------------------------------------

#text que vai mostrar a mensagem de erro de cadastro
texto_erro = ft.Text("")

#-----------------------------------------------------------------------------------------------------------------------------------------

def view():
    return ft.View(
        #nome da view
        "tela login",

        #o que mostrar na tela
        [                           
            ft.Text('Tela login', size=20),
            ft.Container(content = ft.Text("ENTRAR", size = 20)),
            
            ##NOME
            ft.TextField(label = "Insira seu nome aqui.", ref = componentes["nome"], width=400, hint_text="Apenas letras maiúsculas e minúsculas"),

            #SENHA
            ft.TextField(label = "Insira sua senha aqui.", ref = componentes["senha"], password=True, width=400, can_reveal_password=True, hint_text="Letra minúscula, maiúscula, número e caractére especial e no mínimo tamanho 8."),

            #BOTAO DE VOLTAR E LOGIN
            ft.Row([
                #BOTAO IR PRO CADASTRO
                ft.ElevatedButton('CRIAR CONTA', icon = ft.Icons.APP_REGISTRATION, on_click = lambda e: cont.page.go("2")),

                #BOTAO LOGIN
                ft.ElevatedButton('ENTRAR', icon = 'login', on_click = logar),
            ]),

            #MENSAGEM DE ERRO
            texto_erro,
        ],
    )


#-----------------------------------------------------------------------------------------------------------------------------------------

def logar(e):
    """Essa função é para o usuário logar numa conta já criada"""

    usuario = {
        'nome' : componentes['nome'].current.value.strip(),
        'senha' : componentes['senha'].current.value,
    }

    if usuario['nome'] == "" or fvi.verifica_nome_correto(usuario["nome"]): 
        altera_erro("Usuário inválido.")  
    elif fvi.verifica_senha_correta(usuario["senha"]): 
        altera_erro("Senha inválida.")  
    else:  
        for cad in cont.carrega_bd():  
            if usuario["nome"] == cad["nome"] and usuario["senha"] == cad["senha"]:  
                
                cont.conta_logada = cad  # Define o usuário logado
                cont.carregar_senhas_usuario()  # Carrega as senhas do usuário logado
                
                altera_erro("Logado com sucesso.")
                print("Conta logada:", cont.conta_logada)

                # Garantindo que o nome do usuário está definido antes de mudar de tela
                if 'nome' in cont.conta_logada:
                    cont.page.go("3")  
                else:
                    altera_erro("Erro no login. Tente novamente.")

                return
        
        # Se nenhuma conta foi encontrada, exibir erro
        altera_erro("Usuário ou senha incorretos.")
