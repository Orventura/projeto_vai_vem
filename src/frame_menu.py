import customtkinter as ctk
from utils.config import CustomButton, RecursosVisuais
from getpass import getuser
from src.modal_cab_config import Listas
from src.cabotagem import Cabotagem


class FrameMenu(ctk.CTkFrame):
    def __init__(self, master, controller):
        """
        Frame lateral esquerdo com sistema de navegação tipo carrossel.
        Mostra apenas seções liberadas de acordo com as permissões do usuário.
        """
        super().__init__(master, width=200, height=450)
        self.place(x=5, y=5)
        self.controller = controller
        self.img = RecursosVisuais()
        self.user = getuser()
        with Listas() as auth:
            self.permissao_total = auth.lista_user_auth()



        # --- Listas de seções ---
        self.secoes_cabotagem = [
            {
                "nome": "Cabotagem",
                "imagem": self.img.cabotagem,
                "acao": self.controller.abrir_cabotagem
            }
        ]

        self.secoes_outros = [
            {"nome": "Vai Vem - Embarcar", "imagem": self.img.emb_vaivem,
             "acao": self.controller.abrir_entradas},
            {"nome": "Vai Vem - Receber", "imagem": self.img.rec_vaivem,
             "acao": self.controller.abrir_recebimento},
            {"nome": "Rodoviário", "imagem": self.img.rodoviario,
             "acao": lambda: print('Rodoviário ainda não implementado')},
        ]

        # --- Combina as listas com base na permissão ---
        if self.user in self.permissao_total:
            self.secoes = self.secoes_cabotagem + self.secoes_outros
        else:
            self.secoes = self.secoes_cabotagem
        self.index_atual = 0  # começa pelo primeiro item

        # --- Construção da interface ---
        self._criar_widgets()

        # --- Exibe o primeiro item e abre sua janela ---
        self._atualizar_exibicao()

    # -------------------------------------------------------------
    # BLOCO 1: Criação dos widgets base
    # -------------------------------------------------------------
    def _criar_widgets(self):
        """Cria os componentes fixos do menu (botões e áreas de exibição)."""
        # Título do menu
        self.label_titulo = ctk.CTkLabel(self, text="Menu", font=("Roboto", 18, "bold"))
        self.label_titulo.place(x=70, y=15)

        # Botão voltar "<"
        self.btn_prev = CustomButton(
            self,
            text="<",
            width=30,
            height=30,
            command=self._anterior
        )
        self.btn_prev.place(x=20, y=60)

        # Botão avançar ">"
        self.btn_next = CustomButton(
            self,
            text=">",
            width=30,
            height=30,
            command=self._proximo
        )
        self.btn_next.place(x=140, y=60)


        # Label com nome da seção
        self.label_secao = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.label_secao.place(x=60, y=120)

        # Imagem ilustrativa da seção
        self.label_imagem = ctk.CTkLabel(self, text="")
        self.label_imagem.place(x=50, y=150)

    # -------------------------------------------------------------
    # BLOCO 2: Lógica de navegação
    # -------------------------------------------------------------
    def _proximo(self):
        """Avança para o próximo item (com loop infinito) e abre a janela correspondente."""
        self.index_atual = (self.index_atual + 1) % len(self.secoes)
        self._atualizar_exibicao()

    def _anterior(self):
        """Volta para o item anterior (com loop infinito) e abre a janela correspondente."""
        self.index_atual = (self.index_atual - 1) % len(self.secoes)
        self._atualizar_exibicao()

    # -------------------------------------------------------------
    # BLOCO 3: Atualização de exibição
    # -------------------------------------------------------------
    def _atualizar_exibicao(self):
        """Atualiza o label, imagem e abre a janela da seção atual."""
        secao = self.secoes[self.index_atual]

        # Atualiza texto e imagem
        self.label_secao.configure(text=secao["nome"])
        self.label_imagem.configure(image=secao["imagem"])

        # Abre a janela associada automaticamente
        if secao["acao"]:
            secao["acao"]()
