import tkinter as tk
from tkinter import ttk, messagebox
import random

# ---------- Configuración visual ----------
BG_MAIN = "#071422"      # fondo principal
PANEL = "#0b2433"        # panel superior
BTN_BG = "#0f3a53"       # botones
BTN_ACTIVE = "#186a96"
CELL_ON = "#6ec6ff"      # celda viva
CELL_OFF = "#071422"     # celda muerta
GRID_LINE = "#0b3750"    # líneas sutiles
FG_TEXT = "#dbeefc"

# ---------- Lógica Regla 90 ----------
# (left, self, right) → next_state
RULE90 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 0,
    (0, 0, 1): 1,
    (0, 0, 0): 0
}


class Regla90App:
    def __init__(self, root):
        self.root = root
        self.root.title("Regla 90 — Autómata Celular (Oscuro-Azulado)")
        self.root.configure(background=BG_MAIN)

        # Parámetros
        self.cell_size = 4
        self.cols = 201
        self.max_rows = 200
        self.speed_ms = 80
        self.running = False
        self.generation = 0

        # Estado inicial: un 1 en el centro
        self.current = [0] * self.cols
        self.current[self.cols // 2] = 1
        self.history = [self.current.copy()]

        self._build_ui()
        self._draw_grid_base()

    # ---------- UI ----------
    def _build_ui(self):
        top = tk.Frame(self.root, bg=BG_MAIN, pady=8)
        top.pack(fill="x")

        panel = tk.Frame(top, bg=PANEL, padx=8, pady=6)
        panel.pack(side="left", padx=12)

        # Botones principales
        self.btn_start = tk.Button(panel, text="Iniciar", bg=BTN_BG, fg=FG_TEXT,
                                   activebackground=BTN_ACTIVE, width=9,
                                   command=self.toggle_run)
        self.btn_start.grid(row=0, column=0, padx=6, pady=4)

        btn_step = tk.Button(panel, text="Paso", bg=BTN_BG, fg=FG_TEXT,
                             activebackground=BTN_ACTIVE, width=9,
                             command=self.step)
        btn_step.grid(row=0, column=1, padx=6)

        btn_rand = tk.Button(panel, text="Aleatorizar", bg=BTN_BG, fg=FG_TEXT,
                             activebackground=BTN_ACTIVE, width=11,
                             command=self.randomize)
        btn_rand.grid(row=0, column=2, padx=6)

        btn_clear = tk.Button(panel, text="Limpiar", bg=BTN_BG, fg=FG_TEXT,
                              activebackground=BTN_ACTIVE, width=9,
                              command=self.clear)
        btn_clear.grid(row=0, column=3, padx=6)

        # Panel de ajustes
        panel2 = tk.Frame(top, bg=BG_MAIN)
        panel2.pack(side="right", padx=12)

        tk.Label(panel2, text="Velocidad (ms)", bg=BG_MAIN, fg=FG_TEXT).grid(row=0, column=0, sticky="e")
        self.s_speed = ttk.Scale(panel2, from_=10, to=500, orient="horizontal", command=self._on_speed_change)
        self.s_speed.set(self.speed_ms)
        self.s_speed.grid(row=0, column=1, padx=8)

        tk.Label(panel2, text="Tamaño celda", bg=BG_MAIN, fg=FG_TEXT).grid(row=1, column=0, sticky="e")
        self.s_size = ttk.Scale(panel2, from_=2, to=12, orient="horizontal", command=self._on_size_change)
        self.s_size.set(self.cell_size)
        self.s_size.grid(row=1, column=1, padx=8)

        self.lbl_info = tk.Label(self.root, text=f"Generación: {self.generation}",
                                 bg=BG_MAIN, fg=FG_TEXT, pady=6)
        self.lbl_info.pack()

        canvas_frame = tk.Frame(self.root, bg=BG_MAIN, padx=10, pady=8)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=BG_MAIN, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self._on_canvas_click)

    # ---------- Dibujado ----------
    def _draw_grid_base(self):
        w = self.cols * self.cell_size
        h = self.max_rows * self.cell_size
        self.canvas.config(scrollregion=(0, 0, w, h))
        self.canvas.delete("all")

        for c in range(self.cols):
            if c % 10 == 0:
                x = c * self.cell_size
                self.canvas.create_line(x, 0, x, h, fill=GRID_LINE, width=1)
        for r in range(self.max_rows):
            if r % 10 == 0:
                y = r * self.cell_size
                self.canvas.create_line(0, y, w, y, fill=GRID_LINE, width=1)

        for r, row in enumerate(self.history):
            self._draw_row(r, row)

    def _draw_row(self, r, row):
        y1 = r * self.cell_size
        for c, val in enumerate(row):
            x1 = c * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            color = CELL_ON if val else CELL_OFF
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline=color if val else "",
                                         fill=color, tags=f"cell_{r}_{c}")

    # ---------- Actualización ----------
    def next_generation(self):
        new = [0] * self.cols
        for i in range(self.cols):
            left = self.current[(i - 1) % self.cols]
            me = self.current[i]
            right = self.current[(i + 1) % self.cols]
            new[i] = RULE90[(left, me, right)]
        self.current = new
        self.history.append(self.current.copy())
        if len(self.history) > self.max_rows:
            self.history.pop(0)
        self.generation += 1

    def render(self):
        self.canvas.delete("all")
        self._draw_grid_base()

    # ---------- Acciones ----------
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
        self.canvas.delete("all")
        for r, row in enumerate(self.history):
            self._draw_row(r, row)
        self.lbl_info.config(text=f"Generación: {self.generation}")

    def randomize(self):
        self.current = [random.choice([0, 1]) for _ in range(self.cols)]
        self.history = [self.current.copy()]
        self.generation = 0
        self.render()
        self.lbl_info.config(text=f"Generación: {self.generation}")

    def clear(self):
        self.current = [0] * self.cols
        self.history = [self.current.copy()]
        self.generation = 0
        self.render()
        self.lbl_info.config(text=f"Generación: {self.generation}")

    # ---------- Sliders ----------
    def _on_speed_change(self, val):
        try:
            self.speed_ms = float(val)
        except Exception:
            pass

    def _on_size_change(self, val):
        try:
            self.cell_size = int(float(val))
        except Exception:
            return
        self.render()

    # ---------- Edición manual ----------
    def _on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= col < self.cols and 0 <= row < len(self.history):
            self.history[row][col] = 1 - self.history[row][col]
            if row == len(self.history) - 1:
                self.current = self.history[-1].copy()
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            color = CELL_ON if self.history[row][col] else CELL_OFF
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline=color if self.history[row][col] else "",
                                         fill=color, tags=f"cell_{row}_{col}")


# ---------- Ejecutar aplicación ----------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except Exception:
        pass
    app = Regla90App(root)
    root.geometry("820x520")
    root.minsize(600, 400)
    root.mainloop()
