import sqlite3
import os
from utils.helpers import hash_password

DB_PATH = 'inventario.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            nombre TEXT,
            rol TEXT DEFAULT 'vendedor'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE,
            nombre TEXT,
            tipo TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio_cliente REAL,
            precio_proveedor REAL,
            precio_instalador REAL,
            stock INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            usuario_id INTEGER,
            persona_id INTEGER,
            cantidad INTEGER,
            precio_usado REAL,
            fecha TEXT,
            is_deleted INTEGER DEFAULT 0,
            deleted_by INTEGER,
            deleted_at TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (persona_id) REFERENCES personas(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            tipo TEXT,
            cantidad INTEGER,
            fecha TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')

    cursor.execute('SELECT COUNT(*) as cuenta FROM usuarios')
    if cursor.fetchone()['cuenta'] == 0:
        cursor.execute(
            'INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)',
            ('admin', hash_password('admin123'), 'Administrador', 'admin')
        )

    # Migraciones: añadir columnas si no existen
    for alter in [
        "ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'vendedor'",
        "ALTER TABLE ventas ADD COLUMN is_deleted INTEGER DEFAULT 0",
        "ALTER TABLE ventas ADD COLUMN deleted_by INTEGER",
        "ALTER TABLE ventas ADD COLUMN deleted_at TEXT",
    ]:
        try:
            cursor.execute(alter)
        except Exception:
            pass

    cursor.execute("UPDATE usuarios SET rol = 'admin' WHERE username = 'admin'")
    conn.commit()
    conn.close()
