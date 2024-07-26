import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('rastreamento_entregas.db')
        self.cursor = self.conn.cursor()
    
    def criar_tabelas(self):
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

        self.conn.commit()

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def inserir(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid

# Teste
db = Database()
db.criar_tabelas()

# Inserir dados
db.inserir('INSERT INTO Clientes (Nome, EnderecoEntrega, Telefone, Email) VALUES ("João", "Rua 1", "123456", "joao@email.com")')
db.inserir('INSERT INTO Produtos (NomeProduto, Descricao, Peso, Dimensoes) VALUES ("Produto 1", "Descrição do produto 1", 1.5, "10x10x10")')
db.inserir('INSERT INTO Pedidos (ClienteID, DataPedido, Status) VALUES (1, "2021-10-01", "Pendente")')
db.inserir('INSERT INTO Entregas (PedidoID, VeiculoID, DataHoraInicio, DataHoraFim, StatusEntrega) VALUES (1, 1, "2021-10-01 10:00", "2021-10-01 11:00", "Entregue")')
db.inserir('INSERT INTO Veiculos (TipoVeiculo, Capacidade, LocalizacaoAtual) VALUES ("Caminhão", 1000, "Rua 2")')
db.inserir('INSERT INTO Motoristas (Nome, CNH, VeiculoID) VALUES ("José", "123", 1)')

print(db.select('SELECT * FROM Clientes'))
print(db.select('SELECT * FROM Produtos'))
print(db.select('SELECT * FROM Pedidos'))
print(db.select('SELECT * FROM Entregas'))
print(db.select('SELECT * FROM Veiculos'))
print(db.select('SELECT * FROM Motoristas'))
