import socket
import threading

# Definimos IP y puerto del servidor.
host = '127.0.0.1'
port = 55555

# ---- Datos del usuario ----
print("---- Información ---- \nPara desconectarse del chat, introduzca 'exit'.\n")
user = input("Nombre de usuario: ")
print("\n")
# ---- Iniciamos la conexión ----

# Creamos el socket:
# socket.AF_INET - Dominio (conector IPv4)
# socket.SOCK_STREAM - Tipo (TCP Stream)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Nos conectamos al servidor.
client.connect(('127.0.0.1', 55555))

# ---- Threads Recepción/Envío ----

# Envío de mensajes al servidor.
def send_msg():
    while True:
        msg = input() # Guardamos el mensaje introducido por el usuario.

        if msg == 'exit':
            client.send(msg.encode("utf-8"))
            break

        msg = "{}: {}".format(user,msg)
        client.send(msg.encode("utf-8")) # Lo envíamos al servidor.


# Recepción de mensajes.
def receive_msg():
    while True:
        msg = client.recv(1024) # Lee 1024 bytes.
        msg = msg.decode()

        print(msg) # Imprimimos el mensaje recibido.
        if msg == 'Has salido del chat.': break


# ---- Iniciamos los Threads ----

# Creamos los threads de recepción y envío.
receive = threading.Thread(target=receive_msg)
send = threading.Thread(target=send_msg)

# Los iniciamos.
receive.start()
send.start()
