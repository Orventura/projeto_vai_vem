import customtkinter as ctk
from tkinter import messagebox
from utils.config import CustomButton, CustomEntry, CustomComboBox
from models.model_cab_config import Listas
from datetime import datetime
from src.bd_cabotagem import Database
import sqlite3
from utils.config import *
import pandas as pd
from getpass import getuser

class Liberacao(ctk.CTkToplevel):
    """Cria um modal para liberar os veículos,
    recebe o master_widget, lista dos dados selecionados, indice dos
    dados selecionados na sheet prinsipal, caminho do banco de dados,
    e controller."""
    def __init__(self, master, lista: list, id, bd_path):

        super().__init__(master)
        self.title("REGISTRAR LIBERAÇÃO")
        #self.resizable(False, False)
        #self.controller = controller
        self.grab_set()
        self.focus_force()
        self.user = getuser().upper()
        self.data = None
        self.status = None        
        self.id = id
        self.lista_dados = lista
        self.armador = lista[3]
        self.transp = lista[4]
        self.conteiner = lista[5]
        self.bd_path = bd_path
        self.dicionario_listas = self._carregar_listas()
        self.lista_fabrica = self.dicionario_listas['fabrica']
        self.lista_booking = self.dicionario_listas['booking']
        

        self.widgets = {}

        self.frame_principal = ctk.CTkFrame(self, width=800, height=500, fg_color='transparent')
        self.frame_principal.pack(fill='both', side='bottom', padx=5, pady=5, expand=True)
        self.frame_principal.pack_propagate(True)

        self.frame_cabecalho = ctk.CTkFrame(self, width=800, height=100,)
        self.frame_cabecalho.pack(fill=None, side='top', padx=5, pady=(5, 0), expand=True,)
        self.label_cabecalho = ctk.CTkLabel(self.frame_cabecalho, text_color='gray',
                                            text="CONTEINER            ARMADOR             TRANSPORTADORA",
                                            font=('arial', 16, 'bold')
                                            
                                            )
        self.label_cabecalho.pack(pady= 5)
        self.label_cabecalho2 = ctk.CTkLabel(self.frame_cabecalho, text_color='gray',
                                            text=f"{self.conteiner}          {self.armador}                      {self.transp}            ",
                                            font=('arial', 16, 'normal', ), anchor='w'      
                                            )

        self.label_cabecalho2.pack(pady= 5, padx=(0,0), expand=True, fill='both')

        self.btn_fechar = CustomButton(self.frame_principal, text="fechar", command=lambda: self.coletar_dados())
        self.btn_fechar.pack(side='bottom', expand=False, fill="y")

        self.frame_esq = ctk.CTkFrame(self, width=150, height=200,)
        self.frame_esq.pack(fill='x', side='left', padx=5, pady=(5, 0), expand=True)

        self.e_nf = CustomEntry(self.frame_esq, placeholder_text='Nota Fiscal')
        self.e_nf.pack(pady=(5,0))

        self.e_valor_nf = CustomEntry(self.frame_esq, placeholder_text='Valor da Carga')
        self.e_valor_nf.pack(pady=(5,0))

        self.e_pesob = CustomEntry(self.frame_esq, placeholder_text='Peso Bruto')
        self.e_pesob.pack(pady=(5,0))

        self.e_pesol = CustomEntry(self.frame_esq, placeholder_text='Peso Líquido')
        self.e_pesol.pack(pady=(5,5))

        self.frame_cent = ctk.CTkFrame(self, width=150, height=200,)
        self.frame_cent.pack(fill='x', side='left', padx=5, pady=(5, 0), expand=True)

        self.e_lacre_arm = CustomEntry(self.frame_cent, placeholder_text='Lacre Armador')
        self.e_lacre_arm.pack(pady=(5,0))

        self.e_lacre_ph = CustomEntry(self.frame_cent, placeholder_text='Lacre Philco')
        self.e_lacre_ph.pack(pady=(5,0))

        self.cbbooking = CustomComboBox(self.frame_cent, values=self.lista_booking)
        self.cbbooking.pack(pady=(5,0))
        self.cbbooking.set("Booking")

        self.cb_tp_carga = CustomComboBox(self.frame_cent, values=['CLIENTE', 'AG'])
        self.cb_tp_carga.pack(pady=(5,5))
        self.cb_tp_carga.set("Carga")


        self.frame_dir = ctk.CTkFrame(self, width=150, height=200,)
        self.frame_dir.pack(fill='both', side='right', padx=5, pady=(5, 0), expand=True)

        self.e_isca1 = CustomEntry(self.frame_dir, placeholder_text='Isca 1')
        self.e_isca1.pack(pady=(5,0))

        self.e_isca2 = CustomEntry(self.frame_dir, placeholder_text='Isca 2')
        self.e_isca2.pack(pady=(5,0))

        self.cb_tp_fabrica = CustomComboBox(self.frame_dir, values=self.lista_fabrica)
        self.cb_tp_fabrica.pack(pady=(5,0))
        self.cb_tp_fabrica.set("Fábrica")

        self.e_obs = CustomEntry(self.frame_dir, placeholder_text='Observação')
        self.e_obs.pack(pady=(5,5))

    def _carregar_listas(self):
        """Retorna dicionario, para carregar todas as listas de combobox"""
        with Listas() as users:
            dicionario = users.dicionario_de_listas()
            return dicionario


    # 🔹 Coleta os dados de todos os widgets
    def coletar_dados(self) -> dict:
        dados = {
            "NOTA_FISCAL": self.e_nf.get().strip(),
            "VALOR": self.e_valor_nf.get().strip(),
            "PESO_BRUTO": self.e_pesob.get().strip(),
            "PESO_LIQUIDO": self.e_pesol.get().strip(),
            "LACRE_ARMADOR": self.e_lacre_arm.get().strip(),
            "LACRE_PHILCO": self.e_lacre_ph.get().strip(),
            "ARMADOR_BOOKING_DESTINO": self.cbbooking.get().strip(),
            "FABRICA": self.cb_tp_fabrica.get().strip(),
            "ISCA_1": self.e_isca1.get().strip(),
            "ISCA_2": self.e_isca2.get().strip(),
            "OBS": self.e_obs.get().strip(),
            "STATUS": "LIBERADO",
            "TIPO_CARGA": self.cb_tp_carga.get().strip(),
        }
        if not self.validar_vazios(dados=dados):
            return

        if not self.validar_booking(dados=dados):
            return

        dados.pop('TIPO_CARGA')
        with Database() as db:
            db.update_base(self.id, **dados)
        self.destroy()
        return dados


    def validar_vazios(self, dados: dict) -> bool:
        """Valida os campos paa não permitir entradas null"""

        combo_valores = ["Booking", "Fábrica", "Carga"]
        validar = list(dados.values())
        campos = list(dados.keys())
        for i, valor in enumerate(validar):
            if not valor:
                messagebox.showerror(title="Erro", message=f"Preencha o campo obrigatório: {campos[i]}")
                return False
            if valor in combo_valores:
                messagebox.showerror(title="Erro",message=f"Preencha o campo obrigatório: {campos[i]}")
                return False
        return True        

    def validar_booking(self, dados: dict) -> bool:
        try:
            with Database() as db:
                registro = db.fetch_base(INDICE=int(self.id))[0]
                print(registro, "lista direto do banco")

                teste1 = registro['DESTINO']
                teste2 = registro['ARMADOR']
                print('ID', self.id)
                print('teste 1 DESTINO', teste1)
                print('teste 2 ARMADOR', teste1)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar dados: {e}")
            return False

        validacao = dados.get('ARMADOR_BOOKING_DESTINO', '')

        if teste1 in validacao and teste2 in validacao:
            return True
        if teste1 in validacao and teste2 not in validacao:
            messagebox.showerror('Erro Armador x Booking', f"{self.user}, procure o responsável da cabotagem!")
            return False
        if teste1 not in validacao and teste2 in validacao:
            messagebox.showerror('Erro Destino x Booking', f"{self.user}, procure o responsável da cabotagem!")
            return False
        messagebox.showerror('Erro Destino x Armador x Booking', f"{self.user}, procure o responsável da cabotagem!")
        return False




if __name__ =="__main__":
    root = ctk.CTk()
    root.geometry('250x250')
    def abrir_modal():
        
        modal = Liberacao(root, [1,2,3,4,5,6], 5, r'data\database_cabotagem.db')
        root.wait_window(modal)

    def fechar():
        root.destroy()


    btn = ctk.CTkButton(root, command=lambda: abrir_modal(), text='Abrir Modal')
    btn.grid()

    root.mainloop()