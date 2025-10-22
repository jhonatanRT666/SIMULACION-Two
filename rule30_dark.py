import tkinter as tk
from tkinter import ttk, messagebox
import random

# ---------- Configuración visual ----------
BG_MAIN = "#071422"      # fondo principal muy oscuro
PANEL = "#0b2433"        # paneles
BTN_BG = "#0f3a53"       # botones
BTN_ACTIVE = "#186a96"
CELL_ON = "#6ec6ff"      # celda viva (azulado claro)
CELL_OFF = "#071422"     # celda muerta (mismo fondo)
GRID_LINE = "#0b3750"    # líneas sutiles
FG_TEXT = "#dbeefc"

# ---------- Lógica Regla 30 ----------
# Mapear (left, self, right) -> next_state (0/1)
RULE30 = {
    (1,1,1):0,
    (1,1,0):0,
    (1,0,1):0,
    (1,0,0):1,
    (0,1,1):1,
    (0,1,0):1,
    (0,0,1):1,
    (0,0,0):0
}

class Rule30App:
    def __init__(self, root):
        self.root = root
        self.root.title("Regla 30 — Autómata Celular (Oscuro-Azulado)")
        self.root.configure(background=BG_MAIN)

        # Parámetros iniciales
        self.cell_size = 4
        self.cols = 201            # número de celdas por fila
        self.max_rows = 200        # número máximo de generaciones a mostrar
        self.speed_ms = 80        # intervalo de actualización
        self.running = False
        self.generation = 0

        # Estado actual: lista de 0/1 (fila actual)
        self.current = [0]*self.cols
        # Por defecto, un único 1 en el centro
        self.current[self.cols//2] = 1

        # Matriz de generaciones (lista de listas)
        self.history = [self.current.copy()]

        self._build_ui()
        self._draw_grid_base()

    # ---------- UI ----------
    def _build_ui(self):
        # Top frame (controles)
        top = tk.Frame(self.root, bg=BG_MAIN, pady=8)
        top.pack(fill="x")

        # Panel de botones
        panel = tk.Frame(top, bg=PANEL, padx=8, pady=6)
        panel.pack(side="left", padx=12)

        # Botones
        self.btn_start = tk.Button(panel, text="Iniciar", bg=BTN_BG, fg=FG_TEXT, activebackground=BTN_ACTIVE,
                                   command=self.toggle_run, width=9)
        self.btn_start.grid(row=0, column=0, padx=6, pady=4)

        btn_step = tk.Button(panel, text="Paso", bg=BTN_BG, fg=FG_TEXT, activebackground=BTN_ACTIVE,
                             command=self.step, width=9)
        btn_step.grid(row=0, column=1, padx=6)

        btn_rand = tk.Button(panel, text="Aleatorizar", bg=BTN_BG, fg=FG_TEXT, activebackground=BTN_ACTIVE,
                             command=self.randomize, width=11)
        btn_rand.grid(row=0, column=2, padx=6)

        btn_clear = tk.Button(panel, text="Limpiar", bg=BTN_BG, fg=FG_TEXT, activebackground=BTN_ACTIVE,
                              command=self.clear, width=9)
        btn_clear.grid(row=0, column=3, padx=6)

        # Panel ajustes
        panel2 = tk.Frame(top, bg=BG_MAIN)
        panel2.pack(side="right", padx=12)

        # Velocidad
        tk.Label(panel2, text="Velocidad (ms)", bg=BG_MAIN, fg=FG_TEXT).grid(row=0, column=0, sticky="e")
        self.s_speed = ttk.Scale(panel2, from_=10, to=500, orient="horizontal", command=self._on_speed_change)
        self.s_speed.set(self.speed_ms)
        self.s_speed.grid(row=0, column=1, padx=8)

        # Tamaño de celda
        tk.Label(panel2, text="Tamaño celda", bg=BG_MAIN, fg=FG_TEXT).grid(row=1, column=0, sticky="e")
        self.s_size = ttk.Scale(panel2, from_=2, to=12, orient="horizontal", command=self._on_size_change)
        self.s_size.set(self.cell_size)
        self.s_size.grid(row=1, column=1, padx=8)

        # Info label
        self.lbl_info = tk.Label(self.root, text=f"Generación: {self.generation}", bg=BG_MAIN, fg=FG_TEXT, pady=6)
        self.lbl_info.pack()

        # Canvas para dibujar generaciones
        canvas_frame = tk.Frame(self.root, bg=BG_MAIN, padx=10, pady=8)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=BG_MAIN, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bind para editar celdas con clic (en la fila actual)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    # ---------- Dibujado ----------
    def _draw_grid_base(self):
        # recalcular dimensiones
        w = self.cols * self.cell_size
        h = self.max_rows * self.cell_size
        self.canvas.config(scrollregion=(0,0,w,h))
        self.canvas.delete("all")
        # Dibujar fondo de rejilla sutil (opcional)
        for c in range(self.cols):
            x = c * self.cell_size
            # líneas verticales sutiles cada 10 celdas para estética
            if c % 10 == 0:
                self.canvas.create_line(x, 0, x, h, fill=GRID_LINE, width=1)
        for r in range(self.max_rows):
            y = r * self.cell_size
            if r % 10 == 0:
                self.canvas.create_line(0, y, w, y, fill=GRID_LINE, width=1)
        # Redibujar el historial
        for r, row in enumerate(self.history):
            self._draw_row(r, row)

    def _draw_row(self, r, row):
        y1 = r * self.cell_size
        for c, val in enumerate(row):
            x1 = c * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            if val:
                # celda viva
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=CELL_ON, fill=CELL_ON, tags=f"cell_{r}_{c}")
            else:
                # celda muerta: no dibujar (se mantiene el fondo)
                # Para limpieza visual, podemos crear un rect con borde sutil
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill=CELL_OFF, tags=f"cell_{r}_{c}")

    # ---------- Actualización ----------
    def next_generation(self):
        new = [0]*self.cols
        for i in range(self.cols):
            left = self.current[(i-1) % self.cols]
            me   = self.current[i]
            right= self.current[(i+1) % self.cols]
            new[i] = RULE30[(left, me, right)]
        self.current = new
        self.history.append(self.current.copy())
        # mantener solo hasta max_rows
        if len(self.history) > self.max_rows:
            # descartamos la primera fila (shift hacia arriba)
            self.history.pop(0)
        # la generación a mostrar corresponderá al índice final
        self.generation += 1

    def render(self):
        self.canvas.delete("all")
        # ajustar tamaño si cambió cell_size
        self._draw_grid_base()

    # ---------- Acciones de usuario ----------
    def toggle_run(self):
        if not self.running:
            self.running = True
            self.btn_start.config(text="Pausar")
            self._run_loop()
        else:
            self.running = False
            self.btn_start.config(text="Iniciar")

    def _run_loop(self):
        if not self.running:
            return
        self.step()
        self.root.after(int(self.speed_ms), self._run_loop)

    def step(self):
        self.next_generation()
        # redibujar: para eficiencia solo redibujamos las últimas filas
        self.canvas.delete("all")
        # recalcular y dibujar todo el historial (sencillo y claro)
        for r, row in enumerate(self.history):
            self._draw_row(r, row)
        self.lbl_info.config(text=f"Generación: {self.generation}")

    def randomize(self):
        self.current = [random.choice([0,1]) for _ in range(self.cols)]
        self.history = [self.current.copy()]
        self.generation = 0
        self.render()
        self.lbl_info.config(text=f"Generación: {self.generation}")

    def clear(self):
        self.current = [0]*self.cols
        self.history = [self.current.copy()]
        self.generation = 0
        self.render()
        self.lbl_info.config(text=f"Generación: {self.generation}")

    # Cambiar velocidad desde slider
    def _on_speed_change(self, val):
        try:
            self.speed_ms = float(val)
        except Exception:
            pass

    # Cambiar tamaño de celda desde slider
    def _on_size_change(self, val):
        try:
            new_size = int(float(val))
        except Exception:
            return
        if new_size < 2:
            new_size = 2
        self.cell_size = new_size
        # re-calcular canvas y redibujar
        self.render()

    # Editar celda actual con clic (solo afecta la última fila mostrada si está en pantalla)
    def _on_canvas_click(self, event):
        # determinar fila/col clicada
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if col < 0 or col >= self.cols:
            return
        # Solo permitimos editar la última fila actual en la parte visible (la más reciente)
        # Si el clic cae fuera de la última fila, igual togglear la correspondiente fila en history si existe.
        if 0 <= row < len(self.history):
            self.history[row][col] = 1 - self.history[row][col]
            # si modificamos la última fila, también sincronizar current
            if row == len(self.history) - 1:
                self.current = self.history[-1].copy()
            self.canvas.delete(f"cell_{row}_{col}")
            # redibujar solo esa celda
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            val = self.history[row][col]
            if val:
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=CELL_ON, fill=CELL_ON, tags=f"cell_{row}_{col}")
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill=CELL_OFF, tags=f"cell_{row}_{col}")

# ---------- Ejecutar aplicación ----------
if __name__ == "__main__":
    root = tk.Tk()
    # Hacer estilo ttk concordante (opcional)
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except Exception:
        pass

    app = Rule30App(root)
    root.geometry("820x520")
    root.minsize(600, 400)
    root.mainloop()
