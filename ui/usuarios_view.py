from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QMessageBox, QGroupBox, QFormLayout,
                               QLineEdit, QComboBox)
from services.usuario_service import usuario_service

class UsuariosView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        group = QGroupBox("Crear Nuevo Usuario")
        form = QFormLayout()
        self.in_username = QLineEdit()
        self.in_password = QLineEdit()
        self.in_password.setEchoMode(QLineEdit.Password)
        self.in_nombre = QLineEdit()
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["vendedor", "admin"])
        form.addRow("Usuario:", self.in_username)
        form.addRow("Contraseña:", self.in_password)
        form.addRow("Nombre:", self.in_nombre)
        form.addRow("Rol:", self.combo_rol)
        btn_crear = QPushButton("Crear Usuario")
        btn_crear.clicked.connect(self.crear_usuario)
        form.addRow(btn_crear)
        group.setLayout(form)
        layout.addWidget(group)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Username", "Nombre", "Rol"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        btn_eliminar = QPushButton("Eliminar Usuario Seleccionado")
        btn_eliminar.setStyleSheet("color: red; font-weight: bold;")
        btn_eliminar.clicked.connect(self.eliminar_usuario)
        layout.addWidget(btn_eliminar)

        self.setLayout(layout)
        self.cargar_datos()

    def update_data(self):
        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        for u in usuario_service.get_all():
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            for col, val in enumerate([u['id'], u['username'], u['nombre'], u['rol']]):
                self.tabla.setItem(row, col, QTableWidgetItem(str(val)))

    def crear_usuario(self):
        username = self.in_username.text().strip()
        password = self.in_password.text()
        nombre = self.in_nombre.text().strip()
        rol = self.combo_rol.currentText()
        if not username or not password or not nombre:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos.")
            return
        if usuario_service.create(username, password, nombre, rol):
            QMessageBox.information(self, "Éxito", f"Usuario '{username}' creado correctamente.")
            self.in_username.clear()
            self.in_password.clear()
            self.in_nombre.clear()
            self.cargar_datos()
        else:
            QMessageBox.warning(self, "Error", "El usuario ya existe o hubo un error.")

    def eliminar_usuario(self):
        row = self.tabla.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un usuario de la lista.")
            return
        user_id = int(self.tabla.item(row, 0).text())
        username = self.tabla.item(row, 1).text()
        if username == 'admin':
            QMessageBox.warning(self, "Error", "No puedes eliminar al administrador principal.")
            return
        resp = QMessageBox.question(self, "Confirmar", f"¿Eliminar al usuario '{username}'?")
        if resp == QMessageBox.Yes:
            if usuario_service.delete(user_id):
                QMessageBox.information(self, "Éxito", "Usuario eliminado.")
                self.cargar_datos()
