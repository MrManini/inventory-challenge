import cv2
import time
import customtkinter as ctk
from PIL import ImageTk, Image
import threading
import mysql.connector


username = 'root'
password = 'jhonatan'
host = 'localhost'
database = 'datostiempo'

# Establish a connection to the database
cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    database=database
)
cursor = cnx.cursor()



class QRCodeScannerAndStopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Scanner and Stopwatch")
        self.master.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.cap = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()
        self.canvas = ctk.CTkCanvas(self.master, width=600, height=400)
        self.canvas.pack(pady=20)

        self.time_frame = ctk.CTkFrame(self.master)
        self.time_frame.pack(pady=20)
        self.time_label = ctk.CTkLabel(self.time_frame, text="00:00:00", font=("Verdana", 48), text_color="white")
        self.time_label.pack(side="left", padx=20)

        self.decode_label = ctk.CTkLabel(self.master, text="", font=("Verdana", 24), text_color="white")
        self.decode_label.pack(pady=20)

        self.running = True
        self.stopwatch_running = False
        self.elapsed_time = 0
        self.interval = 1
        self.previous_qr_data = None
        self.stopwatch_thread = None
        self.validador=True

        self.update_qr_code_and_stopwatch()


    def start_stopwatch(self):
        if self.stopwatch_thread and self.stopwatch_thread.is_alive():
            self.stop_stopwatch()
        self.elapsed_time = 0
        self.stopwatch_running = True
        self.stopwatch_thread = threading.Thread(target=self.update_time)
        self.stopwatch_thread.start()

    def stop_stopwatch(self):
        self.stopwatch_running = False
        if self.stopwatch_thread and self.stopwatch_thread.is_alive():
            self.stopwatch_thread.join()

    def update_time(self):
        first_iteration = True
        while self.stopwatch_running:
            if first_iteration:
                first_iteration = False
            else:
                self.elapsed_time += self.interval
            hours = int(self.elapsed_time // 3600)
            minutes = int((self.elapsed_time % 3600) // 60)
            seconds = int(self.elapsed_time % 60)
            self.time_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            time.sleep(self.interval)

    def update_qr_code_and_stopwatch(self):
        if self.running:
            _, img = self.cap.read()
            data, _, _ = self.detector.detectAndDecode(img)
            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(img))
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=photo, anchor="nw")
            self.canvas.image = photo
            data_array=[]
            tiempo_array=[]

            if data:
                if data != self.previous_qr_data:

                    self.stop_stopwatch()
                    self.time_label.configure(text="00:00:00")
                    self.previous_qr_data = data
                    self.start_stopwatch()
                    self.decode_label.configure(text=data)
                    self.validador=True

                if data==self.previous_qr_data and self.elapsed_time>5:
                    if self.validador==True:
                        cursor.execute("INSERT INTO decodificaciones (mensaje,segundos) VALUES (%s, %s)", (data,self.elapsed_time))
                        cnx.commit()
                    self.validador=False
                    self.stop_stopwatch()
            else:
                pass

            self.master.after(5, self.update_qr_code_and_stopwatch)

if __name__ == "__main__":
    root = ctk.CTk()
    qr_scanner_and_stopwatch = QRCodeScannerAndStopwatch(root)
    root.mainloop()


cursor.close()
cnx.close()