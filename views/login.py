import customtkinter as ctk
from utils import limpar_msg_erro
from database import confirmar_acesso
from utils import sincronizar_campo


class TelaLogin(ctk.CTkFrame):
        
    def __init__(self, master, app_controlador):
        super().__init__(master, width=320, height=420)               
        self.app = app_controlador
        self.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            self, text="Acesso Restrito", font=("Roboto", 24, "bold")
        ).pack(pady=30)

        # Campo Usuário (email serve com usuario)
        self.entry_email = ctk.CTkEntry(
            self, width=250, placeholder_text="Usuário"
        )
        self.entry_email.pack(pady=10)
        self.entry_email.bind(
            "<Key>",
            lambda event: limpar_msg_erro(self.label_login) # Limpa erro ao digitar
        ) 

        # Campo Senha
        self.entry_senha = ctk.CTkEntry(
            self, width=250, placeholder_text="Senha", show="*"
        )
        self.entry_senha.pack(pady=10)
        self.entry_senha.bind(
            "<Key>",
            lambda event: limpar_msg_erro(self.label_login) # Limpa erro ao digitar
        )

        # Botão Login
        self.btn_login = ctk.CTkButton(
            self, text="ENTRAR", width=250, command=self.processar_login
        )
        self.btn_login.pack(pady=10)
        self.label_login = ctk.CTkLabel(
            self, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.label_login.pack(pady=5)


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

    def processar_login(self):
        """Lógica de validação simples para teste do layout."""
        email_login = self.entry_email.get().strip()
        senha_login =self.entry_senha.get().strip()

        if not email_login or not senha_login:
            self.label_login.configure(
                text="⚠️ Preencha todos os campos!", text_color="#fa5252"
            )
            return

        sucesso, mensagem_banco, cargo_cod = confirmar_acesso(email_login, senha_login)                

        if sucesso:
            self.label_login.configure(
                text=f"✅ {mensagem_banco}", text_color="#006400"
            )
        else:
            self.label_login.configure(
                text=f"❌ {mensagem_banco}", text_color="#fa5252"
            )
