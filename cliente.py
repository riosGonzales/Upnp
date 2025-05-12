import socket
import cv2
import numpy as np

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
        ip_servidor = addr[0]  # IP obtenida automáticamente desde el descubrimiento UDP
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
    cliente_tcp.connect((ip_servidor, TCP_PORT))  # Conexión usando la IP detectada
    cliente_tcp.send("¡Hola desde el celular con descubrimiento automático!".encode())
    respuesta = cliente_tcp.recv(1024).decode()
    print(f"[📥] Respuesta del servidor: {respuesta}")
except Exception as e:
    print(f"[❌] Error al conectar por TCP: {e}")
finally:
    cliente_tcp.close()

# ---------- ENVÍO DE VIDEO ----------
UDP_PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)  # Usar la cámara predeterminada

while True:
    ret, frame = cap.read()
    if ret:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, encoded_img = cv2.imencode(".jpg", frame, encode_param)
        byte_frame = encoded_img.tobytes()

        # Enviar el paquete por UDP
        sock.sendto(byte_frame, (ip_servidor, UDP_PORT))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
sock.close()
