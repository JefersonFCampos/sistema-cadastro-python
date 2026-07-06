from validations import validate_product_name, validate_product_values
from database import db_save_new_product, db_list_products, db_quick_increment_stock, db_update_product



class StockController:

    def __init__(self, dashboard_view):
        """
        Gerencia toda a regra de negócio e dados do estoque.
        :param dashboard_view: Referência da View para atualizar o layout gráfico.
        """
        self.view = dashboard_view

    def get_filtered_products(self, search_term=""):
        """Busca produtos direto do banco aplicando o filtro digitado."""
        return db_list_products(search_term)


    def get_products(self):
        """Retorna a lista atual de produtos para a tabela renderizar."""
        return db_list_products()


    def add_quick_stock(self, product_item, current_view):
        """Aumenta a quantidade do item no SQLite e manda a tela se atualizar."""
        product_id = product_item["id"]
        # Executa o UPDATE +10 no banco
        if db_quick_increment_stock(product_id):
            current_view.render_products_table()


    def process_new_product(self, name, qty_raw, price_raw, cost_raw, barcode, batch, expiry, error_label, modal_instance, product_data=None):
        """Aplica as barreiras de validação e salva o novo produto na lista."""
        error_label.configure(text="") # Limpa mensagens de erro anteriores

        # 1. Barreira de Segurança do Nome do Produto
        name_ok, name_msg = validate_product_name(name)
        if not name_ok:
            error_label.configure(text=f"❌ {name_msg}")
            return False

        # 2. Barreira de Segurança dos Valores Numéricos (Quantidade, Custo e Venda)
        is_admin_user = (self.view.user_role == "Administrador")
        values_ok, values_msg = validate_product_values(qty_raw, cost_raw, price_raw, is_admin_user)
        if not values_ok:
            error_label.configure(text=f"❌ {values_msg}")
            return False

        # Se passou por todas as validações, as conversões de tipo abaixo estão 100% seguras
        formatted_name = " ".join(name.strip().split()).title()
        final_qty = int(qty_raw.strip())
        final_price = float(price_raw.strip().replace(",", "."))

        # --- NOVA PERSISTÊNCIA REAL NO BANCO DE DADOS ---
        # Envia os parâmetros validados. Lote, validade, custo e código de barras 
        # (caso não fornecidos) serão tratados como opcionais e NULL no banco.
        # Se já possui dados, executa a atualização física usando o ID existente
        if product_data and "id" in product_data:    
            success, db_msg = db_update_product(
                product_id=product_data["id"],
                name=formatted_name,
                qty=final_qty,
                price_sale=final_price,
                barcode=barcode,
                batch=batch,
                expiry=expiry,
                price_cost=cost_raw
            )
        
        else:
            # Se não possui dados anteriores, segue o fluxo normal de novo cadastro
            success, db_msg = db_save_new_product(
                name=formatted_name,
                qty=final_qty,
                price_sale=final_price,
                barcode=barcode,
                batch=batch,
                expiry=expiry,
                price_cost=cost_raw
            )

        if success:
           # Pede para a "casca" principal acessar a subview ativa do estoque e atualizar a tabela visual
            if hasattr(self.view, 'current_subview') and hasattr(self.view.current_subview, 'render_products_table'):
                self.view.current_subview.render_products_table()
        
            # Fecha a janela do formulário flutuante
            modal_instance.destroy()
            return True
        
        else:
            error_label.configure(text=f"❌ {db_msg}")
            return False


    def open_edit_product_modal(self, product_item):
        """Abre o arquivo do modal injetando os dados da linha selecionada."""
        from views.modals.add_product_modal import AddProductModal
        # O quarto argumento 'product_item' ativa o modo de edição dentro do modal
        AddProductModal(self.view, self, self.view.user_role, product_data=product_item)


    def load_stock_screen(self, container):
        """O controlador importa e monta a tela no contêiner fornecido."""
        from views.dashboard.stock_view import StockManagementFrame
        # Instancia a tela neta colando-a no contêiner da direita
        self.view.current_subview = StockManagementFrame(container, self, self.view.user_role, self.view)
        self.view.current_subview.pack(fill="both", expand=True)
 
