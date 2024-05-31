import serial
import cv2
import numpy as np

# Configura el puerto serial y la velocidad de baudios
ser = serial.Serial('COM14', 1000000, timeout=1)  # Ajusta el nombre del puerto y la velocidad de baudios

# Configura las dimensiones de la imagen
width, height = 96, 96

def buscar_encabezado():
    # Busca el encabezado 0x55AA
    while True:
        byte = ser.read(1)
        if byte == b'\x55':  # Primer byte del encabezado
            second_byte = ser.read(1)
            if second_byte == b'\xAA':  # Segundo byte del encabezado
                return True

try:
    while True:
        if buscar_encabezado():  # Busca el encabezado correcto
            image_data = ser.read(width * height)  # Lee los datos de la imagen
            if len(image_data) == width * height:
                # Convierte los datos a un array de numpy y redimensiona
                img = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width))
                # Muestra la imagen
                cv2.imshow('Imagen desde Arduino', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
                    break
            else:
                print("Datos incompletos recibidos")
finally:
    ser.close()  # Cierra el puerto serial cuando termines
    cv2.destroyAllWindows()  # Cierra todas las ventanas de OpenCV