import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import pandas as pd
import re

class ValidarNf:
    def __init__(self, range:int):
        self.df_acumulado = pd.DataFrame()

        for _ in range(50):
            novo_df = self.acumular_dados()
            if novo_df is not None:
                self.df_acumulado = pd.concat([self.df_acumulado, novo_df], ignore_index=True)

        print(self.df_acumulado)

    def selecionar_pdf(self):
        root = tk.Tk()
        root.withdraw()
        caminho = filedialog.askopenfilename(
            title="Selecione o PDF da Nota Fiscal",
            filetypes=[("PDF files", "*.pdf")]
        )
        return caminho

    def extrair_texto_pdf(self, caminho):
        try:
            doc = fitz.open(caminho)
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            return texto
        except Exception as e:
            print(f"Erro ao abrir PDF: {e}")
            return ""

    def extrair_dados(self, texto):
        dados = {}

        nf = re.search(r"Nº\.?\s*(\d{6,})", texto)
        serie = re.search(r"SÉRIE\s*(\d+)", texto)
        valor_total = re.search(r"VALOR TOTAL DA NOTA\s*([\d.,]+)", texto)
        peso_bruto = re.search(r"PESO BRUTO\s*([\d.,]+)", texto)
        peso_liquido = re.search(r"PESO L[IÍ]QUIDO\s*([\d.,]+)", texto)

        if nf: dados["Numero NF"] = nf.group(1)
        if serie: dados["Série"] = serie.group(1)
        if valor_total: dados["Valor Total"] = valor_total.group(1)
        if peso_bruto: dados["Peso Bruto"] = peso_bruto.group(1)
        if peso_liquido: dados["Peso Líquido"] = peso_liquido.group(1)

        return pd.DataFrame([dados]) if dados else None

    def acumular_dados(self):
        caminho_pdf = self.selecionar_pdf()
        if not caminho_pdf:
            print("Nenhum arquivo selecionado.")
            return None

        texto = self.extrair_texto_pdf(caminho_pdf)
        if not texto:
            print("Texto vazio ou erro na leitura do PDF.")
            return None

        novo_df = self.extrair_dados(texto)
        if novo_df is None or novo_df.empty:
            print("Nenhum dado extraído do PDF.")
            return None

        return novo_df

if __name__ == "__main__":
    app = ValidarNf()