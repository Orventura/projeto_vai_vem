import customtkinter as ctk
from utils.config import *
import pandas as pd
from tkinter import messagebox
import getpass
import platform
from datetime import datetime
from src.modal_cab_entrada import FormularioEntrada
from src.modal_cab_editar import EditarStatus
from src.modal_cab_liberar import Liberacao
from src.modal_cab_config import ModalConfiguracoes
from models.model_cab_config import Listas
from models.model_veiculos import veiculos_cabotagem
from src.bd import BancoDeDados

class Cabotagem:
    def __init__(self, root):
        self.root = root
        self.img = RecursosVisuais()


        self.frame = None
        #self.sheet = None
        self._criar_cabotagem()

        self.carregar_sheet()

    def _criar_cabotagem(self):
        self.modo_atual = ctk.get_appearance_mode()
        self.dic_listas = self._carregar_listas()        

        # Frame principal
        self.frame = ctk.CTkFrame(self.root, width=783, height=450)
        self.frame.place(x=210, y=5)

        self.frame_inferior = ctk.CTkFrame(self.frame, width=700, height=37, fg_color='transparent')
        self.mostrar_frame_inferior()

        self.label_hover = ctk.CTkLabel(self.frame_inferior, text="", font=("Arial", 12), text_color='darkgray', width=50, height=37)
        self.label_hover.place(x=230, y=1)

        self.botoes_info = {
            "Adicionar Veículo": {"imagem": self.img.adicionar, "comando": lambda: self.abrir_entrada_cabotagem(self.root)},
            "Editar Status": {"imagem": self.img.editar, "comando": lambda: self.abrir_editar_status(self.root)},
            "Liberar Veículo": {"imagem": self.img.liberar, "comando": lambda: self.abrir_liberacao()},
            "Registrar Saída": {"imagem": self.img.sair, "comando": lambda: print("Sair")},
            "Retornar Veículo": {"imagem": self.img.retornar, "comando": lambda: print("Retornar")},
            "Configurações": {"imagem": self.img.config, "comando": lambda: self.abrir_configuracoes()}
        }

        self.criar_botoes()

    def criar_botoes(self):
        frame_botoes = ctk.CTkFrame(self.frame_inferior, height=37, width=105, fg_color='transparent')
        frame_botoes.place(x=345, y=3)
        
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

        self.sheet = CustomSheet(
            self.frame,
            data=self.df_cabotagem_sheet.values.tolist(),
            headers=list(self.df_cabotagem_sheet.columns),
            width=778,
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
        self.sheet.font(("Calibri", 10, "normal"))         # Fonte da tabela
        self.sheet.header_font(("Calibri", 10, "bold"))    # Fonte do cabeçalho
        self.sheet.index_font(("Calibri", 10, "normal"))   # Fonte do índice (se estiver visível)
        self.sheet.extra_bindings([
                ("row_select", self.coletar_indice)
                ])

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
        self.sheet.extra_bindings([
                ("row_select", self.coletar_indice)
                ])


    def mostrar(self):
        self.esconder()
        self._criar_cabotagem()
        self.carregar_sheet()

    def esconder(self):
        if self.frame:
            self.frame.destroy()

    def mostrar_frame_inferior(self):
        self.frame_inferior.place(x=0, y=412)

    def abrir_entrada_cabotagem(self, root):
        self.formulario = FormularioEntrada(master=root, listas=self._carregar_listas, on_close=self.resetar_sheet)
        self.formulario.grab_set()
        self.formulario.focus_force()

    def coletar_indice(self, event=None):
        """Recebe a lista de dados da linha
            selecionada na Sheet, e retorna
            o índice.
        """
        selecionados = self.sheet.get_currently_selected()
        linha = selecionados[0]
        dados_linha = self.sheet.get_row_data(linha)

        self.df_cabotagem_completa, self.df_cabotagem_sheet = veiculos_cabotagem()
        df_consulta = self.df_cabotagem_completa[['DT_ENTRADA', 'CONTEINER', 'INDICE']].copy()
        df_consulta['DT_ENTRADA'] = pd.to_datetime(df_consulta['DT_ENTRADA'], errors='coerce').dt.strftime("%d/%m/%Y")
        indice_df = pd.DataFrame([dados_linha], columns=self.df_cabotagem_sheet.columns.to_list()) 

        mescla = pd.merge(
            indice_df[['DT_ENTRADA', 'CONTEINER']],
            df_consulta,
            how='inner',
            on=['DT_ENTRADA', 'CONTEINER'])
        self.id = mescla['INDICE'][0]
        return int(self.id)

    def abrir_editar_status(self, root):        
        try:
            selecionados = self.sheet.get_currently_selected()
            if not selecionados:
                messagebox.showerror(
                    "Erro de Seleção",
                    "Nenhum veículo foi selecionado.\nSelecione uma linha antes de continuar."
                )
                return None  # aborta a função
            # Captura a linha e os dados
            
            linha = selecionados[0]
            dados_linha = self.sheet.get_row_data(linha)
            
            self.formulario = EditarStatus(root, dados_linha, BD_CABOTAGEM, self.id, on_close=self.resetar_sheet)
            self.formulario.grab_set()
            self.formulario.focus_force()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar obter os dados do veículo:\n{e}")

    def abrir_liberacao(self):
        try:
            selecionados = self.sheet.get_currently_selected()
            if not selecionados:
                messagebox.showerror(
                    "Erro de Seleção",
                    "Nenhum veículo foi selecionado.\nSelecione uma linha antes de continuar."
                )
                return None  # aborta a função
            # Captura a linha e os dados
            linha = selecionados[0]
            dados_linha = self.sheet.get_row_data(linha)

            app = Liberacao(
            master=self.root,
            lista=dados_linha,
            id=self.id,
            bd_path=BD_CABOTAGEM,
            on_close=self.resetar_sheet
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar obter os dados do veículo:\n{e}")

    def abrir_configuracoes(self):
        """Abre o modal de configurações da view cabotagem"""
        self.config = ModalConfiguracoes(self.root)

    def fechar_formulario(self):
        if hasattr(self, 'formulario') and self.formulario.winfo_exists():
            self.formulario.destroy()

    def _carregar_listas(self):
        """Retorna um dicionario com todas as listas para configurações de combobox"""
        with Listas() as l:
            dicionario = l.dicionario_de_listas()
        return dicionario
    
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("teste_cabotagem")
    root.geometry('815x460')
    app = Cabotagem(root)

    root.mainloop()