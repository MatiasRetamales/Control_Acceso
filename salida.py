from leer_qr import leer_qr
from ingresar_salida import ingresar_salida

def procesar_salida():
    # Aquí leemos el QR
    ingreso = leer_qr()  
    # Y luego procesamos el ingreso
    ingresar_salida(ingreso)

# Este bloque se ejecuta solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    procesar_salida()  # Se ejecuta solo si el archivo es ejecutado directamente
