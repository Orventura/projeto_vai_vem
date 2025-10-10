from utils.config import CustomButton, CustomComboBox, CustomEntry, CustomLabel
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from utils.config import *
from datetime import datetime
from src.bd_cabotagem import Database
import getpass
from models.model_cab_config import Listas

class FormularioEntrada(ctk.CTkToplevel):
    def __init__(self, master=None, listas=None, on_close=None):

        super().__init__(master)
        self.on_close = on_close
        self.title("LANÇAR ENTRADA")
        self.resizable(False, False)
        self.grab_set()        # Torna modal
        self.focus_force()     # Foco na janela
        self.dicionario_listas = self._carregar_listas()
        self.lista_fabrica = self.dicionario_listas['fabrica']
        self.lista_armador = self.dicionario_listas['armador']
        self.usuarios_autorizados = self.dicionario_listas['user_auth']
        self.lista_destino = self.dicionario_listas['destino']
        self.lista_transportador = self.dicionario_listas['transportador']

        self.img = RecursosVisuais()

        self.widgets = {}

        self._campos = [
            ("Data:", "date"),
            ("Booking de entrada:", "entry"),
            ("Fabrica:", "combo", self.lista_fabrica),
            ("Armador:", "combo", self.lista_armador),
            ("Transportador:", "combo", self.lista_transportador),
            ("Conteiner:", "entry"),
            ("Destino:", "combo", self.lista_destino), 
            ("Status:", "combo", ['VAZIO']),
        ]

        self._criar_campos()
        self._criar_botao()

    def _criar_campos(self):
        for i, campo in enumerate(self._campos):
            texto, tipo = campo[0], campo[1]
            opcoes = campo[2] if len(campo) > 2 else []

            label = ctk.CTkLabel(self, text=texto)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            if tipo == "entry":
                entrada = CustomEntry(self)
            elif tipo == "combo":
                entrada = CustomComboBox(self, values=opcoes)
                entrada.set("")
            elif tipo == "date":
                entrada = DateEntry(self, locale='pt_br', background='darkblue', foreground='white', borderwidth=2)

            entrada.grid(row=i, column=1, columnspan=2, padx=10, pady=10, sticky='nswe')
            self.widgets[texto] = entrada

    def _criar_botao(self):
        botao = CustomButton(self, text="Lançar", command=self._lancar_dados, height=29)
        botao.grid(row=len(self._campos), column=1, padx=10, sticky='w')

        botao_config = CustomButton(
            self,
            text="",
            image=self.img.config,
            width=35,
            fg_color="transparent",
            hover_color="#cccccc",
            corner_radius=5,
            command=lambda: messagebox.showinfo("Configuração", "Abrir configurações...")
        )
        botao_config.grid(row=len(self._campos), column=0, sticky='w')

    def _lancar_dados(self):
        user = getpass.getuser()
        dados = {}
        try:
            # Coleta os dados
            for texto, widget in self.widgets.items():
                if isinstance(widget, CustomEntry) or isinstance(widget, CustomComboBox):
                    dados[texto] = widget.get().strip().upper()
                elif isinstance(widget, DateEntry):
                    dados[texto] = widget.get_date().strftime('%Y-%m-%d')
            print(f'esses saõ os dados DEBUG{dados}')

            # Validação: verifica se algum campo está vazio
            for key, value in dados.items():
                if value == "":
                    raise ValueError(f'Campo "{key}" é obrigatório!')

            self.dados_finais  = dicionario_entrada_veiculos(list(dados.values()))
            self.dados_status = dicionario_editar_status(list(self.dados_finais.values()), user)
            print(f'\n\n--------DEBUG DADOS SELECIONADO - entrada Status \n{self.dados_status}\n\n')
        
            with Database() as db:
                # Converter a string de data para date
                dt_formatada = datetime.strptime(self.dados_finais["DT_ENTRADA"], "%Y-%m-%d").date()
                self.dados_finais["DT_ENTRADA"] = dt_formatada

                # Inserir usando **kwargs
                id_inserido = db.insert_base(**self.dados_finais)
                print(f"Registro inserido com INDICE = {id_inserido}")
            
            with Database() as db:
                db.insert_status(**self.dados_status)

            if self.on_close:
                self.on_close()
                self.destroy()

            messagebox.showinfo('Sucesso', 'O veículo foi registrado com êxito!')

        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def _carregar_listas(self):
        """Retorna dicionario, para carregar todas as listas de combobox"""
        with Listas() as users:
            dicionario = users.dicionario_de_listas()
            return dicionario
    

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = FormularioEntrada()
    app.mainloop()
