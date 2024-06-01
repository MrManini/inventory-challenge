import cv2, typing
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
import socket, pymysql
 
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
 
url='http://192.168.0.100/'
#cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

mysql = pymysql.connect(
    host = 'localhost',
    user = 'central',
    password = 'Central-Stati0n',
    db = 'storage',
    cursorclass = pymysql.cursors.DictCursor
)
cursor = mysql.cursor()

prev=""
pres=""
HOST = "192.168.0.125"
PORT = 8080
mode = "subtract"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def send_command(command: str, color: str = "") -> None:
    s.sendall(color+command)

print("Inicio")
while True:
    try:
        img_resp=urllib.request.urlopen(url+'cam-lo.jpg')
    except:
        continue
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    #_, frame = cap.read()
    frame = cv2.flip(frame, -1)
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        pres=obj.data
        if prev == pres:
            pass
        else:
            print("Type:",obj.type)
            print("Data: ",obj.data)
            try: #TODO: añadir modo resta
                led = int(obj.data)
                if mode == "add":
                    cursor.execute("UPDATE inventory SET amount = amount + %s WHERE id = %s;", (pedido[led+1], led+1))

                send_command(obj.data)
                print(f"Sending {obj.data}")
            except ValueError:
                if obj.data == b'pop_pedido':
                    cursor.execute("SELECT * FROM ORDER BY id ASC LIMIT 1;")
                    pedido = cursor.fetchone()
                    if pedido is not None:
                        mode = "add"
                        cursor.execute("DELETE FROM orders ORDER BY id ASC LIMIT 1;")
                        mysql.commit()
                        for i in range(1, 5): #TODO: Cambiar a 31 cuando esté lista la página web
                            if pedido[f"kit{i}"] != 0:
                                send_command(str(i-1), "c")
                                print(f"Sending c{i-1}")
                        #sql_update = "UPDATE inventory SET amount = amount + %s WHERE id = %s;"
                elif obj.data == b'cancel':
                    mode = "subtract"
            prev = pres
        cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                    (255, 0, 0), 3)
 
    #cv2.imshow("live transmission", frame)
 
    key = cv2.waitKey(1)
    if key == 27:
        break
 
cv2.destroyAllWindows()
#obj.data[2:-1]