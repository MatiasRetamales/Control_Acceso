import tkinter as tk
from tkinter import ttk
import sqlite3
from entrada import procesar_ingreso
from salida import procesar_salida

# Función para obtener los datos de la base de datos, con soporte para filtros
def obtener_datos(filtro_columna=None, filtro_criterio=None):
    conn = sqlite3.connect('ingresos.db')
    cursor = conn.cursor()
    
    # Construir la consulta SQL con filtro si es necesario
    if filtro_columna and filtro_criterio:
        query = f"SELECT * FROM ingresos WHERE {filtro_columna} LIKE ?"
        cursor.execute(query, ('%' + filtro_criterio + '%',))
    else:
        cursor.execute("SELECT * FROM ingresos")
    
    datos = cursor.fetchall()
    conn.close()
    return datos

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Ingresos y Salidas")
root.geometry("800x500")
root.config(bg="#dcdcdc")  # Color de fondo de la ventana principal

# Crear la tabla (Treeview) para mostrar los datos
tree = ttk.Treeview(root, columns=("ID", "Casa", "Dueño1", "Fecha Entrada", "Hora Entrada", 
                                   "Quien Ingresa", "Personas", "Patente", "Fecha Salida", "Hora Salida"), 
                    show="headings")

# Estilo del Treeview
style = ttk.Style()
style.configure("Treeview",
                background="#e8e8e8",  # Color de fondo de la tabla
                foreground="black",     # Color del texto
                rowheight=25,           # Altura de las filas
                font=("Arial", 10))     # Fuente de la tabla

style.configure("Treeview.Heading",
                background="#dcdcdc",  # Color de fondo de las cabeceras
                foreground="black",    # Color del texto de las cabeceras
                font=("Arial", 12, "bold"))

# Configuración de las columnas de la tabla
tree.heading("ID", text="ID")
tree.heading("Casa", text="Casa")
tree.heading("Dueño1", text="Dueño 1")
tree.heading("Fecha Entrada", text="Fecha Entrada")
tree.heading("Hora Entrada", text="Hora Entrada")
tree.heading("Quien Ingresa", text="Quien Ingresa")
tree.heading("Personas", text="Número de Personas")
tree.heading("Patente", text="Patente")
tree.heading("Fecha Salida", text="Fecha Salida")
tree.heading("Hora Salida", text="Hora Salida")

# Añadir las columnas de la tabla
tree.column("ID", width=50, anchor="center")
tree.column("Casa", width=100)
tree.column("Dueño1", width=100)
tree.column("Fecha Entrada", width=100)
tree.column("Hora Entrada", width=100)
tree.column("Quien Ingresa", width=150)
tree.column("Personas", width=80, anchor="center")
tree.column("Patente", width=100)
tree.column("Fecha Salida", width=100)
tree.column("Hora Salida", width=100)

# Colocar la tabla en la ventana
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Función para cargar los datos en la tabla
def cargar_datos(filtro_columna=None, filtro_criterio=None):
    # Obtener los datos de la base de datos
    datos = obtener_datos(filtro_columna, filtro_criterio)
    
    # Limpiar la tabla antes de cargar los nuevos datos
    for row in tree.get_children():
        tree.delete(row)
    
    # Insertar los datos en la tabla
    for row in datos:
        tree.insert("", tk.END, values=row)

# Función para aplicar el filtro
def aplicar_filtro():
    filtro_columna = columna_var.get()
    filtro_criterio = filtro_entry.get()
    cargar_datos(filtro_columna, filtro_criterio)
    
def actualizar_datos():
    cargar_datos() 

# Crear campos para seleccionar la columna y el término de búsqueda
tk.Label(root, text="Filtrar por columna:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
columna_var = tk.StringVar()
columna_menu = ttk.Combobox(root, textvariable=columna_var, values=["ID", "Casa", "Dueño1", "Fecha Entrada", 
                                                                   "hora_entrada", "quien_ingresa", "Personas", 
                                                                   "Patente", "fecha_salida", "hora_salida"], font=("Arial", 10))
columna_menu.set("Casa")  # Valor por defecto
columna_menu.pack(pady=5)

tk.Label(root, text="Filtrar criterio:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
filtro_entry = tk.Entry(root, font=("Arial", 10))
filtro_entry.pack(pady=5)

# Crear un frame para los botones, que se alineará en el centro
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Botón para aplicar el filtro
btn_filtrar = tk.Button(button_frame, text="Filtrar", command=aplicar_filtro, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
btn_filtrar.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón para actualizar los datos de la base de datos
btn_actualizar = tk.Button(button_frame, text="Actualizar", command=actualizar_datos, bg="#FFC107", fg="black", font=("Arial", 12, "bold"))
btn_actualizar.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón de ingreso
btn_ingreso = tk.Button(button_frame, text="Ingreso", command=procesar_ingreso, bg="#FFC107", fg="black", font=("Arial", 12, "bold"))
btn_ingreso.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón de salida
btn_salida = tk.Button(button_frame, text="Salida", command=procesar_salida, bg="#FFC107", fg="black", font=("Arial", 12, "bold"))
btn_salida.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Cargar los datos al iniciar la aplicación
cargar_datos()

# Ejecutar la aplicación
root.mainloop()
