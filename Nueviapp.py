import tkinter as tk
from tkinter import messagebox
import json
import os


# === COLORES BASE DEL DISEÑO ===
BG_COLOR = "#AEE1E1"
BTN_COLOR = "#E5F9F7"
TEXT_COLOR = "#1C2B2D"
BTN_HIGHLIGHT = "#F9C0C0"

# === ARCHIVO DE USUARIOS ===
USERS_FILE = "usuarios.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

MOVIMIENTOS_FILE = "movimientos.json"
if not os.path.exists(MOVIMIENTOS_FILE):
    with open(MOVIMIENTOS_FILE, "w") as f:
        json.dump({"ingresos": [], "gastos": []}, f)

def agregar_movimiento(tipo, monto):
    with open(MOVIMIENTOS_FILE, "r") as f:
        datos = json.load(f)
    datos[tipo].append(monto)
    with open(MOVIMIENTOS_FILE, "w") as f:
        json.dump(datos, f)

def calcular_saldo():
    with open(MOVIMIENTOS_FILE, "r") as f:
        datos = json.load(f)
    total_ingresos = sum(datos["ingresos"])
    total_gastos = sum(datos["gastos"])
    return total_ingresos - total_gastos


# === FUNCIONES DE USUARIO ===
def guardar_usuario(usuario, contrasena, correo):
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    if usuario in data:
        return False
    data[usuario] = {"contrasena": contrasena, "correo": correo}
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)
    return True

def validar_usuario(usuario, contrasena):
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    return usuario in data and data[usuario]["contrasena"] == contrasena


# === APLICACIÓN PRINCIPAL ===
class OniomaticApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Oniomatic - Finanzas Estudiantiles")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.current_frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


# === LOGIN ===
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        tk.Label(self, text="Bienvenido a Oniomatic", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)

        tk.Label(self, text="Inicia Sesión", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        self.username = tk.Entry(self, font=("Arial", 12), justify="center")
        self.username.insert(0, "Usuario")
        self.username.bind("<FocusIn>", lambda e: self.limpiar_entry(self.username, "Usuario"))
        self.username.pack(pady=5, ipadx=10, ipady=5)

        self.password = tk.Entry(self, font=("Arial", 12), justify="center")
        self.password.insert(0, "Contraseña")
        self.password.bind("<FocusIn>", lambda e: self.limpiar_entry(self.password, "Contraseña"))
        self.password.pack(pady=5, ipadx=10, ipady=5)

        tk.Button(self, text="Iniciar sesión", bg=BTN_COLOR, command=self.login).pack(pady=8)
        tk.Button(self, text="Registrarse", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(RegisterFrame)).pack(pady=2)
        tk.Button(self, text="¿Olvidaste tu contraseña?", bg=BG_COLOR, fg=TEXT_COLOR, bd=0, command=self.recuperar_contraseña).pack(pady=10)

    def limpiar_entry(self, entry, texto_original):
        if entry.get() == texto_original:
            entry.delete(0, tk.END)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if validar_usuario(user, pwd):
            self.master.switch_frame(MenuPrincipal)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def recuperar_contraseña(self):
        usuario = self.username.get()
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        if usuario in data:
            correo = data[usuario]["correo"]
            messagebox.showinfo("Recuperar contraseña", f"El correo registrado es:\n{correo}\n(Se recomienda contactarte con soporte para resetear la contraseña)")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

#registro
class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        tk.Label(self, text="Regístrate en Oniomatic", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)

        tk.Label(self, text="Crear Cuenta", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        self.username = tk.Entry(self, font=("Arial", 12), justify="center")
        self.username.insert(0, "Nuevo usuario")
        self.username.bind("<FocusIn>", lambda e: self.limpiar_entry(self.username, "Nuevo usuario"))
        self.username.pack(pady=5, ipadx=10, ipady=5)

        self.password = tk.Entry(self, font=("Arial", 12), justify="center")
        self.password.insert(0, "Contraseña")
        self.password.bind("<FocusIn>", lambda e: self.limpiar_entry(self.password, "Contraseña"))
        self.password.pack(pady=5, ipadx=10, ipady=5)

        self.email = tk.Entry(self, font=("Arial", 12), justify="center")
        self.email.insert(0, "Correo electrónico")
        self.email.bind("<FocusIn>", lambda e: self.limpiar_entry(self.email, "Correo electrónico"))
        self.email.pack(pady=5, ipadx=10, ipady=5)

        tk.Button(self, text="Registrar", bg=BTN_COLOR, command=self.registrar).pack(pady=10)
        tk.Button(self, text="Volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(LoginFrame)).pack(pady=5)

    def limpiar_entry(self, entry, texto_original):
        if entry.get() == texto_original:
            entry.delete(0, tk.END)

    def registrar(self):
        user = self.username.get()
        pwd = self.password.get()
        correo = self.email.get()
        if guardar_usuario(user, pwd, correo):
            messagebox.showinfo("Éxito", "Usuario registrado con éxito")
            self.master.switch_frame(LoginFrame)
        else:
            messagebox.showerror("Error", "El usuario ya existe")

# === MENÚ PRINCIPAL ===
class MenuPrincipal(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        # Frame contenedor centrado
        contenedor = tk.Frame(self, bg=BG_COLOR)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")  # centrado en ventana

        tk.Label(contenedor, text="Menú Principal", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        opciones = [
            ("Registrar Gasto", RegistrarGasto),
            ("Registrar Ingreso", RegistrarIngreso),
            ("Ver Inversiones", Inversiones),
            ("Tips Financieros", Tips),
            ("Saldo Actual", SaldoActual),
        ]

        for texto, frame in opciones:
            tk.Button(contenedor, text=texto, width=30, bg=BTN_COLOR,
                      command=lambda f=frame: master.switch_frame(f)).pack(pady=10)


# === GASTO ===
class RegistrarGasto(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="Registrar Gasto", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        self.monto = tk.Entry(self)
        self.monto.insert(0, "Monto")
        self.monto.pack(pady=5)
        self.categoria = tk.Entry(self)
        self.categoria.insert(0, "Categoría")
        self.categoria.pack(pady=5)

        tk.Button(self, text="Siguiente: Emoción", bg=BTN_COLOR, command=self.registrar_gasto).pack(pady=20)
        tk.Button(self, text="Volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(MenuPrincipal)).pack()

    def registrar_gasto(self):
        try:
            monto = float(self.monto.get())
            agregar_movimiento("gastos", monto)
            self.master.switch_frame(Emociones)
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")


# === EMOCIONES ===
class Emociones(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="¿Qué emoción sentiste al comprar?", font=("Helvetica", 14), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        emociones = ["Alegría", "Culpa", "Satisfacción", "Impulsividad", "Tristeza", "Ansiedad"]
        for emo in emociones:
            tk.Button(self, text=emo, bg=BTN_COLOR, width=30, command=self.registrar_emocion).pack(pady=5)

        tk.Button(self, text="Guardar y volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(MenuPrincipal)).pack(pady=20)

    def registrar_emocion(self):
        messagebox.showinfo("Emoción", "Emoción registrada (simulado).")


# === INGRESO ===
class RegistrarIngreso(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="Registrar Ingreso", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        self.monto = tk.Entry(self)
        self.monto.insert(0, "Monto")
        self.monto.pack(pady=5)
        self.fuente = tk.Entry(self)
        self.fuente.insert(0, "Fuente")
        self.fuente.pack(pady=5)

        tk.Button(self, text="Guardar", bg=BTN_COLOR, command=self.guardar).pack(pady=10)
        tk.Button(self, text="Volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(MenuPrincipal)).pack(pady=5)

    def guardar(self):
        try:
            monto = float(self.monto.get())
            agregar_movimiento("ingresos", monto)
            messagebox.showinfo("Ingreso", "Ingreso registrado con éxito.")
            self.master.switch_frame(MenuPrincipal)
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")


# saldo actual
class SaldoActual(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="Saldo Actual", font=("Helvetica", 18), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)

        saldo = calcular_saldo()
        color = "#228B22" if saldo >= 0 else "#B22222"
        texto = f"Tu saldo actual es: ${saldo:.2f} MXN"
        tk.Label(self, text=texto, font=("Helvetica", 16), bg=BG_COLOR, fg=color).pack(pady=10)

        tk.Button(self, text="Volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(MenuPrincipal)).pack(pady=20)



# === INVERSIONES MEJORADAS ===
class Inversiones(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="Opciones de Inversión", font=("Helvetica", 18), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        inversiones = [
            {
                "riesgo": "Bajo",
                "nombre": "CETES",
                "descripcion": "Bonos del gobierno mexicano con rendimiento seguro.",
                "detalles": {
                    "tips": ["Empieza desde $100 MXN", "Elige plazo de 1 a 12 meses"],
                    "riesgos": ["Riesgo muy bajo, casi nulo", "Inflación podría afectar"],
                    "consejos": ["No uses dinero de emergencias", "Reinviértelo automáticamente"],
                    "pasos": ["Abre cuenta en cetesdirecto.com", "Elige monto y plazo", "Confirma inversión"]
                }
            },
            {
                "riesgo": "Medio",
                "nombre": "Fondos de inversión",
                "descripcion": "Fondos gestionados que mezclan bonos y acciones.",
                "detalles": {
                    "tips": ["Revisa la calificación del fondo", "Consulta rendimiento histórico"],
                    "riesgos": ["Rendimiento variable", "Puede perder valor en el corto plazo"],
                    "consejos": ["Invierte a mediano plazo", "Diversifica con otros fondos"],
                    "pasos": ["Ingresa a GBM+, Kuspit u otra", "Selecciona fondo", "Invierte y sigue el desempeño"]
                }
            }
        ]

        for inv in inversiones:
            frame = tk.Frame(self, bg=BTN_COLOR, pady=10, padx=10, relief="raised", bd=1)
            frame.pack(padx=20, pady=10, fill="x")

            riesgo = f"[{inv['riesgo'].upper()} RIESGO]"
            tk.Label(frame, text=riesgo, font=("Helvetica", 10, "bold"), bg=BTN_COLOR, fg="#444").pack(anchor="w")
            tk.Label(frame, text=inv['nombre'], font=("Helvetica", 14), bg=BTN_COLOR, fg=TEXT_COLOR).pack(anchor="w")
            tk.Label(frame, text=inv['descripcion'], wraplength=700, justify="left", bg=BTN_COLOR).pack(anchor="w", pady=5)
            tk.Button(frame, text="Ver más detalles", bg=BTN_HIGHLIGHT,
                      command=lambda d=inv['detalles'], n=inv['nombre']: self.ver_detalles(d, n)).pack(anchor="e", pady=5)

        tk.Button(self, text="Volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(MenuPrincipal)).pack(pady=20)

    def ver_detalles(self, detalles, nombre):
        detalle_ventana = tk.Toplevel(self)
        detalle_ventana.title(f"Detalles - {nombre}")
        detalle_ventana.configure(bg=BG_COLOR)
        detalle_ventana.geometry("600x500")

        tk.Label(detalle_ventana, text=f"Detalles de {nombre}", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        for key, items in detalles.items():
            titulo = key.capitalize()
            tk.Label(detalle_ventana, text=f"{titulo}:", font=("Helvetica", 12, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=5)
            for item in items:
                tk.Label(detalle_ventana, text=f"- {item}", bg=BG_COLOR, wraplength=550, justify="left").pack(anchor="w", padx=40)

        tk.Button(detalle_ventana, text="Cerrar", bg=BTN_HIGHLIGHT, command=detalle_ventana.destroy).pack(pady=20)


# === TIPS FINANCIEROS ===
class Tips(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        tk.Label(self, text="Tips Financieros", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        pasos = [
            "Paso 1: Lleva registro diario de tus gastos.",
            "Paso 2: Define metas mensuales de ahorro.",
            "Paso 3: Usa la regla 50/30/20 para dividir tus ingresos.",
            "Paso 4: Aprende sobre inversión básica."
        ]
        for paso in pasos:
            tk.Label(self, text=paso, bg=BG_COLOR, fg=TEXT_COLOR, wraplength=700, justify="left").pack(pady=5)

        tk.Button(self, text="Volver", bg=BTN_HIGHLIGHT, command=lambda: master.switch_frame(MenuPrincipal)).pack(pady=20)


# === EJECUCIÓN ===
if __name__ == "__main__":
    app = OniomaticApp()
    app.mainloop()

