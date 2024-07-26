from google.oauth2 import service_account
from google.cloud import bigquery
from pandas_gbq import to_gbq
import json

class BigQueryData:
    def _init_(self, credentials_path="credentials.json"):
        with open(credentials_path, "r") as file:
            self.credentials = json.load(file)

    def _get_client(self):
        credentials = service_account.Credentials.from_service_account_info(self.credentials)
        return bigquery.Client(credentials=credentials, project=self.project_id)

    def _execute_query(self, query):
        client = self._get_client()
        query_job = client.query(query)
        return query_job.result()

    def _save_dataframe_to_bq(self, df, table_id, if_exists='append'):
        credentials = service_account.Credentials.from_service_account_info(self.credentials)
        to_gbq(df, table_id, if_exists=if_exists, project_id=self.project_id)