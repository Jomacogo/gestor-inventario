from dataclasses import dataclass

@dataclass
class Venta:
    id: int
    producto_id: int
    usuario_id: int
    persona_id: int
    cantidad: int
    precio_usado: float
    fecha: str
