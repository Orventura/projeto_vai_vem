import sqlite3
from pathlib import Path
from datetime import date

class Database:
    def __init__(self, db_name="database_cabotagem.db"):
        # Cria a pasta data na raiz do projeto
        self.data_dir = Path(__file__).parent.parent / "data"

        self.data_dir.mkdir(exist_ok=True)
        self.db_path = self.data_dir / db_name
        
        # Conecta ao banco
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Cria as tabelas se não existirem
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS BASE (
            INDICE INTEGER PRIMARY KEY AUTOINCREMENT,
            DT_ENTRADA DATE,
            BK_ENTRADA TEXT,
            FABRICA TEXT,
            ARMADOR TEXT,
            TRANSPORTADOR TEXT,
            CONTEINER TEXT,
            NOTA_FISCAL TEXT,
            ARMADOR_BOOKING_DESTINO TEXT,
            LACRE_ARMADOR TEXT,
            LACRE_PHILCO TEXT,
            PESO_BRUTO TEXT,
            PESO_LIQUIDO TEXT,
            VALOR TEXT,
            OBS TEXT,
            ISCA_1 TEXT,
            ISCA_2 TEXT,
            DESTINO TEXT,                
            STATUS TEXT,
            DIAS_PARADOS INTEGER,
            DT_SAIDA DATE,
            OBS_2 TEXT
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS STATUS (
            INDICE INTEGER PRIMARY KEY AUTOINCREMENT,
            DT_ENTRADA DATE,
            BK_ENTRADA TEXT,
            FABRICA TEXT,
            ARMADOR TEXT,
            TRANSPORTADOR TEXT,
            CONTEINER TEXT,
            NOTA_FISCAL TEXT,
            ARMADOR_BOOKING_DESTINO TEXT,
            LACRE_ARMADOR TEXT,
            LACRE_PHILCO TEXT,
            PESO_BRUTO TEXT,
            PESO_LIQUIDO TEXT,
            VALOR TEXT,
            OBS TEXT,
            ISCA_1 TEXT,
            ISCA_2 TEXT,
            DESTINO TEXT,
            STATUS TEXT,
            DIAS_PARADOS REAL,
            DT_SAIDA DATE,
            USUARIO TEXT,
            OBS_2 TEXT
        )
        """)
        self.conn.commit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()
    
    # -----------------------
    # Função interna para DIAS_PARADOS
    # -----------------------
    def _calculate_days(self, dt_entrada, dt_saida):
        """Calcula DIAS_PARADOS. Se dt_saida for None, usa a data atual"""
        if dt_entrada:
            if not dt_saida:
                dt_saida = date.today()
            return (dt_saida - dt_entrada).days
        return 0
    
    # -----------------------
    # Inserções
    # -----------------------
    def insert_base(self, **kwargs):
            """
            Insere dados na tabela BASE.
            """
            try:
                if not kwargs:
                    raise ValueError("Nenhum dado foi fornecido para inserção na tabela BASE.")

                columns = ', '.join(kwargs.keys())
                placeholders = ', '.join('?' for _ in kwargs)
                values = tuple(kwargs.values())

                self.cursor.execute(f"INSERT INTO BASE ({columns}) VALUES ({placeholders})", values)
                self.conn.commit()
                return self.cursor.lastrowid

            except sqlite3.Error as e:
                raise ValueError(f"Erro ao inserir na tabela BASE: {e}")

    def insert_status(self, **kwargs):
        """
        Insere dados na tabela STATUS.
        """
        try:
            if not kwargs:
                raise ValueError("Nenhum dado foi fornecido para inserção na tabela STATUS.")

            columns = ', '.join(kwargs.keys())
            placeholders = ', '.join('?' for _ in kwargs)
            values = tuple(kwargs.values())

            self.cursor.execute(f"INSERT INTO STATUS ({columns}) VALUES ({placeholders})", values)
            self.conn.commit()
            return self.cursor.lastrowid

        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao inserir na tabela STATUS: {e}")
    
    # -----------------------
    # Busca
    # -----------------------
    def fetch_base(self, **filters):
        if filters:
            conditions = ' AND '.join(f"{k}=?" for k in filters)
            self.cursor.execute(f"SELECT * FROM BASE WHERE {conditions}", tuple(filters.values()))
        else:
            self.cursor.execute("SELECT * FROM BASE")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def fetch_status(self, **filters):
        if filters:
            conditions = ' AND '.join(f"{k}=?" for k in filters)
            self.cursor.execute(f"SELECT * FROM STATUS WHERE {conditions}", tuple(filters.values()))
        else:
            self.cursor.execute("SELECT * FROM STATUS")
        return [dict(row) for row in self.cursor.fetchall()]
    
    # -----------------------
    # Atualizações
    # -----------------------
    def update_base(self, indice: int, **kwargs):
        indice = int(indice)
        # Verifica se o registro existe
        self.cursor.execute("SELECT 1 FROM BASE WHERE INDICE=?", (indice,))
        if not self.cursor.fetchone():
            raise ValueError(f"Nenhum registro encontrado com INDICE = {indice}")

        # Verifica se há dados para atualizar
        if not kwargs:
            raise ValueError("Nenhum dado foi fornecido para atualização.")

        # Monta cláusula SET dinamicamente
        set_clause = ', '.join(f"{k}=?" for k in kwargs)
        values = tuple(kwargs.values()) + (indice,)

        try:
            self.cursor.execute(f"UPDATE BASE SET {set_clause} WHERE INDICE=?", values)
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Falha ao atualizar o registro com INDICE {indice}: {e}")

    
    def update_status(self, indice, **kwargs):
        if not kwargs:
            raise ValueError("Nenhum dado foi fornecido para atualização.")

        # Garante que todos os valores sejam convertidos para tipos compatíveis com SQL
        valores_convertidos = tuple(
            self._converter_valor(v) for v in kwargs.values()
        )

        set_clause = ', '.join(f"{k}=?" for k in kwargs)
        sql = f"UPDATE STATUS SET {set_clause} WHERE INDICE=?"

        # Adiciona o índice ao final da tupla de valores
        valores_finais = valores_convertidos + (indice,)

        self.cursor.execute(sql, valores_finais)
        self.conn.commit()

    def _converter_valor(self, valor):
        import datetime
        import numpy as np
    
        if isinstance(valor, datetime.date):
            return valor.isoformat()  # 'YYYY-MM-DD'
        elif isinstance(valor, np.generic):  # cobre numpy.int64, float64, etc.
            return valor.item()
        else:
            return valor


    # -----------------------
    # Deleção
    # -----------------------
    def delete_base(self, indice):
        self.cursor.execute("DELETE FROM BASE WHERE INDICE=?", (indice,))
        self.conn.commit()
    
    def delete_status(self, indice):
        self.cursor.execute("DELETE FROM STATUS WHERE INDICE=?", (indice,))
        self.conn.commit()


# -----------------------
# Exemplo de uso
# -----------------------
#if __name__ == "__main__":
#    from datetime import timedelta
#    
#    with Database() as db:
#        ## Inserir registro na BASE sem DT_SAIDA
#        #db.insert_base(
#        #    DT_ENTRADA=date.today() - timedelta(days=5),
#        #    DT_SAIDA=None,  # Não informado, será usado date.today()
#        #    BK_ENTRADA="BK123",
#        #    FABRICA="Fábrica A",
#        #    ARMADOR="Armador X",
#        #    TRANSPORTADOR="Transportador Y",
#        #    CONTEINER="CONT001",
#        #    NOTA_FISCAL="NF001",
#        #    ARMADOR_BOOKING_DESTINO="Destino",
#        #    LACRE_ARMADOR="L123",
#        #    LACRE_PHILCO="L456",
#        #    PESO_BRUTO="1000",
#        #    PESO_LIQUIDO="900",
#        #    VALOR="5000",
#        #    OBS="Sem observação",
#        #    ISCA_1="Isca1",
#        #    ISCA_2="Isca2",
#        #    STATUS="TESTE",
#        #    OBS_2="TESTE"
#        #)
#        #
#        #registros = db.fetch_base()
#        #print(registros)

if __name__ == "__main__":
    with Database() as db:
        print(db.fetch_base(INDICE=4))