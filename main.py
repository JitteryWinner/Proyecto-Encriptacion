import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from Encriptacion import convertirentero, desencriptar, encriptar, resumirproceso


class AplicacionRSA:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Proyecto de criptografia RSA")
        ventana.geometry("880x780")
        ventana.minsize(740, 680)
        ventana.columnconfigure(0, weight=1)
        ventana.rowconfigure(0, weight=1)

        self.p = tk.StringVar(ventana)
        self.q = tk.StringVar(ventana)
        self.e = tk.StringVar(ventana)
        self.mensaje = tk.StringVar(ventana)
        self.cifrado_entrada = tk.StringVar(ventana)
        self.longitud_entrada = tk.StringVar(ventana)
        self.cifrado_salida = tk.StringVar(ventana)
        self.longitud_salida = tk.StringVar(ventana)
        self.mensaje_salida = tk.StringVar(ventana)
        self.estado = tk.StringVar(ventana, value="Listo.")

        marco = ttk.Frame(ventana, padding=12)
        marco.grid(row=0, column=0, sticky="nsew")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(4, weight=1)
        ttk.Label(marco, text="Encriptacion y desencriptacion RSA",
                  font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w")

        parametros = ttk.LabelFrame(marco, text="Parametros RSA compartidos", padding=10)
        parametros.grid(row=1, column=0, sticky="ew", pady=(10, 12))
        for columna, (nombre, variable) in enumerate((("p", self.p), ("q", self.q), ("e", self.e))):
            ttk.Label(parametros, text=nombre + ":").grid(row=0, column=columna * 2)
            ttk.Entry(parametros, textvariable=variable, width=14).grid(
                row=0, column=columna * 2 + 1, sticky="ew", padx=(4, 12))
            parametros.columnconfigure(columna * 2 + 1, weight=1)
        ttk.Button(parametros, text="Cargar ejemplo", command=self.cargar_ejemplo).grid(
            row=0, column=6)

        self.pestanas = ttk.Notebook(marco)
        self.pestanas.grid(row=2, column=0, sticky="ew")
        cifrar = ttk.Frame(self.pestanas, padding=12)
        descifrar = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(cifrar, text="Encriptar")
        self.pestanas.add(descifrar, text="Desencriptar")
        for pestana in (cifrar, descifrar):
            pestana.columnconfigure(0, weight=1)

        ttk.Label(cifrar, text="Mensaje M (ASCII imprimible; se conservan todos los espacios):").grid(
            row=0, column=0, sticky="w")
        ttk.Entry(cifrar, textvariable=self.mensaje).grid(
            row=1, column=0, sticky="ew", pady=(4, 8))
        ttk.Button(cifrar, text="Encriptar", command=lambda: self.ejecutar("encriptar")).grid(
            row=2, column=0, sticky="w", pady=(0, 8))
        ttk.Label(cifrar, text="Cifrado C (puedes seleccionarlo y copiarlo):").grid(
            row=3, column=0, sticky="w")
        ttk.Entry(cifrar, textvariable=self.cifrado_salida, state="readonly").grid(
            row=4, column=0, sticky="ew", pady=4)
        ttk.Label(cifrar, text="Longitud original L:").grid(row=5, column=0, sticky="w")
        ttk.Entry(cifrar, textvariable=self.longitud_salida, state="readonly", width=14).grid(
            row=6, column=0, sticky="w", pady=4)
        ttk.Label(cifrar, text="C y L se copian tambien a la pestana Desencriptar.").grid(
            row=7, column=0, sticky="w")

        ttk.Label(descifrar, text="Cifrado C (bloques de seis digitos separados por un espacio):").grid(
            row=0, column=0, sticky="w")
        ttk.Entry(descifrar, textvariable=self.cifrado_entrada).grid(
            row=1, column=0, sticky="ew", pady=(4, 8))
        ttk.Label(descifrar, text="Longitud original L:").grid(row=2, column=0, sticky="w")
        ttk.Entry(descifrar, textvariable=self.longitud_entrada, width=14).grid(
            row=3, column=0, sticky="w", pady=4)
        ttk.Button(descifrar, text="Desencriptar",
                   command=lambda: self.ejecutar("desencriptar")).grid(
            row=4, column=0, sticky="w", pady=(4, 8))
        ttk.Label(descifrar, text="Mensaje recuperado M:").grid(row=5, column=0, sticky="w")
        ttk.Entry(descifrar, textvariable=self.mensaje_salida, state="readonly").grid(
            row=6, column=0, sticky="ew", pady=4)

        ttk.Label(marco, text="Detalle del proceso (las comillas permiten distinguir los espacios):").grid(
            row=3, column=0, sticky="w", pady=(12, 4))
        self.detalle = ScrolledText(marco, height=14, wrap="word",
                                   font=("Consolas", 10), state="disabled")
        self.detalle.grid(row=4, column=0, sticky="nsew")
        ttk.Label(marco, textvariable=self.estado, wraplength=700).grid(
            row=5, column=0, sticky="w", pady=(8, 0))

    def mostrar_detalle(self, texto):
        self.detalle.configure(state="normal")
        self.detalle.delete("1.0", tk.END)
        self.detalle.insert("1.0", texto)
        self.detalle.configure(state="disabled")

    def cargar_ejemplo(self):
        self.p.set("367")
        self.q.set("373")
        self.e.set("17")
        self.mensaje.set("RSA")
        for variable in (self.cifrado_entrada, self.longitud_entrada, self.cifrado_salida,
                         self.longitud_salida, self.mensaje_salida):
            variable.set("")
        self.mostrar_detalle("")
        self.estado.set("Ejemplo cargado. Presiona Encriptar para iniciar.")
        self.pestanas.select(0)

    def ejecutar(self, operacion):
        self.mostrar_detalle("")
        if operacion == "encriptar":
            self.cifrado_salida.set("")
            self.longitud_salida.set("")
            self.mensaje_salida.set("")
        else:
            self.mensaje_salida.set("")
        try:
            p = convertirentero(self.p.get(), "p")
            q = convertirentero(self.q.get(), "q")
            e = convertirentero(self.e.get(), "e")
            if operacion == "encriptar":
                datos = encriptar(self.mensaje.get(), p, q, e)
                self.cifrado_salida.set(datos["cifrado"])
                self.longitud_salida.set(str(datos["L"]))
                self.cifrado_entrada.set(datos["cifrado"])
                self.longitud_entrada.set(str(datos["L"]))
            else:
                longitud = convertirentero(self.longitud_entrada.get(), "L")
                datos = desencriptar(self.cifrado_entrada.get(), longitud, p, q, e)
                self.mensaje_salida.set(datos["mensaje"])
        except ValueError as error:
            self.estado.set("Error: " + str(error))
            messagebox.showerror("Datos invalidos", str(error), parent=self.ventana)
            return
        self.mostrar_detalle(resumirproceso(datos))
        self.estado.set("Operacion completada.")


def main():
    ventana = tk.Tk()
    AplicacionRSA(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
