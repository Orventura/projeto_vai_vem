# ...existing code...
import pandas as pd
from models.model_veiculos import veiculos_cabotagem


class ControlRetorno:
    """Controlador para o modal de retorno de veículo."""
    def __init__(self, modal):
        self.modal = modal

    def registrar_retorno(self, dados: dict):
        """Registra o retorno do veículo no banco de dados."""
        try:
            print(f"Registrando retorno com os dados: {dados}")
            self.modal.destroy()
        except Exception as e:
            print(f"Erro ao registrar retorno: {e}")

    def coletar_indice(self, event=None):
        """
        Recebe a seleção feita na Sheet do modal e retorna o INDICE correspondente
        a partir dos dados completos do modelo veiculos_cabotagem().
        """
        try:
            # obtém seleção do sheet do modal (ModalRetorno.armazena o CustomSheet em self.sheet)
            selecionados = self.modal.sheet.get_currently_selected()
            if not selecionados:
                print("Nenhuma linha selecionada.")
                return None

            linha = selecionados[0]
            dados_linha = self.modal.sheet.get_row_data(linha)
            print(f'DEBUG Dados da linha selecionada: {dados_linha}')

            # pega os dataframes diretamente do modelo
            df_cabotagem_completa, df_cabotagem_sheet = veiculos_cabotagem()

            # prepara DataFrame de consulta (usa colunas e formatação iguais às do sheet exibido)
            df_consulta = df_cabotagem_completa[['DT_ENTRADA', 'CONTEINER', 'INDICE']].copy()
            df_consulta['DT_ENTRADA'] = pd.to_datetime(df_consulta['DT_ENTRADA'], errors='coerce').dt.strftime("%d/%m/%Y")

            # cria um DF temporário com a linha selecionada usando os cabeçalhos do df_sheet retornado pelo modelo
            indice_df = pd.DataFrame([dados_linha], columns=df_cabotagem_sheet.columns.to_list())

            # faz merge para recuperar o INDICE original
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
            return self.id

        except Exception as e:
            print(f"Erro em coletar_indice: {e}")
            return None