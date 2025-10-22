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


class DistribucionBinomialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribución Discreta Binomial")
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("750x650")

        # ---- Panel de entrada ----
        frame_inputs = tk.Frame(root, bg=PANEL, padx=10, pady=10)
        frame_inputs.pack(pady=10, fill="x")

        tk.Label(frame_inputs, text="Intentos (n):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=0, padx=5, pady=5)
        self.entry_n = tk.Entry(frame_inputs, width=10)
        self.entry_n.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Probabilidad (p):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=2, padx=5, pady=5)
        self.entry_p = tk.Entry(frame_inputs, width=10)
        self.entry_p.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_inputs, text="Muestras (m):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=4, padx=5, pady=5)
        self.entry_m = tk.Entry(frame_inputs, width=10)
        self.entry_m.grid(row=0, column=5, padx=5, pady=5)

        self.btn_generar = tk.Button(
            frame_inputs,
            text="Generar",
            bg=BTN_BG,
            activebackground=BTN_ACTIVE,
            fg=FG_TEXT,
            command=self.generar_datos
        )
        self.btn_generar.grid(row=0, column=6, padx=10, pady=5)

        # ---- Tabla ----
        frame_tabla = tk.Frame(root, bg=PANEL, padx=10, pady=10)
        frame_tabla.pack(pady=10, fill="both", expand=True)

        columnas = ("#", "Valor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        self.tabla.heading("#", text="#")
        self.tabla.heading("Valor", text="Valor")
        self.tabla.column("#", width=60, anchor="center")
        self.tabla.column("Valor", width=100, anchor="center")

        # Estilo tabla
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

    def generar_datos(self):
        try:
            n = int(self.entry_n.get())
            p = float(self.entry_p.get())
            m = int(self.entry_m.get())

            if n <= 0:
                messagebox.showerror("Error", "El número de intentos (n) debe ser mayor que 0.")
                return
            if not (0 <= p <= 1):
                messagebox.showerror("Error", "La probabilidad (p) debe estar entre 0 y 1.")
                return
            if m <= 0:
                messagebox.showerror("Error", "El número de muestras (m) debe ser mayor que 0.")
                return

            # Generar datos de distribución binomial
            valores = [sum(1 if random.random() < p else 0 for _ in range(n)) for _ in range(m)]

            # Limpiar tabla
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)

            # Insertar en tabla
            for i, valor in enumerate(valores, start=1):
                self.tabla.insert("", "end", values=(i, valor))

            # Mostrar histograma
            self.mostrar_histograma(valores, n)

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    def mostrar_histograma(self, valores, n):
        # Borrar gráfico previo
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6.5, 3.5), facecolor=PANEL)
        ax.hist(valores, bins=range(0, n + 2), align="left", rwidth=0.8, color=BTN_BG, edgecolor=FG_TEXT)
        ax.set_title("Histograma de la Distribución Binomial", color=FG_TEXT)
        ax.set_xlabel("Número de éxitos", color=FG_TEXT)
        ax.set_ylabel("Frecuencia", color=FG_TEXT)
        ax.tick_params(colors=FG_TEXT)
        fig.tight_layout()
        ax.set_facecolor(BG_MAIN)

        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)


# ---- Ejecución principal ----
if __name__ == "__main__":
    root = tk.Tk()
    app = DistribucionBinomialApp(root)
    root.mainloop()
