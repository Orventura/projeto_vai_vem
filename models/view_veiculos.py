from utils.config import *
import sqlite3



def veiculos_cabotagem():
    """Retorna do banco de dados uma lista """
    with sqlite3.connect(BD_CABOTAGEM) as conn:
        query = 'SELECT * FROM BASE'  
        tabela_completa = pd.read_sql_query(query, conn)
        tabela_para_sheet = tabela_completa.iloc[:, [1, 2, 3, 4, 5, 6, 7, 17,18]]
        tabela_para_sheet = tabela_para_sheet[~tabela_para_sheet['STATUS'].isin(['SAIU', 'LIBERADO'])]

        tabela_para_sheet['DT_ENTRADA'] = pd.to_datetime(tabela_para_sheet['DT_ENTRADA'], errors='coerce')
        # 2️⃣ Obter a data de hoje (sem horário)
        hoje = pd.Timestamp(datetime.now().date())

        # 3️⃣ Criar a coluna com a diferença em dias
        tabela_para_sheet['DIAS'] = (hoje - tabela_para_sheet['DT_ENTRADA']).dt.days
        tabela_para_sheet['DT_ENTRADA'] = tabela_para_sheet['DT_ENTRADA'].dt.strftime('%d/%m/%Y')


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

def filtrar_veiculo(tipo_veiculo: str, pesquisa: str):
    conteiner_df, carreta_df = tipos_veiculo()
    pesquisa = str(pesquisa).strip()  # Garante que é string e remove espaços extras

    if tipo_veiculo == 'Carreta':
        # Busca em todas as colunas da carreta_df
        resultado = carreta_df[carreta_df.apply(lambda row: row.astype(str).str.contains(pesquisa, case=False, na=False).any(), axis=1)]

    elif tipo_veiculo == 'Conteiner':
        # Busca em todas as colunas da conteiner_df
        resultado = conteiner_df[conteiner_df.apply(lambda row: row.astype(str).str.contains(pesquisa, case=False, na=False).any(), axis=1)]

    else:
        resultado = pd.DataFrame()  # Retorna vazio se tipo não reconhecido

    return resultado


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
    carreta, conteiner = tipos_veiculo()
    print(f'{carreta}, \n\n\n\n {conteiner}')
