import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ----- Colores -----
BG_MAIN = "#071422"
PANEL = "#0b2433"
BTN_BG = "#0f3a53"
BTN_ACTIVE = "#186a96"
FG_TEXT = "#dbeefc"
TABLE_BG = "#0b2433"
TABLE_FG = "#e8f4ff"


class DistribucionUniformeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribución Discreta Uniforme")
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("700x600")

        # ---- Panel superior de entrada ----
        frame_inputs = tk.Frame(root, bg=PANEL, padx=10, pady=10)
        frame_inputs.pack(pady=10, fill="x")

        tk.Label(frame_inputs, text="Mínimo (b):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=0, padx=5, pady=5)
        self.entry_b = tk.Entry(frame_inputs, width=10)
        self.entry_b.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Máximo (a):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=2, padx=5, pady=5)
        self.entry_a = tk.Entry(frame_inputs, width=10)
        self.entry_a.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_inputs, text="Cantidad (n):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=4, padx=5, pady=5)
        self.entry_n = tk.Entry(frame_inputs, width=10)
        self.entry_n.grid(row=0, column=5, padx=5, pady=5)

        self.btn_generar = tk.Button(
            frame_inputs,
            text="Generar",
            bg=BTN_BG,
            activebackground=BTN_ACTIVE,
            fg=FG_TEXT,
            command=self.generar_numeros
        )
        self.btn_generar.grid(row=0, column=6, padx=10, pady=5)

        # ---- Tabla de resultados ----
        frame_tabla = tk.Frame(root, bg=PANEL, padx=10, pady=10)
        frame_tabla.pack(pady=10, fill="both", expand=True)

        columnas = ("#", "Valor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
        self.tabla.heading("#", text="#")
        self.tabla.heading("Valor", text="Valor")
        self.tabla.column("#", width=50, anchor="center")
        self.tabla.column("Valor", width=100, anchor="center")

        # Estilo de tabla
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background=TABLE_BG, foreground=TABLE_FG, fieldbackground=TABLE_BG, rowheight=25)
        estilo.map("Treeview", background=[("selected", BTN_ACTIVE)])

        self.tabla.pack(fill="both", expand=True)

        # ---- Gráfico ----
        frame_grafico = tk.Frame(root, bg=PANEL, padx=10, pady=10)
        frame_grafico.pack(pady=10, fill="both", expand=True)
        self.frame_grafico = frame_grafico
        self.canvas_grafico = None

    def generar_numeros(self):
        try:
            b = int(self.entry_b.get())
            a = int(self.entry_a.get())
            n = int(self.entry_n.get())

            if b > a:
                messagebox.showerror("Error", "El mínimo (b) no puede ser mayor que el máximo (a).")
                return
            if n <= 0:
                messagebox.showerror("Error", "n debe ser mayor que 0.")
                return

            # Generar números aleatorios uniformes discretos
            valores = [random.randint(b, a) for _ in range(n)]

            # Limpiar tabla
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)

            # Insertar en tabla
            for i, valor in enumerate(valores, start=1):
                self.tabla.insert("", "end", values=(i, valor))

            # Dibujar histograma
            self.mostrar_histograma(valores, a, b)

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    def mostrar_histograma(self, valores, a, b):
        # Borrar gráfico previo si existe
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6, 3), facecolor=PANEL)
        ax.hist(valores, bins=range(b, a + 2), color=BTN_BG, edgecolor=FG_TEXT)
        ax.set_title("Histograma de la Distribución", color=FG_TEXT)
        ax.set_xlabel("Valores", color=FG_TEXT)
        ax.set_ylabel("Frecuencia", color=FG_TEXT)
        ax.tick_params(colors=FG_TEXT)
        fig.tight_layout()

        # Aplicar fondo oscuro
        ax.set_facecolor(BG_MAIN)

        # Mostrar en Tkinter
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)


# ---- Ejecución principal ----
if __name__ == "__main__":
    root = tk.Tk()
    app = DistribucionUniformeApp(root)
    root.mainloop()
