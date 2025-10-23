*Calculadoras de Números Pseudoaleatorios y Reglas de Autómatas Celulares*

Este proyecto contiene un conjunto de calculadoras y simuladores de números pseudoaleatorios y autómatas celulares, desarrolladas en Python con Tkinter, con una interfaz visual oscuro-azulada y funcionalidad interactiva.

Incluye módulos para:
- Algoritmos de generación de números pseudoaleatorios:
    Cuadrados Medios
    Productos Medios
    Multiplicador Constante
- Simuladores de autómatas celulares:
    Juego de la Vida (Conway)
    Regla 30
    Regla 90
- Generadores de distribuciones estadísticas:
    Uniforme
    Exponencial
    Gamma
    Normal
    K-Erlang
    Poisson
    Etc
  
📂 Estructura del proyecto
/calculadoras
│
├─ Menu de las Calculadoras.py        # Menú principal
├─ cuadrados_medios1.py       # Algoritmo Cuadrados Medios
├─ Productos_Medios2.py       # Algoritmo Productos Medios
├─ Multiplicador_Constante3.py# Algoritmo Multiplicador Constante
├─ juego_vida.py              # Juego de la Vida
├─ regla_30_dark.py           # Regla 30
├─ regla_90_dark.py           # Regla 90
├─ uniforme.py                # Distribución Uniforme
├─ exponencial_dark.py        # Distribución Exponencial
├─ gamma.py                   # Distribución Gamma
├─ normal.py                  # Distribución Normal
├─ K_erlang_dark.py           # Distribución K-Erlang
├─ poisson_dark.py            # Distribución Poisson
├─ bernoulli.py               # Distribución bernolli
├─ binomial.py                # Distribución binomial
├─ uniforme_discreto.py       # Distribución uniforme discreta
└─ README.md

🖥️ Requisitos
    Python 3.9 o superior
    Librerías necesarias:
Ejecuta este bash para instalar la libreria correspondiente
    pip install matplotlib scipy

🚀 Cómo ejecutar
1. Clonar el repositorio:
    git clone https://github.com/tu-usuario/calculadoras.git
    cd calculadoras
2. Ejecutar el menu principal:
    python MenuCalculadoras.py
3. Desde la ventana principal podrás abrir cada módulo:
    Botones 1–3: Algoritmos pseudoaleatorios
    Botones 4–6: Reglas de autómatas celulares
    Botones 7–15: Distribuciones estadísticas
Cada módulo tiene su propia interfaz para ingresar parámetros, generar números o simulaciones y visualizar resultados (tabla y/o histograma).

🎨 Funcionalidades principales
Algoritmos de generación de números
- Cuadrados Medios, Productos Medios, Multiplicador Constante: generan secuencias de números pseudoaleatorios con los métodos clásicos.
Autómatas celulares
- Juego de la Vida: simulación interactiva con control de velocidad y tamaño de la cuadrícula.
- Regla 30 y 90: simulación en una línea con actualización automática y visualización en tonalidad oscuro-azulado.
Distribuciones estadísticas
- Uniforme: a + (b - a) * r
- Exponencial: INV.GAMMA(r;1;media)
- K-Erlang: INV.GAMMA(r;k;media/k)
- Gamma: INV.GAMMA(r;media^2/varianza;varianza/media)
- Normal: INV.NORM(r;media;sqrt(varianza))
- Poisson: INV.POISSON(r;λ)
En todas las distribuciones:
- Se ingresan los parámetros por teclado (media, varianza, λ, k, etc.) y la cantidad de valores n.
- Los números generados se muestran en tabla.
- Se puede visualizar un histograma de barras interactivo.

📷 Capturas de pantalla
A continuaicion se presenta una corrida 🥵 del juego de la vida
<img width="902" height="752" alt="Image" src="https://github.com/user-attachments/assets/42e2f55e-de3a-4a77-b414-788128119769" />

Ahora con sus datos correspondientes
<img width="896" height="747" alt="Image" src="https://github.com/user-attachments/assets/7d8c65c5-9f86-4fd2-9335-75f28287491d" />

Ahora se muestra la corrida de la regla 30 🥵
<img width="820" height="554" alt="Image" src="https://github.com/user-attachments/assets/3589dd38-5dd0-41b8-a68b-24a279b611fd" />

Ahora se muestra la corrida de la regla 90 🥵

🎨 Diseño visual
Tema oscuro-azulado consistente en todos los módulos.
Tablas y botones con alto contraste para fácil lectura.
Uso de ttk.Style y colores personalizados para la interfaz profesional.

📝 Licencia
Libre para uso académico, personal y profesional, ordenada por su majestad el rey Sol xd.
