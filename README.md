# Sistema de Cadastro de Clientes - Python & SQLite

Este projeto é um sistema de gerenciamento de cadastros desenvolvido para consolidar conceitos de **Arquitetura Modular**, **Persistência de Dados Relacionais** e **Design de Interação (UX/UI)**. 

Originalmente concebido como um módulo de teste para um sistema de gestão de estoque, a aplicação foca na integridade dos dados e na experiência do usuário em ambiente Desktop.

## 🚀 Funcionalidades

- **Interface Gráfica (GUI):** Desenvolvida com Tkinter, priorizando o feedback visual imediato.
- **Validação em Tempo Real:** Verificação de campos (Nome, DDD, Telefone e E-mail) durante a digitação utilizando **Expressões Regulares (Regex)**.
- **Persistência de Dados:** Integração completa com **SQLite3** para armazenamento local e portável.
- **Arquitetura Modular:** Separação clara entre lógica de validação (`validations.py`), manipulação de dados (`database.py`) e interface (`main.py`).

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.14.5
- **Interface:** Tkinter (GUI)
- **Banco de Dados:** SQLite3
- **Regex:** Biblioteca `re` para validação de padrões de strings.
- **Ambiente:** Desenvolvido e testado no VS Code e PyCharm.

## 📂 Estrutura do Projeto

```text
├── main.py          # Ponto de entrada do sistema e controle da UI
├── validations.py   # Lógica de negócio e regras de validação
├── database.py      # Módulo de persistência e comandos SQL
└── data/            # Pasta gerada automaticamente para o banco .db
```

## 📝 Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone o repositório:
   ```bash
   git clone https://github.com/JefersonFCampos/sistema-cadastro-python
   ```
3. Acesse a pasta do projeto e execute:
   ```bash
   python main.py
   ```

## 🎓 Contexto Acadêmico

Este projeto integra meu portfólio de estudante de **Análise e Desenvolvimento de Sistemas (ADS) na UNINTER**, aplicando conceitos de Engenharia de Software, Modelagem de Dados e Programação Orientada a Objetos.

---
Desenvolvido por **Jeferson F.Campos**
