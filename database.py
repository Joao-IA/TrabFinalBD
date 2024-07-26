import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('rastreamento_entregas.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def criar_tabelas(self):
        # Tabelas originais
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Clientes (
            ClienteID TEXT PRIMARY KEY,
            Nome TEXT NOT NULL,
            EnderecoEntrega TEXT NOT NULL,
            Telefone TEXT,
            Email TEXT,
            Genero TEXT
        );

        CREATE TABLE IF NOT EXISTS Produtos (
            ProdutoID INTEGER PRIMARY KEY,
            NomeProduto TEXT NOT NULL,
            Descricao TEXT,
            Peso REAL,
            Valor REAL,
            Categoria TEXT
        );

        CREATE TABLE IF NOT EXISTS Pedidos (
            PedidoID INTEGER PRIMARY KEY,
            ClienteID TEXT,
            ProdutoID INTEGER,
            DataPedido TEXT NOT NULL,
            Status TEXT,
            FOREIGN KEY (ClienteID) REFERENCES Clientes (ClienteID),
            FOREIGN KEY (ProdutoID) REFERENCES Produtos (ProdutoID)
        );

        CREATE TABLE IF NOT EXISTS Entregas (
            EntregaID INTEGER PRIMARY KEY,
            PedidoID INTEGER,
            VeiculoID INTEGER,
            DataHoraInicio TEXT,
            DataHoraFim TEXT,
            StatusEntrega TEXT,
            FOREIGN KEY (PedidoID) REFERENCES Pedidos (PedidoID),
            FOREIGN KEY (VeiculoID) REFERENCES Veiculos (VeiculoID)
        );

        CREATE TABLE IF NOT EXISTS Veiculos (
            VeiculoID INTEGER PRIMARY KEY,
            TipoVeiculo TEXT NOT NULL,
            Capacidade REAL,
            LocalizacaoAtual TEXT
        );

        CREATE TABLE IF NOT EXISTS Motoristas (
            MotoristaID INTEGER PRIMARY KEY,
            Nome TEXT NOT NULL,
            CNH TEXT NOT NULL,
            VeiculoID INTEGER,
            FOREIGN KEY (VeiculoID) REFERENCES Veiculos (VeiculoID)
        );
        ''')
        self.conn.commit()

    def drop_tabelas(self):
        self.cursor.executescript('''
        DROP TABLE IF EXISTS Clientes;
        DROP TABLE IF EXISTS Produtos;
        DROP TABLE IF EXISTS Pedidos;
        DROP TABLE IF EXISTS Entregas;
        DROP TABLE IF EXISTS Veiculos;
        DROP TABLE IF EXISTS Motoristas;
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
