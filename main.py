# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sqlite3
import smtplib
import time
import pandas as pd
import mimetypes
import os  # Para verificar si el archivo existe
from email.message import EmailMessage
from plantilla import generar_html

def ejecutar_envio():
    USER = "nuevasaccionesturbo@gmail.com"
    PASS = "tu_clave_de_16_letras" 
    
    resultados = []

    try:
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        # Ahora traemos también la columna 'archivo'
        cursor.execute("SELECT nombre, email, archivo FROM contactos")
        destinatarios = cursor.fetchall()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USER, PASS)
            print("🚀 Conectado. Iniciando envío personalizado...")

            for nombre, email, nombre_archivo in destinatarios:
                try:
                    msg = EmailMessage()
                    msg['Subject'] = f"Documento adjunto para {nombre}"
                    msg['From'] = USER
                    msg['To'] = email
                    
                    contenido = generar_html(nombre)
                    msg.add_alternative(contenido, subtype='html')

                    # --- ADJUNTO PERSONALIZADO ---
                    if os.path.exists(nombre_archivo):
                        with open(nombre_archivo, 'rb') as f:
                            file_data = f.read()
                            tipo, _ = mimetypes.guess_type(nombre_archivo)
                            maintype, subtype = tipo.split('/')
                            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=nombre_archivo)
                        
                        smtp.send_message(msg)
                        print(f"✅ Enviado a {nombre} con el archivo: {nombre_archivo}")
                        estado = "Enviado con éxito"
                    else:
                        print(f"⚠️ El archivo {nombre_archivo} no se encontró para {nombre}")
                        estado = "Error: Archivo no encontrado"

                    resultados.append({"Nombre": nombre, "Email": email, "Archivo": nombre_archivo, "Estado": estado})
                    time.sleep(3)

                except Exception as e:
                    print(f"❌ Error con {email}: {e}")
                    resultados.append({"Nombre": nombre, "Email": email, "Archivo": nombre_archivo, "Estado": f"Error: {e}"})

    except Exception as e:
        print(f"💥 Error crítico: {e}")
    finally:
        if resultados:
            pd.DataFrame(resultados).to_excel('reporte_detallado.xlsx', index=False)
            print("\n📊 Reporte final generado.")
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    ejecutar_envio()