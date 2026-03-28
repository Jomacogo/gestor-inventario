from dataclasses import dataclass

@dataclass
class Persona:
    id: int
    cedula: str
    nombre: str
    tipo: str
