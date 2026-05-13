import customtkinter as ctk
from database import conexao_database
from validations import (
    validar_email,
    validar_nome,
    validar_senha,
    validar_telefone,
    validar_confirmacao_senha,
)

# Configurações globais de estilo do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque")
        self.geometry("700x800")

        # Container Principal para as telas
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both")

        self.mostrar_tela_login()

    def limpar_tela(self):
        """Remove todos os widgets do container principal."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_tela_login(self):
        self.limpar_tela()

        # Frame de Login (Centralizado)
        self.frame_login = ctk.CTkFrame(self.container, width=320, height=420)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_login.pack_propagate(False) # Mantém o tamanho fixo

        # Título
        ctk.CTkLabel(
            self.frame_login, text="Acesso Restrito", font=("Roboto", 24, "bold")
        ).pack(pady=30)

        # Campo Usuário
        self.entry_user = ctk.CTkEntry(
            self.frame_login, width=250, placeholder_text="Usuário"
        )
        self.entry_user.pack(pady=10)
        self.entry_user.bind("<Key>", self.limpar_erro) # Limpa erro ao digitar

        # Campo Senha
        self.entry_senha = ctk.CTkEntry(
            self.frame_login, width=250, placeholder_text="Senha", show="*"
        )
        self.entry_senha.pack(pady=10)
        self.entry_senha.bind("<Key>", self.limpar_erro) # Limpa erro ao digitar

        # --- LABEL DE ERRO (Espaço Reservado) ---
        self.label_erro = ctk.CTkLabel(
            self.frame_login, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.label_erro.pack(pady=5)

        # Botão Login
        self.btn_login = ctk.CTkButton(
            self.frame_login, text="ENTRAR", width=250, command=self.validar_login
        )
        self.btn_login.pack(pady=10)

        # Botão Cadastrar
        ctk.CTkButton(
            self.frame_login,
            text="Cadastrar",
            fg_color="transparent",
            font=("Roboto", 11),
            hover=False,
            command=lambda: self.mostrar_tela_cadastro(),
        ).pack()

        # Botão Recuperar
        ctk.CTkButton(
            self.frame_login,
            text="Esqueci minha senha",
            fg_color="transparent",
            font=("Roboto", 11),
            hover=False,
            command=lambda: print("Ir para recuperação"),
        ).pack()

    def limpar_erro(self, event=None):
        """Remove a mensagem de erro da tela."""
        self.label_commit_cad.configure(text="")

    def validar_login(self):
        """Lógica de validação simples para teste do layout."""
        usuario = self.entry_user.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.label_erro.configure(text="⚠️ Preencha todos os campos!")
        elif usuario == "admin" and senha == "123":
            self.label_erro.configure(
                text_color="#006400", text="Sucesso! Entrando..."
            )
        else:
            self.label_erro.configure(text="❌ Usuário ou senha inválidos.")

    def mostrar_tela_cadastro(self):
        self.limpar_tela()

        # 2. Frame de Cadastro (Um pouco mais alto que o de login para caber mais campos)
        self.frame_cad = ctk.CTkFrame(self.container, width=500, height=600)
        self.frame_cad.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_cad.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            self.frame_cad, text="Novo Usuário", font=("Roboto", 22, "bold")
        ).pack(pady=20)

        # Campo Nome
        self.entry_cad_nome = ctk.CTkEntry(
            self.frame_cad, width=280, placeholder_text="Nome Completo"
        )
        self.entry_cad_nome.pack(pady=(10, 0))
        self.label_erro_nome = ctk.CTkLabel(
            self.frame_cad, text="", text_color="#fa5252"
        )
        self.label_erro_nome.pack()
        self.entry_cad_nome.bind(
            "<KeyRelease>",
            lambda event: [
                self.sincronizar_campo(
                    self.entry_cad_nome, self.label_erro_nome, validar_nome
                ),
                self.limpar_erro(),
            ],
        )

        # Campo E-mail
        self.entry_cad_email = ctk.CTkEntry(
            self.frame_cad, width=280, placeholder_text="E-mail"
        )
        self.entry_cad_email.pack(pady=(10, 0))
        self.label_erro_email = ctk.CTkLabel(
            self.frame_cad, text="", text_color="#fa5252"
        )
        self.label_erro_email.pack()
        self.entry_cad_email.bind(
            "<KeyRelease>",
            lambda event: [
                self.sincronizar_campo(
                    self.entry_cad_email, self.label_erro_email, validar_email
                ),
                self.limpar_erro(),
            ],
        )

        # --- Campo Telefone Unificado com Máscara em Tempo Real ---
        self.entry_cad_telefone = ctk.CTkEntry(
            self.frame_cad, width=280, placeholder_text="Telefone Ex: (51) 99999-9999"
        )
        self.entry_cad_telefone.pack(pady=(10, 0))
        
        self.label_erro_telefone = ctk.CTkLabel(
            self.frame_cad, text="", text_color="red", font=("Roboto", 12)
        )
        self.label_erro_telefone.pack()
        
        # O Gatilho dispara a máscara PRIMEIRO e a validação logo em seguida
        self.entry_cad_telefone.bind(
            "<KeyRelease>",
            lambda event: [
                self.aplicar_mascara_telefone(event), # <--- Aplica o visual da máscara
                self.sincronizar_campo(
                    self.entry_cad_telefone, self.label_erro_telefone,validar_telefone
                ),
                self.limpar_erro(),
            ],
        )

        # Campo Senha
        self.entry_cad_senha = ctk.CTkEntry(
            self.frame_cad, width=280, placeholder_text="Criar Senha", show="*"
        )
        self.entry_cad_senha.pack(pady=(10, 0))
        self.label_erro_senha = ctk.CTkLabel(
            self.frame_cad, text="", text_color="#fa5252"
        )
        self.label_erro_senha.pack()

        # Campo Repetir Senha
        self.entry_repetir_senha = ctk.CTkEntry(
            self.frame_cad, width=280, placeholder_text="Repetir Senha", show="*"
        )
        self.entry_repetir_senha.pack(pady=(10, 0))
        self.label_erro_repetir = ctk.CTkLabel(
            self.frame_cad, text="", text_color="#fa5252"
        )
        self.label_erro_repetir.pack()

        # Eventos vinculados à Senha 1
        self.entry_cad_senha.bind(
            "<KeyRelease>",
            lambda event: [
                self.sincronizar_campo(
                    self.entry_cad_senha, self.label_erro_senha, validar_senha
                ),
                self.sincronizar_campo(
                    self.entry_repetir_senha,
                    self.label_erro_repetir,
                    lambda valor: validar_confirmacao_senha(
                        self.entry_cad_senha.get(), valor
                    ),
                ),
                self.limpar_erro(),
            ],
        )

        # Eventos vinculados à Senha 2
        self.entry_repetir_senha.bind(
            "<KeyRelease>",
            lambda event: [
                self.sincronizar_campo(
                    self.entry_repetir_senha,
                    self.label_erro_repetir,
                    lambda valor: validar_confirmacao_senha(
                        self.entry_cad_senha.get(), valor
                    ),
                ),
                self.limpar_erro(),
            ],
        )

        # Menu de Seleção de Nível
        self.option_cargo = ctk.CTkOptionMenu(
            self.frame_cad, width=280, values=["Funcionário", "Administrador"]
        )
        self.option_cargo.pack(pady=(10, 0))
        self.option_cargo.set("Funcionário") # Valor padrão

        # Label de commit para Cadastro
        self.label_commit_cad = ctk.CTkLabel(
            self.frame_cad, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.label_commit_cad.pack(pady=5)

        # Botão Cadastrar
        self.btn_confirmar_cad = ctk.CTkButton(
            self.frame_cad,
            text="FINALIZAR CADASTRO",
            width=280,
            fg_color="#007700",
            hover_color="#006400",
            command=self.salvar_database,
        )
        self.btn_confirmar_cad.pack(pady=10)

        # Botão Voltar
        ctk.CTkButton(
            self.frame_cad,
            text="Voltar ao Login",
            fg_color="transparent",
            command=self.mostrar_tela_login,
        ).pack(pady=(5))

    # --- Lógica de Sincronização ---

    def aplicar_mascara_telefone(self, event):
        """Aplica a máscara (XX) XXXXX-XXXX em tempo real no campo de telefone."""
        # Ignora teclas de controle como Backspace, Delete ou Setas para não quebrar a digitação
        if event.keysym in ("Backspace", "Delete", "Left", "Right", "Tab"):
            return

        # 1. Pega o texto atual e remove tudo o que não for número
        texto_puro = "".join(filter(str.isdigit, self.entry_cad_telefone.get()))
        
        # Limita o máximo absoluto a 11 dígitos numéricos
        texto_puro = texto_puro[:11]
        texto_formatado = ""

        # 2. Constrói a máscara dinamicamente com base no tamanho do texto puro
        tamanho = len(texto_puro)
        
        if tamanho > 0:
            # Se digitou pelo menos o início do DDD
            if tamanho <= 2:
                texto_formatado = f"({texto_puro}"
            # Se já digitou o DDD completo
            elif tamanho <= 7:
                texto_formatado = f"({texto_puro[:2]}) {texto_puro[2:]}"
            # Se chegou no formato completo com o hífen deslocado para o final
            else:
                texto_formatado = f"({texto_puro[:2]}) {texto_puro[2:7]}-{texto_puro[7:]}"

        # 3. Atualiza o campo na tela com o texto mascarado
        # Guarda a posição atual do cursor para o usuário não perder o foco
        posicao_cursor = self.entry_cad_telefone._entry.index("insert")
        
        self.entry_cad_telefone.delete(0, "end")
        self.entry_cad_telefone.insert(0, texto_formatado)
        
        # Reposiciona o cursor de digitação de forma inteligente no final
        self.entry_cad_telefone._entry.icursor(posicao_cursor + 1 if event.char else "end")


    def sincronizar_campo(self, entrada, label_erro, funcao_validacao):
        """Realiza a ponte entre a interface gráfica e a lógica de validação."""
        valor_puro = entrada.get()
        valido, mensagem = funcao_validacao(valor_puro)

        if not valido:
            label_erro.configure(text=mensagem, text_color="#fa5252")
        else:
            label_erro.configure(text="")
        return valido

    # --- Ação Principal ---

    def salvar_database(self):
        """Coordena a validação final e a persistência no banco."""
        nome_ok = self.sincronizar_campo(
            self.entry_cad_nome, self.label_erro_nome, validar_nome
        )
        email_ok = self.sincronizar_campo(
            self.entry_cad_email, self.label_erro_email, validar_email
        )
        telefone_ok = self.sincronizar_campo(
            self.entry_cad_telefone, self.label_erro_telefone, validar_telefone
        )
        senha_ok = self.sincronizar_campo(
            self.entry_cad_senha, self.label_erro_senha, validar_senha
        )
        repetir_senha_ok = self.sincronizar_campo(
            self.entry_repetir_senha,
            self.label_erro_repetir,
            lambda valor: validar_confirmacao_senha(
                self.entry_cad_senha.get(), valor
            ),
        )

        if all([nome_ok, email_ok, telefone_ok ,senha_ok, repetir_senha_ok]):
            nome = self.entry_cad_nome.get().strip()
            email = self.entry_cad_email.get().strip()
            senha = self.entry_cad_senha.get().strip()

            tipo_acesso = {"Administrador": "1", "Funcionário": "2"}
            codigo_cargo = tipo_acesso[self.option_cargo.get()]

            conexao_database(nome, email, senha, codigo_cargo)

            self.label_commit_cad.configure(
                text="Dados salvos com sucesso!", text_color="#006400"
            )

            # Limpeza dos campos após sucesso
            self.entry_cad_nome.delete(0, "end")
            self.entry_cad_email.delete(0, "end")
            self.entry_cad_senha.delete(0, "end")
            self.entry_repetir_senha.delete(0, "end")
        else:
            self.label_commit_cad.configure(
                text="Erro ao salvar os dados.", text_color="#fa5252"
            )
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
