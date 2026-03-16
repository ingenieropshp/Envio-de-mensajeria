# -*- coding: utf-8 -*-
import sqlite3
import smtplib
import time
import pandas as pd  # Para generar el reporte
from email.message import EmailMessage
from plantilla import generar_html

def ejecutar_envio():
    USER = "nuevasaccionesturbo@gmail.com"
    PASS = "wxckynvusksslpqh" 
    
    resultados = [] # Lista para guardar el estado de cada envío

    try:
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, email FROM contactos")
        destinatarios = cursor.fetchall()

        if not destinatarios:
            print("⚠️ Base de datos vacía.")
            return

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USER, PASS)
            print("🚀 Conexión exitosa. Iniciando ráfaga...")

            for nombre, email in destinatarios:
                try:
                    msg = EmailMessage()
                    msg['Subject'] = f"Mensaje para {nombre}"
                    msg['From'] = USER
                    msg['To'] = email
                    
                    contenido = generar_html(nombre)
                    msg.add_alternative(contenido, subtype='html')

                    smtp.send_message(msg)
                    print(f"✅ Enviado: {email}")
                    
                    # Guardamos éxito en la lista
                    resultados.append({"Nombre": nombre, "Email": email, "Estado": "Enviado", "Fecha": time.strftime("%H:%M:%S")})
                    time.sleep(2)

                except Exception as e:
                    print(f"❌ Falló: {email}")
                    resultados.append({"Nombre": nombre, "Email": email, "Estado": f"Error: {str(e)}", "Fecha": time.strftime("%H:%M:%S")})

    except Exception as e:
        print(f"💥 Error de conexión: {e}")
    finally:
        # --- GENERAR REPORTE AL FINAL ---
        if resultados:
            df_reporte = pd.DataFrame(resultados)
            df_reporte.to_excel('reporte_envio.xlsx', index=False)
            print("\n📊 ¡Reporte generado como 'reporte_envio.xlsx'!")
        
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    ejecutar_envio()