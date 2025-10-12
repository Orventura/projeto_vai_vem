import customtkinter as ctk
from utils.config import *
from src.bd_cabotagem import Database
from models.model_veiculos import veiculos_cabotagem
from controllers.ctrl_modal_retorno import ControlRetorno


class ModalRetorno(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.ctrl = ControlRetorno(self)
        self.title("REGISTRAR RETORNO")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()


        self.frame_tabela = ctk.CTkFrame(self, width=400, height=200, fg_color='transparent')
        self.frame_tabela.pack(side='top', padx=10, pady=10)


        self.frame_inferior = ctk.CTkFrame(self, width=400, height=200, fg_color='transparent')
        self.frame_inferior.pack(side='bottom', padx=10, pady=10)

        self.e_pesquisa = CustomEntry(self.frame_inferior, placeholder_text="🔍      Pesquisar...", width=200)
        self.e_pesquisa.pack(pady=10, padx=10, side='left')

        self.btn_fechar = CustomButton(self.frame_inferior, width=50, text="Salvar", command=self.destroy)
        self.btn_fechar.pack(pady=10)

        self.carregar_sheet()

    def carregar_sheet(self):
        """Carrega a Sheet com os dados atuais"""
        self.df_cabotagem_sheet = self._carregar_tabelas()
        self.modo_atual = ctk.get_appearance_mode()

        self.sheet = CustomSheet(
            self.frame_tabela,
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
                ("row_select", self.ctrl.coletar_indice)
                ])
        self.sheet.pack()
    def _carregar_tabelas(self):
        """Carrega as tabelas do banco de dados para alimentar o Sheet"""
        df_cabotagem_completa, df_cabotagem_sheet = veiculos_cabotagem()
        try:
            tabela_para_sheet = df_cabotagem_completa.iloc[:, [1, 2, 3, 4, 5, 6, 7, 17, 18]]
            tabela_para_sheet = tabela_para_sheet[
                                                (tabela_para_sheet['STATUS'] == 'SAIU') |
                                                (tabela_para_sheet['STATUS'] == 'LIBERADO')
                                            ]
            if not tabela_para_sheet.empty:
                tabela_para_sheet['DT_ENTRADA'] = pd.to_datetime(tabela_para_sheet['DT_ENTRADA'], errors='coerce')
                hoje = pd.Timestamp(datetime.now().date())
                tabela_para_sheet['DIAS'] = (hoje - tabela_para_sheet['DT_ENTRADA']).dt.days
                tabela_para_sheet['DT_ENTRADA'] = tabela_para_sheet['DT_ENTRADA'].dt.strftime('%d/%m/%Y')
        except Exception as e:
            print(f"Erro ao processar tabela: {e}")
            tabela_para_sheet = pd.DataFrame()
        return tabela_para_sheet




        # Adicione mais widgets conforme necessário