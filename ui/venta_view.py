from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QComboBox, QMessageBox, QGroupBox, QFormLayout)
from services.persona_service import persona_service
from services.producto_service import producto_service
from services.venta_service import venta_service
from services.auth_service import auth_service

class VentaView(QWidget):
    def __init__(self):
        super().__init__()
        self.persona_actual = None
        self.productos_dict = {}

        layout = QVBoxLayout()

        # Grupo Cliente
        group_cliente = QGroupBox("Datos del Cliente")
        l_cliente = QFormLayout()
        self.in_cedula = QLineEdit()
        self.btn_buscar_cedula = QPushButton("Buscar")
        self.btn_buscar_cedula.clicked.connect(self.buscar_persona)
        box_cedula = QHBoxLayout()
        box_cedula.addWidget(self.in_cedula)
        box_cedula.addWidget(self.btn_buscar_cedula)
        self.lbl_nombre_persona = QLabel("-")
        self.lbl_tipo_persona = QLabel("-")
        l_cliente.addRow("Cédula:", box_cedula)
        l_cliente.addRow("Nombre:", self.lbl_nombre_persona)
        l_cliente.addRow("Tipo:", self.lbl_tipo_persona)
        group_cliente.setLayout(l_cliente)
        layout.addWidget(group_cliente)

        # Grupo Producto
        group_producto = QGroupBox("Datos del Producto")
        l_producto = QFormLayout()
        self.combo_producto = QComboBox()
        self.lbl_precio_unitario = QLabel("0.0")
        self.in_cantidad = QLineEdit()
        self.in_cantidad.setText("1")
        self.in_cantidad.textChanged.connect(self.actualizar_total)
        self.lbl_total = QLabel("0.0")
        self.actualizar_lista_productos()
        self.combo_producto.currentIndexChanged.connect(self.actualizar_precio)
        l_producto.addRow("Producto:", self.combo_producto)
        l_producto.addRow("Precio Unitario:", self.lbl_precio_unitario)
        l_producto.addRow("Cantidad:", self.in_cantidad)
        l_producto.addRow("Total:", self.lbl_total)
        group_producto.setLayout(l_producto)
        layout.addWidget(group_producto)

        self.btn_vender = QPushButton("Registrar Venta")
        self.btn_vender.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        self.btn_vender.clicked.connect(self.registrar_venta)
        layout.addWidget(self.btn_vender)
        self.setLayout(layout)

    def update_products(self):
        self.actualizar_lista_productos()

    def cargar_productos_dict(self):
        self.productos_dict.clear()
        for p in producto_service.get_all():
            self.productos_dict[p.id] = p

    def actualizar_lista_productos(self):
        self.combo_producto.blockSignals(True)
        self.combo_producto.clear()
        self.cargar_productos_dict()
        for p in self.productos_dict.values():
            self.combo_producto.addItem(f"{p.nombre} (Stock: {p.stock})", userData=p.id)
        self.combo_producto.blockSignals(False)

    def buscar_persona(self):
        cedula = self.in_cedula.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Error", "Ingrese una cédula")
            return
        persona = persona_service.get_by_cedula(cedula)
        if persona:
            self.persona_actual = persona
            self.lbl_nombre_persona.setText(persona.nombre)
            self.lbl_tipo_persona.setText(persona.tipo.capitalize())
            self.actualizar_precio()
        else:
            self.persona_actual = None
            self.lbl_nombre_persona.setText("NO ENCONTRADO")
            self.lbl_tipo_persona.setText("-")
            self.lbl_precio_unitario.setText("0.0")
            QMessageBox.warning(self, "Aviso", "Persona no encontrada en el sistema")

    def actualizar_precio(self):
        if not hasattr(self, 'lbl_precio_unitario'):
            return
        if not self.persona_actual:
            self.lbl_precio_unitario.setText("0.0")
            self.actualizar_total()
            return
        prod_id = self.combo_producto.currentData()
        if not prod_id:
            return
        producto = self.productos_dict.get(prod_id)
        if not producto:
            return
        tipo = self.persona_actual.tipo.lower()
        if tipo == 'proveedor':
            precio = producto.precio_proveedor
        elif tipo == 'instalador':
            precio = producto.precio_instalador
        else:
            precio = producto.precio_cliente
        self.lbl_precio_unitario.setText(str(precio))
        self.actualizar_total()

    def actualizar_total(self):
        try:
            cantidad = int(self.in_cantidad.text())
            precio = float(self.lbl_precio_unitario.text())
            self.lbl_total.setText(str(cantidad * precio))
        except ValueError:
            self.lbl_total.setText("0.0")

    def registrar_venta(self):
        if not self.persona_actual:
            QMessageBox.warning(self, "Error", "Debe buscar y seleccionar un cliente primero.")
            return
        prod_id = self.combo_producto.currentData()
        try:
            cantidad = int(self.in_cantidad.text())
            precio_usado = float(self.lbl_precio_unitario.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Verifique cantidad y precio.")
            return
        usuario = auth_service.get_current_user()
        if not usuario:
            QMessageBox.critical(self, "Error Fatal", "No hay usuario en sesión.")
            return
        exito, msg = venta_service.registrar_venta(prod_id, usuario.id, self.persona_actual.id, cantidad, precio_usado)
        if exito:
            QMessageBox.information(self, "Éxito", "Venta Registrada Exitosamente")
            self.actualizar_lista_productos()
            self.in_cantidad.setText("1")
        else:
            QMessageBox.warning(self, "Error en Venta", msg)
