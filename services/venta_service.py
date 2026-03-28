from database.db import get_connection
import datetime

class VentaService:
    def get_historial_ventas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, v.fecha, u.nombre as vendedor, p.nombre as producto, per.nombre as cliente,
                   v.cantidad, v.precio_usado,
                   COALESCE(v.is_deleted, 0) as is_deleted,
                   (SELECT nombre FROM usuarios WHERE id = v.deleted_by) as deleted_by,
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
            cursor.execute('INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)',
                           (producto_id, 'SALIDA', cantidad, fecha))
            conn.commit()
            return True, "Venta exitosa"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

    def eliminar_venta(self, venta_id, admin_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT producto_id, cantidad, is_deleted FROM ventas WHERE id = ?", (venta_id,))
        venta = cursor.fetchone()
        if not venta:
            conn.close()
            return False, "Venta no encontrada."
        if dict(venta).get("is_deleted") == 1:
            conn.close()
            return False, "La venta ya fue anulada previamente."
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE ventas SET is_deleted = 1, deleted_by = ?, deleted_at = ? WHERE id = ?",
                           (admin_id, fecha, venta_id))
            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (venta['cantidad'], venta['producto_id']))
            cursor.execute("INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)",
                           (venta['producto_id'], 'RETORNO (Anulación)', venta['cantidad'], fecha))
            conn.commit()
            conn.close()
            return True, "Venta anulada y stock retornado correctamente."
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, str(e)

venta_service = VentaService()
