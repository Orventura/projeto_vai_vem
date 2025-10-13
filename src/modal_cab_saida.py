
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
        self.local_planilha = None
        self.title("SAÍDA DE VEÍCULOS")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()

        self.criar_widgets()
        #self.carregar_tabelas()
        self.ctrl = ControlSaida(self)
        self.carregar_sheet()

    def criar_widgets(self):
        self.frame_tabela = ctk.CTkFrame(self, width=800, height=200, fg_color='transparent')
        self.frame_tabela.pack(side='top', padx=10, pady=10)


        self.frame_inferior = ctk.CTkFrame(self, width=400, height=200, fg_color='transparent')
        self.frame_inferior.pack(side='bottom', padx=10, pady=10)
        

        self.btn_importar = CustomButton(self.frame_inferior, text="Registrar Saída", command=self.dados_do_sheet)
        self.btn_importar.pack(pady=5)

    def carregar_sheet(self):
        """Carrega a Sheet com os dados atuais"""
        self.df_sheet, self.df_erros = self.mesclar_por_nf()
        self.modo_atual = ctk.get_appearance_mode()

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
        #self.sheet.extra_bindings([
        #        ("row_select", self.ctrl.coletar_indice_conteiner)
        #        ])
        self.sheet.pack()


    def carregar_tabela_liberados(self) -> pd.DataFrame:
        """Carrega as tabelas do banco de dados para alimentar o Sheet
            df_liberados: Dataframe dos dados do banco cabotagem
            """
        
        df_cabotagem_completa, df_cabotagem_sheet = veiculos_cabotagem()
        try:
            df_liberados = df_cabotagem_completa[['INDICE','CONTEINER','DT_ENTRADA', 'NOTA_FISCAL', 'STATUS']]
            df_liberados = df_liberados[
                                                (df_liberados['STATUS'] == 'LIBERADO')
                                            ]
            if not df_liberados.empty:
                df_liberados['DT_ENTRADA'] = pd.to_datetime(df_liberados['DT_ENTRADA'], errors='coerce')
                hoje = pd.Timestamp(datetime.now().date())
                df_liberados['DIAS'] = (hoje - df_liberados['DT_ENTRADA']).dt.days
                df_liberados['DT_ENTRADA'] = df_liberados['DT_ENTRADA'].dt.strftime('%d/%m/%Y')
        except Exception as e:
            print(f"Erro ao processar tabela: {e}")
            df_liberados = pd.DataFrame()
        return df_liberados
    
    def carregar_tabela_saida(self) -> pd.DataFrame:
        """df_saida: Dataframe da planilha de controle de embarques Cabotagem"""
        df_saida = self.ctrl.carregar_tabela_saida()
        return df_saida
    
    def _tabelas(self):
        """Carrega as tabelas do banco de dados para alimentar o Sheet"""
        df_liberados = self.carregar_tabela_liberados()
        print(df_liberados.head(21))  # Apenas para demonstração
        print(df_liberados.info())
        df_saida = self.ctrl.carregar_tabela_saida()
        print(df_saida.head(21))  # Apenas para demonstração
        print(df_saida.info())
        return df_liberados, df_saida

    def mesclar_por_nf(self):
        """
        Mescla os dados de veículos liberados com os dados de saída Philco
        com base na nota fiscal (NF), retornando duas tabelas:
        - df_resultado: com INDICE, CONTEINER, NF, Saída Philco, DIAS
        - df_excluidos: com os registros de df_saida que não foram encontrados em df_liberados
        """

        # 1. Obter os dois DataFrames
        df_liberados, df_saida = self._tabelas()

        # 2. Filtrar df_saida com NF e Saída Philco não nulos
        df_saida_filtrado = df_saida[df_saida['NF'].notna() & df_saida['Saída Philco'].notna()].copy()

        # 3. Remover duplicatas por Contêiner e NF
        df_saida_filtrado = df_saida_filtrado.drop_duplicates(subset=['Contêiner', 'NF'])

        # 4. Garantir que ambas colunas de NF estejam como string
        df_liberados['NOTA_FISCAL'] = df_liberados['NOTA_FISCAL'].astype(str)
        df_saida_filtrado['NF'] = df_saida_filtrado['NF'].astype(str)

        # 5. Mesclar pela NF
        df_merged = pd.merge(
            df_liberados,
            df_saida_filtrado,
            left_on='NOTA_FISCAL',
            right_on='NF',
            how='left'
        )

        # 6. Selecionar colunas desejadas
        df_resultado = df_merged[['INDICE', 'CONTEINER', 'NF', 'Saída Philco', 'DIAS']]

        # 7. Criar tabela com itens que ficaram fora do merge
        df_excluidos = df_saida_filtrado[~df_saida_filtrado['NF'].isin(df_resultado['NF'])]

        # 8. Exibir para depuração
        print("🔹 Resultado do merge:")
        print(df_resultado.head(21))
        print("🔸 Itens excluídos do merge:")
        print(df_excluidos.head(21))

        return df_resultado, df_excluidos
    
    def dados_do_sheet(self):
        """Coleta os dados atuais do Sheet"""
        dados = self.sheet.get_sheet_data(get_header=True)
        print(dados)
        #df_dados = pd.DataFrame(dados[1:], columns=dados[0])
        #print(df_dados.head(21))  # Apenas para demonstração
        #print(df_dados.info())
        #return df_dados