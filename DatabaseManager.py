import sqlite3

class DatabaseManager:
    def __init__(self, db_name='nutriPro.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        # Função auxiliar para verificar e adicionar colunas se necessário
        def add_column_if_not_exists(table, column, column_type):
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in self.cursor.fetchall()]
            if column not in columns:
                self.cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")

        # Criar tabela 'users'
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                email TEXT UNIQUE,
                                username TEXT UNIQUE,
                                password TEXT)''')

        # Criar tabela 'historico' com colunas adicionais 'sexo' e 'idade'
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS historico
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                data TEXT,
                                peso REAL,
                                altura REAL,
                                imc REAL,
                                categoria TEXT,
                                objetivo TEXT,
                                sexo TEXT,
                                idade INTEGER,
                                dieta TEXT,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')

        # Verificar e adicionar colunas faltantes na tabela 'historico'
        add_column_if_not_exists('historico', 'imc', 'REAL')
        add_column_if_not_exists('historico', 'dieta', 'TEXT')

        # Criar tabela 'treinos' para armazenar planos de treino
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS treinos
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                data TEXT,
                                objetivo TEXT,
                                foco TEXT,
                                idade INTEGER,
                                sexo TEXT,
                                nivel_experiencia TEXT,
                                equipamentos TEXT,
                                limitacoes TEXT,
                                tempo REAL,
                                treino TEXT,
                                imc REAL,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')

        # Verificar e adicionar colunas faltantes na tabela 'treinos'
        add_column_if_not_exists('treinos', 'imc', 'REAL')
        self.conn.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
