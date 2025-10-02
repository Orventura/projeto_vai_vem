import customtkinter as ctk
from views.views_vai_vem import vai_vem_pendente
from src.bd import BancoDeDados
from utils.config import *
import pandas as pd
from tkinter import messagebox
import getpass
import platform
from datetime import datetime


class Recebimento:
    def __init__(self, root):
        self.root = root
        self.tabela_vai_vem = vai_vem_pendente()
        self.tabela_filtrada = self.tabela_vai_vem.copy()

        self.frame = None
        self.sheet = None
        self.entry_pesquisa = None

    def _criar_janela_receber(self):
        self.modo_atual = ctk.get_appearance_mode()

        # Frame principal
        self.frame = ctk.CTkFrame(self.root, width=600, height=450)
        self.frame.place(x=210, y=5)

        # Frame para a tabela
        self.frame_tabela = ctk.CTkFrame(self.frame, width=600, height=440)
        self.frame_tabela.place(x=5, y=5)

            #"frame_5": {"x": 0, "y": 412, "width": 598, "height": 37},
        self.frame_pesquisa = ctk.CTkFrame(self.frame, width=598, height=37)
        self.mostrar_frame_pesquisa()
        

        self.e_pesquisa = CustomEntry(self.frame_pesquisa, placeholder_text="🔍      Pesquisar...", width=200)
        self.e_pesquisa.place(x=10, y=3)
        self.e_pesquisa.bind("<KeyRelease>", self.filtrar_sheet)

        self.btn_receber = ctk.CTkButton(self.frame_pesquisa, text='📦   Receber', command=self.selecionar_veículo)
        self.btn_receber.place(x=215, y=3)

        self.e_exportar = ctk.CTkButton(self.frame_pesquisa, text='📁   Exportar')
        self.e_exportar.place(x=365, y=3)

        self.frame_receber = ctk.CTkFrame(self.frame, width=598, height=37)
        
        self.e_conferente = CustomEntry(self.frame_receber, placeholder_text="Conferente",width=210)
        self.e_conferente.place(x=3, y=3)

        self.e_romaneio = CustomEntry(self.frame_receber, placeholder_text="Romaneio")
        self.e_romaneio.place(x=223, y=3)

        self.btn_salvar = ctk.CTkButton(self.frame_receber, text='💾   Salvar', command=self.receber_veículo)
        self.btn_salvar.place(x=400, y=3)

        self.carregar_sheet()

    def carregar_sheet(self):
        """Carrega a Sheet com os dados atuais"""
        self.atualizar_tabelas()

        if self.sheet:
            self.sheet.destroy()

        self.sheet = CustomSheet(
            self.frame_tabela,
            data=self.tabela_filtrada.values.tolist(),
            headers=list(self.tabela_filtrada.columns),
            width=580,
            height=400,
            show_row_index=True,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            set_all_heights_and_widths=True,
            show_index=False,
            header_align='w'
        )
        self.sheet.enable_bindings()
        self.sheet.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')
        self.sheet.place(x=3, y=3)

    def atualizar_tabelas(self):
        """Atualiza os registros pendentes do banco"""
        self.tabela_vai_vem = vai_vem_pendente()
        self.tabela_filtrada = self.tabela_vai_vem.copy()

    def filtrar_sheet(self, event=None):
        """Filtra a tabela de recebimento em todas as colunas."""
        texto = self.e_pesquisa.get().strip()      # novo Entry de pesquisa

        # Carrega todo o DataFrame do banco
        df = vai_vem_pendente()                    # pega todos os pendentes do banco

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

    def mostrar_frame_receber(self):

        self.frame_receber.place(x=0, y=412)
    
   

    def receber_veículo(self):
        """
        Finaliza o recebimento do veículo selecionado.
        Valida os campos obrigatórios e pede confirmação antes de salvar.
        """
        try:
            # --- Dados do sistema ---
            status = 'Finalizado'
            user = getpass.getuser()                # usuário do PC
            pc = platform.node()                     # nome do PC
            data = datetime.now().strftime('%Y-%m-%d')
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M')
            dados = self.selecionar_veículo()
            veiculo = dados[4]

            # --- Dados da seleção ---
            if dados is None:
                return

            # Validação do ID
            try:
                id_2 = dados[3]   # Confirme se a coluna correta é a 4
            except IndexError:
                messagebox.showerror(
                    "Erro nos Dados",
                    "Não foi possível capturar o ID do veículo. Verifique a tabela."
                )
                return

            # --- Validações de campos obrigatórios ---
            conferente = self.e_conferente.get().strip()
            if not conferente:
                messagebox.showwarning(
                    "Campo Obrigatório",
                    "Por favor, insira o nome do conferente antes de receber o veículo."
                )
                return

            romaneio = self.e_romaneio.get().strip() if hasattr(self, 'e_romaneio') else ""
            if not romaneio:
                messagebox.showwarning(
                    "Campo Obrigatório",
                    "O campo 'Romaneio' está vazio. Preencha-o para continuar."
                )
                return

            # --- Confirmação do usuário ---
            confirmacao = messagebox.askyesno(
                "Confirmação de Recebimento",
                f"{user.upper()} deseja realmente receber o veículo {veiculo} com ID {id_2}?"
            )
            if not confirmacao:
                messagebox.showinfo("Cancelado", "O recebimento foi cancelado pelo usuário.")
                self.resetar_frame_receber()
                return

            try:
                with BancoDeDados() as conn:
                    conn.receber_in_sql(id_2, [status, conferente, romaneio, data, user, data_hora, pc])
                    print(id_2)
                    messagebox.showinfo("Sucesso", f"{user.upper()} Você recebeu o Veículo {veiculo} com sucesso!")
                    self.resetar_frame_receber()
            except Exception as e:
                messagebox.showerror('Falha', f'Erro ao inserir os dados no banco: {e}')
                self.resetar_frame_receber()
            #print(id_2, conferente, romaneio, data, user, data_hora, pc)

        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")
            self.resetar_frame_receber()



    def resetar_frame_receber(self):
        for widget in self.frame_receber.winfo_children():
            if isinstance(widget, CustomEntry):
                widget.delete(0, 'end')
        self.esconder_frame_receber()
        self.mostrar_frame_pesquisa()
        self.carregar_sheet()

    def mostrar(self):
        self._criar_janela_receber()

    def esconder(self):
        if self.frame:
            self.frame.destroy()

    def mostrar_frame_pesquisa(self):
        self.frame_pesquisa.place(x=0, y=412)
    

    def selecionar_veículo(self):
        """
        Pesquisa o veículo e seleciona para recebimento.
        Esconde o frame de pesquisa, limpa os campos de entrada
        e retorna os valores da linha selecionada.
        Se nenhuma linha for selecionada, mostra mensagens de erro.
        """
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

            # Validação: garantir que a linha tenha colunas
            if len(dados_linha) < 18:
                messagebox.showwarning(
                    "Aviso",
                    "A tabela não possui o número padrão de colunas para capturar o ID."
                )
                return None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar obter os dados do veículo:\n{e}")
            return None

        # --- Esconde o frame ---
        try:
            self.frame_pesquisa.place_forget()
        except AttributeError:
            messagebox.showerror("Erro", "Frame de pesquisa não encontrado!")
            return None

        # --- Limpar os campos do frame ---
        for widget in self.frame_pesquisa.winfo_children():
            if isinstance(widget, CustomEntry):  # ou CustomEntry
                try:
                    widget.delete(0, 'end')
                except Exception as e:
                    print(f"Erro ao limpar o campo {widget}: {e}")
        self.mostrar_frame_receber()
        return dados_linha

        

    def esconder_frame_receber(self):
        self.frame_receber.place_forget()
        self.mostrar_frame_pesquisa()
