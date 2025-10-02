import customtkinter as ctk
from PIL import Image
import pathlib

class RecursosVisuais:
    def __init__(self):
        self.img_dir = pathlib.Path(__file__).parent / 'img'
        self.img_dir.mkdir(exist_ok=True)
        self.carregar_recursos()

    def carregar_recursos(self):
        self.adicionar = ctk.CTkImage(Image.open(self.img_dir / 'adicionar.png').resize((150, 150)))
        self.editar = ctk.CTkImage(Image.open(self.img_dir / 'editar.png').resize((150, 150)))
        self.liberar = ctk.CTkImage(Image.open(self.img_dir / 'liberar.png').resize((150, 150)))
        self.sair = ctk.CTkImage(Image.open(self.img_dir / 'sair.png').resize((150, 150)))
        self.retornar = ctk.CTkImage(Image.open(self.img_dir / 'retornar.png').resize((150, 150)))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()  
        self.title("Hover com Label")
        self.geometry("500x150")
        self.recursos = RecursosVisuais()

        # Label que será atualizado no hover
        self.label_hover = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color='gray')
        self.label_hover.pack(pady=10)

        # Dicionário de botões
        self.botoes_info = {
            "Adicionar Veículo": {"imagem": self.recursos.adicionar, "comando": lambda: print("Adicionar")},
            "Editar Veículo": {"imagem": self.recursos.editar, "comando": lambda: print("Editar")},
            "Liberar Veículo": {"imagem": self.recursos.liberar, "comando": lambda: print("Liberar")},
            "Registrar Saída": {"imagem": self.recursos.sair, "comando": lambda: print("Sair")},
            "Retornar Veículo": {"imagem": self.recursos.retornar, "comando": lambda: print("Retornar")},
        }

        self.criar_botoes()

    def criar_botoes(self):
        frame_botoes = ctk.CTkFrame(self, fg_color='transparent')
        frame_botoes.pack(pady=10)

        for i, (nome, info) in enumerate(self.botoes_info.items()):
            botao = ctk.CTkButton(
                frame_botoes,
                text="",
                image=info["imagem"],
                command=info["comando"],
                width=100,
                height=100,
                fg_color="transparent",
                hover_color="#cccccc",
                corner_radius=5
            )
            botao.grid(row=0, column=i, padx=10)

            # Bind de hover
            botao.bind("<Enter>", lambda e, n=nome: self.label_hover.configure(text=n))
            botao.bind("<Leave>", lambda e: self.label_hover.configure(text=""))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
