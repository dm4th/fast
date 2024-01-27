from airtable import Airtable
import pandas as pd

class AirtableData:
    def __init__(self, base_id: str, table_name: str, api_key: str) -> None:
        self.base_id = base_id
        self.table_name = table_name
        self.api_key = api_key
        self.airtable = Airtable(self.base_id, self.table_name, self.api_key)

    def get_data(self) -> pd.DataFrame:
        records = self.airtable.get_all()
        data = [record['fields'] for record in records]
        return pd.DataFrame(data)