import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app_controller, role_code="2"):
        super().__init__(master, corner_radius=0)
        self.app = app_controller
        self.user_role = "Administrador" if role_code == "1" else "Funcionário"

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
        
        # Inicia exibindo o estoque por padrão para desenharmos ele primeiro
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

        # Título da Seção
        ctk.CTkLabel(
            self.content_frame, text="Gerenciamento de Estoque", font=("Roboto", 22, "bold")
        ).pack(anchor="w", pady=(0, 15))

        # --- BARRA DE FERRAMENTAS SUPERIOR (Busca e Cadastro) ---
        tools_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tools_frame.pack(fill="x", pady=(0, 15))

        # Campo de busca esticado na esquerda
        self.search_entry = ctk.CTkEntry(
            tools_frame, placeholder_text="🔍 Comece a digitar o nome do produto para filtrar...", width=450
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Botão de Ação chamativo na direita
        self.add_product_button = ctk.CTkButton(
            tools_frame, text="+ Novo Produto", fg_color="#2b8a3e", hover_color="#237032", font=("Roboto", 13, "bold"), command=self.open_add_product_modal
        )
        self.add_product_button.pack(side="right")


        # --- CORPO DA TABELA (Scrollable Grid) ---
        # Usamos o ScrollableFrame para garantir que a lista role se houver 100 produtos
        self.table_scroll = ctk.CTkScrollableFrame(self.content_frame, height=380)
        self.table_scroll.pack(fill="both", expand=True)

        # 1. Cabeçalho Fixo da Tabela Planilhada
        # Muda sutilmente de cor se o tema do Windows for Dark ou Light
        header_bg = "gray25" if ctk.get_appearance_mode() == "Dark" else "gray85"
        table_header = ctk.CTkFrame(self.table_scroll, fg_color=header_bg, height=35)
        table_header.pack(fill="x", pady=(0, 5))
        table_header.pack_propagate(False)

        # Alinhamento das Colunas usando larguras fixas baseadas em pixels
        ctk.CTkLabel(table_header, text="ID", font=("Roboto", 12, "bold"), width=50, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Nome do Produto", font=("Roboto", 12, "bold"), width=320, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Qtd Estoque", font=("Roboto", 12, "bold"), width=100, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Preço Venda", font=("Roboto", 12, "bold"), width=100, anchor="w").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(table_header, text="Ações", font=("Roboto", 12, "bold"), width=80, anchor="center").pack(side="right", padx=10, pady=5)

        # 2. Massa de Dados Simulada (Mock)
        # Criada puramente para vermos como as linhas horizontais se comportam na interface gráfica
        mock_products = [
            ("1", "Arroz Integral Camil 1kg", 45, 8.90),
            ("2", "Feijão Preto Calgari 1kg", 2, 9.40),  # Quantidade crítica para testar o alerta
            ("3", "Óleo de Soja Soya 900ml", 18, 6.75),
            ("4", "Açúcar Refinado Caravelas 1kg", 0, 4.20), # Zerado para testar alerta severo
            ("5", "Leite Integral Piracanjuba 1L", 60, 5.10)
        ]

        # Renderiza cada linha simulada na nossa grid visual
        for prod_id, name, qty, price in mock_products:
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            # Coluna ID
            ctk.CTkLabel(row_frame, text=prod_id, width=50, anchor="w").pack(side="left", padx=10)
            
            # Coluna Nome
            ctk.CTkLabel(row_frame, text=name, width=320, anchor="w").pack(side="left", padx=10)
            
            # Coluna Quantidade (Se for menor ou igual a 3 unidades, colore o texto de vermelho de alerta)
            qty_color = "#fa5252" if qty <= 3 else None
            qty_weight = "bold" if qty <= 3 else "normal"
            ctk.CTkLabel(
                row_frame, text=f"{qty} un", width=100, anchor="w", text_color=qty_color, font=("Roboto", 13, qty_weight)
            ).pack(side="left", padx=10)
            
            # Coluna Preço de Venda
            ctk.CTkLabel(row_frame, text=f"R$ {price:.2f}", width=100, anchor="w").pack(side="left", padx=10)

            # Coluna Direita: Caixa de Ferramentas / Botões Rápidos de Ação por Linha
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.pack(side="right", padx=10)

            # Botão Rápido Editar (Apenas visual)
            ctk.CTkButton(
                actions_frame, text="✏️", width=30, height=25, fg_color="transparent", hover=False, command=lambda n=name: self.edit_product(n)
            ).pack(side="left", padx=2)

            # Botão Rápido Entrada Rápida de mercadoria (Apenas visual)
            ctk.CTkButton(
                actions_frame, text="➕", width=30, height=25, fg_color="transparent", hover=False, command=lambda n=name: self.quick_add_stock(n)
            ).pack(side="left", padx=2)

    # =====================================================================
    # MÉTODOS DE AÇÃO DO ESTOQUE (FUNCIONALIDADES)
    # =====================================================================

    def open_add_product_modal(self):
        """Abre uma janela flutuante (Toplevel) para preencher o formulário do novo item."""
        modal = ctk.CTkToplevel(self)
        modal.title("Adicionar Item ao Estoque")
        modal.geometry("450x450")
        
        # Trava o foco nesta janela. O usuário não consegue clicar atrás até fechar o modal.
        modal.grab_set()
        modal.focus_force()

        # Título interno do Formulário
        ctk.CTkLabel(modal, text="📦 Cadastrar Novo Produto", font=("Roboto", 18, "bold")).pack(pady=20)

        # Campos de Entrada de Dados (Layout limpo em pilha)
        name_ent = ctk.CTkEntry(modal, placeholder_text="Nome do Produto (Ex: Sabão em Pó 1kg)", width=320)
        name_ent.pack(pady=8)

        qty_ent = ctk.CTkEntry(modal, placeholder_text="Quantidade em Estoque Inicial", width=320)
        qty_ent.pack(pady=8)

        # Se o usuário for Administrador, ele vê o preço de custo. 
        # (Lembra da regra de negócio de ocultar custos de funcionários comuns?)
        cost_ent = None
        if self.user_role == "Administrador":
            cost_ent = ctk.CTkEntry(modal, placeholder_text="Preço de Custo Unitário (R$)", width=320)
            cost_ent.pack(pady=8)

        price_ent = ctk.CTkEntry(modal, placeholder_text="Preço de Venda ao Cliente (R$)", width=320)
        price_ent.pack(pady=8)

        # Label invisível para mostrar mensagens de erro de validação futura
        error_lbl = ctk.CTkLabel(modal, text="", text_color="#fa5252", font=("Roboto", 12))
        error_lbl.pack(pady=5)

        # Função interna disparada ao clicar em Salvar
        def save_action():
            print(f"--- Tentativa de Cadastro ---")
            print(f"Nome: {name_ent.get()}")
            print(f"Quantidade: {qty_ent.get()}")
            if cost_ent:
                print(f"Custo: {cost_ent.get()}")
            print(f"Venda: {price_ent.get()}")
            
            # Fecha a janela temporariamente após simular o clique
            modal.destroy()

        # Botão Concluir dentro do Modal
        ctk.CTkButton(
            modal, text="CONCLUIR CADASTRO", fg_color="#007700", hover_color="#006400", width=320, command=save_action
        ).pack(pady=20)


    def quick_add_stock(self, product_name):
        """Simula a entrada rápida (+10 unidades) na linha do produto."""
        print(f"📦 [ENTRADA RÁPIDA] Adicionado +10 unidades ao produto: '{product_name}'")


    def edit_product(self, product_name):
        """Simula a abertura da tela de edição do item selecionado."""
        print(f"✏️ [EDITAR] Abrindo formulário de edição para o produto: '{product_name}'")
