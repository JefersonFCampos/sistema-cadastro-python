import customtkinter as ctk
from utils import limpar_msg_erro


class TelaLogin(ctk.CTkFrame):
        
    def __init__(self, master, app_controlador):
        super().__init__(master, width=320, height=420)               
        self.app = app_controlador
        self.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            self, text="Acesso Restrito", font=("Roboto", 24, "bold")
        ).pack(pady=30)

        # Campo Usuário
        self.entry_user = ctk.CTkEntry(
            self, width=250, placeholder_text="Usuário"
        )
        self.entry_user.pack(pady=10)
        self.entry_user.bind("<Key>", limpar_msg_erro) # Limpa erro ao digitar

        # Campo Senha
        self.entry_senha = ctk.CTkEntry(
            self, width=250, placeholder_text="Senha", show="*"
        )
        self.entry_senha.pack(pady=10)
        self.entry_senha.bind("<Key>", limpar_msg_erro) # Limpa erro ao digitar

        # --- LABEL DE ERRO (Espaço Reservado) ---
        self.label_erro = ctk.CTkLabel(
            self, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.label_erro.pack(pady=5)

        # Botão Login
        self.btn_login = ctk.CTkButton(
            self, text="ENTRAR", width=250, command=self.validar_login
        )
        self.btn_login.pack(pady=10)

        # Botão Cadastrar
        ctk.CTkButton(
            self,
            text="Cadastrar",
            fg_color="transparent",
            font=("Roboto", 11),
            hover=False,
            command=lambda: self.app.mostrar_tela_cadastro(),
        ).pack()

        # Botão Recuperar
        ctk.CTkButton(
            self,
            text="Esqueci minha senha",
            fg_color="transparent",
            font=("Roboto", 11),
            hover=False,
            command=lambda: print("Ir para recuperação"),
        ).pack()

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
            