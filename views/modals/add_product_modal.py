import customtkinter as ctk


class AddProductModal(ctk.CTkToplevel):
    def __init__(self, master, controller, user_role):
        super().__init__(master)
        self.controller = controller
        self.user_role = user_role

        # Configurações do Pop-up
        self.title("Adicionar Item ao Estoque")
        self.geometry("450x450")
        self.grab_set() #Mantem o foco no Pop-up
        self.focus_force()

        # Titulo interno
        ctk.CTkLabel(self, text="📦 Cadastrar Novo Produto", font=("Roboto", 18, "bold")).pack(pady=20)

        # Campos de entrada
        self.name_ent = ctk.CTkEntry(self, placeholder_text="Nome do Produto", width=320)
        self.name_ent.pack(pady=8)

        self.qty_ent = ctk.CTkEntry(self, placeholder_text="Quantidade em Estoque Inicial", width=320)
        self.qty_ent.pack(pady=8)

        self.cost_ent = None
        if self.user_role == "Administrador":
            self.cost_ent = ctk.CTkEntry(self, placeholder_text="Preço de Custo do Unitário (R$)", width=320)
            self.cost_ent.pack(pady=8)

        self.price_ent = ctk.CTkEntry(self, placeholder_text="Preço de Venda ao Cliente (R$)", width=320)
        self.price_ent.pack(pady=8)

        # Label para exibir erros na tela do pop-up
        self.error_lbl = ctk.CTkLabel(self, text="", text_color="#fa5252", font=("Roboto", 12))
        self.error_lbl.pack(pady=5)

        # Botão Concluir chamando o gatilho externo do controlador
        ctk.CTkButton(
            self, 
            text="CONCLUIR CADASTRO",
            fg_color="#007700",
            hover_color="#006400",
            width=320,
            command=self.trigger_save
        ).pack(pady=20)

    def trigger_save(self):
        """Coleta os dados dos campos e terceiriza o processamento para o controlador."""
        name = self.name_ent.get().strip()
        qty_raw = self.qty_ent.get().strip()
        cost_raw = self.cost_ent.get().strip() if self.cost_ent else "0"
        price_raw = self.price_ent.get().strip()

        # Dispara a lógica de validação e salvamento no StockController
        self.controller.process_new_product(name, qty_raw, price_raw, cost_raw, self.error_lbl, self)