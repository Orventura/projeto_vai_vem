import customtkinter as ctk
import sqlite3
import getpass
from tkinter import messagebox
from models.model_cab_config import Listas
from pathlib import Path
from utils.config import *

# Inicialização do CTk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


db_path = data_dir = BD_CABOTAGEM

print('DEBUG', 'ACESSO_BD_CABOTAGEM', 'modal_cab_config.py',db_path)

# Conexão com banco SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Cria tabelas_config se não existirem
tabelas_config = ["fabrica", "armador", "transportador", "destino", "situacao", "booking", "iscas_ag", "iscas_cliente"]
tabelas_criar = tabelas_config + ["user_auth"]
for tabela in tabelas_criar:
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tabela} (valor TEXT)")
conn.commit()


class ModalConfiguracoes(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.user = str(getpass.getuser()).upper()
        self._autenticacao()
        self.title("Configurações")
        self.geometry("800x650")
        self.transient(master)
        self.grab_set()
        self.focus_force()

        self.textboxes = {}



        # Frame rolável
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Organiza os campos em 2 colunas
        colunas = 2
        for i, tabela in enumerate(tabelas_config):
            linha = i // colunas
            coluna = i % colunas

            frame_item = ctk.CTkFrame(self.scroll_frame)
            frame_item.grid(row=linha, column=coluna, padx=10, pady=10, sticky="nsew")

            label = ctk.CTkLabel(frame_item, text=tabela.capitalize())
            label.pack(pady=(5, 0))

            textbox = ctk.CTkTextbox(frame_item, width=250, height=120)
            textbox.pack(pady=(5, 5), fill='x')
            self.textboxes[tabela] = textbox

            self.carregar_dados(tabela, textbox)

        # Configura as colunas do scroll_frame para expandirem
        for c in range(colunas):
            self.scroll_frame.grid_columnconfigure(c, weight=1)

        # Botão de salvar
        btn_salvar = ctk.CTkButton(self, text="Salvar Alterações", command=self.salvar_todos)
        btn_salvar.pack(pady=15)

    def carregar_dados(self, tabela, textbox):
        """Carrega os dados do banco no textbox."""
        textbox.delete("1.0", "end")
        cursor.execute(f"SELECT valor FROM {tabela}")
        for (valor,) in cursor.fetchall():
            textbox.insert("end", f"{valor}\n")

    def permissao(self):
        """Valida permissão de usuário"""
        with Listas() as auth:
            usuarios_autorizados = auth.lista_user_auth()
            if self.user in usuarios_autorizados:
                return True
            return False

    def _autenticacao(self):
        if not self.permissao():
            messagebox.showerror("Erro", f'{self.user}, você não é autorizado!')
            self.destroy()  # Fecha o modal

    def salvar_todos(self):
        """Salva os valores dos textboxes no banco."""
        for tabela, textbox in self.textboxes.items():
            linhas = textbox.get("1.0", "end").strip().split("\n")
            cursor.execute(f"DELETE FROM {tabela}")
            for linha in linhas:
                if linha.strip():
                    cursor.execute(f"INSERT INTO {tabela} (valor) VALUES (?)", (linha.strip().upper(),))
        conn.commit()
        self.destroy()

    def obter_valores(self):
        """
        Retorna os valores de cada tabela como uma tupla de listas.
        Exemplo:
        ([fabrica1, fabrica2], [armador1, armador2], ...)
        """
        resultado = []
        for tabela in tabelas_config:
            cursor.execute(f"SELECT valor FROM {tabela}")
            lista = [row[0] for row in cursor.fetchall()]
            resultado.append(lista)
        return tuple(resultado)


if __name__ == "__main__":
    # Janela principal para teste
    app = ctk.CTk()
    app.geometry("350x200")
    app.title("Principal")

    def abrir_modal():
        modal = ModalConfiguracoes(app)
        app.wait_window(modal)
        print("Valores salvos:")
        print(modal.obter_valores())

    btn_abrir_modal = ctk.CTkButton(app, text="Abrir Configurações", command=abrir_modal)
    btn_abrir_modal.pack(pady=60)

    app.mainloop()
