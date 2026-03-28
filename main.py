import sys
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

    # Mostrar ventana de login primero
    login = LoginWindow()
    login.show()

    # Iniciar servidor móvil en background
    api_thread = threading.Thread(target=start_mobile_api, daemon=True)
    api_thread.start()

    sys.exit(app_qt.exec())

if __name__ == "__main__":
    main()
