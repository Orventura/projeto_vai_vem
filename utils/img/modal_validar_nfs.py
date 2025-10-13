import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import fitz  # PyMuPDF
import pandas as pd
import re

class ColetaNf:
    def __init__(self, qtd_notas:int):
        self.qtd_notas = qtd_notas
        self.df_acumulado = pd.DataFrame()

        for _ in range(self.qtd_notas):
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

class ModalNf(ctk.CTkToplevel):
    """Cria um modal para coletar as nfs a serem liberadas, trata os dados
    de peso bruto, liquido, e valor, carrega para o modal liberar"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Registrar Notas Fiscais")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        
        self.criar_widgets()
      
    def criar_widgets(self):
        self.frame1 = ctk.CTkFrame(self, width=400, height=200, fg_color='red')
        self.frame1.pack(side='top')
        self.frame2 = ctk.CTkFrame(self, width=400, height=200, fg_color='red')
        self.frame2.pack(side='bottom')








        label_peso_b= ctk.CTkLabel(self.frame1, text='Peso Bruto')
        label_peso_b.pack(side='right', padx=5)
        label_peso_l= ctk.CTkLabel(self.frame1, text='Peso Líquido')
        label_peso_l.pack(side='right', padx=5)
        label_vl_total= ctk.CTkLabel(self.frame1, text='Valor Total')
        label_vl_total.pack(pady=5, padx=5, side='right')
        label_serie= ctk.CTkLabel(self.frame1, text='Série', )
        label_serie.pack(pady=5, padx=5, side='right')
        label_nf= ctk.CTkLabel(self.frame1, text='Nota Fiscal')
        label_nf.pack(pady=5, padx=5, side='right')

        label_peso_b= ctk.CTkLabel(self.frame1, text='Peso Bruto')
        label_peso_b.pack(side='right', padx=5)
        label_peso_l= ctk.CTkLabel(self.frame1, text='Peso Líquido')
        label_peso_l.pack(side='right', padx=5)
        label_vl_total= ctk.CTkLabel(self.frame1, text='Valor Total')
        label_vl_total.pack(pady=5, padx=5, side='right')
        label_serie= ctk.CTkLabel(self.frame1, text='Série', )
        label_serie.pack(pady=5, padx=5, side='right')
        label_nf= ctk.CTkLabel(self.frame1, text='Nota Fiscal')
        label_nf.pack(pady=5, padx=5, side='right')

        label_peso_b2= ctk.CTkLabel(self.frame2, text='Peso Bruto')
        label_peso_b2.pack(side='right', padx=5)
        label_peso_l2= ctk.CTkLabel(self.frame2, text='Peso Líquido')
        label_peso_l2.pack(side='right', padx=5)
        label_vl_total2= ctk.CTkLabel(self.frame2, text='Valor Total')
        label_vl_total2.pack(pady=5, padx=5, side='right')
        label_serie2= ctk.CTkLabel(self.frame2, text='Série', )
        label_serie2.pack(pady=5, padx=5, side='right')
        label_nf= ctk.CTkLabel(self.frame2, text='Nota Fiscal')
        label_nf.pack(pady=5, padx=5, side='right')
        pass
    


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry('555x555')
    nfs = ColetaNf(1)
    modal = ModalNf(app)
    modal.mainloop()

