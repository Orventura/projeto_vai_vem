
from tkinter import messagebox, filedialog as fd
import pandas as pd
from datetime import datetime
from models.model_veiculos import veiculos_cabotagem
from src.bd_cabotagem import Database
from getpass import getuser


class ControlSaida:
    """Controlador para o modal de saida de veículo."""
    def __init__(self, modal):
        self.modal = modal
        self.user = str(getuser()).upper()

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
                df['NOTA_FISCAL'] = df['NOTA_FISCAL'].apply(lambda x: self.limpar_nf(str(x)))

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar a planilha:\n{e}")
        elif not self.local_planilha:
            messagebox.showerror("Erro", "Verifique o arquivo selecionado:\nSe possui as colunas (Contêiner, Saída Philco).\nSe possui a planilha 'Base'")
        return df

    def limpar_nf(self, valor: str) -> str:
        valor_str = str(valor)
        novo = valor_str.lstrip('0').split('-')[0].strip()
        return novo


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
                df_liberados['NOTA_FISCAL'] = df_liberados['NOTA_FISCAL'].apply(lambda x: self.limpar_nf(str(x)))

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
            pergunta = messagebox.askyesno(
                "Atenção",
                "⚠️ Não há dados de saída na planilha selecionada.\nDeseja continuar?"
            )
            if not pergunta:
                self.modal.destroy()
                return
            else:
                return pd.DataFrame(), pd.DataFrame(), "Sem dados de saída na planilha.", "info"
    
        if df_liberados.empty:
            pergunta = messagebox.askyesno(
                "Atenção",
                "⚠️ Não há veículos liberados no sistema.\nDeseja continuar?"
            )
            if not pergunta:
                self.modal.destroy()
                return
            else:
                return pd.DataFrame(), pd.DataFrame(), "Sem veículos liberados no sistema.", "info"
    
        # Padronização de tipos
        df_saida['NOTA_FISCAL'] = df_saida['NOTA_FISCAL'].astype(str)
        df_liberados['NOTA_FISCAL'] = df_liberados['NOTA_FISCAL'].astype(str)
    
        # Merge
        try:
            merge_ok = pd.merge(
                df_saida,
                df_liberados,
                how='left',
                on='NOTA_FISCAL'
            )
        except Exception as e:
            msg = f"❌ Falha ao unir tabelas: {str(e)}"
            msg_type = "erro"
            messagebox.showerror("Erro", msg)
            return pd.DataFrame(), pd.DataFrame(), msg, msg_type
    
        # Filtro por status
        merge_ok = merge_ok[merge_ok['STATUS'] == 'LIBERADO']
        merge_ok['CONTEINER'] = merge_ok.apply(
            lambda row: row['CONTEINER_x'] if row['CONTEINER_x'] == row['CONTEINER_y'] else '',
            axis=1
        )
        merge_ok = merge_ok[['INDICE', 'CONTEINER', 'NOTA_FISCAL', 'DT_SAIDA', 'STATUS', 'DIAS']]
    
        # Separação dos dados válidos e com erro
        df_sheet = merge_ok[merge_ok['CONTEINER'] != ""].copy()
        df_erro = merge_ok[merge_ok['CONTEINER'] == ""][['NOTA_FISCAL']].copy()
    
        # Conversões
        if not df_sheet.empty:
            df_sheet['INDICE'] = df_sheet['INDICE'].astype(int)
            df_sheet['DIAS'] = df_sheet['DIAS'].astype(int)
            df_sheet['DT_SAIDA'] = pd.to_datetime(df_sheet['DT_SAIDA']).dt.strftime('%d/%m/%Y')
    
        # Mensagens
        self.df_sheet = df_sheet
        self.df_erro = df_erro
    
        if df_sheet.empty and df_erro.empty:
            msg = "Sem datas de saída para atualizar.\nSem erros encontrados."
            msg_type = "info"
            messagebox.showinfo("Aviso", msg)
        elif df_sheet.empty and not df_erro.empty:
            msg = "Sem datas de saída para atualizar.\nForam encontrados erros na NF:\n" + "\n".join(df_erro['NOTA_FISCAL'].tolist())
            msg_type = "erro"
            messagebox.showerror("Erro", msg)
        elif not df_sheet.empty and df_erro.empty:
            msg = "Todas as datas de saída foram atualizadas com sucesso.\nNenhum erro encontrado."
            msg_type = "sucesso"
            messagebox.showinfo("Sucesso", msg)
        elif not df_sheet.empty and not df_erro.empty:
            msg = "Algumas datas de saída serão atualizadas.\nForam encontrados erros na NF:\n" + "\n".join(df_erro['NOTA_FISCAL'].tolist())
            msg_type = "atenção"
            messagebox.showwarning("Atenção", msg)
    
        return df_sheet, df_erro, msg, msg_type

    def registrar_saida(self):
        """Atualiza o banco de dados com as saídas registradas."""
        dados = self.modal.sheet.get_sheet_data()
        for dado in dados:
            if dado[6]:
                dicionario = {
                    'INDICE': dado[0],
                    'DT_SAIDA': dado[3],
                    'STATUS': 'SAIU'
                }
                try:
                    with Database() as db:
                        db.update_base(indice=int(dicionario['INDICE']),
                                        DT_SAIDA=(datetime.strptime(dicionario['DT_SAIDA'], '%d/%m/%Y').strftime('%Y-%m-%d')),
                                        STATUS=dicionario['STATUS'])
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados:\n{e}")
                    return
                try:
                    with Database() as db:
                        dados_status = db.fetch_base(INDICE=int(dicionario['INDICE']))
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao buscar dados para status:\n{e}")
                    return
                if dados_status:
                    dados_status = dados_status[0]
                    dados_status.pop("INDICE")
                    dados_status['DT_ENTRADA'] = datetime.now().strftime('%Y-%m-%d')
                    dados_status['USUARIO'] = str(getuser()).upper()
                    try:
                        with Database() as db:
                            db.insert_status(**dados_status)
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao inserir dados na tabela STATUS:\n{e}")
                        return

if __name__ == "__main__":
    app = ControlSaida(None)
    app.tabelas_para_sheet()