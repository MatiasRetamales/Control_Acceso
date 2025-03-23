import sqlite3
from datetime import datetime

    

def ingresar_entrada(ingreso):
    # Conectar a la base de datos SQLite (se crea si no existe)
    conn = sqlite3.connect('ingresos.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            casa TEXT,
            dueño1 TEXT,
            fecha_entrada TEXT,
            hora_entrada TEXT,
            quien_ingresa TEXT,
            personas INTEGER,
            patente TEXT,
            fecha_salida TEXT,
            hora_salida TEXT,
            observaciones TEXT
            
        )
    ''')
    
    

    # Obtener datos de entrada
    quien = input("Quien ingresa: ")
    cantidad = input("Cantidad: ")
    patente = input("Patente: ")

    # Obtener fecha y hora actuales como string
    hora_actual = datetime.now().strftime("%H:%M")
    fecha_actual = datetime.now().strftime("%d-%m-%Y")

    # Agregar al diccionario de ingreso
    ingreso["Fecha de entrada"] = fecha_actual
    ingreso["Hora de entrada"] = hora_actual
    ingreso["Quien ingresa"] = quien
    ingreso["Personas"] = cantidad
    ingreso["Patente"] = patente

    # Insertar los datos en la base de datos
    cursor.execute('''
        INSERT INTO ingresos (casa, dueño1, fecha_entrada, hora_entrada, quien_ingresa, personas, patente)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (ingreso["Casa"], ingreso["Dueño 1"], ingreso["Fecha de entrada"], 
          ingreso["Hora de entrada"], ingreso["Quien ingresa"], 
          ingreso["Personas"], ingreso["Patente"]))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print("Datos agregados con éxito.")
