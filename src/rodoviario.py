import customtkinter as ctk
from utils.config import *
import pandas as pd
from tkinter import messagebox
import getpass
import platform
from datetime import datetime

from views.view_veiculos import veiculos_cabotagem
from .bd import BancoDeDados

class Rodoviario:
    def __init__(self, root):
        self.root = root
        self.img = RecursosVisuais()

        self.frame = None
        #self.sheet = None
        self._criar_cabotagem()

       # self.carregar_sheet()

    def _criar_cabotagem(self):
        self.modo_atual = ctk.get_appearance_mode()
        

        # Frame principal
        self.frame = ctk.CTkFrame(self.root, width=600, height=450)
        self.frame.place(x=210, y=5)

        self.frame_inferior = ctk.CTkFrame(self.frame, width=598, height=37, fg_color='transparent')
        self.mostrar_frame_inferior()

        self.label_hover = ctk.CTkLabel(self.frame_inferior, text="", font=("Arial", 12), text_color='darkgray', width=50, height=37)
        self.label_hover.place(x=250, y=1)


        self.botoes_info = {
            "Adicionar Veículo": {"imagem": self.img.adicionar, "comando": lambda: print("Adicionar")},
            "Editar Veículo": {"imagem": self.img.editar, "comando": lambda: print("Editar")},
            "Liberar Veículo": {"imagem": self.img.liberar, "comando": lambda: print("Liberar")},
            "Registrar Saída": {"imagem": self.img.sair, "comando": lambda: print("Sair")},
            "Retornar Veículo": {"imagem": self.img.retornar, "comando": lambda: print("Retornar")},
        }

        self.criar_botoes()

    def criar_botoes(self):
        frame_botoes = ctk.CTkFrame(self.frame_inferior, height=37, width=105, fg_color='transparent')
        frame_botoes.place(x=370, y=3)
        
        for i, (nome, info) in enumerate(self.botoes_info.items()):
            botao = ctk.CTkButton(
                frame_botoes,
                text="",
                image=info["imagem"],
                command=info["comando"],
                width=35,
                height=35,
                fg_color="transparent",
                hover_color="#cccccc",
                corner_radius=5
            )
            botao.grid(row=0, column=i, padx=5)

            # Bind de hover
            botao.bind("<Enter>", lambda e, n=nome: self.label_hover.configure(text=n))
            botao.bind("<Leave>", lambda e: self.label_hover.configure(text=""))


        self.e_pesquisa = CustomEntry(self.frame_inferior, placeholder_text="🔍      Pesquisar...", width=200)
        self.e_pesquisa.place(x=10, y=3)
        self.e_pesquisa.bind("<KeyRelease>", self.filtrar_sheet)

    def carregar_sheet(self):
        """Carrega a Sheet com os dados atuais"""
        self.df_cabotagem_completa, self.df_cabotagem_sheet = veiculos_cabotagem()
        print(self.df_cabotagem_sheet.head())


        self.sheet = CustomSheet(
            self.frame,
            data=self.df_cabotagem_sheet.values.tolist(),
            headers=list(self.df_cabotagem_sheet.columns),
            width=593,
            height=406,
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
        #self.sheet.font(("Calibri", 10, "normal"))         # Fonte da tabela
        #self.sheet.header_font(("Calibri", 10, "bold"))    # Fonte do cabeçalho
        #self.sheet.index_font(("Calibri", 10, "normal"))   # Fonte do índice (se estiver visível)


    def resetar_sheet(self):
        self.sheet.destroy()
        self.carregar_sheet()

    def filtrar_sheet(self, event=None):
        """Filtra a tabela de recebimento em todas as colunas."""
        texto = self.e_pesquisa.get().strip()      # novo Entry de pesquisa

        # Carrega todo o DataFrame do banco
        self.df_cabotagem_completa, self.df_cabotagem_sheet = veiculos_cabotagem()  
        df = self.df_cabotagem_sheet                # pega todos os pendentes do banco

        # Se há texto, filtra localmente no pandas
        if texto:
            mask = df.apply(
                lambda col: col.astype(str).str.contains(texto, case=False, na=False)
            )
            df = df[mask.any(axis=1)]

        # Atualiza a sheet
        self.sheet.set_sheet_data(
            df.values.tolist(),
            reset_col_positions=True,
            reset_row_positions=True
        )
        self.sheet.headers(list(df.columns))
        self.sheet.deselect("all")
        self.sheet.set_all_column_widths()

    def mostrar(self):
        self.esconder()
        self._criar_cabotagem()
        self.carregar_sheet()

    def esconder(self):
        if self.frame:
            self.frame.destroy()

    def mostrar_frame_inferior(self):
        self.frame_inferior.place(x=0, y=412)
    

if __name__ == '__main__':
    root = ctk.CTk()
    root.title("teste_cabotagem")
    root.geometry('815x460')
    app = Rodoviario(root)
    root.mainloop()