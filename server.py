import socket
import threading

# Definimos host y puerto.
host = '127.0.0.1'
port = 55555

# ---- Iniciamos la conexión ----

# Creamos el socket:
# socket.AF_INET - Dominio (conector IPv4)
# socket.SOCK_STREAM - Tipo (TCP Stream)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociamos el servidor con el puerto y la dirección IP.
server.bind((host, port))

# Ponemos el servidor en modo escucha.
server.listen()

# ---- Determinación de variables ----

# Lista de clientes conectados.
clients = set()


# ---- Conexión de clientes ----

# Se ejecuta un bucle infinito que acepta nuevos clientes y los conecta al servidor.
def receive():
    while True:
        # Aceptamos la conexión e imprimimos mensaje.
        client, address = server.accept()
        print("Se ha conectado", format(str(address)))

        # Añadimos el cliente a la lista y avisamos por el chat.
        clients.add(client)
        client.send(("Bienvenido!!").encode('utf-8'))
        sendAll("\nAll: Un nuevo usuario se ha unido.".encode('utf-8'))

        # Creamos e iniciamos el thread del cliente.
        t = threading.Thread(target=clientHandler, args=(client,))
        t.start()


# ---- Recepción de mensajes ----

# Envía los mensajes al resto de usuarios y desconecta el cliente del chat (excepción).
def clientHandler(client):
    # Cuando un cliente se conecta, entra en el siguiente bucle infinito de recepción de mensajes.
    while True:
        try:
            msg = client.recv(1024)  # Intenta recibir y lee 1024 bytes.

            # Si el usuario introduce 'exit', lo eliminamos del chat.
            if (msg.decode('utf-8') == 'exit'):
                # Eliminamos al cliente de la lista, cerramos el socket y paramos el bucle.
                client.send(("Has salido del chat.").encode('utf-8'))
                clients.remove(client)
                client.close()

            sendAll(msg)  # Envíamos el mensaje al resto de usuarios.

        # Si el usuario se desconecta, salta una excepción. Lo eliminamos del chat.
        except:
            # Eliminamos al cliente de la lista, cerramos el socket y paramos el bucle.
            break


# ---- Enviar mensaje global ----
def sendAll(msg):
    for cliente in clients:
        cliente.send(msg)


receive() # Iniciamos el servidor.
