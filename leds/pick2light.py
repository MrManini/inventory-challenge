import socket

HOST = '192.168.226.130'  # Puedes encontrar la IP del Arduino en el monitor serial del Arduino IDE
PORT = 80

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())

if __name__ == "__main__":
    while True:
        cmd = input("Enviar datos a Arduino Nano RP2040 Connect: ")
        try:
            send_command(cmd)
        except Exception as e:
            print(f"Error: {e}")
            