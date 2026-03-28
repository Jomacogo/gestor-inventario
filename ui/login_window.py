from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from services.auth_service import auth_service

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión - Login")
        self.setFixedSize(350, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.in_user = QLineEdit()
        self.in_user.setPlaceholderText("Usuario")
        self.in_pass = QLineEdit()
        self.in_pass.setPlaceholderText("Contraseña")
        self.in_pass.setEchoMode(QLineEdit.Password)
        self.in_pass.returnPressed.connect(self.attempt_login)

        btn_login = QPushButton("Iniciar Sesión")
        btn_login.clicked.connect(self.attempt_login)

        layout.addWidget(QLabel("Ingrese sus credenciales:"))
        layout.addWidget(self.in_user)
        layout.addWidget(self.in_pass)
        layout.addWidget(btn_login)
        self.setLayout(layout)

    def attempt_login(self):
        username = self.in_user.text().strip()
        password = self.in_pass.text()

        if auth_service.login(username, password):
            from ui.main_window import MainWindow
            self.main_window_ref = MainWindow()
            self.main_window_ref.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            self.in_pass.clear()
