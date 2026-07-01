import customtkinter as ctk
from utils import clean_error_msg
from database import confirm_access


class LoginFrame(ctk.CTkFrame):
        
    def __init__(self, master, app_controller):
        super().__init__(master, width=320, height=420)               
        self.app = app_controller
        self.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            self, text="Acesso Restrito", font=("Roboto", 24, "bold")
        ).pack(pady=30)

        # Campo Usuário (email serve com usuario)
        self.email_entry = ctk.CTkEntry(
            self, width=250, placeholder_text="Usuário"
        )
        self.email_entry.pack(pady=10)
        self.email_entry.bind(
            "<Key>",
            lambda event: clean_error_msg(self.login_status_label) # Limpa erro ao digitar
        ) 

        # Campo Senha
        self.password_entry = ctk.CTkEntry(
            self, width=250, placeholder_text="Senha", show="*"
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind(
            "<Key>",
            lambda event: clean_error_msg(self.login_status_label) # Limpa erro ao digitar
        )

        # Botão Login
        self.login_button = ctk.CTkButton(
            self, text="ENTRAR", width=250, command=self.process_login
        )
        self.login_button.pack(pady=10)
        self.login_status_label = ctk.CTkLabel(
            self, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.login_status_label.pack(pady=5)


        # Botão Cadastrar
        ctk.CTkButton(
            self,
            text="Cadastrar",
            fg_color="transparent",
            font=("Roboto", 11),
            hover=False,
            command=lambda: self.app.show_signup_frame(),
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

    def process_login(self):
        """Lógica de validação simples para teste do layout."""
        email_input = self.email_entry.get().strip()
        password_input =self.password_entry.get().strip()

        if not email_input or not password_input:
            self.login_status_label.configure(
                text="⚠️ Preencha todos os campos!", text_color="#fa5252"
            )
            return

        success, db_message, rule_cod = confirm_access(email_input, password_input)                

        if success:
            self.login_status_label.configure(
                text=f"✅ {db_message}", text_color="#006400"
            )
            # Aguarda meio segundo para o usuário ver o feedback visual de sucesso e muda de tela
            self.after(500, lambda: self.app.show_dashboard_frame(role_code=rule_cod))
        else:
            self.login_status_label.configure(
                text=f"❌ {db_message}", text_color="#fa5252"
            )

