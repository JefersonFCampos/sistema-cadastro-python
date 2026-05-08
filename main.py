from tkinter import *
from validations import *
from database import conexao_database

# --- Funções de Evento (Interface) ---

def real_time_validar_nome(event):
    """Gatilho para validação de nome em tempo real durante a digitação."""
    sincronizar_campo(entrada_nome, nome_erro, validar_nome)


def real_time_validar_ddd(event):
    """Gatilho para validação de DDD em tempo real."""
    sincronizar_campo(entrada_ddd, ddd_erro, validar_ddd)


def real_time_validar_telefone(event):
    """Gatilho para validação de telefone em tempo real."""
    sincronizar_campo(entrada_telefone, telefone_erro, validar_telefone)


def real_time_validar_email(event):
    """Gatilho para validação de e-mail em tempo real."""
    sincronizar_campo(entrada_email, email_erro, validar_email)

# --- Lógica de Sincronização ---

def sincronizar_campo(entrada, label_erro, funcao_validacao):
    """
    Realiza a ponte entre a interface gráfica e a lógica de validação.
    Lê o widget de entrada, aplica a função de validação e atualiza a label de erro.
    
    :param entrada: Widget Entry do Tkinter.
    :param label_erro: Widget Label onde a mensagem será exibida.
    :param funcao_validacao: Função lógica vinda de 'validations.py'.
    :return: Booleano indicando se o campo é válido.
    """
    valor_puro = entrada.get().strip()
    valido, mensagem = funcao_validacao(valor_puro)
    
    if not valido:
        label_erro.config(text=mensagem, bg="#008", fg="red")
    else:
        label_erro.config(text="")
        
    return valido

# --- Ação Principal ---

def salvar_database():
    """
    Coordena a validação final de todos os campos e a persistência no banco de dados.
    Verifica a integridade de todos os dados antes de chamar o módulo de banco de dados.
    """
    # Valida todos os campos e armazena os estados booleanos
    check_nome = sincronizar_campo(entrada_nome, nome_erro, validar_nome)
    check_ddd = sincronizar_campo(entrada_ddd, ddd_erro, validar_ddd)
    check_telefone = sincronizar_campo(entrada_telefone, telefone_erro, validar_telefone)
    check_email = sincronizar_campo(entrada_email, email_erro, validar_email)

    # Se todos os checks retornarem True, prossegue com o salvamento
    if all([check_nome, check_ddd, check_fone, check_email]):
        # Coleta os dados finais para envio ao SQLite
        nome = entrada_nome.get().strip()
        ddd = entrada_ddd.get().strip()
        telefone = entrada_telefone.get().strip()
        email = entrada_email.get().strip()
        
        conexao_database(nome, ddd, telefone, email)
        
        label_resultado.config(text="Dados salvos com sucesso!", fg="green")
        
        # Limpeza dos campos após sucesso
        entrada_nome.delete(0, END)
        entrada_ddd.delete(0, END)
        entrada_telefone.delete(0, END)
        entrada_email.delete(0, END)

    else:
        label_resultado.config(text="Erro ao salvar os dados.", fg="red")


app = Tk()
app.title("Test")
app.geometry("500x600")
app.configure(bg="#00f")

# Título da página
label_cadastro = Label(app, text="Cadastro", bg="#dd2", fg="#008", font=("Arial", 15))
label_cadastro.place(x=10, y=10, width=480, height=40)

# Cria o Frame
frame_cadastro = Frame(app, bg="#008", borderwidth=1, relief="sunken")
frame_cadastro.place(x=10, y=60, width=480, height=300)

# TextBox do nome com validação
label_nome = Label(frame_cadastro, text="Nome", bg="#008", fg="#fff", anchor=W)
label_nome.place(x=10, y=20)

entrada_nome = Entry(frame_cadastro)
entrada_nome.place(x=10, y=40, width=200, height=20)
entrada_nome.bind("<KeyRelease>", real_time_validar_nome)

nome_erro = Label(frame_cadastro, text="", bg="#008", fg="red")
nome_erro.place(x=10, y=60)

# TextBox do DDD com validação
label_ddd = Label(frame_cadastro, text="DDD -", bg="#008", fg="#fff", anchor=W)
label_ddd.place(x=10, y=100)

entrada_ddd = Entry(frame_cadastro)
entrada_ddd.place(x=10, y=120, width=30, height=20)
entrada_ddd.bind("<KeyRelease>", real_time_validar_ddd)

ddd_erro = Label(frame_cadastro, text="", bg="#008", fg="red")
ddd_erro.place(x=10, y=140)

# TextBox do Telefone com validação
label_telefone = Label(frame_cadastro, text="Telefone", bg="#008", fg="#fff", anchor=W)
label_telefone.place(x=50, y=100)

entrada_telefone = Entry(frame_cadastro)
entrada_telefone.place(x=50, y=120, width=100, height=20)
entrada_telefone.bind("<KeyRelease>", real_time_validar_telefone)

telefone_erro = Label(frame_cadastro, text="", bg="#008", fg="red")
telefone_erro.place(x=10, y=160)

# TextBox do E-mail com validação
label_email = Label(frame_cadastro, text="E-mail", bg="#008", fg="#fff", anchor=W)
label_email.place(x=10, y=180, width=100, height=20)

entrada_email = Entry(frame_cadastro)
entrada_email.place(x=10, y=200, width=200, height=20)
entrada_email.bind("<KeyRelease>", real_time_validar_email)

email_erro = Label(frame_cadastro, text="", bg="#008", fg="red")
email_erro.place(x=10, y=220)

# Mensagem do Resultado da validação
label_resultado = Label(app, text="", bg="#00f", fg="green", font=("Arial", 15))
label_resultado.place(x=10, y=380)

# Botão para salvar os dados validados
botao_salvar = Button(app, text="Salvar", command=salvar_database)
botao_salvar.place(x=10, y=420, width=100, height=20)

app.mainloop()
