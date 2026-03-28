from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QMessageBox, QGroupBox, QFormLayout, QLineEdit, QComboBox)
from services.persona_service import persona_service

class PersonasView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        group = QGroupBox("Registrar Persona")
        form = QFormLayout()
        self.in_cedula = QLineEdit()
        self.in_nombre = QLineEdit()
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["cliente", "proveedor", "instalador"])
        form.addRow("Cédula:", self.in_cedula)
        form.addRow("Nombre:", self.in_nombre)
        form.addRow("Tipo:", self.combo_tipo)
        btn_add = QPushButton("Registrar")
        btn_add.clicked.connect(self.agregar_persona)
        form.addRow(btn_add)
        group.setLayout(form)
        layout.addWidget(group)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Cédula", "Nombre", "Tipo"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        self.cargar_datos()

    def update_data(self):
        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        for p in persona_service.get_all():
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            for col, val in enumerate([p.id, p.cedula, p.nombre, p.tipo]):
                self.tabla.setItem(row, col, QTableWidgetItem(str(val)))

    def agregar_persona(self):
        cedula = self.in_cedula.text().strip()
        nombre = self.in_nombre.text().strip()
        tipo = self.combo_tipo.currentText()
        if not cedula or not nombre:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos.")
            return
        if persona_service.create(cedula, nombre, tipo):
            QMessageBox.information(self, "Éxito", "Persona registrada correctamente.")
            self.in_cedula.clear()
            self.in_nombre.clear()
            self.cargar_datos()
        else:
            QMessageBox.warning(self, "Error", "La cédula ya existe o hubo un error.")
