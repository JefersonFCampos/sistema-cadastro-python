import customtkinter as ctk
from utils import sync_field, clean_error_msg, save_user
from validations import (
    validate_name,
    validate_email,
    validate_phone,
    validate_password,
    confirm_password_match,
)


class SignUpFrame(ctk.CTkFrame):
        
    def __init__(self, master, app_controller):
        super().__init__(master, width=350, height=560)
        self.app = app_controller
        self.pack_propagate(False)    

        # Título
        ctk.CTkLabel(
            self, text="Novo Usuário", font=("Roboto", 22, "bold")
        ).pack(pady=(15, 10))

        # Campo Nome
        self.name_entry = ctk.CTkEntry(
            self, width=280, placeholder_text="Nome Completo"
        )
        self.name_entry.pack(pady=(5, 0))
        self.name_error_label = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.name_error_label.pack()
        self.name_entry.bind(
            "<KeyRelease>",
            lambda event: [
                sync_field(
                    self.name_entry, self.name_error_label, validate_name
                ),
                clean_error_msg(self.submit_status_label)
            ]
        )

        # Campo E-mail
        self.email_entry = ctk.CTkEntry(
            self, width=280, placeholder_text="E-mail"
        )
        self.email_entry.pack(pady=(5, 0))
        self.email_error_label = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.email_error_label.pack(pady=(0, 2))
        self.email_entry.bind(
            "<KeyRelease>",
            lambda event: [
                sync_field(
                    self.email_entry, self.email_error_label, validate_email
                ),
                clean_error_msg(self.submit_status_label)
            ]
        )

        # --- Campo Telefone Unificado com Máscara em Tempo Real ---
        self.phone_entry = ctk.CTkEntry(
            self, width=280, placeholder_text="Telefone Ex: (51) 99999-9999"
        )
        self.phone_entry.pack(pady=(10, 0))
        
        self.phone_error_label = ctk.CTkLabel(
            self, text="", text_color="red", font=("Roboto", 12)
        )
        self.phone_error_label.pack()
        
        # O Gatilho dispara a máscara PRIMEIRO e a validação logo em seguida
        self.phone_entry.bind(
            "<KeyRelease>",
            lambda event: [
                self.apply_phone_mask(event), # <--- Aplica o visual da máscara
                sync_field(
                    self.phone_entry, self.phone_error_label,validate_phone
                ),
                clean_error_msg(self.submit_status_label)
            ]
        )

        # Campo Senha
        self.password_entry = ctk.CTkEntry(
            self, width=280, placeholder_text="Criar Senha", show="*"
        )
        self.password_entry.pack(pady=(10, 0))
        self.password_error_label = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.password_error_label.pack()

        # Campo Confirmar Senha
        self.confirm_password_entry = ctk.CTkEntry(
            self, width=280, placeholder_text="Repetir Senha", show="*"
        )
        self.confirm_password_entry.pack(pady=(10, 0))
        self.confirm_password_error_label = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.confirm_password_error_label.pack()

        # Eventos vinculados à Senha 1
        self.password_entry.bind(
            "<KeyRelease>",
            lambda event: [
                sync_field(
                    self.password_entry, self.password_error_label, validate_password
                ),
                sync_field(
                    self.confirm_password_entry,
                    self.confirm_password_error_label,
                    lambda valor: confirm_password_match(
                        self.password_entry.get(), valor
                    )
                ),
                clean_error_msg(self.submit_status_label)
            ]
        )

        # Eventos vinculados à Senha 2
        self.confirm_password_entry.bind(
            "<KeyRelease>",
            lambda event: [
                sync_field(
                    self.confirm_password_entry,
                    self.confirm_password_error_label,
                    lambda valor: confirm_password_match(
                        self.password_entry.get(), valor
                    )
                ),
                clean_error_msg(self.submit_status_label)
            ]
        )

        # Menu de Seleção de Nível
        self.role_option_menu = ctk.CTkOptionMenu(
            self, width=280, values=["Funcionário", "Administrador"]
        )
        self.role_option_menu.pack(pady=(10, 0))
        self.role_option_menu.set("Funcionário") # Valor padrão

        # Label de commit para Cadastro
        self.submit_status_label = ctk.CTkLabel(
            self, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.submit_status_label.pack(pady=5)

        # Botão Cadastrar
        self.submit_button = ctk.CTkButton(
            self,
            text="FINALIZAR CADASTRO",
            width=280,
            fg_color="#007700",
            hover_color="#006400",
            command=lambda: save_user(self)
        )
        self.submit_button.pack(pady=10)

        # Botão Voltar
        ctk.CTkButton(
            self,
            text="Voltar ao Login",
            fg_color="transparent",
            command=lambda: self.app.mostrar_tela_login()
        ).pack(pady=(5))

    # --- Lógica de Sincronização ---

    def apply_phone_mask(self, event):
        """Aplica a máscara (XX) XXXXX-XXXX em tempo real no campo de telefone."""
        # Ignora teclas de controle como Backspace, Delete ou Setas para não quebrar a digitação
        if event.keysym in ("Backspace", "Delete", "Left", "Right", "Tab"):
            return

        # 1. Pega o texto atual e remove tudo o que não for número
        raw_text = "".join(filter(str.isdigit, self.phone_entry.get()))
        
        # Limita o máximo absoluto a 11 dígitos numéricos
        raw_text = raw_text[:11]
        formatted_text = ""

        # 2. Constrói a máscara dinamicamente com base no tamanho do texto puro
        text_length = len(raw_text)
        
        if text_length > 0:
            # Se digitou pelo menos o início do DDD
            if text_length <= 2:
                formatted_text = f"({raw_text}"
            # Se já digitou o DDD completo
            elif text_length <= 7:
                formatted_text = f"({raw_text[:2]}) {raw_text[2:]}"
            # Se chegou no formato completo com o hífen deslocado para o final
            else:
                formatted_text = f"({raw_text[:2]}) {raw_text[2:7]}-{raw_text[7:]}"

        # 3. Atualiza o campo na tela com o texto mascarado
        # Guarda a posição atual do cursor para o usuário não perder o foco
        cursor_position = self.phone_entry._entry.index("insert")
        
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, formatted_text)
        
        # Reposiciona o cursor de digitação de forma inteligente no final
        self.phone_entry._entry.icursor(cursor_position + 1 if event.char else "end")
