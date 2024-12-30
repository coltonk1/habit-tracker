import json
import os

DB_SAVE_LOCATION = "./data/db.duck"

def encryption(data_bytes, key=b"some random key"):
    return xor_encrypt_decrypt(data_bytes, key)

def xor_encrypt_decrypt(data_bytes, key):
    key_repeated = (key * (len(data_bytes) // len(key))) + key[:len(data_bytes) % len(key)]
    return bytes([data_bytes[i] ^ key_repeated[i] for i in range(len(data_bytes))])

def load_tables():
    try:
        with open(DB_SAVE_LOCATION, 'rb') as file:
            data = encryption(file.read())
            json_data = json.loads(data.decode('utf-8'))
            tables = json_data.get('tables')
            return tables
    except FileNotFoundError:
        print("Database not found. Creating template.")
        json_data = {"tables": {}}
        json_str = json.dumps(json_data)
        json_bytes = json_str.encode('utf-8')
        encrypted_bytes = encryption(json_bytes)

        os.makedirs(os.path.dirname(DB_SAVE_LOCATION), exist_ok=True)
        with open(DB_SAVE_LOCATION, "wb") as file:
            file.write(encrypted_bytes)
        
        return {}

class MemoryDatabase:
    def __init__(self):
        self.tables = load_tables()
        self.current_table = None
    
    def read_tables(self):
        print(self.tables)
    
    def is_empty(self):
        return len(self.tables.keys()) == 0

    def add_table(self, table_name, column_names, data_types):
        data_types_str = [data_type.__name__ for data_type in data_types]

        if table_name not in self.tables:
            self.tables[table_name] = {
                "column_names": column_names,
                "column_data_types": data_types_str,
                "column_data": []
            }
        else:
            print(f"Table {table_name} already exists!")

    def add_data(self, data):
        if self.current_table not in self.tables:
            print(f"Table {self.current_table} does not exist!")
            return
        
        if len(data) != len(self.tables[self.current_table]["column_names"]):
            print("Data does not match the number of columns!")
            return
        
        column_data_types = self.tables[self.current_table]["column_data_types"]
        for i, value in enumerate(data):
            expected_type_str = column_data_types[i]  
            expected_type = __builtins__.get(expected_type_str)
            if not isinstance(value, expected_type):
                print(f"Error: Data for column '{self.tables[self.current_table]['column_names'][i]}' should be of type {expected_type.__name__}, but got {type(value).__name__}.")
                return
        
        self.tables[self.current_table]["column_data"].append(data)
    
    def select_table(self, table_name):
        if table_name not in self.tables:
            print(f"Table {table_name} does not exist!")
            return

        self.current_table = table_name

    def get_data_by_column_names(self, *column_names):
        if self.current_table not in self.tables:
            print(f"Table {self.current_table} does not exist!")
            return
        
        for name in column_names:
            if name not in self.tables[self.current_table]["column_names"]:
                print(f"{name} not in table")
                return
        
        if len(column_names) == 0:
            return self.tables[self.current_table]["column_data"]
    
        indices = []
        for name in column_names:
            index = self.tables[self.current_table]["column_names"].index(name)
            indices.append(index)
        output = []
        for items in self.tables[self.current_table]["column_data"]:
            inner = []
            for index in indices:
                inner.append(items[index])
            output.append(inner)
        
        return output
    
    def save(self):
        json_data = {"tables": self.tables}
        json_str = json.dumps(json_data)
        json_bytes = json_str.encode('utf-8')
        encrypted_bytes = encryption(json_bytes)
        os.makedirs(os.path.dirname(DB_SAVE_LOCATION), exist_ok=True)
        with open(DB_SAVE_LOCATION, "wb") as file:
            file.write(encrypted_bytes)

    def update_column(self, column_names, column_data, filter_fn=None):
        # Find the indices of the columns to update
        column_indices = [self.tables[self.current_table]["column_names"].index(col_name) for col_name in column_names]

        # Iterate through rows and update data based on the filter function
        for row in self.tables[self.current_table]["column_data"]:
            if filter_fn is None or filter_fn(row):
                for idx, col_index in enumerate(column_indices):
                    row[col_index] = column_data[idx]

    def remove_row(self, filter_fn):
        if self.current_table not in self.tables:
            print(f"Table {self.current_table} does not exist!")
            return

        table = self.tables[self.current_table]
        column_data = table["column_data"]

        table["column_data"] = [row for row in column_data if not filter_fn(row)]