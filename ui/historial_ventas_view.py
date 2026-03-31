from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QMessageBox, QFileDialog, QLineEdit, QLabel)
from PySide6.QtGui import QColor
from openpyxl import Workbook
from services.venta_service import venta_service
from services.auth_service import auth_service

class HistorialVentasView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.in_busqueda = QLineEdit()
        self.in_busqueda.setPlaceholderText("Escriba para buscar en el historial...")
        self.in_busqueda.textChanged.connect(self.filtrar_tabla)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.in_busqueda)
        layout.addLayout(search_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Vendedor", "Cliente", "Producto", "Cantidad", "Total ($)"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        btn_anular = QPushButton("Anular / Eliminar Venta Seleccionada")
        btn_anular.setStyleSheet("color: red; font-weight: bold; padding: 5px;")
        btn_anular.clicked.connect(self.anular_venta)
        layout.addWidget(btn_anular)

        btn_excel = QPushButton("Exportar Historial a Excel")
        btn_excel.setStyleSheet("color: white; background-color: #28a745; font-weight: bold; font-size: 14px; padding: 5px;")
        btn_excel.clicked.connect(self.exportar_excel)
        layout.addWidget(btn_excel)

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
        ventas = venta_service.get_historial_ventas()
        for v in ventas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            total = float(v['cantidad']) * float(v['precio_usado'])
            for col, val in enumerate([v['id'], v['fecha'], v['vendedor'], v['cliente'], v['producto'], v['cantidad'], f"${total:.2f}"]):
                item = QTableWidgetItem(str(val))
                if v['is_deleted'] == 1:
                    item.setBackground(QColor('#ffcccc'))
                self.tabla.setItem(row, col, item)

    def anular_venta(self):
        row = self.tabla.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione una venta de la lista.")
            return
        venta_id = int(self.tabla.item(row, 0).text())
        usuario = auth_service.get_current_user()
        if not usuario or usuario.rol != 'admin':
            QMessageBox.warning(self, "Acceso denegado", "Solo el administrador puede anular ventas.")
            return
        resp = QMessageBox.question(self, "Confirmar", f"¿Anular la venta #{venta_id}? Se devolverá el stock.")
        if resp == QMessageBox.Yes:
            exito, msg = venta_service.eliminar_venta(venta_id, usuario.id)
            if exito:
                QMessageBox.information(self, "Éxito", msg)
                self.cargar_datos()
            else:
                QMessageBox.warning(self, "Error", msg)

    def exportar_excel(self):
        ventas = venta_service.get_historial_ventas()
        if not ventas:
            QMessageBox.information(self, "Aviso", "No hay ventas registradas para exportar.")
            return
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar Excel", "Reporte_Ventas.xlsx", "Archivos Excel (*.xlsx)")
        if not ruta:
            return
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Historial Ventas"
            ws.append(["ID", "Fecha", "Vendedor", "Cliente", "Producto", "Cantidad", "Total ($)", "Estado", "Anulado Por", "Fecha Anulación"])
            for v in ventas:
                total = float(v['cantidad']) * float(v['precio_usado'])
                estado = "Anulada" if v['is_deleted'] == 1 else "Activa"
                ws.append([v['id'], v['fecha'], v['vendedor'], v['cliente'], v['producto'],
                            v['cantidad'], total, estado, v.get('deleted_by') or '', v.get('deleted_at') or ''])
            for col in ws.columns:
                max_length = max((len(str(cell.value)) for cell in col if cell.value), default=10)
                ws.column_dimensions[col[0].column_letter].width = max_length + 2
            wb.save(ruta)
            QMessageBox.information(self, "Éxito", f"Archivo exportado:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al exportar:\n{e}")
