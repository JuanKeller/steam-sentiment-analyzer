
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, date
import pandas as pd
import os

# ==============================
# BASE DE DATOS
# ==============================

def crear_bd():
    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nombre TEXT,
        documento TEXT,
        cargo TEXT,
        area TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencia(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        fecha TEXT,
        entrada TEXT,
        salida TEXT,
        estado TEXT
    )
    """)

    conexion.commit()
    conexion.close()

crear_bd()

# ==============================
# REGISTRO DE EMPLEADOS
# ==============================

def registrar_empleado():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    documento = entry_documento.get()
    cargo = entry_cargo.get()
    area = entry_area.get()

    if codigo == "" or nombre == "":
        messagebox.showerror("Error", "Complete los campos obligatorios")
        return

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("INSERT INTO empleados(codigo,nombre,documento,cargo,area) VALUES(?,?,?,?,?)",
                       (codigo,nombre,documento,cargo,area))
        conexion.commit()
        messagebox.showinfo("Éxito", "Empleado registrado correctamente")
    except:
        messagebox.showerror("Error", "Código ya existente")

    conexion.close()

# ==============================
# REGISTRO DE ENTRADA
# ==============================

HORA_LIMITE = "08:00:00"

def marcar_entrada():
    codigo = entry_codigo_asistencia.get()
    fecha_actual = str(date.today())
    hora_actual = datetime.now().strftime("%H:%M:%S")

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM asistencia WHERE codigo=? AND fecha=?",
                   (codigo, fecha_actual))
    registro = cursor.fetchone()

    if registro:
        messagebox.showwarning("Aviso", "Ya marcó entrada hoy")
    else:
        estado = "Puntual"
        if hora_actual > HORA_LIMITE:
            estado = "Retardo"

        cursor.execute("INSERT INTO asistencia(codigo,fecha,entrada,estado) VALUES(?,?,?,?)",
                       (codigo,fecha_actual,hora_actual,estado))
        conexion.commit()
        messagebox.showinfo("Correcto", f"Entrada registrada a las {hora_actual}")

    conexion.close()

# ==============================
# REGISTRO DE SALIDA
# ==============================

def marcar_salida():
    codigo = entry_codigo_asistencia.get()
    fecha_actual = str(date.today())
    hora_actual = datetime.now().strftime("%H:%M:%S")

    conexion = sqlite3.connect("asistencia.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT entrada FROM asistencia WHERE codigo=? AND fecha=?",
                   (codigo, fecha_actual))
    registro = cursor.fetchone()

    if registro:
        cursor.execute("UPDATE asistencia SET salida=? WHERE codigo=? AND fecha=?",
                       (hora_actual,codigo,fecha_actual))
        conexion.commit()
        messagebox.showinfo("Correcto", f"Salida registrada a las {hora_actual}")
    else:
        messagebox.showerror("Error", "No hay entrada registrada hoy")

    conexion.close()

# ==============================
# CONSULTA DE ASISTENCIA
# ==============================

def consultar():
    codigo = entry_codigo_asistencia.get()

    conexion = sqlite3.connect("asistencia.db")
    df = pd.read_sql_query(f"SELECT * FROM asistencia WHERE codigo='{codigo}'", conexion)
    conexion.close()

    if df.empty:
        messagebox.showinfo("Info", "No hay registros")
        return

    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Historial de Asistencia")

    tree = ttk.Treeview(ventana_reporte)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")

# ==============================
# EXPORTAR A EXCEL
# ==============================

def exportar_excel():
    conexion = sqlite3.connect("asistencia.db")
    df = pd.read_sql_query("SELECT * FROM asistencia", conexion)
    conexion.close()

    if df.empty:
        messagebox.showinfo("Info", "No hay datos para exportar")
        return

    df.to_excel("reporte_asistencia.xlsx", index=False)
    messagebox.showinfo("Éxito", "Reporte exportado correctamente")

# ==============================
# LOGIN SIMPLE
# ==============================

def verificar_login():
    if entry_user.get() == "admin" and entry_pass.get() == "1234":
        ventana_login.destroy()
        ventana_principal()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

# ==============================
# INTERFAZ PRINCIPAL
# ==============================

def ventana_principal():
    global entry_codigo, entry_nombre, entry_documento
    global entry_cargo, entry_area, entry_codigo_asistencia

    ventana = tk.Tk()
    ventana.title("Sistema de Control de Asistencia")
    ventana.geometry("600x500")

    tk.Label(ventana,text="Registro de Empleados",font=("Arial",14)).pack()

    entry_codigo = tk.Entry(ventana)
    entry_codigo.pack()
    entry_codigo.insert(0,"Código")

    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()
    entry_nombre.insert(0,"Nombre")

    entry_documento = tk.Entry(ventana)
    entry_documento.pack()
    entry_documento.insert(0,"Documento")

    entry_cargo = tk.Entry(ventana)
    entry_cargo.pack()
    entry_cargo.insert(0,"Cargo")

    entry_area = tk.Entry(ventana)
    entry_area.pack()
    entry_area.insert(0,"Área")

    tk.Button(ventana,text="Registrar Empleado",command=registrar_empleado).pack(pady=5)

    tk.Label(ventana,text="Control de Asistencia",font=("Arial",14)).pack(pady=10)

    entry_codigo_asistencia = tk.Entry(ventana)
    entry_codigo_asistencia.pack()
    entry_codigo_asistencia.insert(0,"Código Empleado")

    tk.Button(ventana,text="Marcar Entrada",command=marcar_entrada).pack(pady=5)
    tk.Button(ventana,text="Marcar Salida",command=marcar_salida).pack(pady=5)
    tk.Button(ventana,text="Consultar Historial",command=consultar).pack(pady=5)
    tk.Button(ventana,text="Exportar Excel",command=exportar_excel).pack(pady=5)

    ventana.mainloop()

# ==============================
# VENTANA LOGIN
# ==============================

ventana_login = tk.Tk()
ventana_login.title("Login Administrador")
ventana_login.geometry("300x200")

tk.Label(ventana_login,text="Usuario").pack()
entry_user = tk.Entry(ventana_login)
entry_user.pack()

tk.Label(ventana_login,text="Contraseña").pack()
entry_pass = tk.Entry(ventana_login,show="*")
entry_pass.pack()

tk.Button(ventana_login,text="Ingresar",command=verificar_login).pack(pady=10)

ventana_login.mainloop()