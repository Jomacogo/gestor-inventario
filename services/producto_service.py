from database.db import get_connection
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
            prod_id = cursor.lastrowid
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)',
                           (prod_id, 'ENTRADA', stock, fecha))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

producto_service = ProductoService()
