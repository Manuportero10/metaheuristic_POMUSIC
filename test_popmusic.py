# Programa de prueba para la implementacion del algoritmo metaheuristico POPMUSIC
from elemento import Elemento
from mochila import Mochila  
import random


# Implementacion del meta-algoritmo POPMUSIC
def popmusic(mochila : Mochila, lista_elementos : list) -> list:
    lista_elementos_inmutable = lista_elementos.copy() # Creamos una copia de la lista de elementos	

    # Generamos una solucion inicial aleatoriamente
    s_inicial : Mochila = meter_al_azar(mochila, lista_elementos)
    print("\n----------Solucion inicial---------\n")
    for elemento in s_inicial.objetos:
        print(elemento.__str__())

    # Dividimos la solucion en partes, que sera una lista de listas
    s_inicial_aux : Mochila = s_inicial.copy()
    n = 2 # Numero de elementos por parte, criterio libre
    partes_list : list = dividir_solucion(s_inicial_aux,n)

    print("\n----------Partes de la solucion inicial---------\n")
    indice : int = 0
    for parte in partes_list:
        print(f'Parte {indice}\n')
        for elemento in parte:
            print(elemento.__str__())
        indice += 1

    # Creamos un conjunto optimizado, que sera una lista de partes s_i
    conjunto_optimizado : list = []
    
    # Mientras que no se haya optimizado todas las partes
    # Si todas las partes estan optimizadas, eso significa que conjunto_optimizado tiene todas las partes
    while not todas_partes_optimizadas(conjunto_optimizado, partes_list):
        # Seleccionamos una parte aleatoria, que no haya sido optimizada antes
        while True:
            indice_aleatorio = random.randint(0, len(partes_list) - 1)
            parte = partes_list[indice_aleatorio] # Seleccionamos una parte aleatoria s_i
            if parte not in conjunto_optimizado: 
                break # Salimos del bucle, hemos cogido una parte que no ha sido optimizada

            print(f'indice aleatorio: {indice_aleatorio}') 
             
   
        print(f"\nParte seleccionada\n")
        for elemento in parte:
            print(elemento.__str__())

        subproblema : list = []

        # Creamos un vector de indices donde guardaremos las partes vecinas s_i correspondientes
        vector_i : list = []

        # Creamos el subproblema con la parte seleccionada con su vecindad
        subproblema,vector_i = crear_subproblema(parte, partes_list)
        vector_i.insert(0,indice_aleatorio) # Insertamos el indice de la parte seleccionada

        print("\n------------Subproblema-------------\n")
        for parte_n in subproblema:
            for elemento in parte_n:
                print(elemento.__str__())

        # Creamos una copia de la lista de elementos y del subproblema auxiliares
        # porque tanto lista_elementos como subproblema se van a modificar
        lista_elementos_aux = lista_elementos_inmutable.copy()
        subproblema_aux = []
        for parte_n in subproblema:
            subproblema_aux.append(parte_n[:])

        # optimizamos el suproblema
        parte_optimizada,elemento_menor = optimizar_subproblema(mochila.capacidad_max,subproblema_aux,lista_elementos_aux,mochila.objetos)
        print("\n------------Subproblema optimizado-------------\n")
        for parte_n in parte_optimizada:
            for elemento in parte_n:
                print(elemento.__str__())

        # Si la parte optimizada es mejor que la solucion inicial y cabe los elementos de la parte optimizada en la mochila
        if calcular_productividad_subproblema(parte_optimizada) > calcular_productividad_subproblema(subproblema):
            print("\n--------------[SOLUCION OPTIMIZADA]---------------\n")
            # Creamos una copia de los objetos que tiene la mochila antes de actualizarla
            lista_objetos_aux = s_inicial.objetos[:]
            s_inicial.objetos = actualizar_solucion(s_inicial.objetos, parte_optimizada,elemento_menor) # Se actualiza la solucion inicial

            # Cabe la posibilidad de que a la hora de haber optimizado un subproblema
            # A la hora de meter la solucion parcial a la mochila, no quepa
            if sum([elemento.peso for elemento in s_inicial.objetos]) > mochila.capacidad_max:
                print("La solucion no cabe en la mochila")
                s_inicial.objetos = lista_objetos_aux
                conjunto_optimizado.append(parte)
            else:
                actualizar_partes(partes_list,parte_optimizada,vector_i) # Se actualizan las partes del problema
                conjunto_optimizado = []

            print(f'------------Estado de la solucion optimizada------------\n')
            for elemento in s_inicial.objetos:
                print(elemento.__str__())
        else: # No se ha optimizdo la solucion
            print("\n---------------------[SOLUCION NO OPTIMIZADA]---------------------------\n")
            conjunto_optimizado.append(parte)
            
            
    return s_inicial


def meter_al_azar(mochila : Mochila, lista_elementos : list) -> Mochila:
    # Creamos una copia de la mochila
    mochila_copia = Mochila(mochila.capacidad_max, mochila.objetos)
    # Mientras la mochila no este llena
    while mochila_copia.capacidad_max > 0 and len(lista_elementos) > 0:
        # Seleccionamos un elemento aleatorio
        indice_aleatorio = random.randint(0, len(lista_elementos) - 1)
        elemento = lista_elementos.pop(indice_aleatorio)
        # Si el elemento cabe en la mochila
        if elemento.peso <= mochila_copia.capacidad_max:
            # Lo agregamos a la mochila
            mochila_copia.agregar_objeto(elemento)
            # Restamos el peso del elemento a la capacidad de la mochila
            mochila_copia.capacidad_max -= elemento.peso

    return mochila_copia

'''
    Funcion para dividir la solucion en partes, cada parte tendra n_elementos_parte elementos
'''
def dividir_solucion(solucion : Mochila, n_elementos_parte : int) -> list:
    # Creamos una lista de listas
    lista_partes = []

    # Mientras haya elementos en la solucion
    while len(solucion.objetos) > 0:
        # Creamos una lista temporal
        lista_temporal = []
        # Mientras la lista temporal no tenga el tamaño de la parte
        while len(lista_temporal) < n_elementos_parte and len(solucion.objetos) > 0:
            # Agregamos un elemento a la lista temporal
            lista_temporal.append(solucion.objetos.pop())
        # Agregamos la lista temporal a la lista de partes
        lista_partes.append(lista_temporal)

    return lista_partes

def crear_subproblema(parte : list, partes_list : list) -> list:
    # Creamos un vector de indices donde guardaremos las partes vecinas s_i correspondientes
    vector_i : list = []
    # Creamos una lista de subproblemas
    subproblema = []
    # Agregamos la parte al subproblema
    subproblema.append(parte)
    # Se recorre las demas partes para ver si se pueden agregar a la vecindad
    for parte_vecina in partes_list:
        # Si la parte vecina no es la parte actual
        if parte_vecina != parte:
            # Determinamos si 2 partes son vecinas, si el ratio de valor/peso difiere en 1 unidades o menos
            if abs(calcular_productividad(parte) - calcular_productividad(parte_vecina)) <= 1:
                subproblema.append(parte_vecina)
                # añadimos el indice de la parte vecina, es decir el i del s_i
                vector_i.append(partes_list.index(parte_vecina))

    return subproblema,vector_i

def calcular_productividad(parte : list) -> float:
    suma_peso = 0
    suma_valor = 0
    for elemento in parte:
        suma_peso += elemento.peso
        suma_valor += elemento.valor
    return suma_valor / suma_peso

def calcular_productividad_subproblema(parte : list) -> float:
    suma_valor = 0
    for parte_n in parte:
        for elemento in parte_n:
            suma_valor += elemento.valor

    print(f'VALOR DEL SUBPROBLEMA: {suma_valor}')
    return suma_valor

'''
 Basicamente nuestro criterio de optimizar el subproblema reside en ver que elemento del subproblema tiene menor productividad
    y cambiarlo por un elemento de una productividad mayor (elegido aleatoriamente) que no este en la mochila, por lo que no estará en el subproblema
'''
def optimizar_subproblema(capacidad_maxima : int,subproblema : list, lista_elementos_aux : list, mochila_objetos : list) -> list:
    # Variable para guardar el elemento con menor productividad
    productivada_menor = 999999
    elemento_menor = None
    
    # Variable auxiliar para saber en que parte esta el elemento con menor productividad dentro de las partes
    vecino_i : int = 0
    # bucle para encontrar el elemento con menor productividad
    for i_parte in subproblema:
        for elemento in i_parte:
            productividad = elemento.valor / elemento.peso
            if productividad < productivada_menor:
                productivada_menor = productividad
                vecino_i = subproblema.index(i_parte)
                elemento_menor = elemento
                
    
    # Se busca el primer elemento de lista_elementos_aux que no este en la mochila y que tenga mayor productividad que el elemento_menor
    # El elemento lo elegiremos aleatoriamente
    while True and len(lista_elementos_aux) > 0:
        indice_aleatorio = random.randint(0, len(lista_elementos_aux) - 1)
        elemento = lista_elementos_aux.pop(indice_aleatorio) # cogemos elemento aleatorio
        # Comprobamos si el elemento no esta en la lista de elementos y si su productividad es mayor que la del elemento_menor 
        # y si cabe en la mochila
        if elemento_no_en_mochila(elemento,mochila_objetos) and elemento.valor / elemento.peso > productivada_menor and cabe_elemento_en_mochila(capacidad_maxima,elemento_menor,elemento,subproblema):
            subproblema[vecino_i].remove(elemento_menor)
            subproblema[vecino_i].append(elemento)
            break

    return subproblema,elemento_menor

def actualizar_solucion(objetos_mochila : list, subproblema_optimizado : list, elemento_menor : Elemento) -> list:
    # Quitamos el elemento con menor productividad de la mochila
    objetos_mochila.remove(elemento_menor)
    # Agregamos el elemento que nos permite actualizar la solucion, recorriendo las partes del subproblema optimizado
    for parte in subproblema_optimizado:
        for elemento in parte:
            if elemento not in objetos_mochila:
                objetos_mochila.append(elemento)
                break

    return objetos_mochila

def actualizar_partes(partes : list, parte_optimizada : list, lista_s_i : list) -> None:
    # Se actualizan las partes
    if len(parte_optimizada) == 1:
        partes[lista_s_i[0]] = parte_optimizada[0]
    else:
        indice : int = 0 # Variable auxiliar para recorrer las partes optimizadas
        for i in lista_s_i:
            if partes[i] not in parte_optimizada:
                partes[i] = parte_optimizada[indice]

            indice += 1


'''
    Funcion para determinar si un elemento esta en alguna de las partes
'''
def elemento_no_en_mochila(elemento : Elemento, mochila_objetos : list) -> bool:
    if elemento in mochila_objetos:
        return False # Si el elemento esta en la mochila, no lo podemos añadir otra vez
    
    return True
'''
    Funcion para determinar si todas las partes estan optimizadas, eso quiere decir si
    en el conjunto de partes optimizadas, estan todas las partes de partes_list
'''
def todas_partes_optimizadas(conjunto_optimizado : list, partes_list : list) -> bool:
    for parte in partes_list:
        if parte not in conjunto_optimizado:
            return False
        
    return True

'''
    Funcion para determinar si un elemento cabe en la mochila, se omitira el peso del elemento que se va a quitar
    y comprobamos si la suma con el elemento que querremos incluir, es menor o igual a la capacidad maxima de la mochila 
'''
def cabe_elemento_en_mochila(capacidad_maxima : int, elemento_a_quitar : Elemento, elemento_a_poner : Elemento, subproblema : list) -> bool:
    suma_peso = 0
    for i_parte in subproblema:
        for elemento in i_parte:
            if elemento is not elemento_a_quitar:
                suma_peso += elemento.peso # Omitimos en el peso el elemento que iriamos a quitar

    return suma_peso + elemento_a_poner.peso <= capacidad_maxima

# Funcion para crear los elementos
def crear_elementos() -> list:
    lista_elementos = []
    # Se crean los elementos arbitrarios
    elemento1 = Elemento("Radio", 2, 3) #3/2 = 1.5
    elemento2 = Elemento("Tostadora", 1, 1) #1/1 = 1
    elemento3 = Elemento("CD", 2, 4) #4/2 = 2
    elemento4 = Elemento("Television", 8, 10) #10/8 = 1.25
    elemento5 = Elemento("Altavoz", 4, 5) #5/4 = 1.25
    elemento6 = Elemento("Ordenador", 3, 6) #6/3 = 2
    elemento7 = Elemento("Anillo", 2, 5) #5/2 = 2.5

    # Se agregan los elementos a la lista
    lista_elementos.append(elemento1)
    lista_elementos.append(elemento2)
    lista_elementos.append(elemento3)
    lista_elementos.append(elemento4)
    lista_elementos.append(elemento5)
    lista_elementos.append(elemento6)
    lista_elementos.append(elemento7)
    return lista_elementos
# Funcion principal
def main():
    lista_elementos = crear_elementos()
    print("----------------[ELEMENTOS DISPONIBLES]----------------\n")
    for elemento in lista_elementos:
        print(elemento.__str__())

    # Creamos la mochila
    lista_elementos = crear_elementos()
    mochila = Mochila(17, [])
    solucion : Mochila = popmusic(mochila, lista_elementos)
    print("----------------[SOLUCION]----------------\n")
    for elemento in solucion.objetos:
        print(elemento.__str__())
    print(f'Suma total del valor de la mochila: {sum([elemento.valor for elemento in solucion.objetos])}')
        

if __name__ == "__main__":
    main()

