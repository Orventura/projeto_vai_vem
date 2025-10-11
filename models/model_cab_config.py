import sqlite3
import pandas as pd
from tkinter import messagebox as mb
from utils.config import *

class Listas:
    def __init__(self, caminho_db: str = BD_CABOTAGEM):
        self.caminho = caminho_db
        self.conexao = None

    def __enter__(self):
        try:
            self.conexao = sqlite3.connect(self.caminho)
            return self
        except Exception as e:
            mb.showerror("Erro", f"Falha ao conectar ao banco: {str(e)}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conexao:
            self.conexao.close()

    def _extrair_lista(self, tabela: str) -> list:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {tabela}", self.conexao)
            coluna = df.columns[0]
            return df[coluna].dropna().astype(str).str.strip().tolist()
        except Exception as e:
            mb.showerror("Erro", f"Erro ao acessar tabela '{tabela}': {str(e)}")
            return []

    # Métodos individuais para cada tabela
    def lista_user_auth(self):
        return self._extrair_lista("user_auth")

    def lista_transportes(self):
        return self._extrair_lista("transportador")

    def lista_fabricas(self):
        return self._extrair_lista("fabrica")

    def lista_armadores(self):
        return self._extrair_lista("armador")

    def lista_destinos(self):
        return self._extrair_lista("destino")

    def lista_situacoes(self):
        return self._extrair_lista("situacao")

    def lista_bookings(self):
        return self._extrair_lista("booking")
    
    def lista_pgr(self):
        ag = self._extrair_lista("iscas_ag")
        cliente = self._extrair_lista("iscas_cliente")
        return ag, cliente
    
    def dicionario_de_listas(self):
        lista = []
        tabelas = ['user_auth', 'transportador', 'fabrica', 'armador', 'destino', 'situacao', 'booking', 'iscas_ag', 'iscas_cliente']
        for tabela in tabelas:
            v = self._extrair_lista(tabela)
            lista.append(v)
        dicionario = dict(zip(tabelas, lista))
        return dicionario