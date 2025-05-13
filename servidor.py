import socket
import threading
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# ---------- CONFIGURACIÓN DE AUDIO (pycaw) ----------
dispositivos = AudioUtilities.GetSpeakers()
interfaz = dispositivos.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
control_volumen = interfaz.QueryInterface(IAudioEndpointVolume)

def obtener_volumen_actual():
    return round(control_volumen.GetMasterVolumeLevelScalar() * 100)

def establecer_volumen(valor):
    control_volumen.SetMasterVolumeLevelScalar(valor / 100, None)

def cambiar_volumen(comando):
    volumen_actual = obtener_volumen_actual()
    if comando == "VOLUMEN_ARRIBA" and volumen_actual < 100:
        volumen_actual = min(100, volumen_actual + 2)
    elif comando == "VOLUMEN_ABAJO" and volumen_actual > 0:
        volumen_actual = max(0, volumen_actual - 2)
    establecer_volumen(volumen_actual)
    return volumen_actual

# ---------- MANEJO DE CLIENTES TCP ----------
def manejar_cliente_tcp(conn, addr):
    try:
        print(f"[TCP] Conexión de {addr}")
        mensaje = conn.recv(1024).decode().strip()
        print(f"[TCP] Comando recibido: {mensaje}")

        if mensaje in ["VOLUMEN_ARRIBA", "VOLUMEN_ABAJO"]:
            nuevo_volumen = cambiar_volumen(mensaje)
            respuesta = f"✅ Volumen actualizado: {nuevo_volumen}%"
        else:
            respuesta = "❌ Comando desconocido"

        conn.send(respuesta.encode())
    except Exception as e:
        print(f"[ERROR TCP] {e}")
        conn.send(f"❌ Error interno: {e}".encode())
    finally:
        conn.close()

# ---------- SERVIDOR TCP ----------
def iniciar_servidor_tcp():
    HOST = ""
    PORT = 12345

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((HOST, PORT))
    servidor_socket.listen(5)
    print(f"[TCP] Servidor escuchando en el puerto {PORT}...")

    while True:
        conn, addr = servidor_socket.accept()
        hilo = threading.Thread(target=manejar_cliente_tcp, args=(conn, addr), daemon=True)
        hilo.start()

# ---------- SERVIDOR UDP (DESCUBRIMIENTO) ----------
def iniciar_servidor_udp():
    HOST = ""
    PORT = 50000

    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind((HOST, PORT))
    print(f"[UDP] Servidor escuchando descubrimientos en el puerto {PORT}...")

    while True:
        try:
            data, addr = sock_udp.recvfrom(1024)
            mensaje = data.decode().strip()
            if mensaje == "DESCUBRIR_SERVIDOR":
                print(f"[UDP] Descubrimiento desde {addr}")
                sock_udp.sendto("SERVIDOR_DISPONIBLE".encode(), addr)
        except Exception as e:
            print(f"[ERROR UDP] {e}")

# ---------- PROGRAMA PRINCIPAL ----------
if __name__ == "__main__":
    print("[🟢] Servidor de volumen iniciando...")

    hilo_udp = threading.Thread(target=iniciar_servidor_udp, daemon=True)
    hilo_tcp = threading.Thread(target=iniciar_servidor_tcp, daemon=True)

    hilo_udp.start()
    hilo_tcp.start()

    try:
        while True:
            pass  
    except KeyboardInterrupt:
        print("\n[🚪] Servidor detenido manualmente.")
