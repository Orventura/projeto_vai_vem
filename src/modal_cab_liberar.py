import customtkinter as ctk
from tkinter import messagebox
import sqlite3 as lite

class Liberacao(ctk.CTkToplevel):
    def __init__(self, master, conteiner, bd_path, lista_fabrica, lista_status, lista_booking_retirada, lista_destino):
        super().__init__(master)
        self.title("REGISTRAR LIBERAÇÃO")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()

        self.conteiner = conteiner
        self.bd_path = bd_path
        self.lista_fabrica = lista_fabrica
        self.lista_status = lista_status
        self.lista_booking_retirada = lista_booking_retirada
        self.lista_destino = lista_destino
        self.widgets = {}

        self._carregar_dados()
        self._criar_layout()
        self._criar_campos()
        self._criar_botao()

    def _carregar_dados(self):
        conexao = lite.connect(self.bd_path)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM BASE WHERE CONTEINER = ?", (self.conteiner,))
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            self.dados_cntr = {
                "UNIDADE": resultado[6],
                "ARMADOR": resultado[4],
                "TRANSPORTADOR": resultado[5],
                "BOOKING ENTRADA": resultado[2]
            }
        else:
            messagebox.showerror("Erro", "Contêiner não encontrado.")
            self.destroy()

    def _criar_layout(self):
        self.frames = {
            "superior_esquerda": ctk.CTkFrame(self),
            "superior_meio": ctk.CTkFrame(self),
            "superior_direita": ctk.CTkFrame(self),
            "inferior": ctk.CTkFrame(self),
            "inferior_esquerda": ctk.CTkFrame(self),
            "inferior_meio": ctk.CTkFrame(self),
            "inferior_direita": ctk.CTkFrame(self),
            "extra": ctk.CTkFrame(self)
        }

        self.frames["superior_esquerda"].grid(row=0, column=0, padx=10, pady=10, sticky='nswe')
        self.frames["superior_meio"].grid(row=0, column=1, padx=10, pady=10, sticky='nswe')
        self.frames["superior_direita"].grid(row=0, column=2, padx=10, pady=10, sticky='nswe')
        self.frames["inferior_esquerda"].grid(row=1, column=0, padx=10, pady=10, sticky='nswe')
        self.frames["inferior_meio"].grid(row=1, column=1, padx=10, pady=10, sticky='nswe')
        self.frames["inferior_direita"].grid(row=1, column=2, padx=10, pady=10, sticky='nswe')
        self.frames["extra"].grid(row=1, column=3, padx=10, pady=10, sticky='nswe')
        self.frames["inferior"].grid(row=0, column=3, padx=10, pady=10, sticky='nswe')

    def _criar_campos(self):
        # Labels informativos
        for i, (label, valor) in enumerate(self.dados_cntr.items()):
            campo = ctk.CTkLabel(self.frames["superior_esquerda"], text=f"{label}: {valor}")
            campo.grid(row=i, column=0, padx=10, pady=5, sticky='w')

        # Campos editáveis
        campos = [
            ("Nota Fiscal", "entry", "inferior_esquerda"),
            ("Lacre Armador", "entry", "inferior_esquerda"),
            ("Lacre Philco", "entry", "inferior_esquerda"),
            ("Peso Bruto", "entry", "inferior_meio"),
            ("Peso Líquido", "entry", "inferior_meio"),
            ("Valor da Carga", "entry", "inferior_meio"),
            ("Fábrica", "combo", "inferior_direita", self.lista_fabrica),
            ("Booking Retirada", "combo", "inferior_direita", self.lista_booking_retirada),
            ("Status", "combo", "inferior_direita", self.lista_status),
            ("Destino", "combo", "extra", self.lista_destino),
            ("Isca 1", "entry", "extra"),
            ("Isca 2", "entry", "extra"),
            ("Observações", "textbox", "extra")
        ]

        for i, campo in enumerate(campos):
            texto, tipo, frame = campo[:3]
            opcoes = campo[3] if len(campo) > 3 else []

            label = ctk.CTkLabel(self.frames[frame], text=texto)
            label.grid(row=i*2, column=0, padx=10, pady=5, sticky='w')

            if tipo == "entry":
                widget = ctk.CTkEntry(self.frames[frame])
            elif tipo == "combo":
                widget = ctk.CTkComboBox(self.frames[frame], values=opcoes, state='readonly')
                widget.set("")
            elif tipo == "textbox":
                widget = ctk.CTkTextbox(self.frames[frame], width=100, height=30)

            widget.grid(row=i*2+1, column=0, padx=10, pady=5, sticky='nswe')
            self.widgets[texto] = widget

        self.widgets["Status"].set("LIBERADO")

    def _criar_botao(self):
        botao = ctk.CTkButton(self.frames["inferior"], text="Lançar dados", command=self._salvar_dados)
        botao.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')

    def _salvar_dados(self):
        dados = {}
        for texto, widget in self.widgets.items():
            if isinstance(widget, ctk.CTkTextbox):
                dados[texto] = widget.get("1.0", "end").strip()
            else:
                dados[texto] = widget.get().strip()

        print("Dados lançados:")
        for k, v in dados.items():
            print(f"{k}: {v}")

        # Aqui você pode adicionar lógica para salvar no banco
        self.fechar()

    def fechar(self):
        self.destroy()
