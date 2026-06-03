import tkinter as tk
from datetime import datetime
import random

def start_animation():
    # 1. Animar el crecimiento del tallo (árbol)
    grow_tree(0)
    # 2. Empezar a mostrar las flores después de 3 segundos (3000 ms)
    root.after(3000, show_flowers)
    # 3. Mostrar el mensaje después de 4 segundos (4000 ms)
    root.after(4000, show_message)

def grow_tree(step):
    # Animación de crecer de abajo hacia arriba en 50 pasos
    if step <= 50:
        altura_actual = step * 3 # Crecerá hasta 150px
        # Actualizamos las coordenadas del rectángulo en el canvas (crece hacia arriba)
        canvas.coords(tree, 195, 300 - altura_actual, 205, 300)
        root.after(60, grow_tree, step + 1)

def show_flowers():
    for i in range(60):
        # Retraso aleatorio simulando la animación del CSS
        delay = random.randint(0, 2000)
        # Usamos lambda para capturar el valor correcto de "i" en el bucle
        root.after(delay, lambda idx=i: draw_flower(idx))

def draw_flower(i):
    # Organización en forma de "grid" igual que en el CSS (10 columnas)
    col = i % 10
    row = i // 10
    
    # Posición específica para cada flor
    x = 75 + col * 25
    y = 50 + row * 25
    
    # Dibujar pétalos (Círculo amarillo)
    canvas.create_oval(x, y, x + 15, y + 15, fill="#ffed00", outline="")
    # Dibujar centro (Círculo marrón)
    canvas.create_oval(x + 5, y + 5, x + 10, y + 10, fill="#331a00", outline="")

def show_message():
    # Mostrar el contenedor con el texto después de que crecen las flores
    message_frame.pack(pady=10)
    # Iniciar la lógica del contador
    update_timer()

def update_timer():
    # Fecha de inicio igual a la del código original
    start_date = datetime(2023, 3, 21)
    now = datetime.now()
    diff = now - start_date
    
    days = diff.days
    seconds = diff.seconds
    hours = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    
    timer_var.set(f"{days} días, {hours} horas, {mins} minutos y {secs} segundos")
    
    # Refrescar en 1000 milisegundos (1 segundo)
    root.after(1000, update_timer)

# --- Configuración principal de la Ventana ---
root = tk.Tk()
root.title("Flores Amarillas para Ti")
root.geometry("450x550")
root.configure(bg="#fff5f5") # Color de fondo similar al original

# Área de dibujo para el árbol y las flores
canvas = tk.Canvas(root, width=400, height=320, bg="#fff5f5", highlightthickness=0)
canvas.pack()

# Crear el tallo inicial (altura de cero en y=300)
tree = canvas.create_rectangle(195, 300, 205, 300, fill="#4d2600", outline="")

# Contenedor para todo el texto. Se oculta hasta ejecutar "show_message()"
message_frame = tk.Frame(root, bg="#fff5f5")

# --- Creación de los componentes de texto con sus estilos ---
title_label = tk.Label(message_frame, text="Flores amarillas para el amor de mi vida", 
                       fg="#d63384", bg="#fff5f5", font=("Segoe UI", 14, "bold"))
title_label.pack()

desc_label = tk.Label(message_frame, text="Mi amor por ti comenzó hace...", 
                      fg="#d63384", bg="#fff5f5", font=("Segoe UI", 11))
desc_label.pack(pady=5)

timer_var = tk.StringVar()
timer_var.set("Cargando tiempo...")
timer_label = tk.Label(message_frame, textvariable=timer_var, 
                       fg="#444444", bg="#fff5f5", font=("Segoe UI", 12, "bold"))
timer_label.pack(pady=5)

quote_label = tk.Label(message_frame, text='"Si pudiera elegir un lugar seguro, sería a tu lado."', 
                       fg="#d63384", bg="#fff5f5", font=("Segoe UI", 11, "italic"))
quote_label.pack(pady=5)

# --- INICIAR SECUENCIA ---
start_animation()

# Arrancar la aplicación
root.mainloop()
