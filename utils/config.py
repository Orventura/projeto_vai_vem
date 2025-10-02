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
            self.adicionar = ctk.CTkImage(Image.open(self.img_dir / 'adicionar.png').resize((60, 60)))
            self.editar = ctk.CTkImage(Image.open(self.img_dir / 'editar.png').resize((60, 60)))
            self.liberar = ctk.CTkImage(Image.open(self.img_dir / 'liberar.png').resize((60, 60)))
            self.sair = ctk.CTkImage(Image.open(self.img_dir / 'sair.png').resize((60, 60)))
            self.retornar = ctk.CTkImage(Image.open(self.img_dir / 'retornar.png').resize((60, 60)))
            self.receber = ctk.CTkImage(Image.open(self.img_dir / 'receber_veiculo.png').resize((60, 60)))
            self.exportar = ctk.CTkImage(Image.open(self.img_dir / 'exportar.png').resize((60, 60)))

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

        
