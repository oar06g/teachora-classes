import sqlite3
from typing_extensions import TypeAlias
from os import PathLike

StrOrBytesPath: TypeAlias = str | bytes | PathLike[str] | PathLike[bytes]

class DatabaseManegar:
  class Data_Pers:
    def __init__(self, db_name: StrOrBytesPath) -> None:
      self.db_name = db_name
      self.connection = sqlite3.connect(self.db_name)
      self.cursor = self.connection.cursor()
  
    def get_data(self, table_name):
      self.cursor.execute(f"SELECT * FROM {table_name}")
      user_info = self.cursor.fetchall()
      for _user in user_info:
        return _user[1], _user[2]
      self.connection.commit()
      self.connection.close()
      
    def insert_or_update_user(self, table_name, username, password):
      self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
      count = self.cursor.fetchone()[0]

      if count == 0:
        self.cursor.execute(f"INSERT INTO {table_name} (username, password) VALUES (?, ?)", (username, password))
      else:
        self.cursor.execute(F"UPDATE {table_name} SET username = ?, password = ? WHERE id = 1", (username, password))
      
      self.connection.commit()
      self.connection.close()
    
    def create_table_userinfo(self):
      self.connection.execute("""CREATE TABLE IF NOT EXISTS user_info (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL UNIQUE,
                              password TEXT NOT NULL)""")
    
    def execute(self, sql: str, params=None):
      self.cursor.execute(sql, params)
      