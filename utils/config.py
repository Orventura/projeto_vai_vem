# Configurações dos frames do menu Entradas
subframes = {
    "frame_1": {"x": 0, "y": 0, "width": 198, "height": 170},
    "frame_2": {"x": 200, "y": 0, "width": 198, "height": 170},
    "frame_3": {"x": 400, "y": 0, "width": 198, "height": 170},
    "frame_4": {"x": 0, "y": 173, "width": 598, "height": 236},
    "frame_5": {"x": 0, "y": 412, "width": 598, "height": 37},
}

def dados_para_input(valor: list):
    """"""
    dicionario = {
        "romaneio": valor[13],
        "segmento": valor[1],
        "data": valor[6],
        "transportadora": valor[9],
        "placa_num_conteiner": valor[8],
        "frota": valor[10],
        "lacre": valor[11],
        "galpao_origem": valor[15],
        "galpao_destino": valor[16],
        "turno": valor[17],
        "conferente": valor[18],
        "localizacao": valor[14],
        "item": valor[0],
        "descricao": valor[2],
        "quantidade": valor[3],
        "nf": valor[12],
        "motivo": valor[4],
        "justificativa": valor[5],
        "status": valor[7],
        "conferente2": "",
        "romaneio2": "",
        "data2": "",
        "end_user": "",
        "final_hour": "",
        "pc": ""
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
        self.light: ctk.CTkImage | None = None
        self.dark: ctk.CTkImage | None = None
        self.img_dir: pathlib.Path | None = None
        self.adict: ctk.CTkImage | None = None
        self.subtract: ctk.CTkImage | None = None
        self.carregar_recursos()

    def carregar_recursos(self):

        """Carrega imagens de tema claro e escuro"""
        try:
            self.img_dir = pathlib.Path(__file__).parent / 'img'
            self.img_dir.mkdir(exist_ok=True)
            self.light = ctk.CTkImage(Image.open(self.img_dir / '2_sol.png').resize((40, 40)))
            self.dark = ctk.CTkImage(Image.open(self.img_dir / '2_lua.png').resize((40, 40)))
            self.adict = ctk.CTkImage(Image.open(self.img_dir / 'adicao.png').resize((40, 40)))
            self.subtract = ctk.CTkImage(Image.open(self.img_dir / 'subtracao.png').resize((10, 40)))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagens: {str(e)}")
            raise SystemExit(1)


