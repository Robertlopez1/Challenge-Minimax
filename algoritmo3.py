import random
import time
import pygame

# Dimensiones de la matriz
f = 5
c = 5

# Tamaño de la ventana y de los cuadrados de la matriz
ancho_ventana = 500
alto_ventana = 500
ancho_celda = ancho_ventana // c
alto_celda = alto_ventana // f

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Laberinto: Gato y Ratón")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Generar posiciones iniciales no solapadas
def generar_posiciones_iniciales():
    gato = (random.randint(0, f-1), random.randint(0, c-1))
    raton = (random.randint(0, f-1), random.randint(0, c-1))
    salida = (random.randint(0, f-1), random.randint(0, c-1))
    while len({gato, raton, salida}) < 3:
        gato = (random.randint(0, f-1), random.randint(0, c-1))
        raton = (random.randint(0, f-1), random.randint(0, c-1))
        salida = (random.randint(0, f-1), random.randint(0, c-1))
    return gato, raton, salida

gato, raton, salida = generar_posiciones_iniciales()

# Función para definir movimientos válidos
def movimientos_validos(pos):
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(pos[0] + mov[0], pos[1] + mov[1]) for mov in movimientos if 0 <= pos[0] + mov[0] < f and 0 <= pos[1] + mov[1] < c]

# Función de evaluación: distancia de Manhattan entre el gato y el ratón
def evaluar_estado(gato, raton):
    return abs(gato[0] - raton[0]) + abs(gato[1] - raton[1])

# Algoritmo Minimax con memoización
def minimax(gato, raton, profundidad, maximizar_gato, memo=None, posicion_anterior=None):
    if memo is None:
        memo = {}
    
    clave_estado = (gato, raton, profundidad, maximizar_gato)
    if clave_estado in memo:
        return memo[clave_estado]
    
    if profundidad == 0 or gato == raton:
        evaluacion = evaluar_estado(gato, raton)
        memo[clave_estado] = (evaluacion, gato if maximizar_gato else raton)
        return evaluacion, gato if maximizar_gato else raton

    if maximizar_gato:
        mejor_valor = float('-inf')
        mejor_movimiento = gato
        for mov in movimientos_validos(gato):
            if mov != posicion_anterior:
                valor, _ = minimax(mov, raton, profundidad - 1, False, memo, gato)
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = mov
        memo[clave_estado] = (mejor_valor, mejor_movimiento)
        return mejor_valor, mejor_movimiento
    else:
        mejor_valor = float('inf')
        mejor_movimiento = raton
        for mov in movimientos_validos(raton):
            if mov != posicion_anterior:
                valor, _ = minimax(gato, mov, profundidad - 1, True, memo, raton)
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = mov
        memo[clave_estado] = (mejor_valor, mejor_movimiento)
        return mejor_valor, mejor_movimiento

# Función para dibujar el laberinto
def dibujar_laberinto():
    ventana.fill(BLANCO)
    for i in range(f):
        for j in range(c):
            if (i, j) == gato:
                color = ROJO
            elif (i, j) == raton:
                color = AZUL
            elif (i, j) == salida:
                color = VERDE
            else:
                color = BLANCO
            pygame.draw.rect(ventana, color, (j * ancho_celda, i * alto_celda, ancho_celda, alto_celda))
            pygame.draw.rect(ventana, NEGRO, (j * ancho_celda, i * alto_celda, ancho_celda, alto_celda), 1)
    pygame.display.update()

# Ciclo del laberinto
ejecutando = True
raton_anterior = raton
gato_anterior = gato

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Dibujar el laberinto
    dibujar_laberinto()

    # Revisar condiciones de victoria o derrota
    if raton == gato:
        print("El gato atrapó al ratón. ¡El gato gana!")
        ejecutando = False
        continue
    elif raton == salida:
        print("El ratón encontró la salida. ¡El ratón gana!")
        ejecutando = False
        continue

    # Mover ratón y gato usando Minimax con memoización
    _, nuevo_raton = minimax(gato, raton, 3, False, posicion_anterior=raton_anterior)
    _, nuevo_gato = minimax(gato, raton, 3, True, posicion_anterior=gato_anterior)

    # Actualizar posiciones
    raton_anterior, raton = raton, nuevo_raton
    gato_anterior, gato = gato, nuevo_gato

    # Pausa para observar los movimientos (ajustable)
    time.sleep(0.5)

pygame.quit()


