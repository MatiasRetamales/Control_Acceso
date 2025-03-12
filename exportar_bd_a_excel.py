import pandas as pd
import sqlite3

def exportar_a_excel():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('ingresos.db')

    # Leer los datos directamente desde la base de datos a un DataFrame de pandas
    df = pd.read_sql_query("SELECT * FROM ingresos", conn)

    # Exportar el DataFrame a un archivo Excel
    df.to_excel('ingresos_exportados.xlsx', index=False)

    # Cerrar la conexión
    conn.close()

    # Mensaje de confirmación
    print("Datos exportados exitosamente a ingresos_exportados.xlsx")

# Este bloque se ejecuta solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    exportar_a_excel()  # Se ejecuta solo si el archivo es ejecutado directamente
