import random
import heapq

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = self.generar_matriz_aleatoria()
        self.start = None
        self.end = None

    def generar_matriz_aleatoria(self):
        return [[random.choices(['C', 'E', 'A', 'B'], weights=[0.6, 0.1, 0.2, 0.1])[0] for _ in range(self.columnas)] for _ in range(self.filas)]

    def agregar_obstaculo(self, x, y, tipo_obstaculo):
        if tipo_obstaculo in ('E', 'A', 'B'):
            self.mapa[x][y] = tipo_obstaculo
        else:
            raise ValueError("Tipo de obstáculo no válido.")

    def quitar_obstaculo(self, x, y):
        self.mapa[x][y] = 'C'

    def es_accesible(self, x, y):
        return self.mapa[x][y] not in ('E')

    def imprimir_mapa(self):
        for fila in self.mapa:
            print(' '.join(fila))

    def imprimir_mapa_con_camino(self, path):
        mapa_con_camino = [fila[:] for fila in self.mapa]  # Hacer una copia del mapa
        for x, y in path:
            mapa_con_camino[x][y] = '*'
        
        mapa_con_camino[self.start[0]][self.start[1]] = 'S'  # Marcar el inicio
        mapa_con_camino[self.end[0]][self.end[1]] = 'F'  # Marcar el fin

        for fila in mapa_con_camino:
            print(' '.join(fila))


class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa
        self.costos = {
            'C': 1,  # Carreteras
            'E': float('infinity'),  # Edificios
            'A': 5,  # Agua
            'B': 7,  # Áreas bloqueadas temporalmente
        }

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start, end):
        filas, columnas = self.mapa.filas, self.mapa.columnas
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]
            
            closed_set.add(current)
            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimientos posibles (arriba, abajo, izquierda, derecha)
                neighbor = (x + dx, y + dy)
                if 0 <= neighbor[0] < filas and 0 <= neighbor[1] < columnas:
                    if neighbor in closed_set:
                        continue

                    terreno = self.mapa.mapa[neighbor[0]][neighbor[1]]
                    if terreno != 'E':  # Ignorar edificios
                        tentative_g_score = g_score[current] + self.costos[terreno]
                        if tentative_g_score < g_score.get(neighbor, float('infinity')):
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, end)
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []

def preguntar_tamano_matriz():
    while True:
        try:
            filas = int(input("Introduce el número de filas: "))
            columnas = int(input("Introduce el número de columnas: "))
            if filas > 0 and columnas > 0:
                return filas, columnas
            else:
                print("El número de filas y columnas debe ser mayor que 0.")
        except ValueError:
            print("Por favor, introduce números válidos.")

def preguntar_coordenadas(filas, columnas, tipo):
    while True:
        try:
            x = int(input(f"Introduce la coordenada x de {tipo} (0-{filas-1}): "))
            y = int(input(f"Introduce la coordenada y de {tipo} (0-{columnas-1}): "))
            if 0 <= x < filas and 0 <= y < columnas:
                return x, y
            else:
                print("Las coordenadas deben estar dentro del rango del mapa.")
        except ValueError:
            print("Por favor, introduce números válidos.")

def main():
    # Preguntar tamaño del mapa
    filas, columnas = preguntar_tamano_matriz()
    mapa = Mapa(filas, columnas)

    print("Mapa generado:")
    mapa.imprimir_mapa()

    # Preguntar las coordenadas de inicio y fin
    mapa.start = preguntar_coordenadas(filas, columnas, "inicio")
    mapa.end = preguntar_coordenadas(filas, columnas, "fin")

    # Agregar obstáculos al mapa
    while True:
        try:
            num_obstaculos = int(input("Introduce el número de obstáculos que deseas agregar: "))
            for i in range(num_obstaculos):
                print(f"Agregando obstáculo {i+1} de {num_obstaculos}")
                tipo_obstaculo = input("Introduce el tipo de obstáculo ('E' para edificio, 'A' para agua, 'B' para bloqueo): ").upper()
                x, y = preguntar_coordenadas(filas, columnas, f"obstáculo {i+1}")
                mapa.agregar_obstaculo(x, y, tipo_obstaculo)
            break
        except ValueError:
            print("Por favor, introduce un número válido.")

    print("Mapa con obstáculos:")
    mapa.imprimir_mapa()

    # Verificar que el inicio y el fin sean transitables
    if not mapa.es_accesible(mapa.start[0], mapa.start[1]) or not mapa.es_accesible(mapa.end[0], mapa.end[1]):
        print("El punto de inicio o fin está bloqueado.")
    else:
        # Crear calculadora de rutas y ejecutar el algoritmo A*
        calculadora = CalculadoraRutas(mapa)
        path = calculadora.a_star(mapa.start, mapa.end)
        if path:
            print("Ruta más corta:", path)
            print("Mapa con el camino recorrido:")
            mapa.imprimir_mapa_con_camino(path)
        else:
            print("No se encontró una ruta desde el inicio hasta el fin.")

if __name__ == "__main__":
    main()
