from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                               QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                               QMessageBox, QFormLayout, QGroupBox, QComboBox)
from services.producto_service import producto_service

class InventarioView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Formulario agregar producto
        group = QGroupBox("Agregar Nuevo Producto")
        form = QFormLayout()
        self.in_nombre = QLineEdit()
        self.in_pc = QLineEdit()
        self.in_pp = QLineEdit()
        self.in_pi = QLineEdit()
        self.in_stock = QLineEdit()
        form.addRow("Nombre:", self.in_nombre)
        form.addRow("Precio Cliente:", self.in_pc)
        form.addRow("Precio Proveedor:", self.in_pp)
        form.addRow("Precio Instalador:", self.in_pi)
        form.addRow("Stock Inicial:", self.in_stock)
        btn_add = QPushButton("Agregar Producto")
        btn_add.clicked.connect(self.agregar_producto)
        form.addRow(btn_add)
        group.setLayout(form)
        layout.addWidget(group)

        # Barra de Búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.in_busqueda = QLineEdit()
        self.in_busqueda.setPlaceholderText("Escriba para buscar en esta tabla...")
        self.in_busqueda.textChanged.connect(self.filtrar_tabla)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.in_busqueda)
        layout.addLayout(search_layout)

        # Tabla de productos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "P.Cliente", "P.Proveedor", "P.Instalador", "Stock"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_datos()

    def filtrar_tabla(self, texto):
        for row in range(self.tabla.rowCount()):
            match = False
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                if item and texto.lower() in item.text().lower():
                    match = True
                    break
            self.tabla.setRowHidden(row, not match)

    def update_data(self):
        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        for p in producto_service.get_all():
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            for col, val in enumerate([p.id, p.nombre, p.precio_cliente, p.precio_proveedor, p.precio_instalador, p.stock]):
                self.tabla.setItem(row, col, QTableWidgetItem(str(val)))

    def agregar_producto(self):
        try:
            nombre = self.in_nombre.text().strip()
            pc = float(self.in_pc.text())
            pp = float(self.in_pp.text())
            pi = float(self.in_pi.text())
            stock = int(self.in_stock.text())
            if not nombre:
                raise ValueError("Nombre vacío")
            if producto_service.create(nombre, pc, pp, pi, stock):
                QMessageBox.information(self, "Éxito", "Producto agregado.")
                for w in [self.in_nombre, self.in_pc, self.in_pp, self.in_pi, self.in_stock]:
                    w.clear()
                self.cargar_datos()
            else:
                QMessageBox.warning(self, "Error", "Error al agregar el producto.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Verifique los datos: {e}")
