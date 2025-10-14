# ...existing code...
import pandas as pd
from models.model_veiculos import veiculos_cabotagem
from datetime import datetime
from tkinter import messagebox
from src.bd_cabotagem import Database
from getpass import getuser

class ControlRetorno:
    """Controlador para o modal de retorno de veículo."""
    def __init__(self, modal):
        self.modal = modal

    #def registrar_retorno(self, dados: dict):
    #    """Registra o retorno do veículo no banco de dados."""
    #    try:
    #        print(f"Registrando retorno com os dados: {dados}")
    #        self.modal.destroy()
    #    except Exception as e:
    #        print(f"Erro ao registrar retorno: {e}")

    def coletar_indice_conteiner(self, event=None):
        """
        Recebe a seleção feita na Sheet do modal e retorna o INDICE correspondente, número do conteiner,
        a partir dos dados completos do modelo veiculos_cabotagem().
        """
        try:
            selecionados = self.modal.sheet.get_currently_selected()
            if not selecionados:
                return None
    
            linha = selecionados[0]
            dados_linha = self.modal.sheet.get_row_data(linha)
            conteiner = dados_linha[5]
    
            # Carrega os dataframes do modelo
            df_cabotagem_completa, df_cabotagem_sheet = veiculos_cabotagem()
    
            # Prepara DataFrame de consulta
            df_consulta = df_cabotagem_completa[['DT_ENTRADA', 'CONTEINER', 'INDICE']].copy()
            df_consulta['DT_ENTRADA'] = pd.to_datetime(df_consulta['DT_ENTRADA'], errors='coerce').dt.strftime("%d/%m/%Y")
    
            # Cria DataFrame temporário com a linha selecionada
            indice_df = pd.DataFrame([dados_linha], columns=df_cabotagem_sheet.columns.to_list())
    
            # Garante que DT_ENTRADA tenha o mesmo formato
            indice_df['DT_ENTRADA'] = pd.to_datetime(indice_df['DT_ENTRADA'], errors='coerce').dt.strftime("%d/%m/%Y")
    
            # Faz merge para recuperar o INDICE original
            mescla = pd.merge(
                indice_df[['DT_ENTRADA', 'CONTEINER']],
                df_consulta,
                how='inner',
                on=['DT_ENTRADA', 'CONTEINER']
            )
    
            if mescla.empty:
                print("Nenhuma correspondência encontrada ao tentar mapear para INDICE.")
                return None
    
            self.id = int(mescla['INDICE'].iloc[0])
            print(f"Índice coletado: {self.id}")
            return self.id, conteiner
    
        except Exception as e:
            print(f"Erro em coletar_indice: {e}")
            return None

    def filtrar_sheet(self, event=None):
        """Filtra a tabela de recebimento em todas as colunas."""

        texto = self.modal.e_pesquisa.get().strip().lower()
        colunas = [
            "DT_ENTRADA", "BK_ENTRADA", "FABRICA", "ARMADOR", "TRANSPORTADOR",
            "CONTEINER", "NOTA_FISCAL", "DESTINO", "STATUS", "DIAS"
        ]

        # Carrega os dados do banco
        df_cabotagem_completa, df_cabotagem_sheet = veiculos_cabotagem()

        # Garante que DT_ENTRADA seja datetime e calcula DIAS
        df_cabotagem_completa['DT_ENTRADA'] = pd.to_datetime(df_cabotagem_completa['DT_ENTRADA'], errors='coerce')
        hoje = pd.Timestamp.now().normalize()
        df_cabotagem_completa['DIAS'] = (hoje - df_cabotagem_completa['DT_ENTRADA']).dt.days

        # Seleciona as colunas após calcular DIAS
        df = df_cabotagem_completa[colunas].copy()

        # Aplica filtro por STATUS sempre
        df = df[df['STATUS'].isin(['SAIU', 'LIBERADO'])]

        # Aplica filtro por texto em todas as colunas
        if texto:
            df = df[df.apply(
                lambda row: row.astype(str).str.lower().str.contains(texto).any(),
                axis=1
            )]

        # Atualiza a sheet com os dados filtrados ou completos
        self.modal.sheet.set_sheet_data(
            df.values.tolist(),
            reset_col_positions=True,
            reset_row_positions=True
        )
        self.modal.sheet.headers(list(df.columns))
        self.modal.sheet.deselect("all")
        self.modal.sheet.set_all_column_widths()
        self.modal.sheet.extra_bindings([
            ("row_select", self.coletar_indice_conteiner)
        ])

    def dados_para_retorno(self):
        """Coleta os dados que serão usados para registrar o retorno do veiculo."""

        selecionados = self.modal.sheet.get_currently_selected()
        if not selecionados:
            messagebox.showwarning("Atenção", "Nenhum veículo selecionado para retorno.")
            return None, None
        try:
            indice, conteiner = self.coletar_indice_conteiner()
            if not indice:
                raise ValueError("Nenhum índice selecionado para retorno.")
                return
            dados_retorno = {                
                            'INDICE': int(indice),
                            'DT_ENTRADA': datetime.now().strftime('%Y-%m-%d'),#usar apenas na tabela STATUS
                            'STATUS': 'RETORNOU',
                            'USUARIO': str(getuser()).upper(),
            }
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao coletar dados para retorno: {e}")
            return
        return dados_retorno, conteiner
    
    def lancar_dados(self):
        """Salva o retorno do veículo no banco de dados."""
        dados_do_sheet, conteiner = self.dados_para_retorno()
        if not dados_do_sheet:
            messagebox.showwarning("Atenção", "Nenhum dado válido para registrar o retorno.")
            return

        # ✅ Confirmação do usuário antes de prosseguir
        continuar = messagebox.askokcancel(
            "Confirmação",
            f"Você deseja continuar com o registro do retorno do veículo?\n\n"
            f"Conteiner: {conteiner}\n"
        )
        if not continuar:
            messagebox.showinfo("Cancelado", "Operação de retorno cancelada pelo usuário.")
            return

        try:
            with Database() as db:
                db.update_base(indice=dados_do_sheet['INDICE'], STATUS=dados_do_sheet['STATUS'])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar retorno no banco de dados: {e}")
            return

        try:
            with Database() as db:
                dados_status = db.fetch_base(INDICE=int(dados_do_sheet['INDICE']))
                dados_status[0]['DT_ENTRADA'] = dados_do_sheet['DT_ENTRADA']
                dados_status[0].pop("INDICE")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar alterações de status na tabela base: {e}")
            return

        try:
            with Database() as db:
                db.insert_status(**dados_status[0])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir alterações de status: {e}")
            return

        messagebox.showinfo("Sucesso", "Retorno registrado com sucesso.")

if __name__ == "__main__":
    app = ControlRetorno(None)
    app.filtrar_sheet()