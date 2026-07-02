from validations import validate_product_name, validate_product_values

class StockController:
    def __init__(self, dashboard_view):
        """
        Gerencia toda a regra de negócio e dados do estoque.
        :param dashboard_view: Referência da View para atualizar o layout gráfico.
        """
        self.view = dashboard_view
        
        # Centralização da lista em memória, removida de dentro da View
        self.products_list = [
            {"id": "1", "name": "Arroz Integral Camil 1kg", "qty": 45, "price": 8.90},
            {"id": "2", "name": "Feijão Preto Calgari 1kg", "qty": 2, "price": 9.40},
            {"id": "3", "name": "Óleo de Soja Soya 900ml", "qty": 18, "price": 6.75}
        ]

    def get_products(self):
        """Retorna a lista atual de produtos para a tabela renderizar."""
        return self.products_list

    def add_quick_stock(self, product_item, current_view):
        """Aumenta a quantidade do item e manda a tela neta se atualizar."""
        product_item["qty"] += 10
        current_view.render_products_table() # <--- Atualiza a tela neta específica

    def process_new_product(self, name, qty_raw, price_raw, cost_raw, error_label, modal_instance):
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

        # Estrutura o novo produto em formato de dicionário
        new_product = {
            "id": str(len(self.products_list) + 1),
            "name": formatted_name,
            "qty": final_qty,
            "price": final_price
        }

        # Salva o produto na lista em memória do controlador
        self.products_list.append(new_product)
        
        # Pede para a "casca" principal acessar a subview ativa do estoque e atualizar a tabela visual
        if hasattr(self.view, 'current_subview') and hasattr(self.view.current_subview, 'render_products_table'):
            self.view.current_subview.render_products_table()
            
        # Fecha a janela do formulário flutuante
        modal_instance.destroy()
        return True

