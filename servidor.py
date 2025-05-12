import socket
import threading


# ---------- FUNCIÓN PARA MANEJAR CONEXIONES TCP ----------
def manejar_cliente(conn, addr):
    print(f"[TCP] Conexión recibida de {addr}")
    mensaje = conn.recv(1024).decode()
    print(f"[TCP] Mensaje recibido: {mensaje}")
    conn.send("¡Hola desde la laptop!".encode())
    conn.close()


# ---------- FUNCIÓN: ESCUCHAR UDP (DESCUBRIMIENTO) ----------
def servidor_udp():
    UDP_IP = ""
    UDP_PORT = 50000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"[UDP] Esperando descubrimientos en puerto {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        mensaje = data.decode()
        if mensaje == "DESCUBRIR_SERVIDOR":
            print(f"[UDP] Descubrimiento recibido de {addr}")
            respuesta = "SERVIDOR_DISPONIBLE"
            sock.sendto(respuesta.encode(), addr)


# ---------- FUNCIÓN: SERVIDOR TCP ----------
def servidor_tcp():
    HOST = ""
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[TCP] Servidor escuchando en el puerto {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo_cliente.start()


# ---------- EJECUCIÓN EN PARALELO ----------
if __name__ == "__main__":
    hilo_udp = threading.Thread(target=servidor_udp)
    hilo_tcp = threading.Thread(target=servidor_tcp)

    hilo_udp.start()
    hilo_tcp.start()

    hilo_udp.join()
    hilo_tcp.join()
