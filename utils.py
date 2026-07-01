from database import save_user
from validations import (
      validate_name,
      validate_email,
      validate_phone,
      validate_password,
      confirm_password_match,
)


def sync_field(entry_widget, error_label, validation_function):
        """Realiza a ponte entre a interface gráfica e a lógica de validação."""
        raw_text = entry_widget.get()
        valid, mensagem = validation_function(raw_text)

        if not valid:
            error_label.configure(text=mensagem, text_color="#fa5252")
        else:
            error_label.configure(text="")
        return valid


def clean_error_msg(error_label, event=None):
        """Remove a mensagem de erro da tela."""
        error_label.configure(text="")


def save_user_data(frame): 
    """Coordena a validação final e a persistência no banco."""
    name_ok = sync_field(
        frame.name_entry, 
        frame.name_error_label, 
        validate_name
    )
    email_ok = sync_field(
        frame.email_entry, 
        frame.email_error_label, 
        validate_email
    )
    phone_ok = sync_field(
        frame.phone_entry, 
        frame.phone_error_label, 
        validate_phone
    )
    password_ok = sync_field(
        frame.password_entry, 
        frame.password_error_label, 
        validate_password
    )
    confirm_password_ok = sync_field(
        frame.confirm_password_entry,
        frame.confirm_password_error_label,
        lambda valor: confirm_password_match(
            frame.password_entry.get(), valor
        ),
    )

    if all([name_ok, email_ok, phone_ok, password_ok, confirm_password_ok]):
        raw_name = frame.name_entry.get().strip()
        name_formatted = " ".join(raw_name.split()).title()
        email = frame.email_entry.get().strip()
        password = frame.password_entry.get().strip()
        phone = frame.phone_entry.get().strip()
        
        access_types = {"Administrador": "1", "Funcionário": "2"}
        role_code = access_types[frame.role_option_menu.get()]
        
        success, db_message = save_user(name_formatted, email, phone, password, role_code)
        
        if success:
            frame.submit_status_label.configure(
                text=f"✅ {db_message}", text_color="#006400"
            )
            # Limpeza dos campos após sucesso
            frame.name_entry.delete(0, "end")
            frame.email_entry.delete(0, "end")
            frame.phone_entry.delete(0, "end")
            frame.password_entry.delete(0, "end")
            frame.confirm_password_entry.delete(0, "end")
        else:
            frame.submit_status_label.configure(
                text=f"❌ {db_message}", text_color="#fa5252"
            )
    else:
        frame.submit_status_label.configure(text="Erro: Verifique os campos em destaque", text_color="#fa5252")
