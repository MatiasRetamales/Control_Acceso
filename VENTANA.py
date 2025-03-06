import sqlite3
from datetime import datetime
import tkinter as tk

def obtener_datos():
    quien = entrada1.get()
    cantidad = entrada2.get()
    patente = entrada3.get()
    
    etiqueta_resultado.config(text=f"Quien ingresa: {quien}\nCantidad: {cantidad}\nPatente: {patente}")
    return quien,cantidad,patente
    
    
    
    

# Crear ventana
ventana = tk.Tk()
ventana.title("Captura de 3 datos")

# Crear y posicionar widgets
tk.Label(ventana, text="Quien ingresa:").pack()
entrada1 = tk.Entry(ventana)
entrada1.pack()

tk.Label(ventana, text="Cantidad:").pack()
entrada2 = tk.Entry(ventana)
entrada2.pack()

tk.Label(ventana, text="Patente:").pack()
entrada3 = tk.Entry(ventana)
entrada3.pack()

# Botón para obtener los datos
boton = tk.Button(ventana, text="Ingresar Datos", command=obtener_datos)
boton.pack(pady=5)

# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()

# Ejecutar la ventana
ventana.mainloop()