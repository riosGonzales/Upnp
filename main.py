import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ControlVolumen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.ip_servidor = None

        self.label_estado = Label(text="🔍 Presiona para descubrir servidor", size_hint=(1, 0.2))
        self.add_widget(self.label_estado)

        btn_descubrir = Button(text="🔎 Descubrir Servidor", size_hint=(1, 0.2))
        btn_descubrir.bind(on_press=self.descubrir_servidor)
        self.add_widget(btn_descubrir)

        btn_subir = Button(text="🔊 Volumen Arriba", size_hint=(1, 0.2))
        btn_subir.bind(on_press=lambda x: self.enviar_comando("VOLUMEN_ARRIBA"))
        self.add_widget(btn_subir)

        btn_bajar = Button(text="🔉 Volumen Abajo", size_hint=(1, 0.2))
        btn_bajar.bind(on_press=lambda x: self.enviar_comando("VOLUMEN_ABAJO"))
        self.add_widget(btn_bajar)

    def descubrir_servidor(self, instance):
        mensaje = "DESCUBRIR_SERVIDOR"
        direccion_broadcast = ("255.255.255.255", 50000)

        try:
            sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock_udp.settimeout(3)
            sock_udp.sendto(mensaje.encode(), direccion_broadcast)

            respuesta, addr = sock_udp.recvfrom(1024)
            if respuesta.decode() == "SERVIDOR_DISPONIBLE":
                self.ip_servidor = addr[0]
                self.label_estado.text = f"✅ Servidor: {self.ip_servidor}"
            else:
                self.label_estado.text = "❌ Respuesta no válida"
        except Exception as e:
            self.label_estado.text = f"❌ Error: {e}"
        finally:
            sock_udp.close()

    def enviar_comando(self, comando):
        if not self.ip_servidor:
            self.label_estado.text = "⚠️ Descubre el servidor primero"
            return

        try:
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tcp.connect((self.ip_servidor, 12345))
            sock_tcp.send(comando.encode())
            respuesta = sock_tcp.recv(1024).decode()
            self.label_estado.text = f"📶 {respuesta}"
            sock_tcp.close()
        except Exception as e:
            self.label_estado.text = f"❌ Error TCP: {e}"

class VolumenApp(App):
    def build(self):
        return ControlVolumen()

if __name__ == "__main__":
    VolumenApp().run()
