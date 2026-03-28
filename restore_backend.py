import os

files = {
    "1_Instalar_Requisitos.bat": r"""@echo off
echo.
echo ==============================================
echo   CREANDO ACCESO DIRECTO...
echo ==============================================
powershell -Command "$wshell = New-Object -ComObject WScript.Shell; $s = $wshell.CreateShortcut('%CD%\Sistema de Inventario.lnk'); $s.TargetPath = '%CD%\2_Iniciar_Sistema.bat'; $s.WorkingDirectory = '%CD%'; $s.WindowStyle = 7; $s.Save()"

echo.
echo ==============================================
echo   INSTALACION COMPLETADA CON EXITO
echo ==============================================
echo Se ha creado un acceso directo con el nombre "Sistema de Inventario" en tu Escritorio.
echo Ya puedes cerrar esta ventana y usar el acceso directo.
pause
""",

    "2_Iniciar_Sistema.bat": r"""@echo off
echo Iniciando Sistema de Inventario...
pythonw main.py
""",

    "main.py": r"""import sys
import threading
from PySide6.QtWidgets import QApplication
from database.db import init_db
from ui.login_window import LoginWindow
from api_celular import app

def start_mobile_api():
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error en servidor Flask: {e}")

def main():
    # Inicializar Base de Datos
    init_db()

    # Iniciar Aplicación PyQt
    app_qt = QApplication(sys.argv)
    app_qt.setStyle("Fusion") 

    # Motrar ventana de login primero
    login = LoginWindow()
    login.show()

    # Iniciar servidor móvil en background
    api_thread = threading.Thread(target=start_mobile_api, daemon=True)
    api_thread.start()

    sys.exit(app_qt.exec())

if __name__ == "__main__":
    main()
""",

    "utils/helpers.py": r"""import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
""",

    "database/db.py": r"""import sqlite3
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

    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'vendedor'")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE ventas ADD COLUMN is_deleted INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE ventas ADD COLUMN deleted_by INTEGER")
        cursor.execute("ALTER TABLE ventas ADD COLUMN deleted_at TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute("UPDATE usuarios SET rol = 'admin' WHERE username = 'admin'")

    conn.commit()
    conn.close()
""",

    "models/usuario.py": r"""from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    username: str
    password: str
    nombre: str
    rol: str = "vendedor"
""",

    "models/persona.py": r"""from dataclasses import dataclass

@dataclass
class Persona:
    id: int
    cedula: str
    nombre: str
    tipo: str
""",

    "models/producto.py": r"""from dataclasses import dataclass

@dataclass
class Producto:
    id: int
    nombre: str
    precio_cliente: float
    precio_proveedor: float
    precio_instalador: float
    stock: int
""",

    "models/venta.py": r"""from dataclasses import dataclass

@dataclass
class Venta:
    id: int
    producto_id: int
    usuario_id: int
    persona_id: int
    cantidad: int
    precio_usado: float
    fecha: str
""",

    "models/movimiento.py": r"""from dataclasses import dataclass

@dataclass
class Movimiento:
    id: int
    producto_id: int
    tipo: str
    cantidad: int
    fecha: str
""",

    "services/auth_service.py": r"""from database.db import get_connection
from models.usuario import Usuario
from utils.helpers import check_password

class AuthService:
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            if check_password(password, row['password']):
                self.current_user = Usuario(
                    id=row['id'],
                    username=row['username'],
                    password=row['password'],
                    nombre=row['nombre'],
                    rol=dict(row).get('rol', 'vendedor')
                )
                return True
        return False

    def get_current_user(self):
        return self.current_user

    def logout(self):
        self.current_user = None

auth_service = AuthService()
""",

    "services/producto_service.py": r"""from database.db import get_connection
from models.producto import Producto
import datetime

class ProductoService:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        conn.close()
        return [Producto(*row) for row in rows]

    def get_by_id(self, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        return Producto(*row) if row else None

    def create(self, nombre, precio_cliente, precio_proveedor, precio_instalador, stock):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO productos (nombre, precio_cliente, precio_proveedor, precio_instalador, stock) VALUES (?, ?, ?, ?, ?)',
                (nombre, precio_cliente, precio_proveedor, precio_instalador, stock)
            )
            # Agregar movimiento inicial
            prod_id = cursor.lastrowid
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)', (prod_id, 'ENTRADA', stock, fecha))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

producto_service = ProductoService()
""",

    "services/usuario_service.py": r"""from database.db import get_connection
from utils.helpers import hash_password

class UsuarioService:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, nombre, rol FROM usuarios WHERE is_deleted=0 OR is_deleted IS NULL") # Dummy if is_deleted not exist
        return cursor.fetchall()

    def create(self, username, password, nombre, rol):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)',
                (username, hash_password(password), nombre, rol)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

usuario_service = UsuarioService()
""",

    "services/persona_service.py": r"""from database.db import get_connection
from models.persona import Persona

class PersonaService:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personas')
        rows = cursor.fetchall()
        conn.close()
        return [Persona(*row) for row in rows]

    def get_by_cedula(self, cedula):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personas WHERE cedula = ?', (cedula,))
        row = cursor.fetchone()
        conn.close()
        return Persona(*row) if row else None

    def create(self, cedula, nombre, tipo):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO personas (cedula, nombre, tipo) VALUES (?, ?, ?)',
                (cedula, nombre, tipo)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

persona_service = PersonaService()
""",

    "services/venta_service.py": r"""from database.db import get_connection
import datetime

class VentaService:
    def get_historial_ventas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, v.fecha, u.nombre as vendedor, p.nombre as producto, per.nombre as cliente, 
                   v.cantidad, v.precio_usado, 
                   COALESCE(v.is_deleted, 0) as is_deleted,
                   (SELECT nombre from usuarios WHERE id = v.deleted_by) as deleted_by,
                   v.deleted_at
            FROM ventas v
            JOIN usuarios u ON v.usuario_id = u.id
            JOIN productos p ON v.producto_id = p.id
            JOIN personas per ON v.persona_id = per.id
            ORDER BY v.fecha DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def registrar_venta(self, producto_id, usuario_id, persona_id, cantidad, precio_usado):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT stock FROM productos WHERE id = ?', (producto_id,))
        row = cursor.fetchone()
        if not row or row['stock'] < cantidad:
            conn.close()
            return False, "Stock insuficiente"
            
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO ventas (producto_id, usuario_id, persona_id, cantidad, precio_usado, fecha) VALUES (?, ?, ?, ?, ?, ?)',
                (producto_id, usuario_id, persona_id, cantidad, precio_usado, fecha)
            )
            cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, producto_id))
            cursor.execute('INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)', (producto_id, 'SALIDA', cantidad, fecha))
            conn.commit()
            exito = True
            msg = "Venta exitosa"
        except Exception as e:
            conn.rollback()
            exito = False
            msg = str(e)
        finally:
            conn.close()
        return exito, msg

    def eliminar_venta(self, venta_id, admin_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT producto_id, cantidad, is_deleted FROM ventas WHERE id = ?", (venta_id,))
        venta = cursor.fetchone()
        
        if not venta:
            return False, "Venta no encontrada."
        if dict(venta).get("is_deleted") == 1:
            return False, "La venta ya fue anulada previamente."
            
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE ventas SET is_deleted = 1, deleted_by = ?, deleted_at = ? WHERE id = ?", (admin_id, fecha, venta_id))
            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (venta['cantidad'], venta['producto_id']))
            cursor.execute("INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)", (venta['producto_id'], 'RETORNO (Anulación)', venta['cantidad'], fecha))
            conn.commit()
            conn.close()
            return True, "Venta anulada y stock retornado correctamente."
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Error al anular: {str(e)}"

venta_service = VentaService()
"""
}

# Crear carpetas
for folder in ["database", "models", "services", "ui", "utils"]:
    os.makedirs(folder, exist_ok=True)

# Escribir archivos backend y root
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Backend files restored successfully.")
