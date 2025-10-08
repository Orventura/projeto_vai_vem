
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from pathlib import Path

# Caminhos de produção
PATH_RODOVIARIO = Path(r"H:\EXPEDICAO\03 Rodoviário\03 Dados\rodoviario.db")
PATH_CABOTAGEM  = Path(r"H:\EXPEDICAO\01 Cabotagem\DADOS\1_Última versão\arquivo\philco.db")
PATH_VAI_VEM    = Path(r"x:\x")

# Caminhos de teste
TESTE_RODOVIARIO = Path(r"data\rodoviario.db")
TESTE_CABOTAGEM  = Path(r"data\database_cabotagem.db")
TESTE_VAI_VEM    = Path(r"data\dados.db")

# Verifica se todos os arquivos de produção existem
if all(path.exists() for path in [PATH_RODOVIARIO, PATH_CABOTAGEM, PATH_VAI_VEM]):
    BD_RODOVIARIO = PATH_RODOVIARIO
    BD_CABOTAGEM  = PATH_CABOTAGEM
    BD_VAI_VEM    = PATH_VAI_VEM
    print("✅ Programa em Produção (Rodoviário, Cabotagem e VaiVem)")
    print(f"Rodoviário: {BD_RODOVIARIO}")
    print(f"Cabotagem:  {BD_CABOTAGEM}")
    print(f"VaiVem:     {BD_VAI_VEM}")
else:
    BD_RODOVIARIO = TESTE_RODOVIARIO
    BD_CABOTAGEM  = TESTE_CABOTAGEM
    BD_VAI_VEM    = TESTE_VAI_VEM
    print("⚠️ Usando banco em TESTE (Rodoviário, Cabotagem e VaiVem)")
    print(f"Rodoviário: {BD_RODOVIARIO}")
    print(f"Cabotagem:  {BD_CABOTAGEM}")
    print(f"VaiVem:     {BD_VAI_VEM}")



# Configurações dos frames do menu Entradas Vai Vem
subframes = {
    "frame_1": {"x": 90, "y": 0, "width": 198, "height": 170},
    "frame_2": {"x": 290, "y": 0, "width": 198, "height": 170},
    "frame_3": {"x": 490, "y": 0, "width": 198, "height": 170},
    "frame_4": {"x": 0, "y": 173, "width": 790, "height": 236},
    "frame_5": {"x": 0, "y": 412, "width": 790, "height": 37},
}


def dicionario_entrada_veiculos(valor: list):
    """Dicionario que recebe os dados da interface Lançar entradas CABOTAGEM"""
    dicionario1 = {
        "DT_ENTRADA": valor[0],
        "BK_ENTRADA": valor[1],
        "FABRICA": valor[2],
        "ARMADOR": valor[3],
        "TRANSPORTADOR": valor[4],
        "CONTEINER": valor[5],
        "NOTA_FISCAL": None,
        "ARMADOR_BOOKING_DESTINO": None,
        "LACRE_ARMADOR": None,
        "LACRE_PHILCO": None,
        "PESO_BRUTO": None,
        "PESO_LIQUIDO": None,
        "VALOR": None,
        "OBS": None,
        "ISCA_1": None,
        "ISCA_2": None,
        "STATUS": valor[7],
        "DESTINO": valor[6],
        "DIAS_PARADOS": None,
        "DT_SAIDA": None,
        "OBS_2": None
    }
    return dicionario1

def dicionario_editar_status(valor2: list, user):
    try:# garante que a lista tem pelo menos 20 elementos
        #$#valor2 = valor2 + [None] * (20 - len(valor2))
        print(valor2)

        dicionario2 = {
            'DT_ENTRADA': valor2[0],
            'BK_ENTRADA': valor2[1],
            'FABRICA': valor2[2],
            'ARMADOR': valor2[3],
            'TRANSPORTADOR': valor2[4],
            'CONTEINER': valor2[5],
            'NOTA_FISCAL': valor2[6],
            'ARMADOR_BOOKING_DESTINO': valor2[7],
            'LACRE_ARMADOR': valor2[8],
            'LACRE_PHILCO': valor2[9],
            'PESO_BRUTO': valor2[10],
            'PESO_LIQUIDO': valor2[11],
            'VALOR': valor2[12],
            'OBS': valor2[13],
            'ISCA_1': valor2[14],
            'ISCA_2': valor2[15],
            'STATUS': valor2[17],
            'DESTINO': valor2[16],
            'DIAS_PARADOS': valor2[18],
            'DT_SAIDA': valor2[19],
            'USUARIO': str(user).upper(),
            'OBS_2': valor2[20]
        }
        return dicionario2
    except Exception as e:
        print(f'erro ao obter dicionario STATUS {str(e)}')

def dados_para_input_vaivem(valor: list):
    """"""
    dicionario = {
        "romaneio": str(valor[13]).upper().strip(),
        "segmento": str(valor[1]).upper().strip(),
        "data": str(valor[6]).upper().strip(),
        "transportadora": str(valor[9]).upper().strip(),
        "placa_num_conteiner": str(valor[8]).upper().strip(),
        "frota": str(valor[10]).upper().strip(),
        "lacre": str(valor[11]).upper().strip(),
        "galpao_origem": str(valor[15]).upper().strip(),
        "galpao_destino": str(valor[16]).upper().strip(),
        "turno": str(valor[17]).upper().strip(),
        "conferente": str(valor[18]).upper().strip(),
        "localizacao": str(valor[14]).upper().strip(),
        "item": str(valor[0]).upper().strip(),
        "descricao": str(valor[2]).upper().strip(),
        "quantidade": str(valor[3]).upper().strip(),
        "nf": str(valor[12]).upper().strip(),
        "motivo": str(valor[4]).upper().strip(),
        "justificativa": str(valor[5]).upper().strip(),
        "status": str(valor[7]).upper().strip(),
        "conferente2": None,
        "romaneio2": None,
        "data2": None,
        "end_user": None,
        "final_hour": None,
        "pc": None
    }
    return dicionario

import customtkinter as ctk

class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        # Força o border_width para 0, independentemente do que for passado
        kwargs['border_width'] = 0
        super().__init__(master, **kwargs)


class CustomLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        # Força os valores desejados
        kwargs['corner_radius'] = 6
        kwargs['fg_color'] = ['#F9F9FA', '#343638']
        kwargs['text_color'] = ['gray52', 'gray62']
        super().__init__(master, **kwargs)


class CustomComboBox(ctk.CTkComboBox):
    def __init__(self, master=None, **kwargs):
        # Força o border_width para 0, independentemente do que for passado
        kwargs['border_width'] = 0
        kwargs['state'] = 'readonly'        
        super().__init__(master, **kwargs)

from tksheet import Sheet

class CustomSheet(Sheet):
    def __init__(self, *args, **kwargs):
        # Recupera o tema inicial (padrão: "dark")
        self._theme = kwargs.get("theme", "dark")
        super().__init__(*args, **kwargs)

    @property
    def theme_value(self):
        """Retorna sempre o tema atual."""
        return self._theme

    def change_theme(self, theme: str = "light blue", redraw: bool = True) -> "CustomSheet":
        """
        Sobrescreve o change_theme original para atualizar também
        o atributo _theme da nossa classe customizada.
        """
        # Chama o método original da classe base
        super().change_theme(theme=theme, redraw=redraw)

        # Atualiza o atributo interno
        self._theme = theme

        return self


import pathlib
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox

class RecursosVisuais:
    def __init__(self):
        self.carregar_recursos()

    def carregar_recursos(self):

        """Carrega imagens de tema claro e escuro"""
        try:
            self.img_dir = pathlib.Path(__file__).parent / 'img'
            self.img_dir.mkdir(exist_ok=True)
            self.light = ctk.CTkImage(Image.open(self.img_dir / '2_sol.png'), size=(15, 15))
            self.dark = ctk.CTkImage(Image.open(self.img_dir / '2_lua.png'), size=(15, 15))
            self.adicionar = ctk.CTkImage(Image.open(self.img_dir / 'adicionar.png'), size=(28, 28))
            self.editar = ctk.CTkImage(Image.open(self.img_dir / 'editar.png'), size=(28, 28))
            self.liberar = ctk.CTkImage(Image.open(self.img_dir / 'liberar.png'), size=(28, 28))
            self.sair = ctk.CTkImage(Image.open(self.img_dir / 'sair.png'), size=(28, 28))
            self.retornar = ctk.CTkImage(Image.open(self.img_dir / 'retornar.png'), size=(28, 28))
            self.receber = ctk.CTkImage(Image.open(self.img_dir / 'receber_veiculo.png'), size=(28, 28))
            self.exportar = ctk.CTkImage(Image.open(self.img_dir / 'exportar.png'), size=(28, 28))
            self.config = ctk.CTkImage(Image.open(self.img_dir / 'config.png'), size=(28, 28))

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagens: {str(e)}")

            raise SystemExit(1)


class CustomButton(ctk.CTkButton):
    """
    Botão personalizado no padrão azul do projeto.

    - Cor normal:  #2132F3
    - Hover:       #3A4CF7
    - Texto:       #FFFFFF
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", "#014ae4"),       # Azul padrão
            hover_color=kwargs.pop("hover_color", "#4a7be4"), # Hover azul claro
            text_color=kwargs.pop("text_color", "#FFFFFF"),   # Texto branco
            #corner_radius=kwargs.pop("corner_radius", 8),     # Raio das bordas
            #font=kwargs.pop("font", ("Roboto", 14, "bold")),  # Fonte padrão
            **kwargs
        )

        
