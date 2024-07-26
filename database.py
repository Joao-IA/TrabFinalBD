import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('rastreamento_entregas.db')
        self.cursor = self.conn.cursor()
    
    def criar_tabelas(self):
        # Tabelas originais
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            ClienteID INTEGER PRIMARY KEY,
            Nome TEXT NOT NULL,
            EnderecoEntrega TEXT NOT NULL,
            Telefone TEXT,
            Email TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            ProdutoID INTEGER PRIMARY KEY,
            NomeProduto TEXT NOT NULL,
            Descricao TEXT,
            Peso REAL,
            Dimensoes TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            PedidoID INTEGER PRIMARY KEY,
            ClienteID INTEGER,
            DataPedido TEXT NOT NULL,
            Status TEXT,
            FOREIGN KEY (ClienteID) REFERENCES Clientes (ClienteID)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Entregas (
            EntregaID INTEGER PRIMARY KEY,
            PedidoID INTEGER,
            VeiculoID INTEGER,
            DataHoraInicio TEXT,
            DataHoraFim TEXT,
            StatusEntrega TEXT,
            FOREIGN KEY (PedidoID) REFERENCES Pedidos (PedidoID),
            FOREIGN KEY (VeiculoID) REFERENCES Veiculos (VeiculoID)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Veiculos (
            VeiculoID INTEGER PRIMARY KEY,
            TipoVeiculo TEXT NOT NULL,
            Capacidade REAL,
            LocalizacaoAtual TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Motoristas (
            MotoristaID INTEGER PRIMARY KEY,
            Nome TEXT NOT NULL,
            CNH TEXT NOT NULL,
            VeiculoID INTEGER,
            FOREIGN KEY (VeiculoID) REFERENCES Veiculos (VeiculoID)
        )
        ''')

        # Tabelas de dimensões
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimensaoCliente (
            ClienteID INTEGER PRIMARY KEY,
            Nome TEXT NOT NULL,
            Regiao TEXT,
            Segmento TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimensaoProduto (
            ProdutoID INTEGER PRIMARY KEY,
            NomeProduto TEXT NOT NULL,
            Categoria TEXT,
            Peso REAL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimensaoTempo (
            DataID INTEGER PRIMARY KEY,
            Data TEXT NOT NULL,
            Semana INTEGER,
            Mes INTEGER,
            Ano INTEGER
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimensaoVeiculo (
            VeiculoID INTEGER PRIMARY KEY,
            TipoVeiculo TEXT NOT NULL,
            Capacidade REAL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimensaoMotorista (
            MotoristaID INTEGER PRIMARY KEY,
            Nome TEXT NOT NULL,
            CNH TEXT NOT NULL
        )
        ''')

        # Tabela de fatos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS FatosEntregas (
            EntregaID INTEGER PRIMARY KEY,
            DataHoraInicio TEXT,
            DataHoraFim TEXT,
            TempoEntrega REAL,
            ClienteID INTEGER,
            ProdutoID INTEGER,
            VeiculoID INTEGER,
            MotoristaID INTEGER,
            Quantidade INTEGER,
            FOREIGN KEY (ClienteID) REFERENCES DimensaoCliente (ClienteID),
            FOREIGN KEY (ProdutoID) REFERENCES DimensaoProduto (ProdutoID),
            FOREIGN KEY (VeiculoID) REFERENCES DimensaoVeiculo (VeiculoID),
            FOREIGN KEY (MotoristaID) REFERENCES DimensaoMotorista (MotoristaID)
        )
        ''')

        self.conn.commit()

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def inserir(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid

# Teste
db = Database()
db.criar_tabelas()

# Inserir dados nas tabelas de dimensões
db.inserir('INSERT INTO DimensaoCliente (Nome, Regiao, Segmento) VALUES (?, ?, ?)', ("João", "Sul", "Varejo"))
db.inserir('INSERT INTO DimensaoProduto (NomeProduto, Categoria, Peso) VALUES (?, ?, ?)', ("Produto 1", "Categoria A", 1.5))
db.inserir('INSERT INTO DimensaoTempo (Data, Semana, Mes, Ano) VALUES (?, ?, ?, ?)', ("2021-10-01", 40, 10, 2021))
db.inserir('INSERT INTO DimensaoVeiculo (TipoVeiculo, Capacidade) VALUES (?, ?)', ("Caminhão", 1000))
db.inserir('INSERT INTO DimensaoMotorista (Nome, CNH) VALUES (?, ?)', ("José", "123"))

# Inserir dados na tabela de fatos
db.inserir('INSERT INTO FatosEntregas (DataHoraInicio, DataHoraFim, TempoEntrega, ClienteID, ProdutoID, VeiculoID, MotoristaID, Quantidade) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
           ("2021-10-01 10:00", "2021-10-01 11:00", 1.0, 1, 1, 1, 1, 10))

# Consultar dados das tabelas
print(db.select('SELECT * FROM DimensaoCliente'))
print(db.select('SELECT * FROM DimensaoProduto'))
print(db.select('SELECT * FROM DimensaoTempo'))
print(db.select('SELECT * FROM DimensaoVeiculo'))
print(db.select('SELECT * FROM DimensaoMotorista'))
print(db.select('SELECT * FROM FatosEntregas'))
