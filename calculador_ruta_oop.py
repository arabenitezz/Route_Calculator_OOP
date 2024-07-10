import heapq  # Importa el módulo heapq, que proporciona una implementación de cola de prioridad basada en heap.

class Mapa:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas  # Inicializa el número de filas del mapa.
        self.num_columnas = num_columnas  # Inicializa el número de columnas del mapa.
        self.costos_obstaculos = {
            '!': 5,
            '@': 10,
            '/': float('inf')  # Usamos infinito para representar un obstáculo intransitable.
        }
        self.matriz = self.crear_matriz()  # Crea la matriz del mapa.

    def crear_matriz(self):
        # Crea una matriz de tamaño num_filas x num_columnas llena de '0'.
        return [['0'] * self.num_columnas for _ in range(self.num_filas)]

    def dibujar_matriz(self):
        # Dibuja (imprime) la matriz fila por fila.
        for fila in self.matriz:
            print(" ".join(fila))

    def establecer_entrada(self):
        # Permite al usuario establecer la entrada en la matriz.
        while True:
            fila_entrada = int(input('Elija la fila para la entrada: '))
            columna_entrada = int(input('Elija la columna para la entrada: '))
            if 0 <= fila_entrada < self.num_filas and 0 <= columna_entrada < self.num_columnas:
                self.matriz[fila_entrada][columna_entrada] = 'E'  # Establece la entrada en la posición dada.
                return (fila_entrada, columna_entrada)  # Retorna la posición de la entrada.
            else:
                print('Coordenadas no son válidas')  # Muestra un mensaje de error si las coordenadas son inválidas.

    def establecer_salida(self):
        # Permite al usuario establecer la salida en la matriz.
        while True:
            fila_salida = int(input('Elija la fila para la salida: '))
            columna_salida = int(input('Elija la columna para la salida: '))
            if 0 <= fila_salida < self.num_filas and 0 <= columna_salida < self.num_columnas:
                self.matriz[fila_salida][columna_salida] = 'S'  # Establece la salida en la posición dada.
                return (fila_salida, columna_salida)  # Retorna la posición de la salida.
            else:
                print('Coordenadas no son válidas')  # Muestra un mensaje de error si las coordenadas son inválidas.

    def agregar_obstaculos(self):
        obstaculos = {
            'bache': '!',
            'agua': '@',
            'calle_cerrada': '/'
        }
        # Permite al usuario agregar obstáculos en la matriz.
        while True:
            fila_usuario = int(input('Elija una fila para agregar un obstáculo (o -1 para salir): '))
            if fila_usuario == -1:
                break  # Sale del bucle si el usuario ingresa -1.
            columna_usuario = int(input('Elija una columna para agregar un obstáculo: '))
            if 0 <= fila_usuario < self.num_filas and 0 <= columna_usuario < self.num_columnas:
                print("Tipos de obstáculos:")
                for obstaculo, valor in obstaculos.items():
                    print(f"{obstaculo}: {valor}")
                tipo_obstaculo = input('Elija el tipo de obstáculo: ')
                if tipo_obstaculo in obstaculos:
                    self.matriz[fila_usuario][columna_usuario] = obstaculos[tipo_obstaculo]
                else:
                    print('Tipo de obstáculo no válido')
            else:
                print('Coordenadas no son válidas')  # Muestra un mensaje de error si las coordenadas son inválidas.

    def quitar_obstaculos(self):
        # Permite al usuario quitar obstáculos en la matriz.
        while True:
            quitar = input('¿Desea eliminar algún obstáculo? (si o no): ')
            if quitar.lower() == 'no':
                break  # Sale del bucle si el usuario no desea eliminar más obstáculos.
            elif quitar.lower() == 'si':
                fila_usuario = int(input('Elija una fila para quitar un obstáculo (o -1 para salir): '))
                if fila_usuario == -1:
                    break  # Sale del bucle si el usuario ingresa -1.
                columna_usuario = int(input('Elija una columna para quitar un obstáculo: '))
                if 0 <= fila_usuario < self.num_filas and 0 <= columna_usuario < self.num_columnas:
                    if self.matriz[fila_usuario][columna_usuario] in self.costos_obstaculos:
                        self.matriz[fila_usuario][columna_usuario] = '0'  # Quita el obstáculo en la posición dada.
                        print('Obstáculo quitado.')
                    else:
                        print('No hay obstáculo en esa posición')  # Mensaje si no hay obstáculo en la posición.
                else:
                    print('Coordenadas no son válidas')  # Muestra un mensaje de error si las coordenadas son inválidas.
            else:
                print('Respuesta no válida. Por favor, responda "si" o "no".')

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa.matriz  # Inicializa la matriz del mapa.
        self.num_filas = mapa.num_filas  # Inicializa el número de filas del mapa.
        self.num_columnas = mapa.num_columnas  # Inicializa el número de columnas del mapa.
        self.costos_obstaculos = mapa.costos_obstaculos  # Obtiene los costos de obstáculos del mapa.

    def heuristica(self, a, b):
        # Calcula la heurística (distancia Manhattan) entre los puntos a y b.
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_estrella(self, inicio, fin):
        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Lista de desplazamientos para los vecinos (derecha, izquierda, abajo, arriba).
        costo_g = {inicio: 0}  # Diccionario que almacena el costo desde el inicio a cada nodo.
        costo_f = {inicio: self.heuristica(inicio, fin)}  # Diccionario que almacena el costo estimado total (g + h) desde el inicio a cada nodo.
        lista_abierta = []  # Cola de prioridad (heap) para nodos a explorar.
        heapq.heappush(lista_abierta, (costo_f[inicio], inicio))  # Agrega el nodo inicial a la cola de prioridad.
        lista_cerrada = {}  # Diccionario que almacena nodos ya explorados.

        while lista_abierta:
            _, actual = heapq.heappop(lista_abierta)  # Extrae el nodo con el menor costo f de la cola.
            if actual == fin:
                # Si el nodo actual es el nodo final, reconstruye el camino desde el inicio hasta el final.
                camino = []
                while actual in lista_cerrada:
                    camino.append(actual)
                    actual = lista_cerrada[actual]
                camino.append(inicio)
                camino.reverse()
                return camino  # Retorna el camino encontrado.

            for dx, dy in vecinos:
                vecino = (actual[0] + dx, actual[1] + dy)  # Calcula la posición del vecino.
                if 0 <= vecino[0] < self.num_filas and 0 <= vecino[1] < self.num_columnas:
                    if self.mapa[vecino[0]][vecino[1]] in self.costos_obstaculos:
                        costo_extra = self.costos_obstaculos[self.mapa[vecino[0]][vecino[1]]]
                    else:
                        costo_extra = 1
                    costo_tentativo = costo_g[actual] + costo_extra
                    if vecino not in costo_g or costo_tentativo < costo_g[vecino]:
                        # Si el vecino no ha sido visitado o se encuentra un camino más corto, actualiza los costos.
                        lista_cerrada[vecino] = actual
                        costo_g[vecino] = costo_tentativo
                        costo_f[vecino] = costo_tentativo + self.heuristica(vecino, fin)
                        heapq.heappush(lista_abierta, (costo_f[vecino], vecino))  # Agrega el vecino a la cola de prioridad.

        return None  # Retorna None si no se encuentra un camino.
    
    def dibujar_camino(self, camino, inicio, fin):
        # Marca el camino encontrado en la matriz.
        for paso in camino:
            if paso != inicio and paso != fin:
                self.mapa[paso[0]][paso[1]] = '*'

def main():
    num_filas = 6
    num_columnas = 6
    mapa = Mapa(num_filas, num_columnas)  # Crea una instancia de Mapa con 6 filas y 6 columnas.

    print("Matriz inicial:")
    mapa.dibujar_matriz()  # Dibuja la matriz inicial.
    entrada = mapa.establecer_entrada()  # Establece la entrada y obtiene su posición.
    salida = mapa.establecer_salida()  # Establece la salida y obtiene su posición.
    mapa.agregar_obstaculos()  # Permite al usuario agregar obstáculos.
    mapa.quitar_obstaculos()

    print("\nMatriz con entrada y salida:")
    mapa.dibujar_matriz()  # Dibuja la matriz con la entrada y la salida.

    calculadora = CalculadoraRutas(mapa)  # Crea una instancia de CalculadoraRutas con el mapa.
    camino = calculadora.a_estrella(entrada, salida)  # Calcula el camino usando A*.

    if camino:
        calculadora.dibujar_camino(camino, entrada, salida)  # Dibuja el camino en la matriz si se encuentra.
    else:
        print("No se encontró un camino desde la entrada hasta la salida.")  # Mensaje si no se encuentra un camino.

    print("\nMatriz con el camino encontrado:")
    mapa.dibujar_matriz()  # Dibuja la matriz final con el camino.

if __name__ == "__main__":
    main()  # Llama a la función main si el script se ejecuta directamente.
