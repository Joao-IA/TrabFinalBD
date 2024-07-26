from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/create', methods=['GET'])
def create():
    try:
        db.criar_tabelas()
        return jsonify({"message": "Tables created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
