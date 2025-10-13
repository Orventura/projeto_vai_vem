from src.bd_cabotagem import Database
from utils.config import Conversao
from models.model_cab_config import Listas
from tkinter import messagebox
from src.bd_cabotagem import Database
from datetime import datetime, timedelta

class CtrlLiberar:
    """Classe responsável por controlar o modal de liberação de veículos"""
    def __init__(self, modal_liberar, id_bd, user):
        self.modal_liberar = modal_liberar
        self.id = int(id_bd)
        self.user = user
        self.convert = Conversao() # Converte str para float e float para str
        with Listas()as pgr:
            self.lista_ag, self.lista_cliente =  pgr.lista_pgr()
        self.dados =  {
            "NOTA_FISCAL": modal_liberar.e_nf,
            "VALOR": modal_liberar.e_valor_nf,
            "PESO_BRUTO": modal_liberar.e_pesob,
            "PESO_LIQUIDO": modal_liberar.e_pesol,
            "LACRE_ARMADOR": modal_liberar.e_lacre_arm,
            "LACRE_PHILCO": modal_liberar.e_lacre_ph,
            "ARMADOR_BOOKING_DESTINO": modal_liberar.cbbooking,
            "FABRICA": modal_liberar.cb_tp_fabrica,
            "ISCA_1": modal_liberar.e_isca1,
            "ISCA_2": modal_liberar.e_isca2,
            "OBS": modal_liberar.e_obs,
            "TIPO_CARGA": modal_liberar.cb_tp_carga, # Obj para validação não entra no Banco
        }

    def coletar_dados(self) -> dict:
        """Coleta os valores dos widgets, remove campo de validação e formata"""
        dados_coletados = {}

        for chave, widget in self.dados.items():
            valor = widget.get().strip()
            dados_coletados[chave] = valor
        dados_coletados['STATUS'] = "LIBERADO"

        try:
            dados_coletados["VALOR"] = float(self.convert.formatar_float_usa(dados_coletados["VALOR"]))
            dados_coletados["PESO_BRUTO"] = float(self.convert.formatar_float_usa(dados_coletados["PESO_BRUTO"]))
            dados_coletados["PESO_LIQUIDO"] = float(self.convert.formatar_float_usa(dados_coletados["PESO_LIQUIDO"]))
        except Exception as e:
            messagebox.showerror('Erro', f'Dados invalidos, verifique o peso e valor da NF: {str(e)}')

        return dados_coletados

    def validar_vazios(self, dados: dict) -> bool:
        """
        Valida os campos para não permitir entradas vazias,
        exceto os campos ISCA_1 e ISCA_2, que são validados separadamente.
        """

        # Valores inválidos para comboboxes ou campos padrão
        combo_valores = ["Booking", "Fábrica", "Carga"]

        for campo, valor in dados.items():
            # Ignora os campos de isca (validados em outra função)
            if campo in ["ISCA_1", "ISCA_2"]:
                continue

            # Remove espaços e verifica se está vazio
            if not str(valor).strip():
                messagebox.showerror(title="Erro", message=f"Preencha o campo obrigatório: {campo}")
                return False

            # Verifica se o valor é um placeholder inválido
            if valor in combo_valores:
                messagebox.showerror(title="Erro", message=f"Selecione uma opção válida para: {campo}")
                return False
        return True

    def validar_booking(self, dados: dict) -> bool:
        try:
            with Database() as db:
                registro = db.fetch_base(INDICE=int(self.id))[0]

                teste1 = registro['DESTINO']
                teste2 = registro['ARMADOR']
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar dados: {e}")
            return False

        validacao = dados.get('ARMADOR_BOOKING_DESTINO', '')

        if teste1 in validacao and teste2 in validacao:
            return True
        if teste1 in validacao and teste2 not in validacao:
            messagebox.showerror('Erro Armador x Booking', f"{self.user}, procure o responsável da cabotagem!")
            return False
        if teste1 not in validacao and teste2 in validacao:
            messagebox.showerror('Erro Destino x Booking', f"{self.user}, procure o responsável da cabotagem!")
            return False
        messagebox.showerror('Erro Destino x Armador x Booking', f"{self.user}, procure o responsável da cabotagem!")
        return False

    def validar_iscas(self, dados: dict) -> bool:
        """
        Valida iscas com base em três limites:
        - Se os três limites forem iguais: não exige iscas, mas o valor não pode ultrapassar o limite.
        - Se os limites forem diferentes: aplica regra de 0, 1 ou 2 iscas conforme o valor.
        """
        limites_pgr = self.lista_cliente if dados['TIPO_CARGA'] == "CLIENTE" else self.lista_ag

        try:
            limite_0 = self.convert.formatar_float_usa(limites_pgr[0].split('=')[1].strip())
            limite_1 = self.convert.formatar_float_usa(limites_pgr[1].split('=')[1].strip())
            limite_2 = self.convert.formatar_float_usa(limites_pgr[2].split('=')[1].strip())
        except Exception as e:
            messagebox.showerror('Erro', f'Dados invalidos, Verifique os dados PGR: {str(e)}') #exemplo QTD_ISCAS_1 = 650000



        isca1 = dados.get("ISCA_1", "").strip()
        isca2 = dados.get("ISCA_2", "").strip()

        try:
            valor = float(dados.get("VALOR", 0))
        except ValueError:
            messagebox.showerror("Erro", "Valor da carga inválido.")
            return False

        qtd_iscas = int(bool(isca1)) + int(bool(isca2))

        # Caso especial: todos os limites iguais → não exige isca, mas valor não pode ultrapassar
        if limite_0 == limite_1 == limite_2:
            if valor > limite_0:
                messagebox.showerror(
                    "Erro",
                    f"Valor acima do permitido: R${limite_0:,.2f}.\nIscas embarcadas: {qtd_iscas}"
                )
                return False
            if qtd_iscas > 0:
                messagebox.showwarning(
                    "Validação",
                    f"Carga até R${limite_0:,.2f} não deve ter iscas.\nIscas embarcadas: {qtd_iscas}"
                )
                return False
            return True

        # Validação padrão com faixas
        if valor <= limite_0:
            if qtd_iscas > 0:
                messagebox.showwarning(
                    "Validação",
                    f"Carga até R${limite_0:,.2f} não deve ter iscas.\nIscas embarcadas: {qtd_iscas}"
                )
                return False
        elif limite_0 < valor <= limite_1:
            if qtd_iscas != 1:
                messagebox.showwarning(
                    "Validação",
                    f"Carga entre R${limite_0+0.01:,.2f} e R${limite_1:,.2f} exige exatamente 1 isca.\nIscas embarcadas: {qtd_iscas}"
                )
                return False
        elif limite_1 < valor <= limite_2:
            if qtd_iscas != 2:
                messagebox.showwarning(
                    "Validação",
                    f"Carga entre R${limite_1+0.01:,.2f} e R${limite_2:,.2f} exige 2 iscas.\nIscas embarcadas: {qtd_iscas}"
                )
                return False
        else:
            messagebox.showerror("Erro", "Valor PGR fora da faixa permitida.")
            return False

        return True


        #def carregar_listas(self):
        #    """Retorna dicionario, para carregar todas as listas de combobox"""
        #    with Listas() as users:

    def lancar_dados(self, dados: dict):
        # remove TIPO_CARGA se existir, sem lançar KeyError
        dados.pop('TIPO_CARGA', None)
    
        # atualiza a tabela BASE
        try:
            with Database() as db:
                db.update_base(self.id, **dados)
        except Exception as e:
            messagebox.showerror('Erro tabela BASE', f'Não foi possível salvar os dados:\n {str(e)}')
            return
    
        # busca os dados de status correspondentes e prepara o dicionário para inserir em STATUS
        try:
            with Database() as db:
                dados_status_list = db.fetch_base(INDICE=int(self.id))
    
            # checa se retornou pelo menos uma linha
            if not dados_status_list:
                messagebox.showerror('Erro Tabela STATUS', f'Nenhum registro encontrado em BASE para INDICE={self.id}')
                return
    
            # pega o primeiro dicionário (ou ajuste se houver expectativa de múltiplos)
            dados_status = dados_status_list[0].copy()  # copy para não mutar o objeto original
            # atualiza a data de entrada (use um formato adequado)
            dados_status['DT_ENTRADA'] = datetime.now().strftime('%Y-%m-%d')
    
            # remove a coluna INDICE antes de inserir (se necessário)
            dados_status.pop('INDICE', None)
    
        except Exception as e:
            messagebox.showerror('Erro Tabela STATUS', f'Não foi possível preparar os dados de STATUS:\n {str(e)}')
            return
    
        # insere na tabela STATUS
        try:
            with Database() as db:
                db.insert_status(**dados_status)
        except Exception as e:
            messagebox.showerror('Erro ao inserir STATUS', f'Não foi possível salvar os dados:\n {str(e)}')
            return
    
        messagebox.showinfo('Sucesso', 'Todos os dados foram salvos!')