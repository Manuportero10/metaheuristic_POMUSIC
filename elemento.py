# Implementacion de la clase Elemento
#
class Elemento:
    def __init__(self, nombre : str, peso: int, valor: int):
        self.nombre = nombre
        self.peso = peso
        self.valor = valor

    def __str__(self):
        return f"Elemento: {self.nombre}, Peso: {self.peso}, Valor: {self.valor}\n"