import sqlite3
from datetime import datetime

def ingresar_salida(ingreso):
    try:
        # Paso 2: Conectar con la base de datos SQLite
        conn = sqlite3.connect('ingresos.db')  # Asegúrate de tener esta base de datos
        cursor = conn.cursor()

        # Paso 3: Obtener fecha y hora actuales
        hora_actual = datetime.now().strftime("%H:%M")
        fecha_actual = datetime.now().strftime("%d-%m-%Y")

        # Paso 4: Buscar la última coincidencia de la casa en la base de datos
        cursor.execute("""
            SELECT * FROM ingresos WHERE casa = ?
            ORDER BY id DESC LIMIT 1
        """, (ingreso['Casa'],))  # Ordena por 'id' o el campo adecuado para obtener el último registro
        fila = cursor.fetchone()  # Obtener la última coincidencia

        if fila:
            # Paso 5: Actualizar la fecha y hora de salida
            cursor.execute("""
                UPDATE ingresos
                SET fecha_salida = ?, hora_salida = ?
                WHERE id = ?
            """, (fecha_actual, hora_actual, fila[0]))  # Usar 'id' para especificar el registro

            # Paso 6: Confirmar los cambios
            conn.commit()
            print(f"Datos de salida registrados para la Casa {ingreso['Casa']}.")

        else:
            print("No se encontró la Casa en los registros.")

    except sqlite3.Error as e:
        print(f"Error al interactuar con la base de datos: {e}")
    finally:
        # Asegurarse de cerrar la conexión
        conn.close()
