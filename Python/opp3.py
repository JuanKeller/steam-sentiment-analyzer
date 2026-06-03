"""
APLICACIÓN ORGANIZADOR DE PROYECTOS PUBLICITARIOS
Con imagen de fondo
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Importar Pillow para manejar imágenes
from PIL import Image, ImageTk

class ProyectosPublicitariosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Proyectos Publicitarios")
        self.root.geometry("1100x650")
        
        # Configurar la imagen de fondo
        self.configurar_fondo()
        
        # Configurar la base de datos
        self.configurar_bd()
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Cargar proyectos existentes
        self.cargar_proyectos()
    
    def configurar_fondo(self):
        """Configura una imagen como fondo de la ventana"""
        try:
            # Cargar la imagen (asumiendo que está en la misma carpeta)
            imagen_fondo = Image.open("images (1)")  # Usando el nombre de tu imagen
            
            # Obtener el tamaño de la ventana
            ancho_ventana = self.root.winfo_width()
            alto_ventana = self.root.winfo_height()
            
            # Si la ventana aún no tiene tamaño definido, usar el tamaño por defecto
            if ancho_ventana == 1:  # Tkinter a veces devuelve 1 cuando aún no se ha renderizado
                ancho_ventana = 1100
                alto_ventana = 650
            
            # Redimensionar la imagen al tamaño de la ventana
            imagen_fondo = imagen_fondo.resize((ancho_ventana, alto_ventana), Image.Resampling.LANCZOS)
            self.foto_fondo = ImageTk.PhotoImage(imagen_fondo)
            
            # Crear un label para el fondo
            self.fondo_label = tk.Label(self.root, image=self.foto_fondo)
            self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Hacer que el fondo esté detrás de todo
            self.fondo_label.lower()
            
            # Configurar para que la imagen se redimensione si la ventana cambia de tamaño
            self.root.bind('<Configure>', self.ajustar_fondo)
            
        except FileNotFoundError:
            # Si no encuentra la imagen, usa color de fondo por defecto
            self.root.configure(bg='#f0f0f0')
            print("No se encontró la imagen 'images (1)'. Usando color por defecto.")
            print("Asegúrate de que el archivo esté en la misma carpeta que el programa.")
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            self.root.configure(bg='#f0f0f0')
    
    def ajustar_fondo(self, event=None):
        """Ajusta el tamaño de la imagen de fondo cuando la ventana cambia de tamaño"""
        try:
            if hasattr(self, 'fondo_label') and hasattr(self, 'foto_fondo'):
                # Obtener nuevo tamaño de la ventana
                ancho = self.root.winfo_width()
                alto = self.root.winfo_height()
                
                if ancho > 0 and alto > 0:
                    # Recargar y redimensionar la imagen
                    imagen_fondo = Image.open("images (1)")
                    imagen_fondo = imagen_fondo.resize((ancho, alto), Image.Resampling.LANCZOS)
                    nueva_foto = ImageTk.PhotoImage(imagen_fondo)
                    
                    # Actualizar el label
                    self.fondo_label.configure(image=nueva_foto)
                    self.foto_fondo = nueva_foto  # Mantener referencia
        except:
            pass  # Ignorar errores en el redimensionamiento
    
    def configurar_bd(self):
        """Configura la base de datos SQLite"""
        self.conn = sqlite3.connect('proyectos_publicitarios.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cliente TEXT NOT NULL,
                material TEXT NOT NULL,
                cantidad_disponible INTEGER,
                cantidad_requerida INTEGER,
                tiempo_impresion INTEGER,
                tiempo_entrega INTEGER,
                estado_diseno TEXT
            )
        ''')
        self.conn.commit()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica"""
        
        # Frame contenedor con estilo para que los elementos se vean sobre el fondo
        style = ttk.Style()
        style.configure('Transparent.TFrame', background='#f0f0f0')
        style.configure('Transparent.TLabelframe', background='#f0f0f0')
        style.configure('Transparent.TLabelframe.Label', background='#f0f0f0')
        
        # Frame principal con fondo ligeramente transparente (usando color sólido)
        main_frame = ttk.Frame(self.root, style='Transparent.TFrame', padding="10")
        main_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Configurar que el frame principal se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Título con fondo personalizado
        titulo_frame = tk.Frame(main_frame, bg='#2c3e50', bd=2, relief=tk.RAISED)
        titulo_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky=(tk.W, tk.E))
        
        titulo = tk.Label(titulo_frame, text="ORGANIZADOR DE PROYECTOS PUBLICITARIOS", 
                         font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50', pady=5)
        titulo.pack(fill=tk.BOTH, expand=True)
        
        # ========== SECCIÓN DE REGISTRO ==========
        registro_frame = ttk.LabelFrame(main_frame, text="Registrar Nuevo Proyecto", padding="15")
        registro_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Configurar columnas del registro_frame
        for i in range(4):
            registro_frame.columnconfigure(i, weight=1)
        
        # Campos del formulario - Primera columna
        ttk.Label(registro_frame, text="Nombre del Proyecto:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(registro_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(registro_frame, text="Cliente:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cliente = ttk.Entry(registro_frame, width=30)
        self.entry_cliente.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(registro_frame, text="Material a utilizar:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_material = ttk.Combobox(registro_frame, 
                                          values=["Vinilo", "Pendón", "Lona", "Papel", "Tela"], 
                                          width=28)
        self.combo_material.set("Vinilo")
        self.combo_material.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(registro_frame, text="Cantidad Disponible (m²):").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cant_disp = ttk.Entry(registro_frame, width=30)
        self.entry_cant_disp.grid(row=3, column=1, padx=5, pady=5)
        
        # Segunda columna
        ttk.Label(registro_frame, text="Cantidad Requerida (m²):").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_cant_req = ttk.Entry(registro_frame, width=30)
        self.entry_cant_req.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(registro_frame, text="Tiempo estimado impresión (horas):").grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_tiempo_imp = ttk.Entry(registro_frame, width=30)
        self.entry_tiempo_imp.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(registro_frame, text="Tiempo hábil entrega (días):").grid(
            row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_tiempo_ent = ttk.Entry(registro_frame, width=30)
        self.entry_tiempo_ent.grid(row=2, column=3, padx=5, pady=5)
        
        ttk.Label(registro_frame, text="Estado del diseño:").grid(
            row=3, column=2, sticky=tk.W, padx=5, pady=5)
        self.combo_estado = ttk.Combobox(registro_frame, 
                                        values=["Pendiente", "En proceso", "Finalizado"], 
                                        width=28)
        self.combo_estado.set("Pendiente")
        self.combo_estado.grid(row=3, column=3, padx=5, pady=5)
        
        # Frame para botones (fila separada)
        botones_frame = ttk.Frame(registro_frame)
        botones_frame.grid(row=4, column=0, columnspan=4, pady=15)
        
        ttk.Button(botones_frame, text="Registrar Proyecto", 
                  command=self.registrar_proyecto).pack(side=tk.LEFT, padx=10)
        ttk.Button(botones_frame, text="Limpiar Campos", 
                  command=self.limpiar_campos).pack(side=tk.LEFT, padx=10)
        
        # ========== TABLA DE PROYECTOS ==========
        tabla_frame = ttk.LabelFrame(main_frame, text="Proyectos Registrados", padding="10")
        tabla_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Configurar que la tabla se expanda
        main_frame.rowconfigure(2, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Treeview (tabla)
        columnas = ('ID', 'Nombre', 'Cliente', 'Material', 'Disp.', 'Req.', 
                   'T.Impresión', 'T.Entrega', 'Estado', 'Listo?')
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show='headings', 
                                  yscrollcommand=scrollbar.set, height=8)
        
        # Configurar columnas
        ancho_columnas = [50, 150, 120, 80, 60, 60, 80, 80, 100, 60]
        for col, ancho in zip(columnas, ancho_columnas):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, minwidth=ancho)
        
        self.tabla.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.tabla.yview)
        
        # ========== BOTONES DE ACCIÓN ==========
        acciones_frame = ttk.Frame(main_frame)
        acciones_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(acciones_frame, text="Editar Proyecto", 
                  command=self.editar_proyecto).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Eliminar Proyecto", 
                  command=self.eliminar_proyecto).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Verificar Material", 
                  command=self.verificar_material).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Actualizar Tabla", 
                  command=self.cargar_proyectos).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Salir", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # ========== BARRA DE ESTADO ==========
        self.status_bar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
    
    def validar_datos(self, datos):
        """
        Valida los datos ingresados en el formulario
        Retorna: (True, "") si son válidos, (False, mensaje_error) si no
        """
        # Validar campos obligatorios
        if not datos['nombre'] or not datos['cliente']:
            return False, "El nombre del proyecto y el cliente son obligatorios"
        
        # Validar que las cantidades sean números positivos
        try:
            cant_disp = int(datos['cantidad_disponible'])
            cant_req = int(datos['cantidad_requerida'])
            
            if cant_disp < 0 or cant_req < 0:
                return False, "Las cantidades deben ser números positivos"
            
            if cant_req > cant_disp:
                return False, "La cantidad requerida no puede ser mayor a la disponible"
                
        except ValueError:
            return False, "Las cantidades deben ser números enteros"
        
        # Validar tiempos
        try:
            tiempo_imp = int(datos['tiempo_impresion'])
            tiempo_ent = int(datos['tiempo_entrega'])
            
            if tiempo_imp < 0 or tiempo_ent < 0:
                return False, "Los tiempos deben ser números positivos"
        except ValueError:
            return False, "Los tiempos deben ser números enteros"
        
        return True, ""
    
    def verificar_disponibilidad_material(self, material, cantidad_requerida, proyecto_id=None):
        """
        Verifica si hay suficiente material disponible
        Si proyecto_id se proporciona, excluye ese proyecto del cálculo (para ediciones)
        """
        # Obtener todos los proyectos del mismo material
        if proyecto_id:
            self.cursor.execute('''
                SELECT cantidad_requerida FROM proyectos 
                WHERE material = ? AND id != ?
            ''', (material, proyecto_id))
        else:
            self.cursor.execute('''
                SELECT cantidad_requerida FROM proyectos 
                WHERE material = ?
            ''', (material,))
        
        proyectos_mismo_material = self.cursor.fetchall()
        
        # Calcular material total comprometido
        material_comprometido = sum(p[0] for p in proyectos_mismo_material)
        
        # Obtener cantidad disponible total (del nuevo proyecto)
        self.cursor.execute('''
            SELECT cantidad_disponible FROM proyectos 
            WHERE material = ? LIMIT 1
        ''', (material,))
        
        resultado = self.cursor.fetchone()
        if resultado:
            disponible_total = resultado[0]
        else:
            # Si no hay proyectos de este material, usamos la cantidad del formulario
            disponible_total = cantidad_requerida
        
        material_restante = disponible_total - (material_comprometido + cantidad_requerida)
        
        # Verificar si hay suficiente
        if material_restante < 0:
            return False, f"Material insuficiente. Faltan {abs(material_restante)} m²"
        
        # Alerta si el material es bajo (menos del 20% de material disponible)
        if material_restante < (disponible_total * 0.2):
            messagebox.showwarning("Alerta de Material", 
                                 f"¡Material bajo! Quedan solo {material_restante} m² de {material}")
        
        return True, f"Material disponible. Quedan {material_restante} m²"
    
    def determinar_listo_entrega(self, estado, tiempo_entrega):
        """Determina si un proyecto está listo para entrega"""
        if estado == "Finalizado" and tiempo_entrega >= 0:
            return "SÍ"
        return "NO"
    
    def registrar_proyecto(self):
        """Registra un nuevo proyecto en la base de datos"""
        try:
            # Recoger datos del formulario
            datos = {
                'nombre': self.entry_nombre.get().strip(),
                'cliente': self.entry_cliente.get().strip(),
                'material': self.combo_material.get(),
                'cantidad_disponible': self.entry_cant_disp.get().strip(),
                'cantidad_requerida': self.entry_cant_req.get().strip(),
                'tiempo_impresion': self.entry_tiempo_imp.get().strip(),
                'tiempo_entrega': self.entry_tiempo_ent.get().strip(),
                'estado_diseno': self.combo_estado.get()
            }
            
            # Validar datos
            valido, mensaje = self.validar_datos(datos)
            if not valido:
                messagebox.showerror("Error de validación", mensaje)
                return
            
            # Verificar disponibilidad de material
            disponible, mensaje_material = self.verificar_disponibilidad_material(
                datos['material'], int(datos['cantidad_requerida'])
            )
            
            if not disponible:
                messagebox.showerror("Material insuficiente", mensaje_material)
                return
            
            # Insertar en la base de datos
            self.cursor.execute('''
                INSERT INTO proyectos 
                (nombre, cliente, material, cantidad_disponible, cantidad_requerida, 
                 tiempo_impresion, tiempo_entrega, estado_diseno)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['nombre'], datos['cliente'], datos['material'],
                int(datos['cantidad_disponible']), int(datos['cantidad_requerida']),
                int(datos['tiempo_impresion']), int(datos['tiempo_entrega']),
                datos['estado_diseno']
            ))
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Proyecto registrado correctamente")
            self.limpiar_campos()
            self.cargar_proyectos()
            self.status_bar.config(text=f"Proyecto '{datos['nombre']}' registrado - {mensaje_material}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el proyecto: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.combo_material.set("Vinilo")
        self.entry_cant_disp.delete(0, tk.END)
        self.entry_cant_req.delete(0, tk.END)
        self.entry_tiempo_imp.delete(0, tk.END)
        self.entry_tiempo_ent.delete(0, tk.END)
        self.combo_estado.set("Pendiente")
    
    def cargar_proyectos(self):
        """Carga todos los proyectos en la tabla"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Obtener proyectos de la base de datos
        self.cursor.execute('SELECT * FROM proyectos ORDER BY id')
        proyectos = self.cursor.fetchall()
        
        # Insertar en la tabla
        for proyecto in proyectos:
            listo = self.determinar_listo_entrega(proyecto[8], proyecto[7])
            self.tabla.insert('', tk.END, values=proyecto + (listo,))
    
    def editar_proyecto(self):
        """Edita el proyecto seleccionado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Por favor, seleccione un proyecto para editar")
            return
        
        # Obtener datos del proyecto seleccionado
        item = self.tabla.item(seleccion[0])
        proyecto = item['values']
        
        # Crear ventana de edición
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("Editar Proyecto")
        ventana_editar.geometry("500x400")
        
        # Frame para los campos
        frame_editar = ttk.Frame(ventana_editar, padding="10")
        frame_editar.pack(fill=tk.BOTH, expand=True)
        
        # Campos de edición
        campos_editar = [
            ("Nombre:", proyecto[1]),
            ("Cliente:", proyecto[2]),
            ("Material:", proyecto[3]),
            ("Cant. Disponible:", proyecto[4]),
            ("Cant. Requerida:", proyecto[5]),
            ("T. Impresión:", proyecto[6]),
            ("T. Entrega:", proyecto[7]),
            ("Estado:", proyecto[8])
        ]
        
        entries_editar = []
        
        for i, (label_text, valor) in enumerate(campos_editar):
            ttk.Label(frame_editar, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            if "Estado" in label_text:
                entry = ttk.Combobox(frame_editar, values=["Pendiente", "En proceso", "Finalizado"], width=27)
                entry.set(valor)
            elif "Material" in label_text:
                entry = ttk.Combobox(frame_editar, values=["Vinilo", "Pendón", "Lona", "Papel", "Tela"], width=27)
                entry.set(valor)
            else:
                entry = ttk.Entry(frame_editar, width=30)
                entry.insert(0, str(valor))
            
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries_editar.append(entry)
        
        def guardar_edicion():
            try:
                # Recoger nuevos valores
                nuevos_valores = [e.get() for e in entries_editar]
                
                # Actualizar base de datos
                self.cursor.execute('''
                    UPDATE proyectos 
                    SET nombre=?, cliente=?, material=?, cantidad_disponible=?,
                        cantidad_requerida=?, tiempo_impresion=?, tiempo_entrega=?,
                        estado_diseno=?
                    WHERE id=?
                ''', (
                    nuevos_valores[0], nuevos_valores[1], nuevos_valores[2],
                    int(nuevos_valores[3]), int(nuevos_valores[4]),
                    int(nuevos_valores[5]), int(nuevos_valores[6]),
                    nuevos_valores[7], proyecto[0]
                ))
                
                self.conn.commit()
                self.cargar_proyectos()
                ventana_editar.destroy()
                messagebox.showinfo("Éxito", "Proyecto actualizado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")
        
        ttk.Button(frame_editar, text="Guardar Cambios", command=guardar_edicion).grid(
            row=len(campos_editar), column=0, columnspan=2, pady=20)
    
    def eliminar_proyecto(self):
        """Elimina el proyecto seleccionado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Por favor, seleccione un proyecto para eliminar")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proyecto?"):
            item = self.tabla.item(seleccion[0])
            proyecto_id = item['values'][0]
            
            self.cursor.execute('DELETE FROM proyectos WHERE id = ?', (proyecto_id,))
            self.conn.commit()
            
            self.cargar_proyectos()
            self.status_bar.config(text="Proyecto eliminado correctamente")
    
    def verificar_material(self):
        """Verifica el estado del material de todos los proyectos"""
        self.cursor.execute('SELECT DISTINCT material, cantidad_disponible FROM proyectos')
        materiales = self.cursor.fetchall()
        
        if not materiales:
            messagebox.showinfo("Información", "No hay proyectos registrados")
            return
        
        mensaje = "ESTADO DE MATERIALES:\n\n"
        
        for material, cantidad_total in materiales:
            self.cursor.execute('''
                SELECT SUM(cantidad_requerida) FROM proyectos WHERE material = ?
            ''', (material,))
            
            total_requerido = self.cursor.fetchone()[0] or 0
            disponible = cantidad_total - total_requerido
            
            mensaje += f"{material}:\n"
            mensaje += f"  Total disponible: {cantidad_total} m²\n"
            mensaje += f"  Total requerido: {total_requerido} m²\n"
            mensaje += f"  Material restante: {disponible} m²\n"
            
            if disponible < 0:
                mensaje += "  ⚠️ ¡INSUFICIENTE!\n"
            elif disponible < (cantidad_total * 0.2):
                mensaje += "  ⚠️ ¡BAJO!\n"
            else:
                mensaje += "  ✅ Suficiente\n"
            mensaje += "\n"
        
        messagebox.showinfo("Verificación de Material", mensaje)
    
    def __del__(self):
        """Cierra la conexión a la base de datos al finalizar"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Punto de entrada principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ProyectosPublicitariosApp(root)
    root.mainloop()