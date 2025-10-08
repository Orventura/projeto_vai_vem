import customtkinter as ctk
from tkinter import messagebox
import sqlite3 as lite
from utils.config import CustomButton, CustomEntry, CustomLabel, CustomComboBox
from models.views_cab_config import Listas

class Liberacao(ctk.CTkToplevel):
    """Cria um modal para liberar os veículos,
    recebe o master_widget, lista dos dados selecionados, indice dos
    dados selecionados na sheet prinsipal, caminho do banco de dados."""
    def __init__(self, master, lista: list, id, bd_path):

        super().__init__(master)
        self.title("REGISTRAR LIBERAÇÃO")
        #self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.id = id
        self.lista_dados = lista
        self.conteiner = lista[1]
        self.bd_path = bd_path
        self.dicionario_listas = self._carregar_listas()
        self.lista_fabrica = self.dicionario_listas['fabrica']
        self.lista_booking = self.dicionario_listas['booking']

        #self.on_close = on_close
        

        self.widgets = {}

        self.frame_principal = ctk.CTkFrame(self, width=800, height=500, fg_color='transparent')
        self.frame_principal.pack(fill='both', side='bottom', padx=5, pady=5, expand=True)
        self.frame_principal.pack_propagate(True)

        self.frame_cabecalho = ctk.CTkFrame(self, width=800, height=100,)
        self.frame_cabecalho.pack(fill=None, side='top', padx=5, pady=(5, 0), expand=True,)
        self.label_cabecalho = ctk.CTkLabel(self.frame_cabecalho, text_color='gray',
                                            text="CONTEINER     -      ARMADOR      -      TRANSPORTADORA",
                                            font=('arial', 20, 'bold')
                                            
                                            )
        self.label_cabecalho.pack(pady= 5, ipadx=10)
        self.label_cabecalho2 = ctk.CTkLabel(self.frame_cabecalho, text_color='gray',
                                            text="CONTEINER     -      ARMADOR      -      TRANSPORTADORA",
                                            font=('arial', 20, 'normal')
                                            )

        self.label_cabecalho2.pack(pady= 5, ipadx=10, expand=True, fill='both')

        self.btn_fechar = CustomButton(self.frame_principal, text="fechar", command=lambda: messagebox.showerror('salvar','salvando os dados'))
        self.btn_fechar.pack(side='bottom', expand=False, fill="y")

        self.frame_esq = ctk.CTkFrame(self, width=150, height=200,)
        self.frame_esq.pack(fill='x', side='left', padx=5, pady=(5, 0), expand=True)

        self.e_nf = CustomEntry(self.frame_esq, placeholder_text='Nota Fiscal')
        self.e_nf.pack(pady=(5,0))

        self.e_valor_nf = CustomEntry(self.frame_esq, placeholder_text='Valor da Carga')
        self.e_valor_nf.pack(pady=(5,0))

        self.e_pesob = CustomEntry(self.frame_esq, placeholder_text='Peso Bruto')
        self.e_pesob.pack(pady=(5,0))

        self.e_pesol = CustomEntry(self.frame_esq, placeholder_text='Peso Líquido')
        self.e_pesol.pack(pady=(5,5))

        self.frame_cent = ctk.CTkFrame(self, width=150, height=200,)
        self.frame_cent.pack(fill='x', side='left', padx=5, pady=(5, 0), expand=True)

        self.e_lacre1 = CustomEntry(self.frame_cent, placeholder_text='Lacre 1')
        self.e_lacre1.pack(pady=(5,0))

        self.e_lacre2 = CustomEntry(self.frame_cent, placeholder_text='Lacre 2')
        self.e_lacre2.pack(pady=(5,0))

        self.cbbooking = CustomComboBox(self.frame_cent, values=self.lista_booking)
        self.cbbooking.pack(pady=(5,0))
        self.cbbooking.set("Booking")

        self.cb_tp_carga = CustomComboBox(self.frame_cent, values=['CLIENTE', 'AG'])
        self.cb_tp_carga.pack(pady=(5,5))
        self.cb_tp_carga.set("Carga")


        self.frame_dir = ctk.CTkFrame(self, width=150, height=200,)
        self.frame_dir.pack(fill='both', side='right', padx=5, pady=(5, 0), expand=True)

        self.e_isca1 = CustomEntry(self.frame_dir, placeholder_text='Isca 1')
        self.e_isca1.pack(pady=(5,0))

        self.e_isca2 = CustomEntry(self.frame_dir, placeholder_text='Isca 2')
        self.e_isca2.pack(pady=(5,0))

        self.cb_tp_fabrica = CustomComboBox(self.frame_dir, values=self.lista_fabrica)
        self.cb_tp_fabrica.pack(pady=(5,0))
        self.cb_tp_fabrica.set("Fábrica")

        self.e_obs = CustomEntry(self.frame_dir, placeholder_text='Observação')
        self.e_obs.pack(pady=(5,5))

    def _carregar_listas(self):
        """Retorna dicionario, para carregar todas as listas de combobox"""
        with Listas() as users:
            dicionario = users.dicionario_de_listas()
            return dicionario

if __name__ =="__main__":
    root = ctk.CTk()
    root.geometry('250x250')

    def abrir_modal():
        modal = Liberacao(root, '543', r'data\database_cabotagem.db', ['LIBERADO'], ['BK1', 'BK2', 'BK3'], ['AG', 'CLIENTE'], fechar)
        root.wait_window(modal)
        print("Valores salvos:")
        #odal.mainloop()

    def fechar():
        root.destroy()


    btn = ctk.CTkButton(root, command=abrir_modal, text='Abrir Modal')
    btn.grid()

    root.mainloop()