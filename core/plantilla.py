# -*- coding: utf-8 -*-
from core.estilos import ESTILOS_CSS

def generar_html(nombre_cliente, mensaje_cuerpo):
    # Convertimos los saltos de línea del área de texto de Streamlit (\n)
    # a etiquetas de salto de línea HTML (<br>) para que mantenga el formato.
    mensaje_html = mensaje_cuerpo.replace("\n", "<br>")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {ESTILOS_CSS}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>¡Hola, {nombre_cliente}!</h1>
            </div>
            <div class="content">
                <p>{mensaje_html}</p>
                
                <center>
                    <a href="https://tuempresa.com" class="button">Visitar nuestro sitio</a>
                </center>
            </div>
            <div class="footer">
                <p>Este es un correo automático, por favor no lo respondas.</p>
                <p>© 2026 Nuevas Acciones Turbo | Medellin, Colombia</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html