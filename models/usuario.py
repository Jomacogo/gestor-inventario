from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    username: str
    password: str
    nombre: str
    rol: str = "vendedor"
