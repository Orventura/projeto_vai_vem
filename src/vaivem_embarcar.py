import customtkinter as ctk
from models.view_veiculos import tipos_veiculo, filtro, filtrar_veiculo
from utils.config import *
from utils.config import dados_para_input_vaivem as dados_para_input
import pandas as pd
from datetime import datetime
from tkinter import messagebox
from src.bd import BancoDeDados


class Entradas:
    def __init__(self, root):
        self.root = root
        self.e_frame = None
        self.img = RecursosVisuais()
        self.hoje = datetime.today().strftime('%Y-%m-%d')
        self.status_inicial = "Pendente"
        self.data = None
        self.status = None        
        self.sheet_produtos = None 
        #self.df_conteiners, self.df_carretas = tipos_veiculo()
        self.veiculo = 'Carreta'


    def _criar_janela_entradas(self, root):
        self.sheet_veiculos = None

        self.modo_atual = ctk.get_appearance_mode()

        # Frame principal
        self.e_frame = ctk.CTkFrame(root, width=783, height=450)
        if self.e_frame is not None:    
            self.frames = {}
            for name, cfg in subframes.items():
                self.frames[name] = ctk.CTkFrame(
                    self.e_frame,
                    fg_color='transparent',
                    width=cfg["width"],
                    height=cfg["height"],
                    #border_color='black',
                    #border_width=1
                )
                self.frames[name].place(x=cfg["x"], y=cfg["y"])

            self.frame_tabela = ctk.CTkFrame(self.frames['frame_4'],width=600, height=150, border_width=1)
            self.frame_tabela.place(x=90, y=82)
            # Widgets do frame_1

            self.atualizar_data_status()

            self.e_tipo_veiculo = ctk.CTkSegmentedButton(self.frames['frame_1'], values=["Conteiner", "Carreta"], command=lambda x: self.carregar_sheet())
            self.e_tipo_veiculo.place(x=33, y=10)
            self.e_tipo_veiculo.set('Carreta')

            self.e_id_veiculo = CustomEntry(self.frames['frame_1'], placeholder_text='Placa / Nº Conteiner', width=130)
            self.e_id_veiculo.place(x=30, y=40)
            self.e_id_veiculo.bind("<KeyRelease>", lambda c: self.filtrar_sheet())

            self.e_transportadora_original_text = 'Transportadora'
            self.e_transportadora = CustomLabel(self.frames['frame_1'],width=130, text=self.e_transportadora_original_text,anchor='w')
            self.e_transportadora.place(x=30, y=70)

            self.e_frota_original_text = 'Frota'
            self.e_frota = CustomLabel(self.frames['frame_1'],width=130, text=self.e_frota_original_text, anchor='w')
            self.e_frota.place(x=30, y=100)

            self.e_lacre = CustomEntry(self.frames['frame_1'], placeholder_text='Lacre', width=130)
            self.e_lacre.place(x=30, y=130)
            self.e_lacre.focus()

            # Widgets do frame_2
            self.e_nf = CustomEntry(self.frames['frame_2'], placeholder_text='Nota Fiscal', width=130)
            self.e_nf.place(x=30, y=10)

            self.e_romaneio = CustomEntry(self.frames['frame_2'], placeholder_text='Romaneio', width=130)
            self.e_romaneio.place(x=30, y=40)

            self.e_local = CustomEntry(self.frames['frame_2'], placeholder_text='Localização', width=130)
            self.e_local.place(x=30, y=70)

            # Widgets do frame_3

            self.e_orig = CustomComboBox(self.frames['frame_3'], values=['Galpão A1', 'Galpão A2', 'Galpão A3', 'Galpão A4', 'Galpão B1',])
            self.e_orig.set('Galpão Origem')
            self.e_orig.place(x=30, y=10)

            self.e_destino = CustomComboBox(self.frames['frame_3'], values=['Galpão A1', 'Galpão A2', 'Galpão A3', 'Galpão A4', 'Galpão B1'])
            self.e_destino.set('Galpão Destino')
            self.e_destino.place(x=30, y=40)

            self.e_turno = CustomComboBox(self.frames['frame_3'], values=['ADM1', 'ADM2', 'A', 'B', 'C']  )
            self.e_turno.set('Turno')
            self.e_turno.place(x=30, y=70)

            self.e_conferente = CustomEntry(self.frames['frame_3'], placeholder_text='Conferente', width=140)
            self.e_conferente.place(x=30, y=100)
            
            # Widgets do frame_4

            self.e_item = CustomEntry(self.frames['frame_4'], placeholder_text='* Item', width=80)
            self.e_item.place(x=90, y=10)

            self.e_desc = CustomEntry(self.frames['frame_4'], placeholder_text='* Descrição', width=250)
            self.e_desc.place(x=175, y=10)

            self.e_qtd = CustomEntry(self.frames['frame_4'], placeholder_text='* Qtd', width=50)
            self.e_qtd.place(x=432, y=10)

            self.e_motivo = CustomComboBox(self.frames['frame_4'], values=['Descasado', 'Bloqueio CQ','Retrabalho', 'Carga PDB'])
            self.e_motivo.set('* Motivo')
            self.e_motivo.place(x=490, y=10)
            #elf.e_motivo.focus()

            # Widgets do frame_5
            self.btn_salvar = CustomButton(self.frames['frame_5'], text="Salvar", width=100, command=lambda: self.salvar_dados())
            self.btn_salvar.place(x=590, y=5)

            self.botao_adict = CustomButton(
            self.frames['frame_4'],
            image=self.img.adicionar,
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="darkgray",
            command=lambda: self.adicionar_produto()
            )   
            self.botao_adict.place(x=650, y=10)

            self.e_justific = CustomEntry(self.frames['frame_4'], placeholder_text='Justificativas', width=538)
            self.e_justific.place(x=90, y=47)

            self.sheet_veiculos = CustomSheet(
                self.frame_tabela,
                set_all_heights_and_widths=True,
                header_align = "w",
                data=[],
                headers=[],
                show_row_index=True,
                show_x_scrollbar=True,
                show_y_scrollbar=True,
                width=765,
                height=130
            )
            self.sheet_veiculos.enable_bindings()
        
            self.carregar_sheet()


            self.sheet_veiculos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')

            # alteração4: bind para preencher_dados_transporte Transportadora
            self.sheet_veiculos.extra_bindings([
                ("row_select", self.preencher_dados_transporte)  # evento
            ])

            #self.e_tipo_veiculo.configure(command=lambda event: self.carregar_sheet())

            return self.e_frame  # retorna o frame criado

    def atualizar_data_status(self):
        self.dt_atual = datetime.today().strftime('%Y-%m-%d')
        self.data = ctk.StringVar(master=self.frames['frame_1'], value=self.dt_atual)
        self.status = ctk.StringVar(master=self.frames['frame_1'], value=self.status_inicial)


    def carregar_sheet(self):
        # Se o sheet foi destruído, recria
        
        tipo = self.e_tipo_veiculo.get().strip()
        if self.sheet_veiculos is not None:
            self.df_conteiners, self.df_carretas = tipos_veiculo()
            self.df_veiculo = self.df_carretas if tipo == "Carreta" else self.df_conteiners


            self.sheet_veiculos = CustomSheet(
                self.frame_tabela,
                width=765,
                height=142,
                
                headers=list(self.df_veiculo.columns),
                set_all_heights_and_widths=True,
                show_row_index=True,
                show_x_scrollbar=True,
                show_y_scrollbar=True,
            )
            self.sheet_veiculos.set_sheet_data(self.df_veiculo.values.tolist(), reset_col_positions=True, reset_row_positions=True),

            self.sheet_veiculos.enable_bindings()
            self.sheet_veiculos.extra_bindings([
                ("row_select", self.preencher_dados_transporte)
            ])
        self.sheet_veiculos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')
        self.sheet_veiculos.place(x=3, y=3)


    def filtrar_sheet(self, event=None):
        """Filtra a sheet com a entrada do campo Placa/Conteiner"""
        df = filtrar_veiculo(pesquisa=self.e_id_veiculo.get(), tipo_veiculo=self.e_tipo_veiculo.get())
        self.sheet_veiculos.set_sheet_data(df.values.tolist(), reset_col_positions=True, reset_row_positions=True),
        self.sheet_veiculos.set_header_data(list(df.columns))
        print(df)
        return df
    
    def mostrar_sheet_produtos(self):
        if self.sheet_produtos:
            self.sheet_produtos.destroy()
            self.sheet_produtos = None

        if self.sheet_produtos == None:
            self.esconder_sheet_veiculos()
            self.sheet_produtos = CustomSheet(
            self.frame_tabela,
            data=[],                      # começa vazio
            headers=["ITEM", "SEGMENTO", "DESC", "QTD", "MOTIVO", "JUSTIF."],
            cell_auto_resize_enabled=True,
            header_align = "w",
            show_row_index=True,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            width=565,
            height=140
            )
        self.sheet_produtos.enable_bindings()
        self.sheet_produtos.place(x=5, y=5)
        self.sheet_produtos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')
        self.sheet_produtos.set_all_column_widths()
        self.esconder_sheet_veiculos()

    def pegar_dados_sheet_produtos(self):
        """Retorna os dados da sheet_produtos como lista de listas."""
        # get_sheet_data retorna lista de listas (cada linha)
        lista_produtos = self.sheet_produtos.get_sheet_data()
        print('debug lista produtos', lista_produtos)

        dicionario = {}
        for nome_attr, widget in self.__dict__.items():
            if isinstance(widget, (ctk.CTkEntry, ctk.CTkComboBox)):
                dicionario[nome_attr] = widget.get()

            elif isinstance(widget, ctk.CTkLabel):
                dicionario[nome_attr] = widget.cget("text")

            elif isinstance(widget, ctk.CTkSegmentedButton):
                dicionario[nome_attr] = widget.get()

            # Adiciona suporte a StringVar, IntVar, DoubleVar, BooleanVar
            elif isinstance(widget, (ctk.StringVar, ctk.IntVar, ctk.DoubleVar, ctk.BooleanVar)):
                dicionario[nome_attr] = widget.get()

            # Se for algum widget customizado que possua .get()
            elif hasattr(widget, "get"):
                try:
                    dicionario[nome_attr] = widget.get()
                except Exception:
                    pass
        print(list(dicionario.values()))
        return lista_produtos, list(dicionario.values())

    def valida_entradas(self, lista):
        """Valida os dados antes de dar entrada no banco de dados"""

        # Mapeamento de índices -> nomes dos campos
        valores_padrao = {
            3: 'Placa/Conteiner',
            4: "Transportadora",
            5: "Frota",
            6: 'Lacre',
            7: 'NF',
            8: 'Romaneio',
            9: 'Localização', 
            10: "Galpão Origem",
            11: "Galpão Destino",
            12: "Turno",
            13: "Conferente"
        }

        try:
            for i, dado in enumerate(lista):
                nome_campo = valores_padrao.get(i, f"Campo {i}")

                # 🔴 Validação de campos obrigatórios (Entry)
                if i in [3, 6, 7, 8, 9, 13]:
                    if not dado or str(dado).strip() == "":
                        messagebox.showerror("Erro", f"Preencha o campo obrigatório: {nome_campo}")
                        raise ValueError(f"Campo obrigatório '{nome_campo}' não preenchido (índice {i})")

                # 🟡 Validação de Labels com valor padrão
                elif i in [4, 5]:
                    if dado == valores_padrao[i]:
                        messagebox.showerror("Erro", f"Selecione um valor válido para o campo '{nome_campo}'")
                        raise ValueError(f"Campo '{nome_campo}' está com valor padrão inválido (índice {i})")

                # 🔵 Validação de Combobox com valor padrão
                elif i in [10, 11, 12]:
                    if dado == valores_padrao[i]:
                        messagebox.showerror("Erro", f"Selecione uma opção válida para o campo '{nome_campo}'")
                        raise ValueError(f"Combobox '{nome_campo}' não selecionado (índice {i})")

            return True  # ✅ Validação concluída com sucesso

        except Exception as e:
            print(f"[Validação de Entradas] Erro: {e}")
            return False
    
    def atualiza_data_frames(self):
        conteiners, carretas = tipos_veiculo()
        return conteiners, carretas


    def adicionar_produto(self):
        """Adiciona os produtos dos widgets, na lista Sheet com botão +"""
        # coleta valores
        item = self.e_item.get().strip().lstrip("0")
        segmento = self.atribuir_segmento().upper()
        desc = self.e_desc.get().strip()
        qtd = self.e_qtd.get().strip()
        motivo = self.e_motivo.get().strip()
        justific = self.e_justific.get().strip()


        if not item or not desc or not qtd or motivo == '* Motivo':
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return
        if motivo == 'Descasado' and justific == '':
            messagebox.showwarning("Atenção", "Justificativa é obrigatória para motivo 'Descasado'.")
            return

        row = [item, segmento, desc, qtd, motivo, justific]

        if self.sheet_produtos is None:
            print("sheet_produtos não encontrada. Crie-a antes.")
            return

        inserted = False
        try:
            # tentativa preferida: kwargs (valores podem variar entre versões)
            self.sheet_produtos.insert_row(values=row, idx=0)
            inserted = True
        except TypeError:
            try:
                # assinatura alternativa: insert_row(row, idx)
                self.sheet_produtos.insert_row(row, 0)
                inserted = True
            except Exception:
                inserted = False
        except Exception:
            inserted = False

        if not inserted:
            # fallback robusto: ler os dados atuais, inserir no início e reescrever todo o dataset
            try:
                try:
                    data = self.sheet_produtos.get_sheet_data(return_copy=True)
                except TypeError:
                    data = self.sheet_produtos.get_sheet_data()

                # data deve ser uma lista de listas
                if not isinstance(data, list):
                    data = list(data)

                data.insert(0, row)
                # atualiza a sheet (mantendo cabeçalhos)
                headers = self.sheet_produtos.headers() if callable(getattr(self.sheet_produtos, "headers", None)) else ["ITEM", "SEGM.", "DESC", "QTD", "MOTIVO", "JUSTIF."]
                self.sheet_produtos.set_sheet_data(data, reset_col_positions=True, reset_row_positions=True)
                # se for necessário, reatribuir headers


                data.insert(0, row)
                # atualiza a sheet (mantendo cabeçalhos)
                headers = self.sheet_produtos.headers() if callable(getattr(self.sheet_produtos, "headers", None)) else ["ITEM", "SEGM.", "DESC", "QTD", "MOTIVO", "JUSTIF."]
                self.sheet_veiculos.set_sheet_data(data.values.tolist(),
                                           reset_col_positions=True,
                                           reset_row_positions=True)
                # se for necessário, reatribuir headers
                try:
                    self.sheet_produtos.headers(headers)
                except Exception:
                    pass
            except Exception as e:
                print("Falha ao inserir na sheet_produtos:", e)
                return

        # limpa campos após inserir
        try:
            self.e_item.delete(0, "end")
            self.e_desc.delete(0, "end")
            self.e_qtd.delete(0, "end")
            self.e_justific.delete(0, "end")
            self.sheet_produtos.set_all_column_widths()

            # se e_motivo for combo, reset:
            try:
                self.e_motivo.set("* Motivo")
            except Exception:
                pass
            self.e_item.focus()
        except Exception:
            pass

    def limpar_id_veiculos(self):
        self.e_id_veiculo.delete(0, "end")
        self.e_frota.configure(text='Frota')
        self.e_transportadora.configure(text='Transportadora')  

    def limpar_sheet(self, sheet):
        """
        Remove todas as linhas da Sheet,
        mantendo apenas os cabeçalhos.
        """
        if sheet and sheet.winfo_exists():
            total_linhas = sheet.get_total_rows()
            if total_linhas > 0:
                sheet.del_rows(range(total_linhas))

    def preencher_dados_transporte(self, event=None):
        """Preenche os campos de Transportadora, Frota e ID Veículo com base na linha selecionada na sheet_veiculos."""
        tipo = self.e_tipo_veiculo.get().strip()
        self.atualizar_data_status()
        try:
            linha = self.sheet_veiculos.get_currently_selected()[0]  # índice da linha selecionada
            dados_linha = self.sheet_veiculos.get_row_data(linha)   # captura todos os valores da linha

            if tipo == 'Conteiner':
                id_veiculo, transportadora = dados_linha
                frota = 'N/A'
            elif tipo == 'Carreta':
                frota, transportadora, id_veiculo = dados_linha

            self.e_transportadora.configure(text=transportadora)
            self.e_id_veiculo.delete(0, "end")
            self.e_id_veiculo.insert(0, str(id_veiculo))
            self.e_frota.configure(text=frota)
            self.esconder_sheet_veiculos()
            self.mostrar_sheet_produtos()

        except Exception as e:
            print("Erro ao preencher_dados_transporte Transportadora:", e)

    def atribuir_segmento(self):
        codigo = str(self.e_item.get())
        
        '''Atribui o valor do segmento com base no código do item.'''
        if not codigo:
            messagebox.showerror('Erro!', 'Digite o código do produta')
            return
        else:
            item = codigo.strip().strip('0')
            item.strip()
            if item.startswith('99'):
                return 'TV'
            elif item.startswith('9666'):
                return 'ARCON'
            elif item.startswith('9665'):
                return 'ARCON'
            elif item.startswith('9825'):
                return 'CELLULAR'
            elif item.startswith('93'):
                return 'VENTILADOR'
            elif item.startswith('9605'):
                return 'FMO'
            else:
                return 'OUTROS'

    def salvar_dados(self):

        self.atualizar_data_status()
        dados_produto, dados_veiculo = self.pegar_dados_sheet_produtos()#Retorna lista de listas da Sheet produtos, dados dos demais widgets
        
        if self.valida_entradas(dados_veiculo) == True:

            if dados_produto:
                try:    
                    with BancoDeDados() as bd:
                        id2 = bd.gerar_id2()
                        print(id2)

                        for lista in dados_produto:    
                            entradas = {
                                    'id_2': id2,
                                    'data1': dados_veiculo[0],
                                    'status': dados_veiculo[1].strip().upper(),
                                    'tipo_veiculo': dados_veiculo[2].strip().upper(),
                                    'placa_cntr': dados_veiculo[3].strip().upper(),
                                    'transportadora': dados_veiculo[4].strip().upper(),
                                    'frota': dados_veiculo[5].strip().upper(),
                                    'lacre': dados_veiculo[6].strip().upper(),
                                    'nf': dados_veiculo[7].strip().upper(),
                                    'romaneio1': dados_veiculo[8].strip().upper(),
                                    'localizacao': dados_veiculo[9].strip().upper(),
                                    'origem': dados_veiculo[10].strip().upper(),
                                    'destino': dados_veiculo[11].strip().upper(),
                                    'turno': dados_veiculo[12].strip().upper(),
                                    'conferente1': dados_veiculo[13].strip().upper(),
                                    'item': lista[0].strip().lstrip('0').upper(), 
                                    'segmento': lista[1].strip().upper(),
                                    'desc':lista[2].strip().upper(),
                                    'quantidade': lista[3].strip().upper(), 
                                    'motivo': lista[4].strip().upper(), 
                                    'justificativa': lista[5].strip().upper(), 
                                    }
                            
                        messagebox.showinfo(
                            "📦 Operação Concluída",
                            "🚚 Todos os dados foram gravados com sucesso no sistema!"
                        )
                        self.limpar_widgets()
                        self.e_turno.set('Turno')
                        self.limpar_sheet(self.sheet_produtos)

                        bd.inserir_dado(**entradas)
                except Exception as e:
                    return messagebox.showerror("❌ Erro ao salvar", f"Ocorreu um problema: \n{e}")

    def esconder_sheet_veiculos(self):
        self.sheet_veiculos.place_forget()

    def limpar_widgets(self, widget=None):
        """
        Percorre recursivamente todos os widgets filhos a partir do 'widget' (ou self.e_frame)
        e limpa Entry, Label e ComboBox, restaurando valores padrão ou placeholder.
        """
        if widget is None:
            widget = self.e_frame  # ponto de partida: frame principal

        # Verifica se é um dos widgets que devem ser limpos
        if isinstance(widget, (CustomEntry, ctk.CTkEntry)):
            # Limpa conteúdo e restaura placeholder
            try:
                placeholder = getattr(widget, "placeholder_text", "")
                widget.delete(0, "end")
                if placeholder:
                    widget.insert(0, placeholder)
            except Exception:
                pass

        elif isinstance(widget, (CustomComboBox, ctk.CTkComboBox)):
            # Restaura o texto padrão se existir
            default = getattr(widget, "default_value", None) or widget.get()
            try:
                widget.set(default if default else "")
            except Exception:
                pass

        elif isinstance(widget, (CustomLabel, ctk.CTkLabel)):
            # Se quiser restaurar para vazio ou texto original
            original = self.e_frota_original_text if widget == self.e_frota else self.e_transportadora_original_text
            widget.configure(text=original if original else "")

        # Percorre filhos recursivamente
        for child in widget.winfo_children():
            self.limpar_widgets(child)

    def esconder(self):
        """Esconde o frame de entradas, se existir. Caso contrário, mostra-o."""
        if self.e_frame is not None:
            self.e_frame.destroy()
            self.e_frame = None
        else:
            self.mostrar()

    def mostrar(self):
        '''Mostra o frame de entradas.'''
        self._criar_janela_entradas(self.root)
        self.e_frame.place(x=210, y=5)

if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry('800x460')
    janela = Entradas(root)
    janela.mostrar()
    root.mainloop()