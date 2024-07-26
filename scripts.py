from database import Database

from os import walk

def generate_file_structure():
    string = ""
    for (dirpath, dirnames, filenames) in walk('.'):
        for filename in filenames:
            if filename.endswith('.py'):
                string += f"{dirpath}/{filename}\n"
    return string

print(generate_file_structure())

def perform_tests():
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
