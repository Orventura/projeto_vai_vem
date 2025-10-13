
from tkinter import messagebox, filedialog as fd
import pandas as pd
from datetime import datetime
from models.model_veiculos import veiculos_cabotagem


class ControlSaida:
    """Controlador para o modal de saida de veículo."""
    def __init__(self, modal):
        self.modal = modal

    def carregar_tabela_saida(self) -> pd.DataFrame:
        """Coleta os dados da planilha de controle de embarques Cabotagem,
        filtra os veículos que ainda não saíram (coluna 'Saída Philco' vazia)"""
        self.local_planilha = fd.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")]
        )
        df = None
        if self.local_planilha:
            try:
                df = pd.read_excel(self.local_planilha, sheet_name='Base', engine='openpyxl', usecols=['Contêiner', 'Saída Philco', 'Nota'])
                df = df[df['Saída Philco'].notna()]
                df.to_clipboard(index=False)
                df = df.drop_duplicates(subset=['Contêiner', 'Nota'])
                df.rename(columns={'Contêiner': 'CONTEINER',
                                    'Nota': 'NOTA_FISCAL', 
                                    'Saída Philco': 'DT_SAIDA'},
                                    inplace=True)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar a planilha:\n{e}")
        elif not self.local_planilha:
            messagebox.showerror("Erro", "Verifique o arquivo selecionado:\nSe possui as colunas (Contêiner, Saída Philco).\nSe possui a planilha 'Base'")
        return df

    def carregar_tabela_liberados(self) -> pd.DataFrame:
        """Carrega as tabelas do banco de dados para alimentar o Sheet
            df_liberados: Dataframe dos dados do banco cabotagem
            """
        def limpar_nf(valor):
            valor_str = str(valor)
            valor_str.lstrip('0').split('-')[0].strip()
            return valor_str

        df_cabotagem_completa, df_cabotagem_sheet = veiculos_cabotagem()
        try:
            df_liberados = df_cabotagem_completa[['INDICE','CONTEINER','DT_ENTRADA', 'NOTA_FISCAL', 'STATUS']]
            df_liberados = df_liberados[
                                                (df_liberados['STATUS'] == 'LIBERADO')
                                            ]
            df_liberados['NOTA_FISCAL'] = df_liberados['NOTA_FISCAL'].apply(lambda x: limpar_nf(x))
            if not df_liberados.empty:
                df_liberados['DT_ENTRADA'] = pd.to_datetime(df_liberados['DT_ENTRADA'], errors='coerce')
                hoje = pd.Timestamp(datetime.now().date())
                df_liberados['DIAS'] = (hoje - df_liberados['DT_ENTRADA']).dt.days
                df_liberados['DT_ENTRADA'] = df_liberados['DT_ENTRADA'].dt.strftime('%d/%m/%Y')
        except Exception as e:
            print(f"Erro ao processar tabela: {e}")
            df_liberados = pd.DataFrame()
        return df_liberados


    def tabelas_para_sheet(self):
        """Carrega e cruza as tabelas de saída e liberados, validando os dados."""
    
        # Carregamento das tabelas
        df_liberados = self.carregar_tabela_liberados()
        df_saida = self.carregar_tabela_saida()
    
        # Validação de carregamento
        if df_saida.empty:
            messagebox.showerror("Erro", "⚠️ Sem dados de saída para atualizar.")
            return pd.DataFrame()
    
        if df_liberados.empty:
            messagebox.showerror("Erro", "⚠️ Sem dados de veículos liberados.")
            return pd.DataFrame()
    
        # Padronização de tipos
        df_saida['NOTA_FISCAL'] = df_saida['NOTA_FISCAL'].astype(str)
        df_liberados['NOTA_FISCAL'] = df_liberados['NOTA_FISCAL'].astype(str)
    
        # Merge
        try:
            merge_ok = pd.merge(
                df_saida,
                df_liberados,
                how='left',
                left_on=['NOTA_FISCAL'],
                right_on=['NOTA_FISCAL']
            )
        except Exception as e:
            messagebox.showerror("Erro ao mesclar", f"❌ Falha ao unir tabelas: {str(e)}")
            return pd.DataFrame()
    
        # Filtro por status
        merge_ok = merge_ok[merge_ok['STATUS'] == 'LIBERADO']
        merge_ok['CONTEINER'] = merge_ok.apply(
                                                lambda row: row['CONTEINER_x'] if row['CONTEINER_x'] == row['CONTEINER_y'] else '',
                                                axis=1
                                            )
        merge_ok = merge_ok[['INDICE', 'CONTEINER', 'NOTA_FISCAL', 'DT_SAIDA','STATUS', 'DIAS']]
    
        if merge_ok.empty:
            messagebox.showinfo("Aviso", "⚠️ Sem datas de saída para atualizar.")
            return pd.DataFrame()

        df_sheet = merge_ok[merge_ok['CONTEINER'] != ""]
        df_erro = merge_ok[merge_ok['CONTEINER'] == ""]

        print("\n\n\n",df_sheet, "\n\n\n", df_erro,"\n\n\n")
        return df_sheet, df_erro
    
    
if __name__ == "__main__":
    app = ControlSaida(None)
    app.tabelas_para_sheet()