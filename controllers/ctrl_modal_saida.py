
from tkinter import messagebox, filedialog as fd
import pandas as pd

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
                df = pd.read_excel(self.local_planilha, engine='openpyxl', usecols=['Contêiner', 'Saída Philco', 'NF'])
                df = df[df['Saída Philco'].notna()]
                df.to_clipboard(index=False)
                #messagebox.showinfo("Planilha Carregada", f"Planilha carregada com {len(df)} registros pendentes.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar a planilha:\n{e}")
        elif not self.local_planilha:
            messagebox.showerror("Erro", "Verifique o arquivo selecionado:\nSe possui as colunas (Contêiner, Saída Philco).\nSe possui a planilha 'Base'")
        return df


if __name__ == "__main__":
    app = ControlSaida(None)
    df =app.carregar_tabela_saida()
    print(df)
