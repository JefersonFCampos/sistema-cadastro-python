import customtkinter as ctk
from views.login import LoginFrame
from views.signup import SignUpFrame
from views.main_dashboard import DashboardFrame

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

        self.show_login_frame()

    def clean_screen(self):
        """Remove todos os widgets do container principal."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_frame(self):
        self.clean_screen()

        self.current_frame = LoginFrame(self.container, self)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_signup_frame(self):
        self.clean_screen()

        self.current_frame = SignUpFrame(self.container, self)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def show_dashboard_frame(self, role_code):
        self.clean_screen()

        # Instancia o Dashboard expandido por toda a janela gráfica
        self.current_frame = DashboardFrame(self.container, self, role_code=role_code)
        self.current_frame.pack(expand=True, fill="both")



if __name__ == "__main__":
    app = App()
    app.mainloop()
