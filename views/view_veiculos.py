import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# Caminhos de produção
PATH_RODOVIARIO = Path(r"H:\EXPEDICAO\03 Rodoviário\03 Dados\rodoviario.db")
PATH_CABOTAGEM = Path(r"H:\EXPEDICAO\01 Cabotagem\DADOS\1_Última versão\arquivo\philco.db")
PATH_VAI_VEM   = Path(r'x:\x')

# Verifica se os arquivos de produção existem
if PATH_RODOVIARIO.exists() and PATH_CABOTAGEM.exists() and PATH_VAI_VEM.exists():
    BD_RODOVIARIO = PATH_RODOVIARIO
    BD_CABOTAGEM  = PATH_CABOTAGEM
    print('✅ Programa em Produção ("Rodoviário e Cabotagem")')
else:
    # Caminhos de teste
    BD_RODOVIARIO = Path(r'dados_teste\rodo\rodoviario.db')
    BD_CABOTAGEM  = Path(r'dados_teste\cabo\arquivo\philco.db')
    BD_VAI_VEM    = Path(r'data/dados.db')
    print('⚠️ Usando banco "Rodoviário e Cabotagem" em TESTE')


def veiculos_cabotagem():
    with sqlite3.connect(BD_CABOTAGEM) as conn:
        query = 'SELECT * FROM BASE'  
        tabela_completa = pd.read_sql_query(query, conn)
        tabela_para_sheet = tabela_completa.iloc[:, [1, 2, 3, 4, 5, 6, 17]]
        tabela_para_sheet = tabela_para_sheet[~tabela_para_sheet['STATUS'].isin(['SAIU', 'LIBERADO'])]
        return tabela_completa, tabela_para_sheet


def tipos_veiculo():
    """Retorna as tabelas de veículos disponíveis, dos bancos Rodoviário e Cabotagem"""
    with sqlite3.connect(BD_RODOVIARIO) as conn:    
        tabela_carretas = pd.read_sql_query(
            '''
            SELECT
                FROTA,         
                TRANSPORTADOR,
                PLACA
            FROM 
                BASE 
            WHERE 
                STATUS NOT IN ("LIBERADO", "SAIU")
            ''',
            conn
        )

    # Consulta cabotagem
    with sqlite3.connect(BD_CABOTAGEM) as conn: 
        tabela_conteineres = pd.read_sql_query(
            '''
            SELECT
                CONTEINER,
                TRANSPORTADOR
            FROM 
                BASE 
            WHERE 
                STATUS NOT IN ("LIBERADO", "SAIU")
            ''',
            conn
        )

    return tabela_conteineres, tabela_carretas


def filtro(consulta: str, tipo_veiculo: str):
    """Retorna o veículo filtrado no Sheet.veiculos da janela entrada"""
    consulta_param = f"%{consulta}%"

    if tipo_veiculo == 'Carreta':
        with sqlite3.connect(BD_RODOVIARIO) as conn:
            lista = pd.read_sql_query(
                '''
                SELECT
                    FROTA,         
                    TRANSPORTADOR,
                    PLACA
                FROM 
                    BASE 
                WHERE 
                    STATUS NOT IN ("LIBERADO", "SAIU") AND PLACA LIKE ?
                ''',
                conn,
                params=(consulta_param,)
            )
    else:
        with sqlite3.connect(BD_CABOTAGEM) as conn:
            lista = pd.read_sql_query(
                '''
                SELECT
                    CONTEINER,
                    TRANSPORTADOR
                FROM 
                    BASE 
                WHERE 
                    STATUS NOT IN ("LIBERADO", "SAIU") AND CONTEINER LIKE ?
                ''',
                conn,
                params=(consulta_param,)
            )

    return lista


if __name__ =="__main__":
    completa, psheet = veiculos_cabotagem()
    print(psheet)
