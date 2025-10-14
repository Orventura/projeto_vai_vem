
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
        self.sheet = None
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
        
        self.btn_salvar = CustomButton(self.frame_inferior, text="Registrar Saída", width=40, fg_color="#1fa533", hover_color="#36a95b", command=self.salvar)
        
        self.btn_buscar_saida = CustomButton(self.frame_inferior, text="Buscar Dados", command=self.carregar_sheet, width=40)
        self.btn_buscar_saida.pack(pady=5, padx=40, side='left') 

        if not self.sheet:
            df = self.ctrl.carregar_tabela_liberados()
            self.df_sheet = df
            print(self.df_sheet)
            self.modo_atual = ctk.get_appearance_mode()
            self.sheet = CustomSheet(
                self.frame_tabela,
                data=df.values.tolist(),
                headers=['INDICE', 'CONTEINER', 'DT_ENTRADA', "NOTA", 'STATUS', 'DIAS'],
                width=500,
                height=450,
            )
            self.sheet.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')
            self.sheet.pack(pady=5, side='top')
            self.sheet.set_all_column_widths()

    def carregar_sheet(self):
        """Carrega a sheet com os dados preparados pelo controller."""
        if self.sheet:
            self.atualizar_tabelas()
            self.sheet.destroy()
            self.modo_atual = ctk.get_appearance_mode()
            
            self.sheet = CustomSheet(
                self.frame_tabela,
                data=self.df_sheet.values.tolist(),
                headers=['INDICE', 'CONTEINER', 'NF', 'DATA DE SAÍDA', 'STATUS', 'DIAS', '✔️'],
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
            self.sheet.checkbox("G", checked=True)
            self.sheet.pack(pady=5, side='top')

            if not self.df_sheet.empty:
                self.btn_salvar.pack(pady=5, padx=40, side='right')
            

    def atualizar_tabelas(self):
        self.df_sheet, self.df_erro, self.msg, self.msg_type = self.ctrl.tabelas_para_sheet()

    def salvar(self):
        """Chama o controlador para registrar a saída dos veículos selecionados."""
        try:
            self.ctrl.registrar_saida()
            if self.msg:
                if self.msg_type == "sucesso":
                    messagebox.showinfo("Sucesso", self.msg)
                elif self.msg_type == "erro":
                    messagebox.showerror("Erro", self.msg)
                else:
                    messagebox.showwarning("Aviso", self.msg)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar saída: {e}")
            return
        
