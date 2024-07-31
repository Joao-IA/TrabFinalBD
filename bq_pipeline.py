import os
import sqlite3
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from pandas_gbq import to_gbq
import json
import logging

logging.basicConfig(level=logging.DEBUG)

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
            sql_file_path = os.path.join(sql_folder, sql_file)
            if not os.path.exists(sql_file_path):
                logging.error(f"Arquivo SQL não encontrado: {sql_file_path}")
                continue

            with open(sql_file_path, 'r') as file:
                query = file.read()

            # Executar a consulta no SQLite
            df = pd.read_sql_query(query, conn)

            # Printar informações sobre o DataFrame
            logging.debug(f'\n{table}:')
            logging.debug(df.info())
            logging.debug("\n" + df.head().to_string())

            # Enviar os dados para o BigQuery
            try:
                self._save_dataframe_to_bq(df, f'seu_dataset.{table}', if_exists='append')
                logging.info(f"Dados da tabela {table} enviados com sucesso para o BigQuery.")
            except Exception as e:
                logging.error(f"Erro ao enviar dados para o BigQuery: {e}")

        # Fechar a conexão com o SQLite
        conn.close()

# Exemplo de uso
if __name__ == "__main__":
    bq_data = BigQueryData(credentials_path="credentials.json")
    bq_data.transfer_data_to_bq(sqlite_db_path='rastreamento_entregas.db', sql_folder='sql')
