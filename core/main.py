# -*- coding: utf-8 -*-
import sqlite3
import smtplib
import time
import pandas as pd
import mimetypes
import os
from email.message import EmailMessage
from plantilla import generar_html

def ejecutar_envio():
    # --- CONFIGURACION ---
    USER = "nuevasaccionesturbo@gmail.com"
    PASS = "rrrkunlulkvvgxcq" # Tu contraseña de 16 letras
    
    # Rutas relativas (mirando hacia afuera de la carpeta 'core')
    DB_PATH = '../datos/clientes.db'
    ADJUNTOS_FOLDER = '../adjuntos/'
    REPORTES_FOLDER = '../reportes/'

    resultados = []

    try:
        # Conectar a la base de datos en la carpeta 'datos'
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, email, archivo FROM contactos")
        destinatarios = cursor.fetchall()

        if not destinatarios:
            print("⚠️ No hay contactos en la base de datos.")
            return

        print(f"📧 Preparando envío para {len(destinatarios)} contactos...")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USER, PASS)
            print("🚀 Conexión exitosa. Iniciando ráfaga personalizada...")

            for nombre, email, nombre_archivo in destinatarios:
                try:
                    msg = EmailMessage()
                    msg['Subject'] = f"Documento importante para {nombre}"
                    msg['From'] = USER
                    msg['To'] = email
                    
                    contenido = generar_html(nombre)
                    msg.add_alternative(contenido, subtype='html')

                    # --- LÓGICA DE ADJUNTO EN CARPETA ---
                    ruta_archivo = os.path.join(ADJUNTOS_FOLDER, nombre_archivo)
                    
                    if os.path.exists(ruta_archivo):
                        with open(ruta_archivo, 'rb') as f:
                            file_data = f.read()
                            tipo, _ = mimetypes.guess_type(ruta_archivo)
                            maintype, subtype = tipo.split('/')
                            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=nombre_archivo)
                        
                        smtp.send_message(msg)
                        print(f"✅ Enviado: {nombre} ({nombre_archivo})")
                        estado = "Enviado con éxito"
                    else:
                        print(f"⚠️ Archivo no encontrado: {nombre_archivo}")
                        estado = "Error: Archivo faltante"

                    resultados.append({"Nombre": nombre, "Email": email, "Archivo": nombre_archivo, "Estado": estado})
                    time.sleep(2)

                except Exception as e:
                    print(f"❌ Falló {email}: {e}")
                    resultados.append({"Nombre": nombre, "Email": email, "Archivo": nombre_archivo, "Estado": f"Error: {e}"})

    except Exception as e:
        print(f"💥 Error crítico: {e}")
    finally:
        # --- GUARDAR REPORTE EN CARPETA 'REPORTES' ---
        if resultados:
            if not os.path.exists(REPORTES_FOLDER): os.makedirs(REPORTES_FOLDER)
            df_reporte = pd.DataFrame(resultados)
            nombre_reporte = f"{REPORTES_FOLDER}reporte_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
            df_reporte.to_excel(nombre_reporte, index=False)
            print(f"\n📊 Reporte guardado en: {nombre_reporte}")
        
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    ejecutar_envio()