# -*- coding: utf-8 -*-
from estilos import ESTILOS_CSS

def generar_html(nombre_cliente):
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
                <p>Esperamos que estés teniendo un excelente día.</p>
                <p>Te enviamos este correo para compartirte la documentación adjunta que solicitaste. Nuestro sistema ha procesado tu solicitud de manera automática para brindarte un mejor servicio.</p>
                <p><strong>Por favor, revisa el archivo adjunto a este mensaje.</strong></p>
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