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


class DistribucionBernoulliApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribución Discreta Bernoulli")
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("700x600")

        # ---- Panel de entrada ----
        frame_inputs = tk.Frame(root, bg=PANEL, padx=10, pady=10)
        frame_inputs.pack(pady=10, fill="x")

        tk.Label(frame_inputs, text="Media (p):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=0, padx=5, pady=5)
        self.entry_media = tk.Entry(frame_inputs, width=10)
        self.entry_media.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Cantidad (n):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=2, padx=5, pady=5)
        self.entry_n = tk.Entry(frame_inputs, width=10)
        self.entry_n.grid(row=0, column=3, padx=5, pady=5)

        self.btn_generar = tk.Button(
            frame_inputs,
            text="Generar",
            bg=BTN_BG,
            activebackground=BTN_ACTIVE,
            fg=FG_TEXT,
            command=self.generar_datos
        )
        self.btn_generar.grid(row=0, column=4, padx=10, pady=5)

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

    def generar_datos(self):
        try:
            media = float(self.entry_media.get())
            n = int(self.entry_n.get())

            if not (0 <= media <= 1):
                messagebox.showerror("Error", "La media debe estar entre 0 y 1.")
                return
            if n <= 0:
                messagebox.showerror("Error", "n debe ser mayor que 0.")
                return

            # Generar datos de la distribución de Bernoulli
            valores = [0 if random.random() < (1 - media) else 1 for _ in range(n)]

            # Limpiar tabla
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)

            # Insertar nuevos valores
            for i, valor in enumerate(valores, start=1):
                self.tabla.insert("", "end", values=(i, valor))

            # Dibujar histograma
            self.mostrar_histograma(valores)

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos (numéricos).")

    def mostrar_histograma(self, valores):
        # Borrar gráfico previo si existe
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6, 3), facecolor=PANEL)
        ax.hist(valores, bins=[-0.5, 0.5, 1.5], rwidth=0.8, color=BTN_BG, edgecolor=FG_TEXT)
        ax.set_xticks([0, 1])
        ax.set_title("Histograma de la Distribución Bernoulli", color=FG_TEXT)
        ax.set_xlabel("Valor", color=FG_TEXT)
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
    app = DistribucionBernoulliApp(root)
    root.mainloop()
