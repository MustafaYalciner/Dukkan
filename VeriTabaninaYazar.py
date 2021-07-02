import os
import sqlite3
from sqlite3 import Error


class VeriTabaninaYazar:

    def __init__(self):
        self.dukkanlar_tablosunu_olustur = """
        CREATE TABLE IF NOT EXISTS dukkanlar (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ad TEXT NOT NULL,
          bosda BOOLEAN,
          lokasyonX INTEGER,
          lokasyonY INTEGER
        );
        """

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect('BizimVeriTabani.db')
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection


    def veriTabaniniBaslast(self):
        baglanti = self.create_connection()
        cursor = baglanti.cursor()
        try:
            cursor.execute(self.dukkanlar_tablosunu_olustur)
            baglanti.commit()
            print("Query basarili")
        except Error as e:
            print(f"query basarisiz, error '{e}' verdi")
        cursor.close()

    def dukkani_kayit_et(self, dukkan):
        self.veriTabaniniBaslast()
        baglanti = self.create_connection()
        cursor = baglanti.cursor()
        try:
            cursor.execute(self.sqlOlustur(dukkan))
            baglanti.commit()
            print("Query basarili")
        except Error as e:
            print(f"query basarisiz, error '{e}' verdi")
        cursor.close()

    def sqlOlustur(self, dukkan):
        return f'INSERT INTO dukkanlar (ad, bosda, lokasyonX, lokasyonY) VALUES("{dukkan.adi}",{dukkan.bosda},{dukkan.lokasyon.x},{dukkan.lokasyon.y})'
