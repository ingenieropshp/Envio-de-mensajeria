# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import os

def cargar():
    # Rutas relativas para movernos entre carpetas
    EXCEL_PATH = '../datos/contactos.xlsx'
    DB_PATH = '../datos/clientes.db'

    try:
        # 1. Verificar si el Excel existe antes de intentar leerlo
        if not os.path.exists(EXCEL_PATH):
            print(f"❌ Error: No se encontró el archivo Excel en {EXCEL_PATH}")
            return

        # 2. Leer el Excel
        print("📖 Leyendo datos del Excel...")
        df = pd.read_excel(EXCEL_PATH)
        
        # Limpiar nombres de columnas (quitar espacios y poner en minúsculas)
        df.columns = [c.lower().strip() for c in df.columns]
        
        # 3. Conectar a SQLite y guardar/reemplazar la tabla
        conexion = sqlite3.connect(DB_PATH)
        df.to_sql('contactos', conexion, if_exists='replace', index=False)
        conexion.close()
        
        print(f"✅ Base de datos '{DB_PATH}' actualizada con éxito.")
        print(f"👥 Total de contactos cargados: {len(df)}")

    except Exception as e:
        print(f"❌ Error al procesar los datos: {e}")

if __name__ == "__main__":
    cargar()