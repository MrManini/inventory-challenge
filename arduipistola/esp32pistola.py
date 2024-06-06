import cv2, typing
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
import socket, pymysql, time, requests
 
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
 
url='http://192.168.1.8/'
blink_url = url + "blink"
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

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
#s.connect((HOST, PORT))

def send_blink_signal():
    try:
        requests.get(blink_url)
    except Exception as e:
        print(f"Failed to send blink signal: {e}")

def send_command(command: bytes, color: bytes = b"") -> None:
    #s.sendall(color+command)
    print(f"Sending {str(color)+str(command)}")

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
        pres = obj.data
        if prev != pres:
            print("Type:",obj.type)
            print("Data: ",obj.data)
            send_blink_signal()
            try: #TODO: añadir modo resta
                led = int(obj.data)
                if mode == "add":
                    cursor.execute("UPDATE inventory SET amount = amount + %s WHERE id = %s;", (pedido[f"kit{led+1}"], int(led+1)))
                    mysql.commit()
                    send_command(obj.data)
                    pedido[f"kit{led+1}"] = 0
                    if sum(pedido.values()) == 0:
                        mode = "subtract"
                        send_command(b"-1")
                else:
                    cursor.execute("SELECT * FROM inventory WHERE id = %s;", (led+1,))
                    producto = cursor.fetchone()
                    if producto["amount"] > 0:
                        cursor.execute("UPDATE inventory SET amount = amount - 1 WHERE id = %s;", (led+1,))
                        mysql.commit()
                        send_command(obj.data)
            except ValueError:
                if obj.data == b'pop_pedido':
                    cursor.execute("SELECT * FROM orders ORDER BY id ASC LIMIT 1;")
                    pedido = cursor.fetchone()
                    print(pedido)
                    if pedido is not None:
                        send_command(b"-1")
                        mode = "add"
                        cursor.execute("DELETE FROM orders ORDER BY id ASC LIMIT 1;")
                        mysql.commit()
                        for i in range(1, 5): #TODO: Cambiar a 31 cuando esté lista la página web
                            if pedido[f"kit{i}"] != 0:
                                send_command(str(i-1), b"c")
                elif obj.data == b'cancel':
                    mode = "subtract"
                    send_command(b"-1")
            prev = pres
        cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                    (255, 0, 0), 3)
 
    cv2.imshow("live transmission", frame)
    time.sleep(0.1)
    key = cv2.waitKey(1)
    if key == 27:
        break
 
cv2.destroyAllWindows()
#obj.data[2:-1]