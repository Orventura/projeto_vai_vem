import customtkinter as ctk
from views.view_veiculos import tipos_veiculo, filtro
from utils.config import *
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

    def _criar_janela_entradas(self, root):

        self.modo_atual = ctk.get_appearance_mode()

        # Frame principal
        self.e_frame = ctk.CTkFrame(root, width=600, height=450)
        if self.e_frame is not None:    
            self.frames = {}
            for name, cfg in subframes.items():
                self.frames[name] = ctk.CTkFrame(
                    self.e_frame,
                    #fg_color='white',
                    width=cfg["width"],
                    height=cfg["height"],
                    #border_color='black',
                    border_width=1
                )
                self.frames[name].place(x=cfg["x"], y=cfg["y"])

            # Widgets do frame_1

            self.atualizar_data_status()



            self.e_tipo_veiculo = ctk.CTkSegmentedButton(self.frames['frame_1'], values=["Conteiner", "Carreta"], command=lambda x: self.carregar_sheet())
            self.e_tipo_veiculo.place(x=33, y=10)
            self.e_tipo_veiculo.set('Carreta')

            self.e_id_veiculo = CustomEntry(self.frames['frame_1'], placeholder_text='Placa / Nº Conteiner', width=130)
            self.e_id_veiculo.place(x=30, y=40)
            self.e_id_veiculo.bind("<KeyRelease>", self.filtrar_sheet)

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

            self.eromaneio = CustomEntry(self.frames['frame_2'], placeholder_text='Romaneio', width=130)
            self.eromaneio.place(x=30, y=40)

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

            self.frame_tabela = ctk.CTkFrame(self.frames['frame_4'],width=580, height=150, border_width=1)
            self.frame_tabela.place(x=10, y=82)

            self.e_item = CustomEntry(self.frames['frame_4'], placeholder_text='* Item', width=80)
            self.e_item.place(x=10, y=10)

            self.e_desc = CustomEntry(self.frames['frame_4'], placeholder_text='* Descrição', width=250)
            self.e_desc.place(x=95, y=10)

            self.e_qtd = CustomEntry(self.frames['frame_4'], placeholder_text='* Qtd', width=50)
            self.e_qtd.place(x=352, y=10)

            self.e_motivo = CustomComboBox(self.frames['frame_4'], values=['Descasado', 'Bloqueio CQ','Retrabalho', 'Carga PDB'])
            self.e_motivo.set('* Motivo')
            self.e_motivo.place(x=410, y=10)
            #elf.e_motivo.focus()

            # Widgets do frame_5
            self.btn_salvar = ctk.CTkButton(self.frames['frame_5'], text="Salvar", width=100, command=lambda: self.salvar_dados())
            self.btn_salvar.place(x=490, y=5)

            self.botao_adict = ctk.CTkButton(
            self.frames['frame_4'],
            image=self.img.adict,
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="darkgray",
            command=lambda: self.adicionar_produto()
            )   
            self.botao_adict.place(x=556, y=10)

            self.botao_subtract = ctk.CTkButton(
            self.frames['frame_4'], 
            image=self.img.subtract,
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="darkgray",
            #command=lambda: self._alterar_tema()
            )
            self.botao_subtract.place(x=556, y=47)

            self.e_justific = CustomEntry(self.frames['frame_4'], placeholder_text='Justificativas', width=538)
            self.e_justific.place(x=10, y=47)

            self.sheet_veiculos = CustomSheet(
                self.frame_tabela,
                data=[],
                headers=[],
                set_all_heights_and_widths=True,
                header_align = "w",
                show_row_index=True,
                show_x_scrollbar=True,
                show_y_scrollbar=True,
                width=565,
                height=140
            )
            self.sheet_veiculos.enable_bindings()

            self.carregar_sheet()
            self.sheet_veiculos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')

            # alteração4: bind para preencher Transportadora
            self.sheet_veiculos.extra_bindings([
                ("row_select", self.preencher)  # evento
            ])

            self.e_tipo_veiculo.configure(command=lambda event: self.carregar_sheet())

            return self.e_frame  # retorna o frame criado

    def atualizar_data_status(self):
        self.dt_atual = datetime.today().strftime('%Y-%m-%d')
        self.data = ctk.StringVar(master=self.frames['frame_1'], value=self.dt_atual)
        self.status = ctk.StringVar(master=self.frames['frame_1'], value=self.status_inicial)

    def filtrar_sheet(self, event=None):
        texto = self.e_id_veiculo.get().strip()
        tipo = self.e_tipo_veiculo.get().strip()

        # Carrega todo o DataFrame do banco
        df = filtro("", tipo)    # Passamos "" para não filtrar no SQL

        # Se há texto, filtra localmente no pandas
        if texto:
            mask = df.apply(lambda col: col.astype(str).str.contains(texto, case=False, na=False))
            df = df[mask.any(axis=1)]

        # Atualiza o sheet
        self.sheet_veiculos.set_sheet_data(df.values.tolist(),
                                           reset_col_positions=True,
                                           reset_row_positions=True)
        self.sheet_veiculos.headers(list(df.columns))
        self.sheet_veiculos.deselect("all")

    def carregar_sheet(self):
        # Se o sheet foi destruído, recria
        if self.sheet_veiculos == None:
            self.atualizar_data_status()
            self.sheet_veiculos = CustomSheet(
                self.frame_tabela,
                data=[],
                headers=[],
                set_all_heights_and_widths=True,
                show_row_index=True,
                show_x_scrollbar=True,
                show_y_scrollbar=True,
                width=525,
                height=113
            )
            self.sheet_veiculos.enable_bindings()
            self.sheet_veiculos.extra_bindings([
                ("row_select", self.preencher)
            ])
        self.sheet_veiculos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')


        self.sheet_veiculos.deselect("all")
        self.limpar_id_veiculos()

        conteiners, carretas = tipos_veiculo()
        tipo = self.e_tipo_veiculo.get()
        self.df_veiculo = carretas if tipo == "Carreta" else conteiners

        self.sheet_veiculos.set_sheet_data(self.df_veiculo.values.tolist(), reset_col_positions=True, reset_row_positions=True)
        self.sheet_veiculos.headers(list(self.df_veiculo.columns))
        self.sheet_veiculos.place(x=10, y=5)
        self.sheet_veiculos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')
        

        if self.sheet_produtos == None:
            pass
        else:
            self.limpar_sheet(self.sheet_produtos)
            self.sheet_produtos.destroy()
            self.sheet_produtos = None
    
    def mostrar_sheet_produtos(self):
        if self.sheet_produtos == None:
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
        self.sheet_produtos.place(x=10, y=5)
        self.sheet_produtos.change_theme('dark' if self.modo_atual == 'Dark' else 'light_blue')

    def pegar_dados_sheet_produtos(self):
        """Retorna os dados da sheet_produtos como lista de listas."""
        if self.sheet_produtos is None:
            return []  # Nenhuma sheet criada ainda
        # get_sheet_data retorna lista de listas (cada linha)
        return self.sheet_produtos.get_sheet_data()

    def adicionar_produto(self):
        # coleta valores
        item = self.e_item.get().strip()
        segmento = self.atribuir_segmento([item]).capitalize()
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

    def preencher(self, event=None):
        """Preenche os campos de Transportadora, Frota e ID Veículo com base na linha selecionada na sheet_veiculos."""
        tipo = self.e_tipo_veiculo.get().strip()
        self.atualizar_data_status()
        try:
            linha = self.sheet_veiculos.get_currently_selected()[0]  # índice da linha selecionada
            dados_linha = self.sheet_veiculos.get_row_data(linha)   # captura todos os valores da linha

            if tipo == 'Conteiner':
                id_veiculo, transportadora = dados_linha
                frota = 'N/A'  # Frota não se aplica a conteiner
                self.e_frota.configure(text='N/A')
            if tipo == 'Carreta':
                frota, transportadora, id_veiculo, = dados_linha

            self.e_transportadora.configure(text=transportadora)
            self.e_id_veiculo.delete(0, "end")
            self.e_id_veiculo.insert(0, id_veiculo)
            self.e_frota.configure(text=frota)
            self.esconder_sheet_veiculos()
            self.mostrar_sheet_produtos()

        except Exception as e:
            print("Erro ao preencher Transportadora:", e)

    def coletar_valores(self):
        """
        Retorna uma lista de listas.
        Cada linha interna é: [dados da sheet] + [dados dos widgets da tela]
        """                
                    
        # Coleta os dados da sheet
        produtos = []
        if self.sheet_produtos is not None:
            produtos = self.pegar_dados_sheet_produtos()
            produtos = [linha for linha in produtos if any(str(campo).strip() for campo in linha)]

        # Coleta valores dos widgets
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

        # Filtra os widgets que não queremos duplicar para cada produto
        lista_dados = [
            v for k, v in dicionario.items()
            if k not in ('e_qtd', 'e_item', 'e_desc', 'e_tipo_veiculo', 'e_motivo', 'e_justific')
        ]
        print(f'PRINT PARA DEBUGAR dicionario {dicionario}')
        # Monta lista final: cada linha é [produto ...] + [outros dados ...]
        valores_finais = []
        for produto in produtos:
            valores_finais.append(produto + lista_dados)
        return valores_finais

    def atribuir_segmento(self,lista):
        '''Atribui o valor do segmento com base no código do item.'''
        for i, item in enumerate(lista):
            if i != 0:
                return
            else:
                item = item.strip().strip('0')
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
        """
        Salva os dados do sheet de produtos no banco de dados.
        """

        try:
            # 1️⃣ Verifica se há produtos no sheet
            if len(self.pegar_dados_sheet_produtos()) == 0:
                messagebox.showwarning("Atenção", "Adicione ao menos um produto antes de salvar.")
                return

            # 2️⃣ Coleta os valores dos widgets
            self.dados = self.coletar_valores()
            print(f'PRINT PARA DEBUGAR "valores dos widgets"{self.dados}')

            # 5️⃣ Converte os dados para lista de dicionários
            self.dados_finais = [
                (
                    dados_para_input(linha)['romaneio'],
                    dados_para_input(linha)['segmento'],
                    dados_para_input(linha)['data'],
                    dados_para_input(linha)['transportadora'],
                    dados_para_input(linha)['placa_num_conteiner'],
                    dados_para_input(linha)['frota'],
                    dados_para_input(linha)['lacre'],
                    dados_para_input(linha)['galpao_origem'],
                    dados_para_input(linha)['galpao_destino'],
                    dados_para_input(linha)['turno'],
                    dados_para_input(linha)['conferente'],
                    dados_para_input(linha)['localizacao'],
                    dados_para_input(linha)['item'],
                    dados_para_input(linha)['descricao'],
                    dados_para_input(linha)['quantidade'],
                    dados_para_input(linha)['nf'],
                    dados_para_input(linha)['motivo'],
                    dados_para_input(linha)['justificativa'],
                    dados_para_input(linha)['status'],
                    dados_para_input(linha)['conferente2'],
                    dados_para_input(linha)['romaneio2'],
                    dados_para_input(linha)['data2'],
                    dados_para_input(linha)['end_user'],
                    dados_para_input(linha)['final_hour'],
                    dados_para_input(linha)['pc']
                )
                for linha in self.dados
            ]

            # 4️⃣ Limpa a interface
            if self.sheet_produtos:
                self.sheet_produtos.destroy()
                self.sheet_produtos = None
            self.esconder()
            self.mostrar()


            print(f'Debug - Dados finais: {self.dados_finais}')

            # 6️⃣ Salva no banco
            try:
                with BancoDeDados() as bd:
                    id2_embarque = bd.gerar_id2()
                    for registro in self.dados_finais:
                        bd.inserir_dado((id2_embarque,) + registro)

                messagebox.showinfo(
                    "📦 Operação Concluída",
                    "🚚 Todos os veículos foram gravados com sucesso no sistema!"
                )
            except Exception as e:
                messagebox.showerror("❌ Erro ao salvar", f"Ocorreu um problema: \n{e}")
                return
        except Exception as e:
            return print(f'erro:{e}')
        
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

