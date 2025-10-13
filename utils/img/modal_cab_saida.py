
import pandas as pd
from tkinter import filedialog as fd
from tkinter import messagebox
import customtkinter as ctk
from models.model_veiculos import veiculos_cabotagem
from datetime import datetime
from controllers.ctrl_modal_saida import ControlSaida
from utils.config import CustomSheet, CustomButton

class ModalSaida(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.ctrl = None  # será definido depois
        self.local_planilha = None
        self.title("SAÍDA DE VEÍCULOS")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.set_controller(ControlSaida(self))
        self.criar_widgets()



    def set_controller(self, controller):
        self.ctrl = controller


        #self.carregar_tabelas()
        #self.ctrl = ControlSaida(self)
        #self.carregar_sheet()

    def criar_widgets(self):
        self.frame_tabela = ctk.CTkFrame(self, width=800, height=200, fg_color='transparent')
        self.frame_tabela.pack(side='top', padx=10, pady=10)


        self.frame_inferior = ctk.CTkFrame(self, width=400, height=200, fg_color='transparent')
        self.frame_inferior.pack(side='bottom', padx=10, pady=10)
        

        self.btn_importar = CustomButton(self.frame_inferior, text="Registrar Saída")
        self.btn_importar.pack(pady=5)

        self.btn_buscar_saida = CustomButton(self.frame_inferior, text="Buscar Dados", command=self.carregar_sheet)
        self.btn_buscar_saida.pack(pady=5, side='left') 


        self.df_sheet, self.df_erros = self.mesclar_por_nf()
        self.modo_atual = ctk.get_appearance_mode()

    def carregar_sheet(self):
        self.modo_atual = ctk.get_appearance_mode()
        self.df_sheet, self.df_erro = self.ctrl.tabelas_para_sheet()
        self.sheet = CustomSheet(
            self.frame_tabela,
            data=self.df_sheet.values.tolist(),
            headers=['INDICE', 'CONTEINER', 'NF', 'DATA DE SAÍDA', 'DIAS', '✔️'],
            width=500,
            height=450,
            show_row_index=True,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            show_index=False,
            header_align='w'
        )
        self.sheet.enable_bindings()
        self.sheet.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')
        self.sheet.set_all_column_widths()
        self.sheet.place(x=3, y=3)
        self.sheet.checkbox("F", checked=True)
        self.sheet.pack(pady=5, side='top')

    
