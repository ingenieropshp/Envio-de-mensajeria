# plantilla.py
from estilos import CUERPO_APP, BOTON_PRO, PIE_PAGINA

def generar_html(nombre):
    return f"""
    <html>
        <body style="background-color: #f4f4f4; padding: 20px;">
            <div style="{CUERPO_APP}">
                <h1 style="color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">
                    ¡Hola, {nombre}!
                </h1>
                <p>Es un placer saludarte. Queríamos informarte que tu suscripción está activa y lista para usarse.</p>
                
                <div style="text-align: center;">
                    <a href="https://tunsitioweb.com" style="{BOTON_PRO}">
                        Acceder a mi Panel
                    </a>
                </div>

                <p>Si tienes alguna duda, simplemente responde a este correo.</p>
                
                <div style="{PIE_PAGINA}">
                    <hr style="border: 0; border-top: 1px solid #eee;">
                    <p>Enviado de forma segura desde tu Base de Datos SQLite.<br>
                    © 2026 Tu Proyecto de Automatización</p>
                </div>
            </div>
        </body>
    </html>
    """