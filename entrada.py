from leer_qr import leer_qr
from ingresar_entrada import ingresar_entrada

def procesar_ingreso():
    # Aquí leemos el QR
    ingreso = leer_qr()  
    # Y luego procesamos el ingreso
    ingresar_entrada(ingreso)

# Este bloque se ejecuta solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    procesar_ingreso()  # Se ejecuta solo si el archivo es ejecutado directamente