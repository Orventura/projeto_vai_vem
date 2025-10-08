import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from getpass import getuser

# Inicializa banco e triggers
def inicializar_banco():
    conn = sqlite3.connect("exemplo.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        morador TEXT,
        rua TEXT,
        bairro TEXT,
        cidade TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log_base (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        id_original INTEGER,
        morador TEXT,
        rua TEXT,
        bairro TEXT,
        cidade TEXT,
        acao TEXT,
        user TEXT,
        data_modificacao TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Remove triggers se já existirem
    cursor.execute("DROP TRIGGER IF EXISTS log_insert_base")
    cursor.execute("DROP TRIGGER IF EXISTS log_update_base")

    # Cria triggers com função integrada para capturar usuário
    cursor.execute(f"""
    CREATE TRIGGER log_insert_base
    AFTER INSERT ON base
    BEGIN
        INSERT INTO log_base (id_original, morador, rua, bairro, cidade, acao, user)
        VALUES (
            NEW.id, NEW.morador, NEW.rua, NEW.bairro, NEW.cidade, 'INSERT', '{getuser()}'
        );
    END;
    """)

    cursor.execute(f"""
    CREATE TRIGGER log_update_base
    AFTER UPDATE ON base
    BEGIN
        INSERT INTO log_base (id_original, morador, rua, bairro, cidade, acao, user)
        VALUES (
            NEW.id, NEW.morador, NEW.rua, NEW.bairro, NEW.cidade, 'UPDATE', '{getuser()}'
        );
    END;
    """)

    conn.commit()
    conn.close()

# Funções de banco
def inserir_dados(morador, rua, bairro, cidade):
    conn = sqlite3.connect("exemplo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO base (morador, rua, bairro, cidade) VALUES (?, ?, ?, ?)",
                   (morador, rua, bairro, cidade))
    conn.commit()
    conn.close()

def listar_base():
    conn = sqlite3.connect("exemplo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM base")
    return cursor.fetchall()

def listar_logs():
    conn = sqlite3.connect("exemplo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM log_base ORDER BY data_modificacao DESC")
    return cursor.fetchall()

# Interface gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Moradores")
        self.root.geometry("700x500")

        self.frame_form = tk.Frame(root)
        self.frame_form.pack(pady=10)

        tk.Label(self.frame_form, text="Morador").grid(row=0, column=0)
        tk.Label(self.frame_form, text="Rua").grid(row=0, column=1)
        tk.Label(self.frame_form, text="Bairro").grid(row=0, column=2)
        tk.Label(self.frame_form, text="Cidade").grid(row=0, column=3)

        self.e_morador = tk.Entry(self.frame_form)
        self.e_rua = tk.Entry(self.frame_form)
        self.e_bairro = tk.Entry(self.frame_form)
        self.e_cidade = tk.Entry(self.frame_form)

        self.e_morador.grid(row=1, column=0)
        self.e_rua.grid(row=1, column=1)
        self.e_bairro.grid(row=1, column=2)
        self.e_cidade.grid(row=1, column=3)

        self.btn_inserir = tk.Button(self.frame_form, text="Inserir", command=self.inserir)
        self.btn_inserir.grid(row=1, column=4, padx=10)

        self.tree_base = ttk.Treeview(root, columns=("id", "morador", "rua", "bairro", "cidade"), show="headings")
        for col in self.tree_base["columns"]:
            self.tree_base.heading(col, text=col)
        self.tree_base.pack(pady=10)

        self.tree_log = ttk.Treeview(root, columns=("id_log", "id_original", "morador", "acao", "user", "data_modificacao"), show="headings")
        for col in self.tree_log["columns"]:
            self.tree_log.heading(col, text=col)
        self.tree_log.pack(pady=10)

        tk.Label(self.frame_form, text="ID para atualizar").grid(row=2, column=0)
        self.e_id_update = tk.Entry(self.frame_form)
        self.e_id_update.grid(row=2, column=1)

        self.btn_carregar = tk.Button(self.frame_form, text="Carregar", command=self.carregar_para_edicao)
        self.btn_carregar.grid(row=2, column=2)

        self.btn_atualizar = tk.Button(self.frame_form, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.grid(row=2, column=3)


        self.atualizar_listas()

    def inserir(self):
        morador = self.e_morador.get().strip()
        rua = self.e_rua.get().strip()
        bairro = self.e_bairro.get().strip()
        cidade = self.e_cidade.get().strip()

        if not all([morador, rua, bairro, cidade]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        inserir_dados(morador, rua, bairro, cidade)
        self.atualizar_listas()
        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")

    def atualizar_listas(self):
        for i in self.tree_base.get_children():
            self.tree_base.delete(i)
        for row in listar_base():
            self.tree_base.insert("", "end", values=row)

        for i in self.tree_log.get_children():
            self.tree_log.delete(i)
        for row in listar_logs():
            self.tree_log.insert("", "end", values=(row[0], row[1], row[2], row[6], row[7], row[8]))

    def carregar_para_edicao(self):
        id_str = self.e_id_update.get().strip()
        if not id_str.isdigit():
            messagebox.showerror("Erro", "Informe um ID válido.")
            return

        conn = sqlite3.connect("exemplo.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM base WHERE id = ?", (int(id_str),))
        row = cursor.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Erro", f"Nenhum registro encontrado com ID {id_str}.")
            return

        self.e_morador.delete(0, tk.END)
        self.e_rua.delete(0, tk.END)
        self.e_bairro.delete(0, tk.END)
        self.e_cidade.delete(0, tk.END)

        self.e_morador.insert(0, row["morador"])
        self.e_rua.insert(0, row["rua"])
        self.e_bairro.insert(0, row["bairro"])
        self.e_cidade.insert(0, row["cidade"])

    def atualizar(self):
        id_str = self.e_id_update.get().strip()
        if not id_str.isdigit():
            messagebox.showerror("Erro", "Informe um ID válido para atualizar.")
            return
    
        morador = self.e_morador.get().strip()
        rua = self.e_rua.get().strip()
        bairro = self.e_bairro.get().strip()
        cidade = self.e_cidade.get().strip()
    
        if not all([morador, rua, bairro, cidade]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
    
        conn = sqlite3.connect("exemplo.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE base SET morador=?, rua=?, bairro=?, cidade=? WHERE id=?",
                       (morador, rua, bairro, cidade, int(id_str)))
        conn.commit()
        conn.close()
    
        self.atualizar_listas()
        messagebox.showinfo("Sucesso", f"Registro {id_str} atualizado com sucesso!")


# Executa
if __name__ == "__main__":
    inicializar_banco()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
