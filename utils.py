from database import conexao_database
from validations import (
      validar_nome,
      validar_email,
      validar_telefone,
      validar_senha,
      validar_confirmacao_senha,
)


def sincronizar_campo(entrada, label_erro, funcao_validacao):
        """Realiza a ponte entre a interface gráfica e a lógica de validação."""
        valor_puro = entrada.get()
        valido, mensagem = funcao_validacao(valor_puro)

        if not valido:
            label_erro.configure(text=mensagem, text_color="#fa5252")
        else:
            label_erro.configure(text="")
        return valido


def limpar_msg_erro(label_erro, event=None):
        """Remove a mensagem de erro da tela."""
        label_erro.configure(text="")


def salvar_database(dado):
        """Coordena a validação final e a persistência no banco."""
        nome_ok = sincronizar_campo(
            dado.entry_cad_nome, dado.label_erro_nome, validar_nome
        )
        email_ok = sincronizar_campo(
            dado.entry_cad_email, dado.label_erro_email, validar_email
        )
        telefone_ok = sincronizar_campo(
            dado.entry_cad_telefone, dado.label_erro_telefone, validar_telefone
        )
        senha_ok = sincronizar_campo(
            dado.entry_cad_senha, dado.label_erro_senha, validar_senha
        )
        repetir_senha_ok = sincronizar_campo(
            dado.entry_repetir_senha,
            dado.label_erro_repetir,
            lambda valor: validar_confirmacao_senha(
                dado.entry_cad_senha.get(), valor
            ),
        )

        if all([nome_ok, email_ok, telefone_ok ,senha_ok, repetir_senha_ok]):
            nome_cru = dado.entry_cad_nome.get().strip()
            nome = " ".join(nome_cru.split()).title()
            
            email = dado.entry_cad_email.get().strip()
            senha = dado.entry_cad_senha.get().strip()
            telefone = dado.entry_cad_telefone.get().strip()

            tipo_acesso = {"Administrador": "1", "Funcionário": "2"}
            codigo_cargo = tipo_acesso[dado.option_cargo.get()]

            sucesso, mensagem_banco = conexao_database(nome, email, telefone, senha, codigo_cargo)

            if sucesso:
                dado.label_commit_cad.configure(
                    text=f"✅ {mensagem_banco}", text_color="#006400"
                )
                # Limpeza dos campos após sucesso
                dado.entry_cad_nome.delete(0, "end")
                dado.entry_cad_email.delete(0, "end")
                dado.entry_cad_telefone.delete(0, "end")
                dado.entry_cad_senha.delete(0, "end")
                dado.entry_repetir_senha.delete(0, "end")
            else:
                dado.label_commit_cad.configure(
                    text=f"❌ {mensagem_banco}", text_color="#fa5252"
                )
        
        else:
            dado.label_commit_cad.configure(text="Erro: Verifique os campos em destaque", text_color="#fa5252")