import heapq

class Mapa:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = self.crear_matriz()

    def crear_matriz(self):
        return [['0'] * self.num_columnas for _ in range(self.num_filas)]

    def dibujar_matriz(self):
        for fila in self.matriz:
            print(" ".join(fila))

    def agregar_obstaculos(self):
        while True:
            fila_usuario = int(input('Elija una fila para agregar un obstáculo (o -1 para salir): '))
            if fila_usuario == -1:
                break
            columna_usuario = int(input('Elija una columna para agregar un obstáculo: '))
            if 0 <= fila_usuario < self.num_filas and 0 <= columna_usuario < self.num_columnas:
                self.matriz[fila_usuario][columna_usuario] = '1'
            else:
                print('Coordenadas no son válidas')

    def establecer_entrada(self):
        while True:
            fila_entrada = int(input('Elija la fila para la entrada: '))
            columna_entrada = int(input('Elija la columna para la entrada: '))
            if 0 <= fila_entrada < self.num_filas and 0 <= columna_entrada < self.num_columnas:
                self.matriz[fila_entrada][columna_entrada] = 'E'
                return (fila_entrada, columna_entrada)
            else:
                print('Coordenadas no son válidas')

    def establecer_salida(self):
        while True:
            fila_salida = int(input('Elija la fila para la salida: '))
            columna_salida = int(input('Elija la columna para la salida: '))
            if 0 <= fila_salida < self.num_filas and 0 <= columna_salida < self.num_columnas:
                self.matriz[fila_salida][columna_salida] = 'S'
                return (fila_salida, columna_salida)
            else:
                print('Coordenadas no son válidas')

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa.matriz
        self.num_filas = mapa.num_filas
        self.num_columnas = mapa.num_columnas

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_estrella(self, inicio, fin):
        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        costo_g = {inicio: 0}
        costo_f = {inicio: self.heuristica(inicio, fin)}
        lista_abierta = []
        heapq.heappush(lista_abierta, (costo_f[inicio], inicio))
        lista_cerrada = {}

        while lista_abierta:
            _, actual = heapq.heappop(lista_abierta)
            if actual == fin:
                camino = []
                while actual in lista_cerrada:
                    camino.append(actual)
                    actual = lista_cerrada[actual]
                camino.append(inicio)
                camino.reverse()
                return camino

            for dx, dy in vecinos:
                vecino = (actual[0] + dx, actual[1] + dy)
                if 0 <= vecino[0] < self.num_filas and 0 <= vecino[1] < self.num_columnas:
                    if self.mapa[vecino[0]][vecino[1]] == '1':
                        continue
                    costo_tentativo = costo_g[actual] + 1
                    if vecino not in costo_g or costo_tentativo < costo_g[vecino]:
                        lista_cerrada[vecino] = actual
                        costo_g[vecino] = costo_tentativo
                        costo_f[vecino] = costo_tentativo + self.heuristica(vecino, fin)
                        heapq.heappush(lista_abierta, (costo_f[vecino], vecino))

        return None
    def dibujar_camino (self, camino, inicio, fin):
         for paso in camino:
            if paso != inicio and paso != fin:
                self.mapa[paso[0]][paso[1]] = '*'
        

def main():
    num_filas = 6
    num_columnas = 6
    mapa = Mapa(num_filas, num_columnas)

    print("Matriz inicial:")
    mapa.dibujar_matriz()
    mapa.agregar_obstaculos()

    entrada = mapa.establecer_entrada()
    salida = mapa.establecer_salida()

    print("\nMatriz con entrada y salida:")
    mapa.dibujar_matriz()

    calculadora = CalculadoraRutas(mapa)
    camino = calculadora.a_estrella(entrada, salida)

    if camino:
        calculadora.dibujar_camino(camino, entrada, salida)
    else:
        print("No se encontró un camino desde la entrada hasta la salida.")

    print("\nMatriz con el camino encontrado:")
    mapa.dibujar_matriz()

if __name__ == "__main__":
    main()
