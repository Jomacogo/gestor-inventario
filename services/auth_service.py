from database.db import get_connection
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

        if row and check_password(password, row['password']):
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
