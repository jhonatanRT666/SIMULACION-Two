import tkinter as tk
from tkinter import ttk, messagebox

from cuadrados_medios1 import CuadradosMediosApp
from Productos_Medios2 import ProductosMediosApp
from Multiplicador_Constante3 import MultiplicadorConstanteApp
from juego_vida import JuegoVidaApp
from rule30_dark import Rule30App
from regla_90 import Regla90App
from uniforme import UniformeApp
from kerlang import KerlangApp
from exponencial import ExponencialApp
from gamma import GammaApp
from normal import NormalApp
from poisson import PoissonApp
from uniforme_discreto import DistribucionUniformeApp
from bernoulli import DistribucionBernoulliApp
from binomial import DistribucionBinomialApp

class MenuCalculadorasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CALCULADORAS DE NÚMEROS PSEUDOALEATORIOS")
        self.root.geometry("950x650")
        self.root.configure(bg="#113E79")

        # 🎨 Estilo personalizado
        style = ttk.Style()
        style.theme_use('clam')

        azul = "#113E79"
        gris = "#3C3F41"
        blanco = "white"
        celeste = "#FFFFFF"

        style.configure("TButton",
                        background=gris,
                        foreground=blanco,
                        font=("Arial", 11, "bold"),
                        padding=10)
        style.map("TButton",
                  background=[("active", "#5A5E60")])

        # 🏷️ Título
        title_label = tk.Label(
            self.root,
            text="CALCULADORAS DE NÚMEROS PSEUDOALEATORIOS",
            font=("Arial", 18, "bold"),
            bg=azul,
            fg=celeste
        )
        title_label.pack(pady=25)

        # 🧩 Contenedor para botones (rejilla de 4 columnas)
        button_frame = tk.Frame(self.root, bg=azul)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=10)

        botones = [
            ("1. Cuadrados Medios", self.abrir_cuadrados_medios),
            ("2. Productos Medios", self.abrir_productos_medios),
            ("3. Multiplicador Constante", self.abrir_multiplicador_constante),
            ("4. Juego de la Vida", self.abrir_juego_vida),
            ("5. Regla de 30", self.abrir_regla_30),
            ("6. Regla de 90", self.abrir_regla_90),
            ("7. Generador Uniforme", self.abrir_generador_uniforme),
            ("8. Prueba Kerland", self.abrir_prueba_kerlan),
            ("9. Generador Exponencial", self.abrir_exponencial),
            ("10. Generador Gamma", self.abrir_generador_gamma),
            ("11. Generador Normal", self.abrir_generador_normal),
            ("12. Generador Poisson", self.abrir_generador_poisson),
            ("13. Uniforme Discreto", self.abrir_generador_uniforme_discreto),
            ("14. Generador Bernoulli", self.abrir_generador_bernoulli),
            ("15. Generador Binomial", self.abrir_generador_binomial),
        ]

        # 🔲 Colocar los botones en una grilla de 4 columnas
        columnas = 4
        for i, (texto, comando) in enumerate(botones):
            fila = i // columnas
            col = i % columnas
            ttk.Button(button_frame, text=texto, command=comando, style="TButton") \
                .grid(row=fila, column=col, padx=10, pady=10, sticky="nsew")

        # Hacer que las columnas crezcan proporcionalmente
        for i in range(columnas):
            button_frame.grid_columnconfigure(i, weight=1)

        # ❌ Botón de salida centrado
        exit_frame = tk.Frame(self.root, bg=azul)
        exit_frame.pack(pady=30)
        ttk.Button(exit_frame, text="❌ CERRAR MENÚ", command=self.root.quit, style="TButton") \
            .pack(pady=10, ipadx=15)

    # ================= FUNCIONES (no modificadas) =================
    def abrir_cuadrados_medios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Algoritmo de Cuadrados Medios")
        CuadradosMediosApp(ventana)

    def abrir_productos_medios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Algoritmo de Productos Medios")
        ProductosMediosApp(ventana)

    def abrir_multiplicador_constante(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Algoritmo de Multiplicador Constante")
        MultiplicadorConstanteApp(ventana)

    def abrir_juego_vida(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Juego de la Vida - Conway")
        JuegoVidaApp(ventana)

    def abrir_regla_30(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Regla de 30")
        Rule30App(ventana)

    def abrir_regla_90(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Regla de 90")
        Regla90App(ventana)

    def abrir_generador_uniforme(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Uniformes")
        UniformeApp(ventana)

    def abrir_prueba_kerlan(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Prueba Kerland - k*ERLANG")
        KerlangApp(ventana)

    def abrir_exponencial(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Exponenciales")
        ExponencialApp(ventana)

    def abrir_generador_gamma(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Gamma")
        GammaApp(ventana)

    def abrir_generador_normal(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Normales")
        NormalApp(ventana)

    def abrir_generador_poisson(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador Poisson")
        PoissonApp(ventana)

    def abrir_generador_uniforme_discreto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Uniforme discreto")
        DistribucionUniformeApp(ventana)        

    def abrir_generador_bernoulli(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador Bernoulli")
        DistribucionBernoulliApp(ventana)  

    def abrir_generador_binomial(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador Bernoulli")
        DistribucionBinomialApp(ventana)  

# 🚀 Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuCalculadorasApp(root)
    root.mainloop()
