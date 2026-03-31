from PySide6.QtWidgets import QMainWindow, QTabWidget, QLabel
from services.auth_service import auth_service
from ui.personas_view import PersonasView
from ui.inventario_view import InventarioView
from ui.venta_view import VentaView
from ui.historial_ventas_view import HistorialVentasView
from ui.usuarios_view import UsuariosView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        user = auth_service.get_current_user()
        nombre = user.nombre if user else "Desconocido"
        self.setWindowTitle(f"InventarioJC - Vendedor: {nombre}")
        self.resize(800, 600)

        # Barra de herramientas
        toolbar = self.addToolBar("Opciones")
        btn_cerrar_sesion = toolbar.addAction("Cerrar Sesión")
        btn_cerrar_sesion.triggered.connect(self.cerrar_sesion)

        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            ip = "127.0.0.1"

        lbl_mobile = QLabel(f"  📱 App Celular: http://{ip}:5000")
        lbl_mobile.setStyleSheet("font-weight: bold; color: blue; padding-left: 20px;")
        toolbar.addWidget(lbl_mobile)

        # Tabs principales
        self.tabs = QTabWidget()

        self.venta_tab = VentaView()
        self.personas_tab = PersonasView()
        self.inventario_tab = InventarioView()
        self.historial_tab = HistorialVentasView()

        self.tabs.addTab(self.venta_tab, "Ventas")
        self.tabs.addTab(self.personas_tab, "Personas")
        self.tabs.addTab(self.inventario_tab, "Inventario")
        self.tabs.addTab(self.historial_tab, "Historial de Ventas")

        # Sólo admin ve gestión de usuarios
        if user and user.rol == 'admin':
            self.usuarios_tab = UsuariosView()
            self.tabs.addTab(self.usuarios_tab, "Gestión Administrativa")

        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)

    def on_tab_changed(self, index):
        widget = self.tabs.widget(index)
        if hasattr(widget, 'update_data'):
            widget.update_data()
        if hasattr(widget, 'update_products'):
            widget.update_products()

    def cerrar_sesion(self):
        auth_service.logout()
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
