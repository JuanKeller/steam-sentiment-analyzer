
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, date

# ===============================
# CREAR BASE DE DATOS
# ===============================

conexion = sqlite3.connect("asistencia.db")
cursor = conexion.cursor()

# Tabla empleados
cursor.execute("""
CREATE TABLE IF NOT EXISTS empleados(
    codigo TEXT PRIMARY KEY,
    nombre TEXT,
    cargo TEXT
)
""")

# Tabla asistencia
cursor.execute("""
CREATE TABLE IF NOT EXISTS asistencia(
    codigo TEXT,
    fecha TEXT,
    entrada TEXT,
    salida TEXT
)
""")

conexion.commit()
conexion.close()

# ===============================
# FUNCION REGISTRAR EMPLEADO
# ===============================

def registrar_empleado():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    cargo = entry_cargo.get()

    if codigo == "" or nombre == "":
        messagebox.showerror("Error", "Complete los campos")
        return

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("INSERT INTO empleados VALUES (?, ?, ?)", 
                       (codigo, nombre, cargo))
        conexion.commit()
        messagebox.showinfo("Éxito", "Empleado registrado")
    except:
        messagebox.showerror("Error", "El código ya existe")

    conexion.close()

# ===============================
# FUNCION MARCAR ENTRADA
# ===============================

def marcar_entrada():
    codigo = entry_codigo_asistencia.get()
    fecha_hoy = str(date.today())
    hora_actual = datetime.now().strftime("%H:%M:%S")

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    # Verificar si ya marcó entrada hoy
    cursor.execute("SELECT * FROM asistencia WHERE codigo=? AND fecha=?", 
                   (codigo, fecha_hoy))
    registro = cursor.fetchone()

    if registro:
        messagebox.showwarning("Aviso", "Ya marcó entrada hoy")
    else:
        cursor.execute("INSERT INTO asistencia VALUES (?, ?, ?, ?)",
                       (codigo, fecha_hoy, hora_actual, ""))
        conexion.commit()
        messagebox.showinfo("Correcto", "Entrada registrada")

    conexion.close()

# ===============================
# FUNCION MARCAR SALIDA
# ===============================

def marcar_salida():
    codigo = entry_codigo_asistencia.get()
    fecha_hoy = str(date.today())
    hora_actual = datetime.now().strftime("%H:%M:%S")

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM asistencia WHERE codigo=? AND fecha=?", 
                   (codigo, fecha_hoy))
    registro = cursor.fetchone()

    if registro:
        cursor.execute("UPDATE asistencia SET salida=? WHERE codigo=? AND fecha=?",
                       (hora_actual, codigo, fecha_hoy))
        conexion.commit()
        messagebox.showinfo("Correcto", "Salida registrada")
    else:
        messagebox.showerror("Error", "Primero debe marcar entrada")

    conexion.close()

# ===============================
# FUNCION VER HISTORIAL
# ===============================

def ver_historial():
    codigo = entry_codigo_asistencia.get()

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM asistencia WHERE codigo=?", (codigo,))
    registros = cursor.fetchall()

    conexion.close()

    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial")

    texto = tk.Text(ventana_historial, width=60, height=20)
    texto.pack()

    for fila in registros:
        texto.insert(tk.END, f"Fecha: {fila[1]} | Entrada: {fila[2]} | Salida: {fila[3]}\n")

# ===============================
# INTERFAZ GRAFICA
# ===============================

ventana = tk.Tk()
ventana.title("Sistema Básico de Asistencia")
ventana.geometry("400x500")

# Registro empleados
tk.Label(ventana, text="Registro de Empleados", font=("Arial", 12)).pack(pady=5)

entry_codigo = tk.Entry(ventana)
entry_codigo.pack()
entry_codigo.insert(0, "Código")

entry_nombre = tk.Entry(ventana)
entry_nombre.pack()
entry_nombre.insert(0, "Nombre")

entry_cargo = tk.Entry(ventana)
entry_cargo.pack()
entry_cargo.insert(0, "Cargo")

tk.Button(ventana, text="Registrar", command=registrar_empleado).pack(pady=5)

# Asistencia
tk.Label(ventana, text="Control de Asistencia", font=("Arial", 12)).pack(pady=15)

entry_codigo_asistencia = tk.Entry(ventana)
entry_codigo_asistencia.pack()
entry_codigo_asistencia.insert(0, "Código Empleado")

tk.Button(ventana, text="Marcar Entrada", command=marcar_entrada).pack(pady=5)
tk.Button(ventana, text="Marcar Salida", command=marcar_salida).pack(pady=5)
tk.Button(ventana, text="Ver Historial", command=ver_historial).pack(pady=5)

ventana.mainloop()