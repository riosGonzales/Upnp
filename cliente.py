import socket
import tkinter as tk
from tkinter import ttk, messagebox

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

# ---------- CONFIGURACIÓN DE AUDIO DE WINDOWS ----------
def obtener_control_volumen():
    dispositivos = AudioUtilities.GetSpeakers()
    interfaz = dispositivos.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interfaz.QueryInterface(IAudioEndpointVolume)

def obtener_volumen_actual():
    return round(control_volumen.GetMasterVolumeLevelScalar() * 100)

def establecer_volumen(valor):
    control_volumen.SetMasterVolumeLevelScalar(valor / 100, None)

# ---------- DESCUBRIMIENTO DEL SERVIDOR POR UDP ----------
def descubrir_servidor():
    mensaje = "DESCUBRIR_SERVIDOR"
    direccion_broadcast = ("255.255.255.255", 50000)
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock_udp.settimeout(3)

    try:
        sock_udp.sendto(mensaje.encode(), direccion_broadcast)
        respuesta, addr = sock_udp.recvfrom(1024)
        if respuesta.decode() == "SERVIDOR_DISPONIBLE":
            return addr[0]
    except socket.timeout:
        return None
    finally:
        sock_udp.close()

# ---------- ENVÍO DE COMANDO POR TCP Y CAMBIO DE VOLUMEN ----------
def enviar_comando(ip_servidor, comando):
    global nivel_volumen
    PORT = 12345
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((ip_servidor, PORT))
        sock_tcp.send(comando.encode())
        sock_tcp.recv(1024)
        sock_tcp.close()

        # Cambiar volumen real
        if comando == "VOLUMEN_ARRIBA" and nivel_volumen < 100:
            nivel_volumen = min(100, nivel_volumen + 2)
        elif comando == "VOLUMEN_ABAJO" and nivel_volumen > 0:
            nivel_volumen = max(0, nivel_volumen - 2)

        establecer_volumen(nivel_volumen)
        actualizar_barra()
    except Exception as e:
        print(f"[TCP] Error: {e}")

# ---------- ACTUALIZAR LA BARRA DE GUI ----------
def actualizar_barra():
    barra_volumen["value"] = nivel_volumen
    etiqueta_valor.config(text=f"{nivel_volumen}")

def verificar_cambios_volumen():
        global nivel_volumen
        nuevo_valor = obtener_volumen_actual()
        if nuevo_valor != nivel_volumen:
            nivel_volumen = nuevo_valor
            actualizar_barra()
        ventana.after(200, verificar_cambios_volumen) 

# ---------- GUI PRINCIPAL ----------
def iniciar_gui(ip_servidor):
    global barra_volumen, etiqueta_valor, nivel_volumen

    ventana = tk.Tk()
    ventana.title("Control de Volumen")
    ventana.geometry("300x200")
    ventana.resizable(False, False)

    etiqueta = tk.Label(ventana, text=f"Servidor conectado: {ip_servidor}", fg="green")
    etiqueta.pack(pady=10)

    barra_volumen = ttk.Progressbar(ventana, length=200, maximum=100)
    barra_volumen.pack(pady=5)

    etiqueta_valor = tk.Label(ventana, text="", font=("Arial", 12, "bold"))
    etiqueta_valor.pack()

    tk.Button(ventana, text="🔊 Volumen Arriba", width=25,
              command=lambda: enviar_comando(ip_servidor, "VOLUMEN_ARRIBA")).pack(pady=5)
    tk.Button(ventana, text="🔉 Volumen Abajo", width=25,
              command=lambda: enviar_comando(ip_servidor, "VOLUMEN_ABAJO")).pack(pady=5)
    tk.Button(ventana, text="❌ Salir", width=25, command=ventana.destroy).pack(pady=10)

    actualizar_barra()

    def verificar_cambios_volumen():
        global nivel_volumen
        nuevo_valor = obtener_volumen_actual()
        if abs(nuevo_valor - nivel_volumen) >= 1:
            nivel_volumen = nuevo_valor
            actualizar_barra()
        ventana.after(200, verificar_cambios_volumen)

    verificar_cambios_volumen()

    ventana.mainloop()

# ---------- PROGRAMA PRINCIPAL ----------
if __name__ == "__main__":
    # Obtener control de volumen de Windows
    control_volumen = obtener_control_volumen()
    nivel_volumen = obtener_volumen_actual()

    ip_servidor = descubrir_servidor()

    if ip_servidor:
        iniciar_gui(ip_servidor)
    else:
        tk.Tk().withdraw()
        messagebox.showerror("Servidor no encontrado", "No se encontró el servidor en la red local.")
