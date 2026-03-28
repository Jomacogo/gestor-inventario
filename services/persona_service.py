from database.db import get_connection
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
            cursor.execute('INSERT INTO personas (cedula, nombre, tipo) VALUES (?, ?, ?)', (cedula, nombre, tipo))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

persona_service = PersonaService()
