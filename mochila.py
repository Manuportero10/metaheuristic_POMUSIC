# Implementacion de la clase Mochila
from elemento import Elemento

class Mochila:
    def __init__(self, capacidad: int, objetos: list):
        self.capacidad_max = capacidad
        self.objetos = objetos

    def agregar_objeto(self, objeto: Elemento ):
        self.objetos.append(objeto)

    def __str__(self):
        return f'objetos: {self.objetos.__str__().__str__()}'
    
    def copy(self):
        return Mochila(self.capacidad_max, self.objetos[:])