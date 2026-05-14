import customtkinter as ctk
from views.login import TelaLogin
from views.cadastro import TelaCadastro


# Configurações globais de estilo do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque")
        self.geometry("700x800")

        # Container Principal para as telas
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both")

        self.mostrar_tela_login()

    def limpar_tela(self):
        """Remove todos os widgets do container principal."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_tela_login(self):
        self.limpar_tela()

        self.tela_atual = TelaLogin(self.container, self)
        self.tela_atual.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_tela_cadastro(self):
        self.limpar_tela()

        self.tela_atual = TelaCadastro(self.container, self)
        self.tela_atual.place(relx=0.5, rely=0.5, anchor="center")
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
