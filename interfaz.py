import tkinter as tk
import threading
from detector_fatiga import iniciar_detector

def iniciar():
    hilo = threading.Thread(target=iniciar_detector)
    hilo.daemon = True
    hilo.start()

def salir():
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Sistema de Detección de Fatiga")
ventana.geometry("400x200")

titulo = tk.Label(ventana, text="Detector de Fatiga para Conductores", font=("Helvetica", 14))
titulo.pack(pady=20)

btn_iniciar = tk.Button(ventana, text="Iniciar Monitoreo", command=iniciar, width=25, bg="green", fg="white")
btn_iniciar.pack(pady=10)

btn_salir = tk.Button(ventana, text="Salir", command=salir, width=25, bg="red", fg="white")
btn_salir.pack(pady=10)

ventana.mainloop()
