from utils.config import CustomButton, CustomComboBox, CustomEntry, CustomLabel
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry

class FormularioEntrada(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("LANÇAR ENTRADA")
        #self.geometry('800x800')
        self.resizable(False, False)
        self.grab_set()        # Torna modal
        self.focus_force()     # Foco na janela

        self.widgets = {}

        self._campos = [
            ("Data:", "date"),
            ("Booking de entrada:", "entry"),
            ("Fabrica:", "combo", ['PHILCO 1', 'PHILCO 2']),
            ("Armador:", "combo", ['ALIANÇA', 'LOGIN', 'MERCOSUL']),
            ("Transportador:", "combo", ['1', '2', '3', '4', '5']),
            ("Conteiner:", "entry"),
            ("Status:", "combo", ['VAZIO', 'CHEIO']),
        ]

        self._criar_campos()
        self._criar_botao()

    def _criar_campos(self):
        for i, campo in enumerate(self._campos):
            texto, tipo = campo[0], campo[1]
            opcoes = campo[2] if len(campo) > 2 else []

            label = ctk.CTkLabel(self, text=texto)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

            if tipo == "entry":
                entrada = CustomEntry(self)
            elif tipo == "combo":
                entrada = CustomComboBox(self, values=opcoes, state='readonly')
                entrada.set("")
            elif tipo == "date":
                entrada = DateEntry(self, locale='pt_br', background='darkblue', foreground='white', borderwidth=2)

            entrada.grid(row=i, column=1, columnspan=2, padx=10, pady=10, sticky='nswe')
            self.widgets[texto] = entrada

    def _criar_botao(self):
        botao = CustomButton(self, text="Lançar", command=self._lancar_dados)
        botao.grid(row=len(self._campos), column=1, padx=10, pady=10, sticky='nswe')

    def _lancar_dados(self):
        dados = {}
        try:
            # Coleta os dados
            for texto, widget in self.widgets.items():
                if isinstance(widget, CustomEntry) or isinstance(widget, CustomComboBox):
                    dados[texto] = widget.get().strip()
                elif isinstance(widget, DateEntry):
                    dados[texto] = widget.get_date().strftime('%Y-%m-%d')

            # Validação: verifica se algum campo está vazio
            for key, value in dados.items():
                if value == "":
                    raise ValueError(f'Campo "{key}" é obrigatório!')

            # Se tudo estiver ok
            self.resetar_campos()
            messagebox.showinfo('Sucesso', 'O veículo foi registrado com êxito!')

        except Exception as e:
            messagebox.showerror('Erro', str(e))


    def resetar_campos(self):
        for texto, widget in self.widgets.items():
            if isinstance(widget, CustomEntry):
                widget.delete(0, 'end')
            elif isinstance(widget, CustomComboBox):
                widget.set("")
            elif isinstance(widget, DateEntry):
                widget.set_date("01/01/2026")  # ou use uma data padrão, como datetime.today()
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = FormularioEntrada()
    app.mainloop()
