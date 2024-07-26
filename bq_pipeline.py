import os
import sqlite3
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from pandas_gbq import to_gbq
import json

class BigQueryData:
    def __init__(self, credentials_path="credentials.json"):
        with open(credentials_path, "r") as file:
            self.credentials = service_account.Credentials.from_service_account_info(json.load(file))
        self.project_id = self.credentials.project_id

    def _get_client(self):
        return bigquery.Client(credentials=self.credentials, project=self.project_id)

    def _execute_query(self, query):
        client = self._get_client()
        query_job = client.query(query)
        return query_job.result()

    def _save_dataframe_to_bq(self, df, table_id, if_exists='append'):
        to_gbq(df, table_id, project_id=self.project_id, if_exists=if_exists, credentials=self.credentials)

    def transfer_data_to_bq(self, sqlite_db_path='rastreamento_entregas.db', sql_folder='sql'):
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(sqlite_db_path)
        
        # Dicionário de tabelas e arquivos SQL correspondentes
        tables_sql_files = {
            'FatosEntregas': 'fatos_entregas.sql',
            'DimensaoCliente': 'dimensao_cliente.sql',
            'DimensaoProduto': 'dimensao_produto.sql',
            'DimensaoTempo': 'dimensao_tempo.sql',
            'DimensaoVeiculo': 'dimensao_veiculo.sql',
            'DimensaoMotorista': 'dimensao_motorista.sql'
        }

        # Iterar sobre as tabelas e carregar dados no BigQuery
        for table, sql_file in tables_sql_files.items():
            with open(os.path.join(sql_folder, sql_file), 'r') as file:
                query = file.read()

            # Executar a consulta no SQLite
            df = pd.read_sql_query(query, conn)

            # Enviar os dados para o BigQuery
            self._save_dataframe_to_bq(df, f'seu_dataset.{table}', if_exists='replace')

        # Fechar a conexão com o SQLite
        conn.close()
