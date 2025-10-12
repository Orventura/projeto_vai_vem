import sqlite3, sys
from pathlib import Path
from utils.config import *

class BancoDeDados:

    def __init__(self):
        self.db_path = BD_VAI_VEM

        self.conn = sqlite3.connect(self.db_path)
        self._criar_tabela()

    def _criar_pasta(self):
        if not self.pasta.exists():
            self.pasta.mkdir()
            print(f"Pasta '{self.pasta}' criada com sucesso.")
        else:
            print(f"Pasta '{self.pasta}' já existe.")

    def _criar_tabela(self):
        criar_tabela_sql = """
        CREATE TABLE IF NOT EXISTS vaivem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_2 INTEGER,
            romaneio1 TEXT,
            segmento TEXT,
            data1 DATE,                -- Data da saída
            transportadora TEXT,
            tipo_veiculo,
            placa_cntr TEXT,
            frota TEXT,
            lacre TEXT,
            origem TEXT,
            destino TEXT,
            turno TEXT,
            conferente1 TEXT,
            localizacao TEXT,
            item TEXT,
            desc TEXT,
            quantidade INTEGER,
            nf TEXT,
            motivo TEXT,
            justificativa TEXT,
            status TEXT,
            conferente2 TEXT,
            romaneio2 TEXT,
            data2 DATE,                -- Data da chegada
            end_user TEXT,
            final_hour DATETIME,       -- Data + hora final
            pc TEXT
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(criar_tabela_sql)
        self.conn.commit()
        print(f"Tabela 'vaivem' criada/verificada com sucesso em '{self.db_path}'.")
    
    def gerar_id2(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id_2) FROM vaivem")
        resultado = cursor.fetchone()
        ultimo_id2 = resultado[0] if resultado[0] is not None else 0
        novo_id2 = ultimo_id2 + 1
        return novo_id2

    def inserir_dado(self, **dados):
        """
        Insere dados na tabela vaivem usando um dicionário como entrada.
        """
        try:
            if not dados:
                raise ValueError("Nenhum dado foi fornecido para inserção na tabela vaivem.")

            # Gera os nomes das colunas e os placeholders
            colunas = ', '.join(dados.keys())
            placeholders = ', '.join('?' for _ in dados)
            valores = tuple(dados.values())

            sql = f"""
            INSERT INTO vaivem (
                {colunas}
            ) VALUES (
                {placeholders}
            )
            """

            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            print(f"Registro inserido com sucesso. ID: {cursor.lastrowid}")
            return cursor.lastrowid

        except sqlite3.Error as e:
            raise ValueError(f"Erro ao inserir na tabela vaivem: {e}")    
        
    def inserir_dado_antigo(self, valores: tuple):
        sql = """
        INSERT INTO vaivem (
            id_2,romaneio1, segmento, data1, transportadora, frota_cntr, placa, lacre,
            origem, destino, turno, conferente1, localizacao, item, desc,
            quantidade, nf, motivo, justificativa, status, conferente2, romaneio2, data2,
            end_user, final_hour, pc
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, valores)
        self.conn.commit()
        print(f"Registro inserido com sucesso. ID: {cursor.lastrowid}")


    def __enter__(self):
        return self

    def __exit__(self, tipo, valor, traceback):
        self.conn.close()
        print(f"Conexão com o banco '{self.db_path.name}' encerrada.")


    def receber_in_sql(self, id2: int, lista: list):
        """
        Atualiza os dados de recebimento no banco.

        Parâmetros
        ----------
        id2 : int
            Identificador do embarque (coluna id_2) que será atualizado.
        lista : list
            Deve conter na ordem:
                [status, conferente2, romaneio2, data2, end_user, final_hour, pc]
        """
        # Validação da lista
        if len(lista) != 7:
            raise ValueError("A lista deve conter 7 valores: status, conferente2, romaneio2, data2, end_user, final_hour, pc")

        params = tuple(lista) + (id2,)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                '''
                UPDATE vaivem
                SET status = ?, 
                    conferente2 = ?, 
                    romaneio2 = ?, 
                    data2 = ?, 
                    end_user = ?, 
                    final_hour = ?, 
                    pc = ?
                WHERE id_2 = ?
                ''',
                params
            )
            conn.commit()

            if cursor.rowcount == 0:  # nenhuma linha foi atualizada
                raise ValueError(f"ID {id2} não encontrado")




# Exemplo de uso
if __name__ == "__main__":
    with BancoDeDados() as bd:
        print("Banco de dados pronto para uso.")
