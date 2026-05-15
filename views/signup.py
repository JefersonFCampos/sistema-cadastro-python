import customtkinter as ctk
from utils import sincronizar_campo, limpar_msg_erro, salvar_database
from validations import (
    validar_email,
    validar_nome,
    validar_senha,
    validar_telefone,
    validar_confirmacao_senha,
)


class TelaCadastro(ctk.CTkFrame):
        
    def __init__(self, master, app_controlador):
        super().__init__(master, width=350, height=560)
        self.app = app_controlador
        self.pack_propagate(False)    

        # Título
        ctk.CTkLabel(
            self, text="Novo Usuário", font=("Roboto", 22, "bold")
        ).pack(pady=(15, 10))

        # Campo Nome
        self.entry_cad_nome = ctk.CTkEntry(
            self, width=280, placeholder_text="Nome Completo"
        )
        self.entry_cad_nome.pack(pady=(5, 0))
        self.label_erro_nome = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.label_erro_nome.pack()
        self.entry_cad_nome.bind(
            "<KeyRelease>",
            lambda event: [
                sincronizar_campo(
                    self.entry_cad_nome, self.label_erro_nome, validar_nome
                ),
                limpar_msg_erro(self.label_commit_cad)
            ]
        )

        # Campo E-mail
        self.entry_cad_email = ctk.CTkEntry(
            self, width=280, placeholder_text="E-mail"
        )
        self.entry_cad_email.pack(pady=(5, 0))
        self.label_erro_email = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.label_erro_email.pack(pady=(0, 2))
        self.entry_cad_email.bind(
            "<KeyRelease>",
            lambda event: [
                sincronizar_campo(
                    self.entry_cad_email, self.label_erro_email, validar_email
                ),
                limpar_msg_erro(self.label_commit_cad)
            ]
        )

        # --- Campo Telefone Unificado com Máscara em Tempo Real ---
        self.entry_cad_telefone = ctk.CTkEntry(
            self, width=280, placeholder_text="Telefone Ex: (51) 99999-9999"
        )
        self.entry_cad_telefone.pack(pady=(10, 0))
        
        self.label_erro_telefone = ctk.CTkLabel(
            self, text="", text_color="red", font=("Roboto", 12)
        )
        self.label_erro_telefone.pack()
        
        # O Gatilho dispara a máscara PRIMEIRO e a validação logo em seguida
        self.entry_cad_telefone.bind(
            "<KeyRelease>",
            lambda event: [
                self.aplicar_mascara_telefone(event), # <--- Aplica o visual da máscara
                sincronizar_campo(
                    self.entry_cad_telefone, self.label_erro_telefone,validar_telefone
                ),
                limpar_msg_erro(self.label_commit_cad)
            ]
        )

        # Campo Senha
        self.entry_cad_senha = ctk.CTkEntry(
            self, width=280, placeholder_text="Criar Senha", show="*"
        )
        self.entry_cad_senha.pack(pady=(10, 0))
        self.label_erro_senha = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.label_erro_senha.pack()

        # Campo Repetir Senha
        self.entry_repetir_senha = ctk.CTkEntry(
            self, width=280, placeholder_text="Repetir Senha", show="*"
        )
        self.entry_repetir_senha.pack(pady=(10, 0))
        self.label_erro_repetir = ctk.CTkLabel(
            self, text="", text_color="#fa5252"
        )
        self.label_erro_repetir.pack()

        # Eventos vinculados à Senha 1
        self.entry_cad_senha.bind(
            "<KeyRelease>",
            lambda event: [
                sincronizar_campo(
                    self.entry_cad_senha, self.label_erro_senha, validar_senha
                ),
                sincronizar_campo(
                    self.entry_repetir_senha,
                    self.label_erro_repetir,
                    lambda valor: validar_confirmacao_senha(
                        self.entry_cad_senha.get(), valor
                    )
                ),
                limpar_msg_erro(self.label_commit_cad)
            ]
        )

        # Eventos vinculados à Senha 2
        self.entry_repetir_senha.bind(
            "<KeyRelease>",
            lambda event: [
                sincronizar_campo(
                    self.entry_repetir_senha,
                    self.label_erro_repetir,
                    lambda valor: validar_confirmacao_senha(
                        self.entry_cad_senha.get(), valor
                    )
                ),
                limpar_msg_erro(self.label_commit_cad)
            ]
        )

        # Menu de Seleção de Nível
        self.option_cargo = ctk.CTkOptionMenu(
            self, width=280, values=["Funcionário", "Administrador"]
        )
        self.option_cargo.pack(pady=(10, 0))
        self.option_cargo.set("Funcionário") # Valor padrão

        # Label de commit para Cadastro
        self.label_commit_cad = ctk.CTkLabel(
            self, text="", text_color="#fa5252", font=("Roboto", 12)
        )
        self.label_commit_cad.pack(pady=5)

        # Botão Cadastrar
        self.btn_confirmar_cad = ctk.CTkButton(
            self,
            text="FINALIZAR CADASTRO",
            width=280,
            fg_color="#007700",
            hover_color="#006400",
            command=lambda: salvar_database(self)
        )
        self.btn_confirmar_cad.pack(pady=10)

        # Botão Voltar
        ctk.CTkButton(
            self,
            text="Voltar ao Login",
            fg_color="transparent",
            command=lambda: self.app.mostrar_tela_login()
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
