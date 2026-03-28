from database.db import get_connection
from utils.helpers import hash_password

class UsuarioService:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, nombre, rol FROM usuarios")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

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

    def delete(self, user_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

usuario_service = UsuarioService()
