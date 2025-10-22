#!/usr/bin/env python3
"""
Distribución Uniforme (Oscuro-Azulado)
Autor: Jhonatan — Ingeniería de Sistemas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt


# ----- Colores y estilo -----
BG_MAIN = "#071422"
PANEL = "#0b2433"
BTN_BG = "#0f3a53"
BTN_ACTIVE = "#186a96"
FG_TEXT = "#dbeefc"
TABLE_BG = "#0b2433"
TABLE_FG = "#e8f4ff"


class DistribucionUniforme:
    """Clase que genera números según la fórmula: a + (b - a) * r"""

    def __init__(self, a, b, n):
        self.a = a
        self.b = b
        self.n = n

    def generar(self):
        """Genera n valores aleatorios uniformes"""
        resultados = []
        for _ in range(self.n):
            r = random.random()  # número aleatorio entre 0 y 1
            x = self.a + (self.b - self.a) * r
            resultados.append(round(x, 4))
        return resultados


class UniformeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribución Uniforme — Estilo Oscuro-Azulado")
        self.root.configure(bg=BG_MAIN)

        self._build_ui()

    def _build_ui(self):
        # ----- Panel superior -----
        frame_top = tk.Frame(self.root, bg=PANEL, pady=10, padx=10)
        frame_top.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_top, text="a (mínimo):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=0, padx=6, pady=4)
        self.entry_a = ttk.Entry(frame_top, width=10)
        self.entry_a.grid(row=0, column=1, padx=6)

        tk.Label(frame_top, text="b (máximo):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=2, padx=6, pady=4)
        self.entry_b = ttk.Entry(frame_top, width=10)
        self.entry_b.grid(row=0, column=3, padx=6)

        tk.Label(frame_top, text="n (cantidad):", bg=PANEL, fg=FG_TEXT).grid(row=0, column=4, padx=6, pady=4)
        self.entry_n = ttk.Entry(frame_top, width=10)
        self.entry_n.grid(row=0, column=5, padx=6)

        btn_generar = tk.Button(frame_top, text="Generar", bg=BTN_BG, fg=FG_TEXT,
                                activebackground=BTN_ACTIVE, width=10, command=self.generar)
        btn_generar.grid(row=0, column=6, padx=10)

        # ----- Tabla -----
        frame_tabla = tk.Frame(self.root, bg=BG_MAIN)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=("valor",), show="headings", height=10)
        self.tabla.heading("valor", text="Valores Generados")
        self.tabla.column("valor", anchor="center", width=180)
        self.tabla.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", background=TABLE_BG, foreground=TABLE_FG,
                        fieldbackground=TABLE_BG, font=('Consolas', 11))
        style.configure("Treeview.Heading", background=BTN_BG, foreground=FG_TEXT, font=('Consolas', 11, 'bold'))

        # ----- Botón de histograma -----
        frame_hist = tk.Frame(self.root, bg=BG_MAIN, pady=10)
        frame_hist.pack()
        btn_hist = tk.Button(frame_hist, text="Mostrar Histograma", bg=BTN_BG, fg=FG_TEXT,
                             activebackground=BTN_ACTIVE, command=self.mostrar_histograma)
        btn_hist.pack()

        # Almacenar datos
        self.valores = []

    # ----- Generar datos -----
    def generar(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            n = int(self.entry_n.get())

            if b <= a:
                messagebox.showerror("Error", "El valor de b debe ser mayor que a.")
                return
            if n <= 0:
                messagebox.showerror("Error", "n debe ser mayor que 0.")
                return

            dist = DistribucionUniforme(a, b, n)
            self.valores = dist.generar()

            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Insertar nuevos valores
            for val in self.valores:
                self.tabla.insert("", "end", values=(val,))

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

    # ----- Mostrar histograma -----
    def mostrar_histograma(self):
        if not self.valores:
            messagebox.showwarning("Aviso", "Primero genere los valores.")
            return

        plt.style.use('dark_background')
        plt.figure(figsize=(7, 4))
        plt.hist(self.valores, bins=10, edgecolor='#1da1f2', color='#0b486b')
        plt.title("Histograma — Distribución Uniforme", color='#b3e5fc', fontsize=13)
        plt.xlabel("Valores", color='#b3e5fc')
        plt.ylabel("Frecuencia", color='#b3e5fc')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()


# ----- Ejecutar la aplicación -----
if __name__ == "__main__":
    root = tk.Tk()
    app = UniformeApp(root)
    root.geometry("680x500")
    root.minsize(620, 450)
    root.mainloop()
