from dataclasses import dataclass

@dataclass
class Producto:
    id: int
    nombre: str
    precio_cliente: float
    precio_proveedor: float
    precio_instalador: float
    stock: int
