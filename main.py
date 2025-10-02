from logging import root
import customtkinter as ctk
from src.vaivem_embarcar import Entradas
from src.vaivem_receber import Recebimento
from utils.config import RecursosVisuais, CustomSheet

class JanelaPrincipal:
    def __init__(self):
        """Inicializa a janela principal da aplicação."""
        ctk.set_appearance_mode("light")

        self.root = ctk.CTk()
        self.root.title("Sistema")
        self.root.geometry('815x460')

        self.entradas = Entradas(self.root)
        self.recebimento = Recebimento(self.root)

        self.root.configure(fg_color='white')
        self.root.resizable(False, False)

        # Frame lateral (menu)
        self.frame_esq = ctk.CTkFrame(self.root, width=200, height=450)
        self.frame_esq.place(x=5, y=5)

        #self.path_img, self.img_light, self.img_dark  = self._carregar_recursos()
        self.img = RecursosVisuais()

        # Botão no menu lateral
        self.label_menu = ctk.CTkLabel(self.frame_esq, text="Vai Vem", font=("Roboto", 16))
        self.label_menu.place(x=60, y=20)

        # Botões de navegação
        self.btn_vaivem_embarcar = ctk.CTkButton(self.frame_esq, text="Embarcar", command=self.abrir_entradas)
        self.btn_vaivem_embarcar.place(x=30, y=50)

        self.btn_vaivem_receber = ctk.CTkButton(self.frame_esq, text="Receber", command=self.abrir_recebimento)
        self.btn_vaivem_receber.place(x=30, y=100)

        self.frame_botoes = ctk.CTkFrame(self.frame_esq, width=598, height=37)
        self.frame_botoes.place(x=0, y=412)

        self.botao_tema = ctk.CTkButton(
            self.frame_botoes,
            image=self.img.dark,
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="darkgray",
            command=lambda: self.alterar_tema()
        )
        self.botao_tema.place(x=3, y=3)

    def abrir_entradas(self):
        """Abre a janela de Entradas, escondendo a de Recebimento se necessário."""
        self.recebimento.esconder()
        self.entradas.mostrar()

    def abrir_recebimento(self):
        """Abre a janela de Recebimento, escondendo a de Entradas se necessário."""
        self.entradas.esconder()
        self.recebimento.mostrar()
  
    def alterar_tema(self):
        '''Altera o tema da aplicação entre claro e escuro.'''
        self.modo_atual = ctk.get_appearance_mode()
        if self.modo_atual == 'Dark':
            ctk.set_appearance_mode("light")
            self.botao_tema.configure(image=self.img.dark)
            self.root.configure(fg_color='white')
            novo_tema = 'light_blue'
        else:
            ctk.set_appearance_mode("dark")
            self.botao_tema.configure(image=self.img.light)
            self.root.configure(fg_color='gray20')
            novo_tema = 'dark'
            
        def coletar_sheets(widget, lista=None):
            """Coleta todas as instâncias de Sheet dentro do widget fornecido recursivamente."""
            if lista is None:
                lista = []
            for child in widget.winfo_children():
                if isinstance(child, CustomSheet):  # ou Sheet se não usar CustomSheet
                    lista.append(child)
                coletar_sheets(child, lista)
            return lista

        sheets = coletar_sheets(self.root)
        for sheet in sheets:
            sheet.change_theme(theme=novo_tema)
        
if __name__ == '__main__':
    app = JanelaPrincipal()
    app.root.mainloop()