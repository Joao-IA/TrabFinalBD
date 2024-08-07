import uuid
import sqlite3
import random
import re
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

def generate_phone_number():
    return f"+{random.randint(1000000000, 9999999999)}"

categories = ['Eletrônicos', 'Roupas', 'Alimentos', 'Móveis', 'Brinquedos', 'Ferramentas', 'Livros', 'Beleza', 'Esportes', 'Automotivo']

product_names = [
    'Smartphone', 'Notebook', 'Tablet', 'Câmera', 'Televisão', 'Refrigerador', 'Fogão', 'Microondas', 'Ar Condicionado', 'Aspirador de Pó',
    'Bicicleta', 'Tênis', 'Camiseta', 'Calça Jeans', 'Jaqueta', 'Relógio', 'Brinquedo de Montar', 'Boneca', 'Carro de Controle Remoto', 'Videogame',
    'Martelo', 'Chave de Fenda', 'Furadeira', 'Livro de Ficção', 'Livro de Não Ficção', 'Perfume', 'Creme Hidratante', 'Bola de Futebol', 'Mochila',
    'Capacete', 'Pneu', 'Rádio Automotivo', 'Lâmpada', 'Ventilador', 'Cafeteira', 'Torradeira', 'Liquidificador', 'Batedeira', 'Grill', 'Churrasqueira',
    'Cadeira', 'Sofá', 'Cama', 'Colchão', 'Estante', 'Prateleira', 'Guarda-Roupa', 'Garrafa Térmica', 'Mamadeira'
]

def generate_description():
    return "Este é um excelente produto para uso diário."

def generate_random_name():
    first_names = ['João', 'Maria', 'José', 'Ana', 'Carlos', 'Francisco', 'Paulo', 'Lucas', 'Gabriel', 'Pedro', 'Marcos', 'Ricardo', 'Rafael', 'Bruno', 'Guilherme', 'Gustavo', 'Tiago', 'Rodrigo', 'Matheus', 'Vitor']
    last_names = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Lima', 'Pereira', 'Carvalho', 'Almeida', 'Ferreira', 'Rodrigues', 'Martins', 'Costa', 'Gomes', 'Ribeiro', 'Barros', 'Freitas', 'Barbosa', 'Araújo', 'Melo', 'Cavalcanti']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_gender():
    return random.choice(['Masculino', 'Feminino', 'Outro'])

def slugify(value):
    value = str(value)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

# Coordenadas de geolocalização e estados do Brasil
locations = [
    {"state": "AC", "latitude": -9.97499, "longitude": -67.8243},
    {"state": "AL", "latitude": -9.66599, "longitude": -35.735},
    {"state": "AM", "latitude": -3.10194, "longitude": -60.025},
    {"state": "AP", "latitude": 0.03493, "longitude": -51.0694},
    {"state": "BA", "latitude": -12.9714, "longitude": -38.5014},
    {"state": "CE", "latitude": -3.71722, "longitude": -38.5436},
    {"state": "DF", "latitude": -15.7797, "longitude": -47.9297},
    {"state": "ES", "latitude": -20.3155, "longitude": -40.3128},
    {"state": "GO", "latitude": -16.6869, "longitude": -49.2648},
    {"state": "MA", "latitude": -2.53073, "longitude": -44.3068},
    {"state": "MG", "latitude": -19.9208, "longitude": -43.9378},
    {"state": "MS", "latitude": -20.4486, "longitude": -54.6295},
    {"state": "MT", "latitude": -15.601, "longitude": -56.0974},
    {"state": "PA", "latitude": -1.45583, "longitude": -48.5039},
    {"state": "PB", "latitude": -7.11509, "longitude": -34.8641},
    {"state": "PE", "latitude": -8.04756, "longitude": -34.877},
    {"state": "PI", "latitude": -5.09194, "longitude": -42.8034},
    {"state": "PR", "latitude": -25.4296, "longitude": -49.2713},
    {"state": "RJ", "latitude": -22.9068, "longitude": -43.1729},
    {"state": "RN", "latitude": -5.79448, "longitude": -35.211},
    {"state": "RO", "latitude": -8.76077, "longitude": -63.8999},
    {"state": "RR", "latitude": 2.82384, "longitude": -60.6753},
    {"state": "RS", "latitude": -30.0277, "longitude": -51.2287},
    {"state": "SC", "latitude": -27.5954, "longitude": -48.548},
    {"state": "SE", "latitude": -10.9472, "longitude": -37.0731},
    {"state": "SP", "latitude": -23.5505, "longitude": -46.6333},
    {"state": "TO", "latitude": -10.1847, "longitude": -48.3336}
]

def populate_clients(database_path='rastreamento_entregas.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for _ in range(50000):  # Aumentado 100 vezes
        nome = generate_random_name()
        cliente_id = str(uuid.uuid4())
        endereco_entrega = f"Endereço {random.randint(1, 1000)}"
        email = str(f"{slugify(nome)}_{str(uuid.uuid4())}@email.com")
        telefone = generate_phone_number()
        genero = generate_random_gender()

        logging.debug(f"Inserting Cliente: {cliente_id}, {nome}, {endereco_entrega}, {telefone}, {email}, {genero}")

        try:
            cursor.execute('''
                INSERT INTO Clientes (ClienteID, Nome, EnderecoEntrega, Telefone, Email, Genero)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cliente_id, nome, endereco_entrega, telefone, email, genero))
        except Exception as e:
            logging.error(f"Error inserting Cliente: {e}")

    conn.commit()
    conn.close()

def populate_products(database_path='rastreamento_entregas.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for i in range(10000):  # Aumentado 100 vezes
        produto_id = i + 1
        nome_produto = random.choice(product_names)
        descricao = generate_description()
        peso = round(random.uniform(0.5, 20.0), 2)
        valor = round(random.uniform(10.0, 2000.0), 2)
        categoria = random.choice(categories)

        logging.debug(f"Inserting Produto: {produto_id}, {nome_produto}, {descricao}, {peso}, {valor}, {categoria}")

        try:
            cursor.execute('''
                INSERT INTO Produtos (ProdutoID, NomeProduto, Descricao, Peso, Valor, Categoria)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (produto_id, nome_produto, descricao, peso, valor, categoria))
        except Exception as e:
            logging.error(f"Error inserting Produto: {e}")

    conn.commit()
    conn.close()

def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

def populate_pedidos(database_path='rastreamento_entregas.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('SELECT ClienteID FROM Clientes')
    clientes = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT ProdutoID FROM Produtos')
    produtos = [row[0] for row in cursor.fetchall()]

    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    for i in range(10000):  # Aumentado 100 vezes
        pedido_id = i + 1
        cliente_id = random.choice(clientes)
        produto_id = random.choice(produtos)
        data_pedido = generate_random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S')
        status = random.choice(['Pendente', 'Processando', 'Concluído', 'Cancelado'])

        logging.debug(f"Inserting Pedido: {pedido_id}, {cliente_id}, {produto_id}, {data_pedido}, {status}")

        try:
            cursor.execute('''
                INSERT INTO Pedidos (PedidoID, ClienteID, ProdutoID, DataPedido, Status)
                VALUES (?, ?, ?, ?, ?)
            ''', (pedido_id, cliente_id, produto_id, data_pedido, status))
        except Exception as e:
            logging.error(f"Error inserting Pedido: {e}")

    conn.commit()
    conn.close()

def populate_entregas(database_path='rastreamento_entregas.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('SELECT PedidoID FROM Pedidos')
    pedidos = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT VeiculoID FROM Veiculos')
    veiculos = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT ProdutoID FROM Produtos')
    produtos = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT MotoristaID FROM Motoristas')
    motoristas = [row[0] for row in cursor.fetchall()]

    for i in range(len(pedidos)):
        entrega_id = i + 1
        pedido_id = pedidos[i]
        veiculo_id = random.choice(veiculos)
        produto_id = random.choice(produtos)
        motorista_id = random.choice(motoristas)
        data_hora_inicio = generate_random_date(datetime.now() - timedelta(days=180), datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        tempo_entrega = timedelta(minutes=random.randint(30, 120))
        data_hora_fim = (datetime.strptime(data_hora_inicio, '%Y-%m-%d %H:%M:%S') + tempo_entrega).strftime('%Y-%m-%d %H:%M:%S')
        status_entrega = random.choice(['Em Trânsito', 'Entregue', 'Cancelada'])
        location = random.choice(locations)
        latitude = location["latitude"]
        longitude = location["longitude"]
        estado = location["state"]

        logging.debug(f"Inserting Entrega: {entrega_id}, {pedido_id}, {veiculo_id}, {produto_id}, {motorista_id}, {data_hora_inicio}, {data_hora_fim}, {status_entrega}, {latitude}, {longitude}, {estado}")

        try:
            cursor.execute('''
                INSERT INTO Entregas (EntregaID, PedidoID, VeiculoID, ProdutoID, MotoristaID, DataHoraInicio, DataHoraFim, StatusEntrega, Latitude, Longitude, Estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (entrega_id, pedido_id, veiculo_id, produto_id, motorista_id, data_hora_inicio, data_hora_fim, status_entrega, latitude, longitude, estado))
        except Exception as e:
            logging.error(f"Error inserting Entrega: {e}")

    conn.commit()
    conn.close()

def generate_plate_number():
    return f"{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}-{random.randint(1000, 9999)}"


def populate_veiculos(database_path='rastreamento_entregas.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    tipos_veiculos = ['Carro', 'Moto', 'Van', 'Caminhão']
    for i in range(1000):  # Aumentado 100 vezes
        veiculo_id = generate_plate_number()
        tipo_veiculo = random.choice(tipos_veiculos)
        capacidade = round(random.uniform(500, 5000), 2)
        localizacao_atual = f"Localização {veiculo_id}"

        logging.debug(f"Inserting Veiculo: {veiculo_id}, {tipo_veiculo}, {capacidade}, {localizacao_atual}")

        try:
            cursor.execute('''
                INSERT INTO Veiculos (VeiculoID, TipoVeiculo, Capacidade, LocalizacaoAtual)
                VALUES (?, ?, ?, ?)
            ''', (veiculo_id, tipo_veiculo, capacidade, localizacao_atual))
        except Exception as e:
            logging.error(f"Error inserting Veiculo: {e}")

    conn.commit()
    conn.close()

def generate_cool_driver_name():
    names = [
        'Carlinho do Grau', 'João Meiotaaaa', 'Zé da Motoca', 'Mário Kart', 'Luigi Velocidade', 
        'Rafael Rally', 'Gabriel Turbo', 'Pedro Nitro', 'Carlos Drift', 'Victor Rápido',
        'Matheus Veloz', 'Tiago Acelera', 'Rodrigo Corrida', 'Gustavo Pneu', 'Bruno Motor',
        'Ricardo Velocímetro', 'Marcos Pista', 'Paulo Pneu', 'Francisco Corrida', 'Carlos Motor',
        'Ana Velocidade', 'José Pneu', 'Maria Corrida', 'João Motor', 'Carla Drift', 'Rafaela Rally'
    ]
    return random.choice(names)

def populate_motoristas(database_path='rastreamento_entregas.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for i in range(1000):  # Aumentado 100 vezes
        motorista_id = i + 1
        nome = generate_cool_driver_name()
        cnh = f"CNH-{random.randint(100000, 999999)}"
        veiculo_id = random.randint(1, 100)  # Ajustado para corresponder ao aumento de veículos

        logging.debug(f"Inserting Motorista: {motorista_id}, {nome}, {cnh}, {veiculo_id}")

        try:
            cursor.execute('''
                INSERT INTO Motoristas (MotoristaID, Nome, CNH, VeiculoID)
                VALUES (?, ?, ?, ?)
            ''', (motorista_id, nome, cnh, veiculo_id))
        except Exception as e:
            logging.error(f"Error inserting Motorista: {e}")

    conn.commit()
    conn.close()

def populate_all_datasets(database_path='rastreamento_entregas.db'):
    print("Populating clients...")
    populate_clients(database_path)
    print("Populating products...")
    populate_products(database_path)
    print("Populating vehicles...")
    populate_veiculos(database_path)
    print("Populating drivers...")
    populate_motoristas(database_path)
    print("Populating orders...")
    populate_pedidos(database_path)
    print("Populating deliveries...")
    populate_entregas(database_path)
    print("All datasets populated successfully.")

