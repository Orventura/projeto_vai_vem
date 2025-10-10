from utils.config import BD_CABOTAGEM, BD_RODOVIARIO, BD_VAI_VEM
import sqlite3
import pandas as pd
from datetime import datetime

def veiculos_cabotagem():
    """Retorna do banco de dados uma lista"""
    with sqlite3.connect(BD_CABOTAGEM) as conn:
        query = 'SELECT * FROM BASE'
        tabela_completa = pd.read_sql_query(query, conn)

    if tabela_completa.empty:
        return tabela_completa, pd.DataFrame()

    try:
        tabela_para_sheet = tabela_completa.iloc[:, [1, 2, 3, 4, 5, 6, 7, 17, 18]]
        tabela_para_sheet = tabela_para_sheet[~tabela_para_sheet['STATUS'].isin(['SAIU', 'LIBERADO'])]

        if not tabela_para_sheet.empty:
            tabela_para_sheet['DT_ENTRADA'] = pd.to_datetime(tabela_para_sheet['DT_ENTRADA'], errors='coerce')
            hoje = pd.Timestamp(datetime.now().date())
            tabela_para_sheet['DIAS'] = (hoje - tabela_para_sheet['DT_ENTRADA']).dt.days
            tabela_para_sheet['DT_ENTRADA'] = tabela_para_sheet['DT_ENTRADA'].dt.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"Erro ao processar tabela: {e}")
        tabela_para_sheet = pd.DataFrame()

    return tabela_completa, tabela_para_sheet

def tipos_veiculo():
    """Retorna as tabelas de veículos disponíveis, dos bancos Rodoviário e Cabotagem"""
    try:
        with sqlite3.connect(BD_RODOVIARIO) as conn:
            tabela_carretas = pd.read_sql_query(
                '''
                SELECT FROTA, TRANSPORTADOR, PLACA
                FROM BASE
                WHERE STATUS NOT IN ("LIBERADO", "SAIU")
                ''',
                conn
            )
    except Exception as e:
        print(f"Erro ao consultar BD_RODOVIARIO: {e}")
        tabela_carretas = pd.DataFrame()

    try:
        with sqlite3.connect(BD_CABOTAGEM) as conn:
            tabela_conteineres = pd.read_sql_query(
                '''
                SELECT CONTEINER, TRANSPORTADOR
                FROM BASE
                WHERE STATUS NOT IN ("LIBERADO", "SAIU")
                ''',
                conn
            )
    except Exception as e:
        print(f"Erro ao consultar BD_CABOTAGEM: {e}")
        tabela_conteineres = pd.DataFrame()

    if tabela_carretas.empty:
        print("⚠️ Nenhum dado encontrado no banco Rodoviário.")
    if tabela_conteineres.empty:
        print("⚠️ Nenhum dado encontrado no banco Cabotagem.")

    return tabela_conteineres, tabela_carretas

def filtrar_veiculo(tipo_veiculo: str, pesquisa: str):
    conteiner_df, carreta_df = tipos_veiculo()
    pesquisa = str(pesquisa).strip()
    resultado = pd.DataFrame()

    try:
        if tipo_veiculo == 'Carreta' and not carreta_df.empty:
            resultado = carreta_df[
                carreta_df.apply(lambda row: row.astype(str).str.contains(pesquisa, case=False, na=False).any(), axis=1)
            ]
        elif tipo_veiculo == 'Conteiner' and not conteiner_df.empty:
            resultado = conteiner_df[
                conteiner_df.apply(lambda row: row.astype(str).str.contains(pesquisa, case=False, na=False).any(), axis=1)
            ]
    except Exception as e:
        print(f"Erro ao filtrar veículo: {e}")

    return resultado

def filtro(consulta: str, tipo_veiculo: str):
    """Retorna o veículo filtrado no Sheet.veiculos da janela entrada"""
    consulta_param = f"%{consulta.strip()}%"
    lista = pd.DataFrame()

    try:
        if tipo_veiculo == 'Carreta':
            with sqlite3.connect(BD_RODOVIARIO) as conn:
                lista = pd.read_sql_query(
                    '''
                    SELECT FROTA, TRANSPORTADOR, PLACA
                    FROM BASE
                    WHERE STATUS NOT IN ("LIBERADO", "SAIU") AND PLACA LIKE ?
                    ''',
                    conn,
                    params=(consulta_param,)
                )
        elif tipo_veiculo == 'Conteiner':
            with sqlite3.connect(BD_CABOTAGEM) as conn:
                lista = pd.read_sql_query(
                    '''
                    SELECT CONTEINER, TRANSPORTADOR
                    FROM BASE
                    WHERE STATUS NOT IN ("LIBERADO", "SAIU") AND CONTEINER LIKE ?
                    ''',
                    conn,
                    params=(consulta_param,)
                )
    except Exception as e:
        print(f"Erro ao consultar banco de dados: {e}")

    if lista.empty:
        print("⚠️ Nenhum resultado encontrado para o filtro.")

    return lista

def vai_vem():
    """Retorna todos os registros de vai vem"""
    tabela = pd.DataFrame()

    try:
        with sqlite3.connect(BD_VAI_VEM) as conn:
            tabela = pd.read_sql_query("SELECT * FROM vaivem", conn)

        if not tabela.empty:
            tabela['data1'] = pd.to_datetime(tabela['data1'], errors='coerce')
            tabela['data2'] = pd.to_datetime(tabela['data2'], errors='coerce')
            tabela['data1'] = tabela['data1'].dt.strftime('%d/%m/%Y')
            tabela['data2'] = tabela['data2'].dt.strftime('%d/%m/%Y')
        else:
            print("⚠️ Nenhum registro encontrado na tabela vaivem.")
    except Exception as e:
        print(f"Erro ao consultar BD_VAI_VEM: {e}")

    return tabela

if __name__ == "__main__":
    conteiner, carreta = tipos_veiculo()
    print(f"Carretas:\n{carreta}\n\nConteineres:\n{conteiner}")
