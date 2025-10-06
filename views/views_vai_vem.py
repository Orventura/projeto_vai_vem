import sqlite3
import pandas as pd
from pathlib import Path
import datetime as dt

# Caminhos de produção
PATH_VAI_VEM   = Path(r"H:\Departamental\EXPEDICAO")

# Verifica se os arquivos de produção existem
if PATH_VAI_VEM.exists():
    BD_VAI_VEM = PATH_VAI_VEM
    print('✅ Programa em Produção (banco: vaivem)')
else:
    # Caminhos de teste
    BD_VAI_VEM    = Path('data/dados.db')
    print('⚠️ Usando banco ´vaivem´ em TESTE')



def vai_vem():
    """Retorna todos os registros de vai vem"""
    with sqlite3.connect(BD_VAI_VEM) as conn:   
        tabela = pd.read_sql_query(
            """
            SELECT
                *
            FROM
                vaivem
            """,
            conn
        )
        tabela['data1'] = pd.to_datetime(tabela['data1'], errors='coerce')
        tabela['data1'] = tabela['data1'].dt.strftime('%d/%m/%Y')
        tabela['data2'] = pd.to_datetime(tabela['data1'], errors='coerce')
        tabela['data2'] = tabela['data1'].dt.strftime('%d/%m/%Y')

    return tabela

def vai_vem_pendente():
    """Retorna Apenas os veículos pendentes de recebimento"""
    with sqlite3.connect(BD_VAI_VEM) as conn:   
        tabela = pd.read_sql_query(
            """
            SELECT
                *
            FROM
                vaivem
            WHERE
                status == "PENDENTE"
            """,
            conn
        )
        tabela['data1'] = pd.to_datetime(tabela['data1'], errors='coerce')
        # 2️⃣ Obter a data de hoje (sem horário)
        hoje = pd.Timestamp(datetime.now().date())

        # 3️⃣ Criar a coluna com a diferença em dias
        tabela['dias_parado'] = (hoje - tabela['data1']).dt.days
        tabela['data1'] = tabela['data1'].dt.strftime('%d/%m/%Y')
        colunas_sheet = [
                    'DIAS', 
                    'ROMAN.', 
                    'LACRE', 
                    'ID', 
                    'PLACA / CNTR', 
                    'FROTA', 
                    'TRANSP.', 
                    'DATA', 
                    'CONFERENTE', 
                    'ORIGEM', 
                    'DESTINO', 
                    'TURNO', 
                    'ITEM', 
                    'DESCRIÇÃO', 
                    'QTD', 
                    'MOTIVO',
                    'JUSTIF.', 
                    'STATUS'
                    ]

        tabela = tabela[['dias_parado', 'romaneio1', 'lacre', 'id_2', 'placa_cntr', 'frota', 'transportadora', 'data1', 'conferente1', 'origem', 'destino', 'turno', 'item', 'desc', 'quantidade', 'motivo', 'justificativa', 'status']]
    return tabela, colunas_sheet

import sqlite3
from datetime import datetime




