import socket
import select


# ---------- FUNCIÓN: ESCUCHAR UDP (DESCUBRIMIENTO) ----------
def servidor_udp():
    UDP_IP = ""
    UDP_PORT = 50000

    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind((UDP_IP, UDP_PORT))
    sock_udp.setblocking(0) 

    print(f"[UDP] Esperando descubrimientos en puerto {UDP_PORT}...")

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
        ready_to_read, _, _ = select.select(
            sockets_activas, [], [], 1
        )  

        for sock in ready_to_read:
            if sock == server_socket:
                conn, addr = server_socket.accept()
                conn.setblocking(0)
                sockets_activas.append(conn)
                print(f"[TCP] Conexión recibida de {addr}")
            else:
                try:
                    mensaje = sock.recv(1024).decode()
                    if mensaje:
                        print(f"[TCP] Mensaje recibido: {mensaje}")
                        sock.send("¡Hola desde la laptop!".encode())
                    else:
                        sockets_activas.remove(sock)
                        sock.close()
                except:
                    sockets_activas.remove(sock)
                    sock.close()


# ---------- EJECUCIÓN EN PARALELO ----------
if __name__ == "__main__":
    import threading

    hilo_udp = threading.Thread(target=servidor_udp)
    hilo_tcp = threading.Thread(target=servidor_tcp)

    hilo_udp.start()
    hilo_tcp.start()

    hilo_udp.join()
    hilo_tcp.join()