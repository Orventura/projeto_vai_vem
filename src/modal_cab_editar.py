import customtkinter as ctk
from tkinter import messagebox
#from bd import BancoDeDados
from src.bd_cabotagem import Database
from utils.config import CustomButton, CustomComboBox, CustomEntry, CustomLabel
from getpass import getuser
from models.views_cab_config import Listas



class EditarStatus(ctk.CTkToplevel):
    def __init__(self, master, lista: list, bd_path, id, on_close=None):
        
        super().__init__(master)
        self.on_close = on_close
        self.title("ALTERAR STATUS")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.lista_dados = lista
        self.conteiner = self.lista_dados[5]
        self.bd_path = bd_path
        self.dicionario_listas = self._carregar_listas()
        self.lista_fabrica = self.dicionario_listas['fabrica']
        self.lista_situacao = self.dicionario_listas['situacao']
        self.usuarios_autorizados = self.dicionario_listas['user_auth']
        self.destino = self.dicionario_listas['destino']
        self.widgets = {}
        self.id = int(id)
        self.user = str(getuser()).upper()

        #self._carregar_dados()
        self._criar_campos()
        self._criar_botao()
        self.ocultar_destino()

    def _criar_campos(self):
        # Labels informativos

        self.widgets = {}
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
            ("Status", "combo", self.lista_situacao),
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
        #entradas_widget = self._valida_dados()

        chaves = ['FABRICA', 'STATUS', 'DESTINO', 'OBS_2']
        valores = []

        # Coleta os valores dos widgets
        for widget in self.winfo_children():
            if isinstance(widget, CustomComboBox):
                v = widget.get()
                valores.append(v)
            if isinstance(widget, CustomEntry):
                v = widget.get()
                valores.append(v)

        dicionario = dict(zip(chaves, valores))

        # Monta dicionário com os dados
        if not self._valida_dados(dados=dicionario):
            return

        with Database() as con:
            # Atualiza a base principal
            dados_para_base = dicionario.copy()

            # Remove DESTINO se estiver vazio
            if dados_para_base.get("DESTINO", "").strip() == "":
                dados_para_base.pop("DESTINO")

            con.update_base(indice=self.id, **dados_para_base)

            # Recupera os dados atualizados
            row = con.fetch_base(INDICE=self.id)
            if not row:
                messagebox.showerror("Erro", "Não foi possível recuperar os dados atualizados.")
                return

            dados_status = row[0]
            dados_status.pop('INDICE')
            dados_status["USUARIO"] = str(getuser()).upper()

            # Lança os dados na tabela de status
            con.insert_status(**dados_status)

            # Confirma sucesso
            messagebox.showinfo("Sucesso", "Todos os dados foram atualizados!")

            # Fecha a janela
            self.on_close()
            self.destroy()


    def _valida_dados(self, dados: dict) -> bool:
        """Recebe o dicionário antes de lançar e valida os dados"""
        print('-------------------\n\n', dados, "\n\ndicionário recebido ---------------")

        user = str(getuser()).upper()



        print("\n\n", user, "<-------------Autorizado")
        print("\n\n",self.usuarios_autorizados, "<<<<<<< usuários autorizados")

        for campo, valor in dados.items():
            valor = str(valor).strip()

            if campo == "DESTINO":
                if user in self.usuarios_autorizados:
                    if valor == "":
                        messagebox.showerror("Erro", f"É necessário preencher o campo '{campo}'.")
                        return False
            else:
                if valor == "":
                    messagebox.showerror("Erro", f"É necessário preencher o campo '{campo}'.")
                    return False
        return True

    def permissão(self):
        """Retorna lista de usuários autorizados"""
        
        if self.user in self.usuarios_autorizados:
            print("/n/n", self.user, "<<<<<<<<<<< user - TRUE<<<<<<<<<<<")
            print("/n/n", self.usuarios_autorizados, "<<<<<<<<<<<<<<<<<<<<<<")
            return True
        print("\n\n", self.user, "<<<<<<<<<<< user - FALSE<<<<<<<<<<<")
        print("\n\n", self.usuarios_autorizados, "<<<<<<<<<<<<<<<<<<<<<<")

        return False

    def ocultar_destino(self):
        for widget in self.winfo_children():
            if isinstance(widget, CustomComboBox) and widget is self.widgets["Destino"]:
                if not self.permissão():
                    widget.grid_forget()

    def _carregar_listas(self):
        """Retorna dicionario, para carregar todas as listas de combobox"""
        with Listas() as users:
            dicionario = users.dicionario_de_listas()
            return dicionario

    def fechar(self):
        self.destroy()

