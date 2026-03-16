# -*- coding: utf-8 -*-
import sqlite3
import smtplib
import time
import pandas as pd
import mimetypes
import os
from email.message import EmailMessage
from core.plantilla import generar_html

def ejecutar_envio(progreso_callback=None, mensaje_personalizado="", asunto_personalizado=""):
    # --- CONFIGURACION ---
    USER = "nuevasaccionesturbo@gmail.com"
    PASS = "rrrkunlulkvvgxcq" 
    
    # Rutas para ejecución desde la raíz (donde vive app_web.py)
    DB_PATH = 'datos/clientes.db'
    ADJUNTOS_FOLDER = 'adjuntos/'
    REPORTES_FOLDER = 'reportes/'

    resultados = []

    try:
        # 1. Conexión a Base de Datos
        if not os.path.exists(DB_PATH):
            print("❌ La base de datos no existe.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, email, archivo FROM contactos")
        destinatarios = cursor.fetchall()

        if not destinatarios:
            print("⚠️ No hay contactos para enviar.")
            return

        total = len(destinatarios)

        # 2. Inicio de Servidor SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USER, PASS)
            print("🚀 Conexión exitosa. Iniciando ráfaga personalizada...")

            for i, (nombre, email, nombre_archivo) in enumerate(destinatarios):
                try:
                    # --- MAGIA DE PERSONALIZACIÓN ---
                    # Personalizamos el ASUNTO
                    asunto_final = asunto_personalizado.replace("{nombre}", nombre).replace("{archivo}", nombre_archivo)
                    
                    # Personalizamos el CUERPO del mensaje
                    mensaje_final = mensaje_personalizado.replace("{nombre}", nombre).replace("{archivo}", nombre_archivo)
                    
                    msg = EmailMessage()
                    msg['Subject'] = asunto_final # <--- ASUNTO DINÁMICO
                    msg['From'] = USER
                    msg['To'] = email
                    
                    # Generamos el HTML con el mensaje ya personalizado
                    contenido_html = generar_html(nombre, mensaje_final)
                    msg.add_alternative(contenido_html, subtype='html')

                    # --- GESTIÓN DE ADJUNTO ---
                    ruta_archivo = os.path.join(ADJUNTOS_FOLDER, nombre_archivo)
                    
                    if os.path.exists(ruta_archivo):
                        with open(ruta_archivo, 'rb') as f:
                            file_data = f.read()
                            tipo, _ = mimetypes.guess_type(ruta_archivo)
                            tipo = tipo if tipo else 'application/octet-stream'
                            maintype, subtype = tipo.split('/')
                            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=nombre_archivo)
                        
                        smtp.send_message(msg)
                        estado = "Enviado con éxito"
                        print(f"✅ {i+1}/{total} Enviado: {nombre} | Asunto: {asunto_final}")
                    else:
                        estado = "Error: Archivo no encontrado"
                        print(f"⚠️ Archivo faltante: {nombre_archivo}")

                    resultados.append({"Nombre": nombre, "Email": email, "Archivo": nombre_archivo, "Estado": estado})
                    
                    # --- ACTUALIZAR INTERFAZ WEB ---
                    if progreso_callback:
                        progreso_callback(i + 1, total)

                    time.sleep(1.5) # Pausa estratégica anti-spam

                except Exception as e:
                    print(f"❌ Error enviando a {email}: {e}")
                    resultados.append({"Nombre": nombre, "Email": email, "Archivo": nombre_archivo, "Estado": f"Error: {e}"})

    except Exception as e:
        print(f"💥 Error crítico en el motor: {e}")
    finally:
        # --- GENERACIÓN DE REPORTE FINAL ---
        if resultados:
            if not os.path.exists(REPORTES_FOLDER): os.makedirs(REPORTES_FOLDER)
            df_reporte = pd.DataFrame(resultados)
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            nombre_reporte = f"{REPORTES_FOLDER}reporte_{timestamp}.xlsx"
            df_reporte.to_excel(nombre_reporte, index=False)
            print(f"📊 Proceso terminado. Reporte generado en carpeta 'reportes'.")
        
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    # Prueba rápida
    ejecutar_envio(
        asunto_personalizado="Prueba para {nombre}", 
        mensaje_personalizado="Hola {nombre}, este es el archivo {archivo}"
    )