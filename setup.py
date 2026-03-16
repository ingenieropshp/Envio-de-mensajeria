import os
import shutil

def organizar_proyecto():
    # 1. Definir las carpetas a crear
    carpetas = ['core', 'datos', 'adjuntos', 'reportes']
    
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"✅ Carpeta creada: {carpeta}")

    # 2. Mover archivos si existen en la raíz
    # (Esto ayuda a limpiar lo que ya tienes)
    movimientos = {
        'main.py': 'core/',
        'plantilla.py': 'core/',
        'cargar_datos.py': 'core/',
        'contactos.xlsx': 'datos/',
        'clientes.db': 'datos/',
        'prueba.pdf': 'adjuntos/'
    }

    for archivo, destino in movimientos.items():
        if os.path.exists(archivo):
            shutil.move(archivo, destino + archivo)
            print(f"🚚 Movido: {archivo} -> {destino}")

    print("\n✨ ¡Estructura profesional lista!")
    print("⚠️ Recuerda actualizar las rutas en tus archivos .py ahora.")

if __name__ == "__main__":
    organizar_proyecto()