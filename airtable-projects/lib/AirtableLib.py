from airtable import Airtable
import pandas as pd
from typing import Dict, List, Union

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
    
    def get_data_by_id(self, id: str) -> pd.DataFrame:
        record = self.airtable.get(id)
        return pd.DataFrame(record['fields'], index=[0])
    
    def get_data_by_field(self, field: str, value: str) -> pd.DataFrame:
        records = self.airtable.search(field, value, typecast=True)
        ids = [record['id'] for record in records]
        data = [record['fields'] for record in records]
        if len(data) == 0:
            return pd.DataFrame()
        return pd.DataFrame(data, index=ids, columns=data[0].keys())
    
    def insert_data(self, data: pd.Series) -> None:
        record = data.to_dict()
        self.airtable.insert(record)

    def delete_data(self, id: List[str]) -> None:
        for i in id:
            self.airtable.delete(i)

    def update_data(self, id: str, data: pd.Series) -> None:
        record = data.to_dict()
        self.airtable.update(id, record)

    def upsert_data(self, data: pd.DataFrame, id_field: str = 'id') -> None:
        for _, row in data.iterrows():
            airtable_record = self.get_data_by_field(id_field, row[id_field])
            if airtable_record.empty:
                self.insert_data(row)
            else:
                for id in airtable_record.index:
                    self.update_data(id, row)
            


    