import customtkinter as ctk


class AddProductModal(ctk.CTkToplevel):
    def __init__(self, master, controller, user_role, product_data=None):
        super().__init__(master)
        self.controller = controller
        self.user_role = user_role
        self.product_data= product_data

        # Configurações do Pop-up
        self.title("Adicionar Item ao Estoque")
        self.geometry("450x330")
        self.grab_set() #Mantem o foco no Pop-up
        self.focus_force()

        # Titulo interno
        ctk.CTkLabel(self, text="📦 Cadastrar Novo Produto", font=("Roboto", 18, "bold")).pack(pady=20)

        # --- CAMPOS OBRIGATÓRIOS (Sempre Visíveis) ---
        self.name_ent = ctk.CTkEntry(self, placeholder_text="Nome do Produto", width=320)
        self.name_ent.pack(pady=8)

        self.qty_ent = ctk.CTkEntry(self, placeholder_text="Quantidade em Estoque Inicial", width=320)
        self.qty_ent.pack(pady=8)

        self.price_ent = ctk.CTkEntry(self, placeholder_text="Preço de Venda ao Cliente (R$)", width=320)
        self.price_ent.pack(pady=8)
        
         # Container invisível para guardar os campos opcionais (Começa oculto)
        self.optional_container = ctk.CTkFrame(self, fg_color="transparent")

        # Cria os campos opcionais DENTRO do container invisível
        self.cost_ent = None
        if self.user_role == "Administrador":
            self.cost_ent = ctk.CTkEntry(self.optional_container, placeholder_text="Preço de Custo do Unitário (R$)", width=320)
            self.cost_ent.pack(pady=8)

        self.barcode_ent = ctk.CTkEntry(self.optional_container, placeholder_text="Código de Barras / SKU (Opcional)", width=320)
        self.barcode_ent.pack(pady=4)

        self.batch_ent = ctk.CTkEntry(self.optional_container, placeholder_text="Lote do Produto (Opcional)", width=320)
        self.batch_ent.pack(pady=4)

        self.expiry_ent = ctk.CTkEntry(self.optional_container, placeholder_text="Data de Validade DD/MM/AAAA (Opcional)", width=320)
        self.expiry_ent.pack(pady=4)

        # Botão estilo Link para esticar/encolher a janela
        self.btn_toggle = ctk.CTkButton(
            self, text="➕ Mostrar Informações Avançadas", fg_color="transparent", 
            text_color=["#1c7ed6", "#3498db"], hover=False, font=("Roboto", 11, "bold"),
            command=self.toggle_advanced_fields
        )
        self.btn_toggle.pack(pady=5)

        # Label para exibir erros na tela do pop-up
        self.error_lbl = ctk.CTkLabel(self, text="", text_color="#fa5252", font=("Roboto", 12))
        self.error_lbl.pack(pady=5)

        if self.product_data:
            self.title("Editar Produto")
            self.name_ent.insert(0, self.product_data.get("name", ""))
            self.qty_ent.insert(0, str(self.product_data.get("qty", 0)))
            self.price_ent.insert(0, f"{self.product_data.get('price', 0.0):.2f}")
            
            # Se vier o ID inteligente sequencial interno, evita exibir no campo para não confundir
            raw_barcode = self.product_data.get("barcode", "")
            if raw_barcode and not raw_barcode.startswith("INT-"):
                self.barcode_ent.insert(0, raw_barcode)

        # Botão Concluir chamando o gatilho externo do controlador

        btn_text = "SALVAR ALTERAÇÕES" if self.product_data else "CONCLUIR CADASTRO"
        ctk.CTkButton(
            self, 
            text=btn_text,
            fg_color="#007700",
            hover_color="#006400",
            width=320,
            command=self.trigger_save
        ).pack(pady=20)


    def toggle_advanced_fields(self):
        """Estica ou encolhe a janela para exibir os campos secundários."""
        if self.optional_container.winfo_ismapped():
            # Se já está visível, esconde e encolhe a janela
            self.optional_container.pack_forget()
            self.geometry("450x330")
            self.btn_toggle.configure(text="➕ Mostrar Informações Avançadas")
        else:
            # Se está oculto, exibe no meio do formulário e estica a janela
            self.optional_container.pack(after=self.btn_toggle, pady=5)
            # Se for admin precisa de mais espaço por causa do campo de custo
            height = "490" if self.user_role == "Administrador" else "450"
            self.geometry(f"450x{height}")
            self.btn_toggle.configure(text="➖ Ocultar Informações Avançadas")


    def trigger_save(self):
        """Coleta os dados dos campos e terceiriza o processamento para o controlador."""
        name = self.name_ent.get().strip()
        qty_raw = self.qty_ent.get().strip()
        price_raw = self.price_ent.get().strip()

        # Coleta das variáveis opcionais
        cost_raw = self.cost_ent.get().strip() if self.cost_ent else "0"
        barcode = self.barcode_ent.get().strip()
        batch = self.batch_ent.get().strip()
        expiry = self.expiry_ent.get().strip()

        # Dispara a lógica de validação e salvamento no StockController
        self.controller.process_new_product(name, qty_raw, price_raw, cost_raw, barcode, batch, expiry, self.error_lbl, self, self.product_data)