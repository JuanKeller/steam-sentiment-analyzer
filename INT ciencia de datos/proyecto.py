import customtkinter as ctk
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA INTERFAZ (Para que se vea bonita) 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steam Sentiment Analyzer - Proyecto Ciencia de Datos")
        self.geometry("500x400")

        # Título Principal
        self.label = ctk.CTkLabel(self, text="Análisis de Sentimiento Games", font=("Roboto", 20, "bold"))
        self.label.pack(pady=20)

        # Formulario de Ingreso
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Usuario", width=200)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=200)
        self.pass_entry.pack(pady=10)

        # Botón de Inicio
        self.button = ctk.CTkButton(self, text="Ingresar y Analizar", command=self.ejecutar_analisis)
        self.button.pack(pady=20)

    # --- EL CORAZÓN DEL PROYECTO (Fases 1 a 4) ---
    def ejecutar_analisis(self):
        usuario = self.user_entry.get()
        password = self.pass_entry.get()

        # Validación simple de usuario
        if usuario == "admin" and password == "7777":
            self.label.configure(text="¡Acceso concedido! Analizando...", text_color="green")
            
            # FASE 1: RECOLECCIÓN Y CARGA [1, 4]
            # Usamos datos de ejemplo con las columnas críticas: Texto, Fecha y Horas
            data = {
                'Review_Text': [
                    "Increíble actualización, el nuevo mapa está genial", 
                    "Pésimo rendimiento tras el parche, muchos bugs",
                    "Cambiaron la interfaz, se ve rara",
                    "El lag después de la actualización es injugable",
                    "Amo este juego, los cambios de balance son perfectos"
                ],
                'Date': ['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05'],
                'Playtime': [10, 5, 2, 1, 20]     # Horas de juego [4]
            }
            df = pd.DataFrame(data)

            # FASE 2: LIMPIEZA DE DATOS (Data Wrangling) [4]
            def limpiar(texto):
                return texto.lower().strip() # Minúsculas y quitar espacios [4]

            df['Review_Cleaned'] = df['Review_Text'].apply(limpiar)

            # FASE 3: PROCESAMIENTO Y CLASIFICACIÓN (NLP) [4]
            # Asignamos puntaje de polaridad: 1 (Positivo), -1 (Negativo), 0 (Neutral) [1]
            def obtener_sentimiento(texto):
                return TextBlob(texto).sentiment.polarity 

            df['Polarity'] = df['Review_Cleaned'].apply(obtener_sentimiento)

            # Clasificación por etiquetas
            def etiquetar(score):
                if score > 0: return 'Positivo'
                elif score < 0: return 'Negativo'
                else: return 'Neutral'
            
            df['Sentiment_Label'] = df['Polarity'].apply(etiquetar)

            # FASE 4: ANÁLISIS DE CORRELACIÓN TEMPORAL [2]
            # Aquí generamos el reporte visual dinámico [3]
            plt.figure(figsize=(8, 5))
            plt.plot(df['Date'], df['Polarity'], marker='o', color='purple', label='Sentimiento')
            
            # Marcamos un "parche" ficticio el 2 de marzo como dice tu metodología [2]
            plt.axvline(x='2024-03-02', color='red', linestyle='--', label='Lanzamiento de Parche')
            
            plt.title('Impacto de Actualizaciones en el Sentimiento')
            plt.xlabel('Fecha de la Reseña')
            plt.ylabel('Polaridad (-1 a 1)')
            plt.legend()
            plt.grid(True)
            
            print("\n--- RESULTADOS DEL ANÁLISIS ---")
            print(df[['Review_Text', 'Sentiment_Label', 'Playtime']])
            
            plt.show() # Muestra la gráfica final [2]

        else:
            self.label.configure(text="Usuario o clave incorrectos", text_color="red")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()