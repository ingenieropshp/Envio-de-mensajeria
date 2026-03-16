import pandas as pd
import sqlite3

def cargar():
    try:
        df = pd.read_excel('contactos.xlsx')
        
        # Esta línea mágica limpia los nombres de las columnas (quita espacios y mayúsculas)
        df.columns = [c.lower().strip() for c in df.columns]
        
        # Limpia también los datos dentro de las celdas
        df['email'] = df['email'].astype(str).str.strip()
        df['nombre'] = df['nombre'].astype(str).str.strip()

        conexion = sqlite3.connect('clientes.db')
        df.to_sql('contactos', conexion, if_exists='replace', index=False)
        conexion.close()
        
        print("✅ ¡Éxito! Base de datos 'clientes.db' creada correctamente.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    cargar()