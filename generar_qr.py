import pandas as pd
import qrcode
import json
import os

def generar_qr():
    # Cargar el archivo Excel
    df = pd.read_excel("Personas.xlsx", engine="openpyxl")

    # Verificar la estructura del DataFrame
    print(df.head())

    # Iterar sobre cada fila
    for index, row in df.iterrows():
        casa = row["Casa"]
        dueño1 = row["Dueño 1"]
        dueño2 = row["Dueño 2"]
        
        # Convertir "Autorizados" en una lista (asumiendo que los nombres están separados por comas)
        autorizados = row["Autorizados"].split(", ")  

        # Crear un diccionario con el formato JSON correcto
        qr_data = {
            "Casa": casa,
            "Dueño 1": dueño1,
            "Dueño 2": dueño2,
            "Autorizados": autorizados
        }

        # Convertir el diccionario a una cadena JSON
        qr_json = json.dumps(qr_data, ensure_ascii=False)

        # Crear el QR
        qr = qrcode.make(qr_json)
        
        directorio = 'CodigosQR'
        
        # Crear la carpeta si no existe
        if not os.path.exists(directorio):
         os.makedirs(directorio)
        

        # Guardar el QR con el nombre de la casa
        qr.save(os.path.join(directorio, f"QR_Casa_{casa}.png"))

    print("✅ Códigos QR generados exitosamente.")


generar_qr()


