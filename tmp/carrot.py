import os
import datetime as dt
import ctypes as ct
import pickle

class Struct(ct.Structure):
    _fields_ = [
        ('Title', ct.c_int),
        ('Price', ct.c_double),
    ]

    def push(self, Title, Price):
        self.Title = Title
        self.Price = Price

    def __str__(self):
        return f"Struct(Title={self.Title}, Price={self.Price})"

class TitanVault:
    def __init__(self, database_name):
        self.database_name = database_name
        self.created_date = dt.datetime.now()
        self.base = []

    def new_struct(self, Title, Price):
        new_structure = Struct()
        new_structure.push(Title, Price)
        self.base.append(new_structure)
        return new_structure

    def delete_struct(self, index):
        if 0 <= index < len(self.base):
            del self.base[index]
            print(f"Structure at index {index} deleted successfully.")
        else:
            print("Error: Index out of range.")

    def get_struct(self, index):
        if 0 <= index < len(self.base):
            return self.base[index]
        else:
            print("Error: Index out of range.")
            return None

    def __str__(self):
        return f"Database: {self.database_name}, Created: {self.created_date}, Structs: {len(self.base)}"

class Cursor:
    dbs = []

    @classmethod
    def about(cls):
        print(f"Number of databases: {len(cls.dbs)}")
        for db in cls.dbs:
            print(db)

    def __init__(self, name, cnt=1):
        self.dbs = [TitanVault(name) for _ in range(cnt)]
        print(f"Created {cnt} database(s): {[db.database_name for db in self.dbs]}")

    def information(self):
        for i, db in enumerate(self.dbs):
            print(f"Index [{i}] - {db}")

    def insert(self, index, header, data_int, data_double):
        if 0 <= index < len(self.dbs):
            new_struct = self.dbs[index].new_struct(header, data_int, data_double)
            print(f"Inserted: {new_struct}")
        else:
            print("Error: Index out of range.")

    def pop(self, index):
        if 0 <= index < len(self.dbs):
            del self.dbs[index]
            print("Database deleted successfully.")
        else:
            print("Error: Index out of range.")

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.dbs, file)
        print(f"Databases saved to {filename}.")

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.dbs = pickle.load(file)
            print(f"Databases loaded from {filename}.")
        else:
            print("Error: File not found.")
