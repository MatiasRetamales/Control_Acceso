import tkinter as tk
from tkinter import ttk
import sqlite3
from entrada import procesar_ingreso
from salida import procesar_salida
from exportar_bd_a_excel import exportar_a_excel

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
root.config(bg="#005f73")  # Color de fondo de la ventana principal (verde azulado oscuro)

# Crear la tabla (Treeview) para mostrar los datos
tree = ttk.Treeview(root, columns=("ID", "Casa", "Dueño1", "Fecha Entrada", "Hora Entrada", 
                                   "Quien Ingresa", "Personas", "Patente", "Fecha Salida", "Hora Salida"), 
                    show="headings")

# Estilo del Treeview
style = ttk.Style()
style.configure("Treeview",
                background="#f0f4f4",  # Color de fondo de las filas
                foreground="black",     # Color del texto
                rowheight=25,           # Altura de las filas
                font=("Arial", 10))     # Fuente de la tabla

style.configure("Treeview.Heading",
                background="#008B8B",  # Color de fondo de las cabeceras
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

# Función para actualizar los datos
def actualizar_datos():
    cargar_datos() 


def editar_celda(event):
    # Verificar si hay una fila seleccionada
    selected_item = tree.selection()
    if not selected_item:  
        return  


    item = selected_item[0]
    

    columna = tree.identify_column(event.x)
    columna_num = int(columna[1:]) - 1  
    
    # Obtener el valor actual de la celda
    valor_actual = tree.item(item, 'values')[columna_num]
    
    # Crear un Entry para editar el valor
    entry = tk.Entry(root, font=("Arial", 10))
    entry.insert(0, valor_actual)
    entry.place(x=event.x + tree.winfo_x(), y=event.y + tree.winfo_y())
    
    # Función para actualizar el valor en la base de datos y en la tabla
    def actualizar_valor(event):
        nuevo_valor = entry.get()
        if nuevo_valor != valor_actual:
            # Actualizar en la base de datos
            id_registro = tree.item(item, 'values')[0]  # Suponiendo que la primera columna es el ID
            columna_nombre = tree["columns"][columna_num]  # Obtener el nombre de la columna
            conn = sqlite3.connect('ingresos.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE ingresos SET {columna_nombre} = ? WHERE ID = ?", (nuevo_valor, id_registro))
            conn.commit()
            conn.close()
            
            # Actualizar el valor en la tabla
            tree.item(item, values=tree.item(item, 'values')[:columna_num] + (nuevo_valor,) + tree.item(item, 'values')[columna_num + 1:])
        
        entry.destroy()  # Eliminar el Entry después de la edición

    entry.bind("<Return>", actualizar_valor)
    entry.bind("<Escape>", lambda event: entry.destroy())


# Función para cerrar el Entry si se hace clic fuera de la tabla
def cerrar_entry(event):
    # Verificar si hay un Entry activo
    if hasattr(root, 'entry_widget'):
        root.entry_widget.destroy()  # Eliminar el Entry si está presente

# Agregar un evento para detectar el doble clic en cualquier celda
tree.bind("<Double-1>", editar_celda)

# Agregar un evento global para detectar clics fuera de la tabla
root.bind("<Button-1>", cerrar_entry)

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
button_frame = tk.Frame(root, bg="#005f73")
button_frame.pack(pady=10)

# Botón para aplicar el filtro
btn_filtrar = tk.Button(button_frame, text="Filtrar", command=aplicar_filtro, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=20, pady=5)
btn_filtrar.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón para actualizar los datos de la base de datos
btn_actualizar = tk.Button(button_frame, text="Actualizar", command=actualizar_datos, bg="#FFC107", fg="black", font=("Arial", 12, "bold"), relief="flat", padx=20, pady=5)
btn_actualizar.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón de ingreso
btn_ingreso = tk.Button(button_frame, text="Ingreso", command=procesar_ingreso, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=20, pady=5)
btn_ingreso.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón de salida
btn_salida = tk.Button(button_frame, text="Salida", command=procesar_salida, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=20, pady=5)
btn_salida.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Botón de exportación a Excel
btn_export = tk.Button(button_frame, text="Exportar", command=exportar_a_excel, bg="#008B8B", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=20, pady=5)
btn_export.pack(side=tk.LEFT, padx=10)  # Coloca el botón a la izquierda dentro del frame

# Cargar los datos al iniciar la aplicación
cargar_datos()

# Ejecutar la aplicación
root.mainloop()
