# =============================================================================
# PROYECTO FINAL — Steam Sentiment Analyzer
# Autor      : Keller Acevedo
# Universidad: Universidad Minuto de Dios — Ingeniería en Ciencia de Datos
# Objetivo 3 : Despliegue Web con Streamlit
#
# DESCRIPCIÓN:
#   Aplicativo web que analiza el sentimiento de reseñas de videojuegos
#   usando NLP (TextBlob), con visualización de correlación temporal entre
#   actualizaciones de software (parches) y la reacción emocional
#   de la comunidad de jugadores en Steam.
#
# TECNOLOGÍAS:
#   - Streamlit   : Framework de interfaz web (reemplaza CustomTkinter)
#   - TextBlob    : Motor NLP para clasificación de sentimientos
#   - Pandas      : Manipulación y análisis de datos estructurados
#   - Matplotlib  : Generación de visualizaciones estadísticas
# =============================================================================

# ── Librerías estándar ────────────────────────────────────────────────────────
import json
import time
import random
from datetime import datetime

# ── Librerías de terceros ─────────────────────────────────────────────────────
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

# =============================================================================
# CONFIGURACIÓN GLOBAL DE LA PÁGINA (debe ser el primer comando Streamlit)
# =============================================================================
st.set_page_config(
    page_title="Steam Sentiment Analyzer",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos CSS personalizados ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo oscuro coherente con el tema gaming */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; }
    .metric-label { font-size: 0.85rem; color: #8b949e; }
    .pos  { color: #3fb950; }
    .neg  { color: #f85149; }
    .neu  { color: #8b949e; }
    .header-badge {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.75rem;
        color: #8b949e;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# MÓDULO 1 — DATASET DE RESEÑAS (Mock API interna)
#
# Simula la respuesta de un endpoint GET /api/reviews de la API de Steam.
# Los datos están distribuidos en 4 periodos narrativos:
#   1. PRE-PARCHE  : sentimiento positivo (Feb 20 – Mar 14, 2024)
#   2. DÍA PARCHE : transición (Mar 15, 2024)
#   3. POST-PARCHE : caída crítica (Mar 16 – Mar 20, 2024)
#   4. RECUPERACIÓN: tendencia positiva (Mar 21 – Abr 5, 2024)
# =============================================================================

REVIEWS_DATABASE = [
    # ── PRE-PARCHE (2024-02-20 al 2024-03-14) ────────────────────────────────
    {"id": 1,  "text": "Absolutely love this game, the new season content is incredible",        "date": "2024-02-20", "score": 342,  "playtime": 580},
    {"id": 2,  "text": "Best competitive FPS I've played in years, the balance feels perfect",   "date": "2024-02-21", "score": 218,  "playtime": 1200},
    {"id": 3,  "text": "Graphics update was worth the wait, runs smoother than ever",             "date": "2024-02-22", "score": 156,  "playtime": 340},
    {"id": 4,  "text": "Matchmaking has improved significantly, finding games in under a minute", "date": "2024-02-23", "score": 98,   "playtime": 890},
    {"id": 5,  "text": "The new character abilities are so well designed, props to the dev team", "date": "2024-02-24", "score": 267,  "playtime": 450},
    {"id": 6,  "text": "Solid update overall, loving the new map layout changes",                 "date": "2024-02-25", "score": 189,  "playtime": 700},
    {"id": 7,  "text": "Community events are engaging and rewards feel meaningful",               "date": "2024-02-26", "score": 134,  "playtime": 320},
    {"id": 8,  "text": "Performance on mid-range hardware is excellent, devs listen to feedback", "date": "2024-02-27", "score": 201,  "playtime": 150},
    {"id": 9,  "text": "Finally fixed the audio glitch that was bothering me for weeks",          "date": "2024-02-28", "score": 445,  "playtime": 2100},
    {"id": 10, "text": "Ranked system overhaul is great, finally feels fair",                     "date": "2024-02-29", "score": 178,  "playtime": 540},
    {"id": 11, "text": "Servers have been stable all week, great improvement",                    "date": "2024-03-01", "score": 92,   "playtime": 230},
    {"id": 12, "text": "New weapon skins are honestly beautiful, worth every penny",              "date": "2024-03-02", "score": 67,   "playtime": 890},
    {"id": 13, "text": "Love the new ping system, communication without voice chat works well",   "date": "2024-03-03", "score": 312,  "playtime": 670},
    {"id": 14, "text": "The economy system update makes the game more accessible for new players","date": "2024-03-04", "score": 143,  "playtime": 45},
    {"id": 15, "text": "Anti-cheat improvements are noticeable, fewer hackers in ranked",         "date": "2024-03-05", "score": 520,  "playtime": 1800},
    {"id": 16, "text": "Game feels alive again after the content drought earlier this year",      "date": "2024-03-06", "score": 234,  "playtime": 760},
    {"id": 17, "text": "Balance is near perfect right now, every strategy seems viable",          "date": "2024-03-07", "score": 188,  "playtime": 430},
    {"id": 18, "text": "Impressive optimization, loading times cut in half",                      "date": "2024-03-08", "score": 156,  "playtime": 290},
    {"id": 19, "text": "Tutorial rework is excellent for onboarding new players",                 "date": "2024-03-09", "score": 89,   "playtime": 12},
    {"id": 20, "text": "Competitive scene is thriving, viewership numbers are insane",            "date": "2024-03-10", "score": 301,  "playtime": 920},
    {"id": 21, "text": "Weekly patches are small but consistent, devs are on top of things",     "date": "2024-03-11", "score": 174,  "playtime": 560},
    {"id": 22, "text": "Really happy with the current state of the game before the big patch",   "date": "2024-03-12", "score": 209,  "playtime": 780},
    {"id": 23, "text": "Community is friendly and the new social features work well",             "date": "2024-03-13", "score": 132,  "playtime": 340},
    {"id": 24, "text": "Hoping the major patch tomorrow keeps up this positive momentum",         "date": "2024-03-14", "score": 267,  "playtime": 1100},

    # ── DÍA DEL PARCHE 3.15 (2024-03-15) — evento crítico ────────────────────
    {"id": 25, "text": "Downloading the patch now, excited to see the changes",                  "date": "2024-03-15", "score": 145,  "playtime": 890},
    {"id": 26, "text": "Patch notes look interesting but some nerfs seem too aggressive",         "date": "2024-03-15", "score": 312,  "playtime": 1560},
    {"id": 27, "text": "Servers are down for maintenance, waiting...",                            "date": "2024-03-15", "score": 78,   "playtime": 230},

    # ── POST-PARCHE INMEDIATO (2024-03-16 al 2024-03-20) — caída crítica ─────
    {"id": 28, "text": "This patch completely destroyed the balance, unplayable right now",      "date": "2024-03-16", "score": 891,  "playtime": 1200},
    {"id": 29, "text": "FPS dropped from 120 to 40 after the update, terrible optimization",     "date": "2024-03-16", "score": 743,  "playtime": 560},
    {"id": 30, "text": "They nerfed my main character into the ground, feels useless now",       "date": "2024-03-16", "score": 567,  "playtime": 2300},
    {"id": 31, "text": "Serious bugs introduced in patch 3.15, crashing every 20 minutes",       "date": "2024-03-16", "score": 1203, "playtime": 890},
    {"id": 32, "text": "The new economy change completely breaks competitive viability",          "date": "2024-03-17", "score": 654,  "playtime": 1800},
    {"id": 33, "text": "How did this pass QA? Game is broken after the patch",                   "date": "2024-03-17", "score": 987,  "playtime": 670},
    {"id": 34, "text": "Lag spike every 3 minutes since the update, unacceptable",               "date": "2024-03-17", "score": 432,  "playtime": 340},
    {"id": 35, "text": "Lost 200 rank points due to server instability post-patch, refund please","date": "2024-03-17", "score": 765,  "playtime": 2100},
    {"id": 36, "text": "The hitbox changes are completely broken, bullets don't register",        "date": "2024-03-18", "score": 543,  "playtime": 1450},
    {"id": 37, "text": "Worst patch in the history of this game, devs need to rollback",         "date": "2024-03-18", "score": 1102, "playtime": 3200},
    {"id": 38, "text": "Game crashes on startup for many users, no hotfix yet after 3 days",     "date": "2024-03-18", "score": 876,  "playtime": 890},
    {"id": 39, "text": "Audio is completely broken, ambient sounds replaced by white noise",      "date": "2024-03-19", "score": 432,  "playtime": 450},
    {"id": 40, "text": "Matchmaking is taking 15 minutes in ranked since the patch dropped",     "date": "2024-03-19", "score": 321,  "playtime": 720},
    {"id": 41, "text": "They broke more things than they fixed, deeply disappointed",             "date": "2024-03-19", "score": 678,  "playtime": 1100},
    {"id": 42, "text": "P2W elements introduced in this patch are disgusting",                   "date": "2024-03-20", "score": 934,  "playtime": 2800},
    {"id": 43, "text": "Still no acknowledgment from devs about the crash bug, terrible comms",  "date": "2024-03-20", "score": 567,  "playtime": 430},

    # ── RECUPERACIÓN PARCIAL (2024-03-21 al 2024-03-28) — señales mixtas ─────
    {"id": 44, "text": "Hotfix 3.15.1 helped a bit but game still feels off",                   "date": "2024-03-21", "score": 234,  "playtime": 890},
    {"id": 45, "text": "At least the crashes are less frequent after the emergency patch",       "date": "2024-03-22", "score": 312,  "playtime": 560},
    {"id": 46, "text": "Some balance issues remain but the game is becoming playable again",     "date": "2024-03-22", "score": 189,  "playtime": 780},
    {"id": 47, "text": "Dev team responded to community feedback, hopeful about next patch",     "date": "2024-03-23", "score": 421,  "playtime": 1200},
    {"id": 48, "text": "Still experiencing fps drops but not as severe as launch day",           "date": "2024-03-23", "score": 267,  "playtime": 340},
    {"id": 49, "text": "New hotfix addressed most of my issues, game is functional",             "date": "2024-03-24", "score": 178,  "playtime": 670},
    {"id": 50, "text": "Servers are stable again, matchmaking times back to normal",             "date": "2024-03-24", "score": 234,  "playtime": 890},
    {"id": 51, "text": "Balance still needs work but at least it doesn't crash anymore",         "date": "2024-03-25", "score": 156,  "playtime": 450},
    {"id": 52, "text": "Communication from devs has improved, appreciate the transparency",      "date": "2024-03-25", "score": 312,  "playtime": 1100},
    {"id": 53, "text": "Game is recovering, cautiously optimistic about the roadmap",            "date": "2024-03-26", "score": 198,  "playtime": 780},
    {"id": 54, "text": "Performance patch helped my PC a lot, back to enjoying the game",        "date": "2024-03-26", "score": 267,  "playtime": 560},
    {"id": 55, "text": "Still some lingering issues but nothing game-breaking anymore",          "date": "2024-03-27", "score": 143,  "playtime": 340},
    {"id": 56, "text": "New character balance feels better after the adjustments",               "date": "2024-03-27", "score": 189,  "playtime": 920},
    {"id": 57, "text": "Giving the game another chance after the fixes, cautious but hopeful",   "date": "2024-03-28", "score": 234,  "playtime": 670},
    {"id": 58, "text": "Things are improving but they lost a lot of trust with that patch",      "date": "2024-03-28", "score": 312,  "playtime": 1800},

    # ── RECUPERACIÓN CONSOLIDADA (2024-03-29 al 2024-04-05) ──────────────────
    {"id": 59, "text": "Game is back to being fun, patch 3.16 fixed most problems",              "date": "2024-03-29", "score": 456,  "playtime": 890},
    {"id": 60, "text": "Enjoying ranked again, balance feels much better now",                   "date": "2024-03-30", "score": 312,  "playtime": 1200},
    {"id": 61, "text": "Great comeback from the devs, they listened to the community",           "date": "2024-03-31", "score": 567,  "playtime": 780},
    {"id": 62, "text": "Smooth performance restored, back to my 120fps consistently",            "date": "2024-04-01", "score": 234,  "playtime": 560},
    {"id": 63, "text": "The crisis response from the team was actually impressive in the end",   "date": "2024-04-02", "score": 398,  "playtime": 1100},
    {"id": 64, "text": "Community trust is rebuilding slowly, game is in a good place now",      "date": "2024-04-03", "score": 267,  "playtime": 890},
    {"id": 65, "text": "Back to recommending this game to friends after the rough patch period", "date": "2024-04-05", "score": 489,  "playtime": 2100},
]


# =============================================================================
# MÓDULO 2 — PIPELINE DE PROCESAMIENTO DE DATOS
# =============================================================================

def simular_peticion_api(termino: str = "", limite: int = 65) -> dict:
    """
    Simula una petición GET a la Mock API de reseñas.

    En el contexto académico reproduce el comportamiento de:
        GET http://localhost:5050/api/reviews?game=<termino>&limit=<limite>

    Incluye una latencia simulada de 50–150 ms para representar
    condiciones reales de red.

    Parámetros:
        termino (str): Filtro de búsqueda por texto (case-insensitive).
        limite  (int): Número máximo de registros a retornar.

    Retorna:
        dict: Respuesta con metadatos y lista de reseñas.
    """
    tiempo_inicio = time.time()
    time.sleep(random.uniform(0.05, 0.15))  # Latencia de red simulada

    resultados = REVIEWS_DATABASE
    if termino:
        resultados = [r for r in resultados if termino.lower() in r["text"].lower()]

    resultados = resultados[:limite]
    latencia_ms = round((time.time() - tiempo_inicio) * 1000, 1)

    return {
        "status":        "success",
        "source":        "Mock Gaming API v1.0",
        "endpoint":      f"/api/reviews?game={termino or 'all'}&limit={limite}",
        "total_results": len(resultados),
        "latencia_ms":   latencia_ms,
        "data":          resultados
    }


def ejecutar_pipeline_nlp(registros: list) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de Ciencia de Datos sobre los registros:

    Fase 1 — Carga       : Convierte la lista de dicts a DataFrame de Pandas.
    Fase 2 — Limpieza    : Normaliza texto (minúsculas, strip), elimina nulos.
    Fase 3 — NLP         : Calcula polaridad con TextBlob y clasifica sentimiento.
    Fase 4 — Preparación : Convierte columna de fechas para análisis temporal.

    Umbral de clasificación (±0.05) elegido para aislar textos neutros
    y reducir el sesgo en reseñas de longitud corta.

    Parámetros:
        registros (list): Lista de dicts provenientes de la Mock API.

    Retorna:
        pd.DataFrame con columnas adicionales: text_clean, polarity, sentiment, date.
    """
    # FASE 1: Carga de datos
    df = pd.DataFrame(registros)

    # FASE 2: Limpieza de datos (Data Wrangling)
    df.dropna(subset=["text"], inplace=True)
    df["text_clean"] = df["text"].str.lower().str.strip()

    # FASE 3: Análisis de sentimiento con TextBlob
    df["polarity"] = df["text_clean"].apply(
        lambda t: TextBlob(t).sentiment.polarity
    )
    df["sentiment"] = df["polarity"].apply(
        lambda p: "Positivo" if p > 0.05 else ("Negativo" if p < -0.05 else "Neutral")
    )

    # FASE 4: Conversión temporal
    df["date"] = pd.to_datetime(df["date"])

    return df


# =============================================================================
# MÓDULO 3 — VISUALIZACIONES
# =============================================================================

def generar_dashboard(df: pd.DataFrame) -> plt.Figure:
    """
    Genera el dashboard de 4 gráficas con tema oscuro gaming.

    Gráfica 1 (sup-izq): Evolución temporal de polaridad con línea de parche.
    Gráfica 2 (sup-der): Distribución de categorías de sentimiento.
    Gráfica 3 (inf-izq): Comparativa Pre-Parche vs Post-Parche.
    Gráfica 4 (inf-der): Histograma de distribución de polaridad.

    Parámetros:
        df (pd.DataFrame): DataFrame procesado por ejecutar_pipeline_nlp().

    Retorna:
        matplotlib.figure.Figure lista para st.pyplot().
    """
    FECHA_PARCHE = pd.Timestamp("2024-03-15")
    df_grouped   = df.groupby("date")["polarity"].mean().reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(
        "Dashboard — Impacto del Parche 3.15 en el Sentimiento de la Comunidad Gaming",
        fontsize=13, fontweight="bold", y=0.98, color="white"
    )
    fig.patch.set_facecolor("#0d1117")
    for ax in axes.flat:
        ax.set_facecolor("#161b22")
        ax.tick_params(colors="#8b949e")
        ax.xaxis.label.set_color("#8b949e")
        ax.yaxis.label.set_color("#8b949e")
        ax.title.set_color("#e6edf3")
        for spine in ax.spines.values():
            spine.set_edgecolor("#30363d")

    # ── Gráfica 1: Polaridad en el tiempo ────────────────────────────────────
    ax1 = axes[0, 0]
    ax1.plot(
        df_grouped["date"], df_grouped["polarity"],
        color="#a78bfa", linewidth=2.5, marker="o", markersize=4,
        label="Polaridad promedio"
    )
    ax1.axhline(y=0, color="#30363d", linestyle="--", alpha=0.6)
    ax1.axvline(x=FECHA_PARCHE, color="#f85149", linewidth=2,
                linestyle="--", label="⚠ Lanzamiento Parche 3.15")
    ax1.fill_between(
        df_grouped["date"], df_grouped["polarity"], 0,
        where=(df_grouped["polarity"] >= 0),
        alpha=0.2, color="#3fb950", label="Zona positiva"
    )
    ax1.fill_between(
        df_grouped["date"], df_grouped["polarity"], 0,
        where=(df_grouped["polarity"] < 0),
        alpha=0.2, color="#f85149", label="Zona negativa"
    )
    ax1.set_title("Evolución Temporal del Sentimiento")
    ax1.set_ylabel("Polaridad (-1 a +1)")
    ax1.legend(fontsize=7, facecolor="#161b22", labelcolor="#e6edf3",
               edgecolor="#30363d")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right",
             fontsize=7, color="#8b949e")

    # ── Gráfica 2: Distribución de sentimientos ───────────────────────────────
    ax2 = axes[0, 1]
    conteo  = df["sentiment"].value_counts()
    colores = {"Positivo": "#3fb950", "Negativo": "#f85149", "Neutral": "#8b949e"}
    orden   = [c for c in ["Positivo", "Negativo", "Neutral"] if c in conteo.index]
    bars = ax2.bar(
        [c for c in orden],
        [conteo[c] for c in orden],
        color=[colores[c] for c in orden],
        edgecolor="#30363d", linewidth=0.8, width=0.5
    )
    for bar, etiqueta in zip(bars, orden):
        val = conteo[etiqueta]
        ax2.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f"{val}\n({val/len(df)*100:.0f}%)",
            ha="center", va="bottom", fontsize=9, color="white"
        )
    ax2.set_title("Distribución de Sentimientos")
    ax2.set_ylabel("Cantidad de reseñas")

    # ── Gráfica 3: Pre vs Post parche ─────────────────────────────────────────
    ax3 = axes[1, 0]
    pre  = df[df["date"] <  FECHA_PARCHE]["polarity"].mean()
    post = df[df["date"] >= FECHA_PARCHE]["polarity"].mean()
    cats = ["Pre-Parche\n(Feb 20 – Mar 14)", "Post-Parche\n(Mar 15 – Abr 5)"]
    vals = [pre, post]
    cols = ["#3fb950" if v >= 0 else "#f85149" for v in vals]
    bars2 = ax3.bar(cats, vals, color=cols, edgecolor="#30363d", width=0.45)
    for bar, val in zip(bars2, vals):
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.005 if val >= 0 else val - 0.015,
            f"{val:+.4f}",
            ha="center", va="bottom" if val >= 0 else "top",
            fontsize=11, fontweight="bold", color="white"
        )
    ax3.axhline(y=0, color="#30363d", linewidth=1, linestyle="--")
    ax3.set_title("Polaridad Promedio: Pre vs Post Parche")
    ax3.set_ylabel("Polaridad promedio")

    # ── Gráfica 4: Histograma de polaridad ────────────────────────────────────
    ax4 = axes[1, 1]
    ax4.hist(df["polarity"], bins=20,
             color="#58a6ff", edgecolor="#30363d", alpha=0.85)
    ax4.axvline(x=df["polarity"].mean(), color="#f0883e",
                linewidth=2, linestyle="--",
                label=f"Media: {df['polarity'].mean():+.3f}")
    ax4.axvline(x=0, color="#8b949e", linewidth=1, linestyle=":")
    ax4.set_title("Histograma de Polaridad")
    ax4.set_xlabel("Polaridad")
    ax4.set_ylabel("Frecuencia")
    ax4.legend(fontsize=8, facecolor="#161b22", labelcolor="#e6edf3",
               edgecolor="#30363d")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


# =============================================================================
# MÓDULO 4 — INTERFAZ WEB (Streamlit)
# =============================================================================

def main():
    """
    Función principal que construye la interfaz web de la aplicación.
    Reemplaza la GUI de CustomTkinter por componentes web de Streamlit,
    manteniendo exactamente la misma lógica de autenticación, pipeline
    de datos y visualizaciones del proyecto original.
    """

    # ── Barra lateral ─────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🎮 Steam Sentiment Analyzer")
        st.markdown('<span class="header-badge">Mock Gaming API v1.0 · Online</span>',
                    unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🔐 Acceso al Sistema")

        usuario  = st.text_input("Usuario", placeholder="admin")
        password = st.text_input("Contraseña", type="password", placeholder="••••")

        st.markdown("---")
        st.markdown("### 🔍 Filtro de Búsqueda")
        termino = st.text_input(
            "Término (opcional)",
            placeholder="ej: patch  |  fps drop  |  update"
        )
        limite = st.slider("Límite de reseñas", min_value=10, max_value=65,
                           value=65, step=5)

        st.markdown("---")
        analizar = st.button("▶ Consultar API y Analizar", use_container_width=True)

        st.markdown("---")
        st.markdown(
            "**Universidad Minuto de Dios**  \n"
            "Ing. Ciencia de Datos  \n"
            "Keller Acevedo · 2026"
        )

    # ── Encabezado principal ──────────────────────────────────────────────────
    st.title("📊 Steam Sentiment Analyzer")
    st.caption(
        "Análisis del impacto de actualizaciones de software en el sentimiento "
        "de comunidades de gaming — Proyecto Final · Objetivo 3"
    )

    # ── Estado inicial (sin análisis) ─────────────────────────────────────────
    if not analizar:
        col1, col2, col3 = st.columns(3)
        col1.info("🟢 Mock API Server activa en puerto 5050")
        col2.info(f"📋 {len(REVIEWS_DATABASE)} reseñas disponibles en el dataset")
        col3.info("⏱ Latencia simulada: 50–150 ms por petición")

        st.markdown("---")
        st.markdown("""
        ### ¿Cómo usar la aplicación?
        1. Ingresa las **credenciales** en la barra lateral (`admin` / `7777`)
        2. Opcionalmente, escribe un **término de búsqueda** para filtrar reseñas
        3. Ajusta el **límite** de registros a procesar
        4. Haz clic en **▶ Consultar API y Analizar**
        """)
        return

    # ── Validación de credenciales ────────────────────────────────────────────
    if usuario != "admin" or password != "7777":
        st.error("❌ Usuario o contraseña incorrectos. Verifique sus credenciales.")
        return

    # ── Ejecución del pipeline ────────────────────────────────────────────────
    with st.spinner("Realizando petición GET a la Mock API..."):
        respuesta_api = simular_peticion_api(termino=termino, limite=limite)

    if not respuesta_api["data"]:
        st.warning("⚠ La API no retornó resultados para ese término de búsqueda.")
        return

    st.success(
        f"✅ Acceso concedido — Petición exitosa · "
        f"{respuesta_api['total_results']} reseñas recibidas · "
        f"Latencia: {respuesta_api['latencia_ms']} ms"
    )

    # Ejecutar pipeline NLP
    with st.spinner("Procesando pipeline de NLP..."):
        df = ejecutar_pipeline_nlp(respuesta_api["data"])

    # ── Métricas principales (tarjetas) ───────────────────────────────────────
    st.markdown("---")
    st.subheader("📈 Métricas del Análisis")

    total    = len(df)
    pos      = (df["sentiment"] == "Positivo").sum()
    neg      = (df["sentiment"] == "Negativo").sum()
    neu      = (df["sentiment"] == "Neutral").sum()
    pol_prom = df["polarity"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total reseñas",      total)
    c2.metric("Polaridad promedio", f"{pol_prom:+.4f}")
    c3.metric("✅ Positivas",        f"{pos} ({pos/total*100:.0f}%)")
    c4.metric("❌ Negativas",         f"{neg} ({neg/total*100:.0f}%)")
    c5.metric("⚪ Neutrales",         f"{neu} ({neu/total*100:.0f}%)")

    # ── Información de la petición API ───────────────────────────────────────
    with st.expander("🔌 Detalles de la Petición HTTP"):
        st.code(
            f"GET {respuesta_api['endpoint']}\n"
            f"Status     : {respuesta_api['status']}\n"
            f"Source     : {respuesta_api['source']}\n"
            f"Records    : {respuesta_api['total_results']}\n"
            f"Latencia   : {respuesta_api['latencia_ms']} ms",
            language="text"
        )

    # ── Dashboard de visualizaciones ─────────────────────────────────────────
    st.markdown("---")
    st.subheader("📊 Dashboard de Visualización")
    fig = generar_dashboard(df)
    st.pyplot(fig)
    plt.close(fig)  # Liberar memoria del objeto figura

    # ── Tabla de Top 5 reseñas más votadas ───────────────────────────────────
    st.markdown("---")
    st.subheader("🏆 Top 5 Reseñas Más Votadas")
    top5 = df.nlargest(5, "score")[["date", "text", "sentiment", "polarity", "score"]].copy()
    top5["date"]      = top5["date"].dt.strftime("%Y-%m-%d")
    top5["polarity"]  = top5["polarity"].round(4)
    top5.columns      = ["Fecha", "Reseña", "Sentimiento", "Polaridad", "Votos"]
    st.dataframe(top5, use_container_width=True, hide_index=True)

    # ── Tabla completa (opcional) ─────────────────────────────────────────────
    with st.expander("📋 Ver todas las reseñas procesadas"):
        df_display = df[["date", "text", "sentiment", "polarity", "score", "playtime"]].copy()
        df_display["date"]     = df_display["date"].dt.strftime("%Y-%m-%d")
        df_display["polarity"] = df_display["polarity"].round(4)
        df_display.columns     = ["Fecha", "Reseña", "Sentimiento", "Polaridad",
                                   "Votos", "Horas Jugadas"]
        st.dataframe(df_display, use_container_width=True, hide_index=True)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    main()
