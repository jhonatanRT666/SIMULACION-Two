import tkinter as tk
from tkinter import ttk, messagebox
import random

class JuegoVidaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de la Vida - Conway")
        self.root.geometry("900x720")
        self.root.configure(bg="#113E79")  # Fondo azul oscuro moderno

        # === Estilo oscuro azulado ===
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        background="#1F6FEB",
                        foreground="#E6EDF3",
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0,
                        padding=6)
        style.map("TButton",
                  background=[("active", "#238636")])
        style.configure("TLabel", background="#0D1117", foreground="#E6EDF3", font=("Segoe UI", 10))

        # === Configuración del tablero ===
        self.filas = 30
        self.columnas = 50
        self.tam_celda = 15
        self.velocidad = 200
        self.ejecutando = False
        self.tablero = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]

        self.crear_interfaz()

    def crear_interfaz(self):
        # ======= Título =======
        title_frame = tk.Frame(self.root, bg="#0D1117")
        title_frame.pack(pady=15)
        tk.Label(
            title_frame,
            text="🧬 Juego de la Vida - Conway",
            font=("Segoe UI", 20, "bold"),
            fg="#58A6FF",
            bg="#0D1117"
        ).pack()

        # ======= Marco de controles =======
        control_frame = tk.Frame(self.root, bg="#161B22", relief="ridge", bd=2)
        control_frame.pack(pady=15, padx=10, fill="x")

        # Columna izquierda (botones)
        left_controls = tk.Frame(control_frame, bg="#161B22")
        left_controls.pack(side=tk.LEFT, padx=20, pady=10)

        ttk.Button(left_controls, text="▶️ Iniciar / Pausar", command=self.toggle_simulacion).pack(pady=5, fill="x")
        ttk.Button(left_controls, text="🧹 Limpiar", command=self.limpiar).pack(pady=5, fill="x")
        ttk.Button(left_controls, text="🎲 Aleatorio", command=self.aleatorio).pack(pady=5, fill="x")
        ttk.Button(left_controls, text="❌ Salir", command=self.root.quit).pack(pady=5, fill="x")

        # Columna central (configuración de velocidad)
        center_controls = tk.Frame(control_frame, bg="#161B22")
        center_controls.pack(side=tk.LEFT, padx=40, pady=10)

        ttk.Label(center_controls, text="Velocidad (ms):", background="#161B22").pack(pady=5)
        self.velocidad_var = tk.IntVar(value=200)
        velocidad_entry = tk.Entry(center_controls,
                                   textvariable=self.velocidad_var,
                                   width=8,
                                   bg="#21262D",
                                   fg="#E6EDF3",
                                   insertbackground="#E6EDF3",
                                   relief="flat",
                                   justify="center")
        velocidad_entry.pack()

        # Columna derecha (indicaciones)
        right_controls = tk.Frame(control_frame, bg="#161B22")
        right_controls.pack(side=tk.RIGHT, padx=20, pady=10)

        tk.Label(
            right_controls,
            text="📋 Instrucciones:",
            font=("Segoe UI", 10, "bold"),
            fg="#58A6FF",
            bg="#161B22"
        ).pack(anchor="w")

        instrucciones = (
            "• Haz clic en las celdas para activarlas.\n"
            "• Presiona 'Iniciar / Pausar' para ejecutar.\n"
            "• Usa 'Limpiar' para reiniciar.\n"
            "• Usa 'Aleatorio' para generar un patrón.\n"
            "• Ajusta la velocidad (ms)."
        )
        tk.Label(
            right_controls,
            text=instrucciones,
            justify="left",
            bg="#161B22",
            fg="#E6EDF3",
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        # ======= Canvas del tablero =======
        frame_tablero = tk.Frame(self.root, bg="#0D1117")
        frame_tablero.pack(pady=10)
        self.canvas = tk.Canvas(
            frame_tablero,
            width=self.columnas * self.tam_celda,
            height=self.filas * self.tam_celda,
            bg="#0D1117",
            highlightthickness=1,
            highlightbackground="#30363D"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_celda)

        # ======= Estado =======
        self.estado_label = tk.Label(
            self.root,
            text="Estado: Pausado",
            bg="#0D1117",
            fg="#E6EDF3",
            font=("Segoe UI", 10, "italic")
        )
        self.estado_label.pack(pady=5)

        self.dibujar_tablero()

    # ======= Lógica del juego =======
    def click_celda(self, event):
        if self.ejecutando:
            return
        col = event.x // self.tam_celda
        fila = event.y // self.tam_celda
        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            self.tablero[fila][col] = 1 - self.tablero[fila][col]
            self.dibujar_tablero()

    def contar_vecinos(self, fila, col):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                f = (fila + i) % self.filas
                c = (col + j) % self.columnas
                total += self.tablero[f][c]
        return total

    def siguiente_generacion(self):
        nuevo_tablero = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                vecinos = self.contar_vecinos(i, j)
                if self.tablero[i][j] == 1:
                    if vecinos == 2 or vecinos == 3:
                        nuevo_tablero[i][j] = 1
                else:
                    if vecinos == 3:
                        nuevo_tablero[i][j] = 1
        self.tablero = nuevo_tablero

    def actualizar(self):
        if self.ejecutando:
            self.siguiente_generacion()
            self.dibujar_tablero()
            try:
                self.velocidad = int(self.velocidad_var.get())
            except:
                self.velocidad = 200
            self.root.after(self.velocidad, self.actualizar)

    def toggle_simulacion(self):
        self.ejecutando = not self.ejecutando
        self.estado_label.config(
            text="Estado: Ejecutando" if self.ejecutando else "Estado: Pausado",
            fg="#58A6FF" if self.ejecutando else "#E6EDF3"
        )
        if self.ejecutando:
            self.actualizar()

    def limpiar(self):
        self.ejecutando = False
        self.tablero = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.estado_label.config(text="Estado: Pausado", fg="#E6EDF3")
        self.dibujar_tablero()

    def aleatorio(self):
        self.ejecutando = False
        for i in range(self.filas):
            for j in range(self.columnas):
                self.tablero[i][j] = random.choice([0, 1])
        self.estado_label.config(text="Estado: Pausado", fg="#E6EDF3")
        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i in range(self.filas):
            for j in range(self.columnas):
                x1 = j * self.tam_celda
                y1 = i * self.tam_celda
                x2 = x1 + self.tam_celda
                y2 = y1 + self.tam_celda
                color = "#58A6FF" if self.tablero[i][j] == 1 else "#0D1117"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#30363D")


# ======= Ejecutar =======
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoVidaApp(root)
    root.mainloop()
