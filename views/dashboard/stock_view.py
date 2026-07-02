import customtkinter as ctk
from views.modals.add_product_modal import AddProductModal

class StockManagementFrame(ctk.CTkFrame):
    def __init__(self, master, controller, user_role, dashboard_frame):
        """
        Classe 'Neta' dedicada exclusivamente ao visual do estoque.
        """
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.user_role = user_role
        self.dashboard_frame = dashboard_frame

        # --- CONSTRUÇÃO DO DESIGN VISUAL (Movido do Dashboard antigo) ---
        
        # Título da Seção
        ctk.CTkLabel(
            self, text="Gerenciamento de Estoque", font=("Roboto", 22, "bold")
        ).pack(anchor="w", pady=(0, 15))

        # --- BARRA DE FERRAMENTAS SUPERIOR ---
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.pack(fill="x", pady=(0, 15))

        # Campo de busca
        self.search_entry = ctk.CTkEntry(
            tools_frame, placeholder_text="🔍 Comece a digitar o nome do produto para filtrar...", width=450
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Botão de Ação chamativo (Chama o controlador externo direto)
        self.add_product_button = ctk.CTkButton(
            tools_frame, 
            text="+ Novo Produto", 
            fg_color="#2b8a3e", 
            hover_color="#237032", 
            font=("Roboto", 13, "bold"),
            command=lambda: AddProductModal(self.dashboard_frame, self.controller, self.user_role)
        )
        self.add_product_button.pack(side="right")

        # --- CORPO DA TABELA (Scrollable Grid) ---
        self.table_scroll = ctk.CTkScrollableFrame(self, height=380)
        self.table_scroll.pack(fill="both", expand=True)

        # Dispara a renderização inicial dos produtos
        self.render_products_table()

    def render_products_table(self):
        """Limpa as linhas visuais e redesenha os produtos usando os dados do controlador."""
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        # Cabeçalho Fixo da Tabela
        header_bg = "gray25" if ctk.get_appearance_mode() == "Dark" else "gray85"
        table_header = ctk.CTkFrame(self.table_scroll, fg_color=header_bg, height=35)
        table_header.pack(fill="x", pady=(0, 5))
        table_header.pack_propagate(False)

        ctk.CTkLabel(table_header, text="ID", font=("Roboto", 12, "bold"), width=50, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Nome do Produto", font=("Roboto", 12, "bold"), width=320, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Qtd Estoque", font=("Roboto", 12, "bold"), width=100, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Preço Venda", font=("Roboto", 12, "bold"), width=100, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Ações", font=("Roboto", 12, "bold"), width=80, anchor="center").pack(side="right", padx=10, pady=5)

        # Coleta a lista de dados protegida dentro do controlador
        for item in self.controller.get_products():
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(row_frame, text=item["id"], width=50, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=item["name"], width=320, anchor="w").pack(side="left", padx=10)
            
            qty_color = "#fa5252" if item["qty"] <= 3 else None
            qty_weight = "bold" if item["qty"] <= 3 else "normal"
            ctk.CTkLabel(row_frame, text=f"{item['qty']} un", width=100, anchor="w", text_color=qty_color, font=("Roboto", 13, qty_weight)).pack(side="left", padx=10)
            
            ctk.CTkLabel(row_frame, text=f"R$ {item['price']:.2f}", width=100, anchor="w").pack(side="left", padx=10)

            # Botões Rápidos de Ação
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.pack(side="right", padx=10)

            # O botão de editar aponta para uma função vazia por enquanto para não quebrar
            ctk.CTkButton(actions_frame, text="✏️", width=30, height=25, fg_color="transparent", hover=False).pack(side="left", padx=2)
            
            # O botão de entrada rápida chama o controlador passando a si mesma (View) para poder atualizar depois
            ctk.CTkButton(actions_frame, text="➕", width=30, height=25, fg_color="transparent", hover=False, command=lambda i=item: self.controller.add_quick_stock(i, self)).pack(side="left", padx=2)
