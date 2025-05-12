import socket
import select
import multiprocessing
import os


# ---------- FUNCIÓN PARA MANEJAR CONEXIONES TCP ----------
def manejar_cliente(conn, addr):
    print(f"[TCP] Conexión recibida de {addr}")
    mensaje = conn.recv(1024).decode()
    print(f"[TCP] Mensaje recibido: {mensaje}")
    conn.send(f"Respuesta desde el servidor (PID: {os.getpid()})".encode())
    conn.close()


# ---------- FUNCIÓN: SERVIDOR UDP (DESCUBRIMIENTO) ----------
def servidor_udp(sock_udp):
    print(f"[UDP] Esperando descubrimientos en el socket UDP...")

    while True:
        ready = select.select([sock_udp], [], [], 1)
        if ready[0]:
            data, addr = sock_udp.recvfrom(1024)
            mensaje = data.decode()
            if mensaje == "DESCUBRIR_SERVIDOR":
                print(f"[UDP] Descubrimiento recibido de {addr}")
                respuesta = "SERVIDOR_DISPONIBLE"
                sock_udp.sendto(respuesta.encode(), addr)


# ---------- FUNCIÓN: SERVIDOR TCP ----------
def servidor_tcp():
    HOST = ""
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    server_socket.setblocking(0)

    print(f"[TCP] Servidor escuchando en el puerto {PORT}...")

    sockets_activas = [server_socket]

    while True:
        ready_to_read, _, _ = select.select(sockets_activas, [], [], 1)

        for sock in ready_to_read:
            if sock == server_socket:
                conn, addr = server_socket.accept()
                conn.setblocking(0)
                sockets_activas.append(conn)
                print(f"[TCP] Conexión establecida con {addr}")
            else:
                proceso_cliente = multiprocessing.Process(
                    target=manejar_cliente, args=(sock, sock.getpeername())
                )
                proceso_cliente.start()
                sockets_activas.remove(sock)


# ---------- EJECUCIÓN EN PARALELO ----------
if __name__ == "__main__":
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind(("", 50000))
    sock_udp.setblocking(0)

    hilo_udp = multiprocessing.Process(target=servidor_udp, args=(sock_udp,))
    hilo_tcp = multiprocessing.Process(target=servidor_tcp)

    hilo_udp.start()
    hilo_tcp.start()

    hilo_udp.join()
    hilo_tcp.join()
