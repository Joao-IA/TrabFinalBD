from flask import Flask, request, jsonify
from database import Database
from bq_pipeline import BigQueryData
from populate_datasets import populate_all_datasets
import logging

app = Flask(__name__)
app.config['DEBUG'] = True

# Habilitar logs detalhados
logging.basicConfig(level=logging.DEBUG)

# Instanciar as classes de banco de dados e BigQuery
db = Database()
bq_data = BigQueryData(credentials_path='credentials.json')  # Certifique-se de que o caminho esteja correto

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/select', methods=['GET'])
def select():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        results = db.select(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    if not data or 'query' not in data or 'params' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    query = data['query']
    params = data['params']
    
    try:
        lastrowid = db.inserir(query, params)
        return jsonify({"lastrowid": lastrowid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/create_tables', methods=['POST'])
def create_tables():
    try:
        db.criar_tabelas()
        return jsonify({"status": "Tables created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/drop_tables', methods=['POST'])
def drop_tables():
    try:
        db.drop_tabelas()
        return jsonify({"status": "Tables dropped successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    try:
        bq_data.transfer_data_to_bq(sqlite_db_path='rastreamento_entregas.db', sql_folder='sql')
        return jsonify({"status": "Pipeline executed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/populate_all_datasets', methods=['POST'])
def populate_all_datasets_route():
    try:
        populate_all_datasets(database_path='rastreamento_entregas.db')
        return jsonify({"status": "All datasets populated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
