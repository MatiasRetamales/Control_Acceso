import cv2
import json

def leer_qr():
    # Inicializar detector de QR
    qr_detector = cv2.QRCodeDetector()

    # Capturar desde la cámara
    cap = cv2.VideoCapture(0)

    # Leer QR continuamente hasta que se detecte uno
    while True:
        exito, imagen = cap.read()
        if not exito:
            break
        
        # Detectar y decodificar
        data, bbox, _ = qr_detector.detectAndDecode(imagen)
        
        if data:
            # Imprimir datos detectados
            print(f"Datos detectados: {data}")
            
            # Reemplazar los saltos de línea en el JSON
            data = data.replace('\n', ' ')

            try:
                # Convertir la cadena a un diccionario JSON
                json_data = json.loads(data)
                print("JSON convertido:", json_data)
                
                # Cerrar la cámara inmediatamente después de escanear
                cap.release()
                cv2.destroyAllWindows()
                
                return json_data  # Retorna el diccionario y termina la función
            except json.JSONDecodeError:
                print("Error: No es un formato JSON válido.")
                return None  # Retorna None si no se puede convertir a JSON
        
        # Mostrar imagen en la ventana
        cv2.imshow("QR Scanner", imagen)
        
        # Si se presiona la tecla 'q', salir del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cerrar la cámara si no se ha leído un QR válido
    cap.release()
    cv2.destroyAllWindows()

# Este bloque se ejecuta solo si el archivo es ejecutado directamente
if __name__ == "__main__":
    leer_qr()
