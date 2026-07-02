import customtkinter as ctk
from validations import validate_product_values, validate_product_name
from controllers.stock_controller import StockController
from views.modals.add_product_modal import AddProductModal

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app_controller, role_code="2"):
        super().__init__(master, corner_radius=0)
        self.app = app_controller
        self.user_role = "Administrador" if role_code == "1" else "Funcionário"

        self.stock_controller = StockController(self)

        # --- SISTEMA DE GRID (Layout Dividido) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # 1. BARRA LATERAL FIXA (ESQUERDA)
        # =====================================================================
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        # Título do Software
        ctk.CTkLabel(
            self.sidebar_frame, text="📦 MakEstoque", font=("Roboto", 22, "bold")
        ).pack(pady=(25, 5), padx=20, anchor="w")
        
        # Indicador de Perfil do Usuário Logado
        role_color = "#1c7ed6" if self.user_role == "Administrador" else "#2b8a3e"
        ctk.CTkLabel(
            self.sidebar_frame, 
            text=f"● Perfil: {self.user_role}", 
            font=("Roboto", 13, "bold"), 
            text_color=role_color
        ).pack(pady=(0, 30), padx=25, anchor="w")

        # --- Botões de Navegação das Abas ---
        self.btn_general_panel = ctk.CTkButton(
            self.sidebar_frame, text="📊 Painel Geral", fg_color="transparent", anchor="w", command=self.show_general_view
        )
        self.btn_general_panel.pack(fill="x", padx=15, pady=5)

        self.btn_stock = ctk.CTkButton(
            self.sidebar_frame, text="📦 Gerenciar Estoque", fg_color="transparent", anchor="w", command=self.show_stock_view
        )
        self.btn_stock.pack(fill="x", padx=15, pady=5)

        self.btn_sales = ctk.CTkButton(
            self.sidebar_frame, text="💰 Registrar Venda", fg_color="transparent", anchor="w", command=self.show_sales_view
        )
        self.btn_sales.pack(fill="x", padx=15, pady=5)

        # Trava visual de Relatórios para Administrador
        if self.user_role == "Administrador":
            self.btn_reports = ctk.CTkButton(
                self.sidebar_frame, text="📋 Relatórios Avançados", fg_color="transparent", anchor="w", command=self.show_reports_view
            )
            self.btn_reports.pack(fill="x", padx=15, pady=5)

        # Botão Sair permanente no rodapé
        ctk.CTkButton(
            self.sidebar_frame, 
            text="🚪 Sair do Sistema", 
            fg_color="#fa5252", 
            hover_color="#e03131",
            command=lambda: self.app.show_login_frame()
        ).pack(side="bottom", fill="x", padx=15, pady=20)

        # =====================================================================
        # 2. ÁREA DE CONTEÚDO DINÂMICO (DIREITA)
        # =====================================================================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        # Inicia exibindo o estoque por padrão
        self.show_stock_view()


    # --- CONTROLADORES DE NAVEGAÇÃO INTERNA ---
    def clean_content_area(self):
        """Limpa o painel da direita antes de desenhar a nova aba."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


    def highlight_active_button(self, active_button):
        """Destaca visualmente qual botão do menu lateral está ativo."""
        buttons = [self.btn_general_panel, self.btn_stock, self.btn_sales]
        if hasattr(self, 'btn_reports'):
            buttons.append(self.btn_reports)
            
        for btn in buttons:
            if btn == active_button:
                btn.configure(fg_color=["#3b8ed0", "#1f538d"]) # Cor padrão de destaque do CustomTkinter
            else:
                btn.configure(fg_color="transparent")


    # --- VIEWS (MÓDULOS DO PAINEL) ---
    def show_general_view(self):
        self.clean_content_area()
        self.highlight_active_button(self.btn_general_panel)
        ctk.CTkLabel(self.content_frame, text="Painel Geral / Resumo de Indicadores", font=("Roboto", 22, "bold")).pack(anchor="w")


    def show_sales_view(self):
        self.clean_content_area()
        self.highlight_active_button(self.btn_sales)
        ctk.CTkLabel(self.content_frame, text="Frente de Caixa (PDV)", font=("Roboto", 22, "bold")).pack(anchor="w")


    def show_reports_view(self):
        self.clean_content_area()
        self.highlight_active_button(self.btn_reports)
        ctk.CTkLabel(self.content_frame, text="Relatórios Gerenciais Avançados", font=("Roboto", 22, "bold")).pack(anchor="w")


    # =====================================================================
    # CONSTRUÇÃO DO DESIGN VISUAL DO ESTOQUE
    # =====================================================================
    def show_stock_view(self):
        self.clean_content_area()
        self.highlight_active_button(self.btn_stock)

        # Importa e aninha a tela neta dedicada ao estoque dentro do frame de conteúdo
        from views.dashboard.stock_view import StockManagementFrame
        self.current_subview = StockManagementFrame(self.content_frame, self.stock_controller, self.user_role, self)
        self.current_subview.pack(fill="both", expand=True)


    def open_add_product_modal(self):
        """Abre uma janela flutuante para cadastro do novo item."""
        AddProductModal(self, self.stock_controller, self.user_role)


    def quick_add_stock(self, product_item):
        """Aumenta a quantidade do item diretamente na memória e re-renderiza a tabela."""
        product_item["qty"] += 10
        self.render_products_table()


    def edit_product(self, product_name):
        """Simula a abertura da tela de edição do item selecionado."""
        print(f"✏️ [EDITAR] Abrindo formulário de edição para o produto: '{product_name}'")
