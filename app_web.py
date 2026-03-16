import streamlit as st
import pandas as pd
import os
import time
from core.main import ejecutar_envio
from core.cargar_datos import cargar

# Configuración de la página
st.set_page_config(page_title="Turbo Mailer Pro", page_icon="🚀", layout="wide")

# Estilo personalizado para el título
st.title("🚀 Turbo Mailer Pro")
st.markdown("""
    ### Sistema de Envío Masivo Profesional
    *Configura tu campaña, redacta el mensaje y lanza el envío en segundos.*
""")

# Crear carpetas necesarias si no existen
for carpeta in ['datos', 'adjuntos', 'reportes']:
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

# --- PANEL DE CONFIGURACIÓN ---
col_archivos, col_mensaje = st.columns([1, 1.2])

with col_archivos:
    st.subheader("1️⃣ Carga de Archivos")
    uploaded_file = st.file_uploader("Subir base de datos (Excel)", type=["xlsx"])
    uploaded_adjuntos = st.file_uploader("Subir archivos adjuntos (PDF/Excel)", accept_multiple_files=True)

with col_mensaje:
    st.subheader("2️⃣ Configuración del Correo")
    
    # NUEVO: Campo para el Asunto
    asunto_usuario = st.text_input(
        "Asunto del correo:", 
        placeholder="Ej: Hola {nombre}, aquí tienes tu documento {archivo}"
    )
    
    # Campo para el Cuerpo del Mensaje
    mensaje_usuario = st.text_area(
        "Cuerpo del correo:",
        height=200,
        placeholder="Hola {nombre}, te adjunto el archivo {archivo}..."
    )
    
    st.markdown("""
        **💡 Etiquetas inteligentes:**
        Puedes usar `{nombre}` y `{archivo}` tanto en el **Asunto** como en el **Cuerpo** para que se cambien automáticamente.
    """)

# --- PROCESAMIENTO Y ENVÍO ---
if uploaded_file and uploaded_adjuntos:
    # 1. Guardar y Procesar Excel
    with open(os.path.join("datos", "contactos.xlsx"), "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    cargar() # Sincroniza con SQLite
    
    # 2. Guardar Adjuntos
    for adjunto in uploaded_adjuntos:
        with open(os.path.join("adjuntos", adjunto.name), "wb") as f:
            f.write(adjunto.getbuffer())
            
    st.success(f"✅ ¡Listos para enviar! {len(uploaded_adjuntos)} archivos cargados.")

    st.divider()

    # 3. Botón de Acción
    if st.button("🔥 LANZAR CAMPAÑA AHORA", use_container_width=True):
        if not asunto_usuario or not mensaje_usuario:
            st.warning("⚠️ Por favor, completa el Asunto y el Mensaje antes de iniciar.")
        else:
            # Interfaz de progreso
            barra_progreso = st.progress(0)
            texto_estado = st.empty()
            
            def actualizar_interfaz(actual, total):
                porcentaje = actual / total
                barra_progreso.progress(porcentaje)
                texto_estado.info(f"🚀 Enviando correo {actual} de {total}...")

            with st.spinner('Ejecutando ráfaga de correos...'):
                # Llamada al motor pasando AMBOS campos personalizados
                ejecutar_envio(
                    progreso_callback=actualizar_interfaz, 
                    mensaje_personalizado=mensaje_usuario,
                    asunto_personalizado=asunto_usuario
                )
            
            st.balloons()
            st.success("¡Campaña finalizada con éxito!")

# --- HISTORIAL DE REPORTES ---
st.divider()
with st.expander("📊 Ver Historial de Reportes"):
    if os.path.exists("reportes"):
        reportes = [f for f in os.listdir("reportes") if f.endswith('.xlsx')]
        if reportes:
            seleccion = st.selectbox("Seleccionar reporte", sorted(reportes, reverse=True))
            if seleccion:
                df_rep = pd.read_excel(os.path.join("reportes", seleccion))
                st.dataframe(df_rep, use_container_width=True)
        else:
            st.info("No hay reportes disponibles.")