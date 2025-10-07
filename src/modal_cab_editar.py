import customtkinter as ctk
from tkinter import messagebox
#from bd import BancoDeDados
from utils.config import CustomButton, CustomComboBox, CustomEntry, CustomLabel

class EditarStatus(ctk.CTkToplevel):

    def __init__(self, master, lista: list, bd_path, lista_fabrica, lista_status, destino):
        
        super().__init__(master)
        self.title("ALTERAR STATUS")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.lista_dados = lista
        self.conteiner = self.lista_dados[5]
        self.bd_path = bd_path
        self.lista_fabrica = lista_fabrica
        self.lista_status = lista_status
        self.destino = destino
        self.widgets = {}

        #self._carregar_dados()
        self._criar_campos()
        self._criar_botao()

    def _criar_campos(self):
        # Labels informativos


        if self.lista_dados:
            self.dados_cntr = {
                "Conteiner": self.conteiner,
                "Armador": self.lista_dados[3],
                "Transportador": self.lista_dados[4],
                "Booking Entrada": self.lista_dados[1]
            }

        for i, (label, valor) in enumerate(self.dados_cntr.items()):
            campo = ctk.CTkLabel(self, text=f"{label}: {valor}")
            campo.grid(row=i, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Campos editáveis
        campos_editaveis = [
            ("Fabrica", "combo", self.lista_fabrica),
            ("Status", "combo", self.lista_status),
            ('Destino', 'combo', self.destino),
            ("Observação 2", "entry")
        ]

        for i, (texto, tipo, *opcoes) in enumerate(campos_editaveis, start=len(self.dados_cntr)):
            label = ctk.CTkLabel(self, text=texto)
            label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            if tipo == "entry":
                entrada = CustomEntry(self)
            elif tipo == "combo":
                entrada = CustomComboBox(self, values=opcoes[0], state='readonly')
                entrada.set("")

            entrada.grid(row=i, column=1, padx=10, pady=5, sticky='nswe')
            self.widgets[texto] = entrada

    def _criar_botao(self):
        botao = CustomButton(self, text="Salvar", command=self._salvar_dados)
        botao.grid(row=len(self.widgets)+len(self.dados_cntr), column=1, padx=10, pady=10, sticky='nswe')

    def _salvar_dados(self):
        dados = {}
        for texto, widget in self.widgets.items():
            valor = widget.get().strip()
            if texto != "Observação 2:" and valor == "":
                messagebox.showerror("Erro", f'O campo "{texto}" é obrigatório.')
                return
            dados[texto] = valor

        print("Dados lançados:")
        for k, v in dados.items():
            print(f"{k}: {v}")

        # Aqui você pode adicionar lógica para atualizar o banco de dados
        self.fechar()



    def fechar(self):
        self.destroy()
