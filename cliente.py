import socket

# ---------- DESCUBRIMIENTO UDP ----------
UDP_IP = "255.255.255.255"
UDP_PORT = 50000
MENSAJE_DESCUBRIMIENTO = "DESCUBRIR_SERVIDOR"
RESPUESTA_ESPERADA = "SERVIDOR_DISPONIBLE"

cliente_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
cliente_udp.settimeout(5)

print("[🔍] Buscando servidor en la red...")

cliente_udp.sendto(MENSAJE_DESCUBRIMIENTO.encode(), (UDP_IP, UDP_PORT))

try:
    data, addr = cliente_udp.recvfrom(1024)
    if data.decode() == RESPUESTA_ESPERADA:
        ip_servidor = addr[0]
        print(f"[✅] Servidor detectado en {ip_servidor}")
    else:
        print("[❌] Respuesta inesperada")
        exit()
except socket.timeout:
    print("[⚠] No se detectó ningún servidor. ¿Está corriendo el script en tu laptop?")
    exit()

cliente_udp.close()

# ---------- CONEXIÓN TCP ----------
TCP_PORT = 12345
cliente_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente_tcp.connect((ip_servidor, TCP_PORT))
    cliente_tcp.send("¡Hola desde el celular con descubrimiento automático!".encode())
    respuesta = cliente_tcp.recv(1024).decode()
    print(f"[📥] Respuesta del servidor: {respuesta}")
except Exception as e:
    print(f"[❌] Error al conectar por TCP: {e}")
finally:
    cliente_tcp.close()
