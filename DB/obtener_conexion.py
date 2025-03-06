# db.py
import sqlite3

def obtener_conexion():
    try:
        conn = sqlite3.connect('ingresos.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None
