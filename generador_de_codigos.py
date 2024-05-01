import cv2
import segno
from qreader import QReader


#Generacion de qr usando segno y modificando su escala

qrcode = segno.make_qr("Mensaje para codificar en el qr")
qrcode.save("basic_qrcode.png", scale=8)


#aqui inicializo la funcion
qreader = QReader()


#Especifico la ruta de la imagenn y la codificacion de color a leer
image = cv2.cvtColor(cv2.imread("imagen2.jpg"), cv2.COLOR_BGR2RGB)


#Decodificar la imagen y guardarla en una tupla
decoded_text = qreader.detect_and_decode(image=image)


#imprimir la tupla
print(decoded_text)












