#Desarrollo de Microproyecto

import pygame
import random

# Inicializar pygame
pygame.init()

# Configurar la ventana
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa las estrellas")

# Colores
AZUL_OSCURO = (15, 25, 55)
BLANCO = (255, 255, 255)
AMARILLO = (255, 220, 40)
AZUL = (60, 160, 255)

# Jugador
jugador = pygame.Rect(350, 520, 100, 25)
velocidad = 7

# Estrella
estrella = pygame.Rect(
    random.randint(0, ANCHO - 20), 0, 20, 20
)
velocidad_estrella = 4

# Puntuación
puntos = 0
fuente = pygame.font.SysFont(None, 36)
reloj = pygame.time.Clock()

# Bucle principal
ejecutando = True

while ejecutando:
    # Detectar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Detectar teclas presionadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= velocidad

    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += velocidad

    # Mover la estrella hacia abajo
    estrella.y += velocidad_estrella

    # Detectar si la estrella sale de la pantalla
    if estrella.top > ALTO:
        estrella.x = random.randint(0, ANCHO - 20)
        estrella.y = 0

    # Detectar colisión con el jugador
    if jugador.colliderect(estrella):
        puntos += 1
        estrella.x = random.randint(0, ANCHO - 20)
        estrella.y = 0

    # Dibujar elementos
    pantalla.fill(AZUL_OSCURO)

    pygame.draw.rect(pantalla, AZUL, jugador)
    pygame.draw.ellipse(pantalla, AMARILLO, estrella)

    texto = fuente.render(
        f"Puntos: {puntos}", True, BLANCO
    )
    pantalla.blit(texto, (20, 20))

    # Actualizar la pantalla
    pygame.display.flip()
    reloj.tick(60)

# Cerrar pygame
pygame.quit()
