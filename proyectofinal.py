
import pygame
import random
import math
from array import array

# -----------------------------------------
# 1. INICIALIZACION DE PYGAME
# -----------------------------------------
pygame.init()

ANCHO = 800
ALTO = 600
TAM_CELDA = 20

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake - Juego de la serpiente")

reloj = pygame.time.Clock()

# Colores
NEGRO = (15, 20, 25)
VERDE = (50, 220, 100)
VERDE_OSCURO = (25, 140, 70)
ROJO = (240, 65, 65)
BLANCO = (255, 255, 255)
GRIS = (40, 48, 55)

fuente = pygame.font.SysFont(None, 36)
fuente_grande = pygame.font.SysFont(None, 65)

# -----------------------------------------
# 2. CONFIGURACION DEL SONIDO
# -----------------------------------------
sonido_comer = None

try:
    pygame.mixer.init()

    # Crear un sonido corto sin archivo externo
    muestras = array("h")
    frecuencia = 44100

    for i in range(int(frecuencia * 0.12)):
        volumen = int(
            10000 * (1 - i / (frecuencia * 0.12))
            * math.sin(2 * math.pi * 700 * i / frecuencia)
        )
        muestras.append(volumen)

    sonido_comer = pygame.mixer.Sound(buffer=muestras.tobytes())

except pygame.error:
    print("No se pudo inicializar el sonido.")

# -----------------------------------------
# 3. CLASE PARA LOS SEGMENTOS DE LA SERPIENTE
# -----------------------------------------
class Segmento(pygame.sprite.Sprite):

    def __init__(self, x, y, cabeza=False):
        super().__init__()

        self.image = pygame.Surface(
            (TAM_CELDA - 2, TAM_CELDA - 2)
        )

        if cabeza:
            self.image.fill(VERDE)
        else:
            self.image.fill(VERDE_OSCURO)

        self.rect = self.image.get_rect(
            topleft=(x, y)
        )


# -----------------------------------------
# 4. CLASE PARA EL ALIMENTO
# -----------------------------------------
class Comida(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface(
            (TAM_CELDA - 2, TAM_CELDA - 2)
        )

        self.image.fill(ROJO)

        self.rect = self.image.get_rect()
        self.reubicar()

    def reubicar(self):
        columnas = ANCHO // TAM_CELDA
        filas = ALTO // TAM_CELDA

        self.rect.x = random.randrange(columnas) * TAM_CELDA
        self.rect.y = random.randrange(filas) * TAM_CELDA


# -----------------------------------------
# 5. FUNCION PARA INICIAR O REINICIAR EL JUEGO
# -----------------------------------------
def iniciar_juego():

    serpiente = [
        Segmento(400, 300, True),
        Segmento(380, 300),
        Segmento(360, 300)
    ]

    grupo_serpiente = pygame.sprite.Group(serpiente)

    comida = Comida()

    # Evitar que la comida aparezca sobre la serpiente
    while pygame.sprite.spritecollideany(
        comida, grupo_serpiente
    ):
        comida.reubicar()

    direccion = (TAM_CELDA, 0)
    puntuacion = 0

    return serpiente, grupo_serpiente, comida, direccion, puntuacion


serpiente, grupo_serpiente, comida, direccion, puntuacion = iniciar_juego()

jugando = True
game_over = False

# Tiempo entre movimientos de la serpiente
TIEMPO_MOVIMIENTO = 120
acumulador = 0

# -----------------------------------------
# 6. CICLO PRINCIPAL DEL VIDEOJUEGO
# -----------------------------------------
while jugando:

    # Control de FPS y tiempo transcurrido
    tiempo = reloj.tick(60)
    acumulador += tiempo

    # -------------------------------------
    # 7. DETECCION DE EVENTOS E INPUT
    # -------------------------------------
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.KEYDOWN:

            if game_over and evento.key == pygame.K_r:
                (
                    serpiente,
                    grupo_serpiente,
                    comida,
                    direccion,
                    puntuacion
                ) = iniciar_juego()

                game_over = False
                acumulador = 0

            elif not game_over:

                # Evitar que la serpiente retroceda sobre sí misma
                if evento.key in (pygame.K_UP, pygame.K_w):
                    nueva_direccion = (0, -TAM_CELDA)

                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    nueva_direccion = (0, TAM_CELDA)

                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    nueva_direccion = (-TAM_CELDA, 0)

                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    nueva_direccion = (TAM_CELDA, 0)

                else:
                    nueva_direccion = direccion

                if nueva_direccion != (
                    -direccion[0], -direccion[1]
                ):
                    direccion = nueva_direccion

    # -------------------------------------
    # 8. MOVIMIENTO Y COLISIONES
    # -------------------------------------
    if not game_over and acumulador >= TIEMPO_MOVIMIENTO:

        acumulador = 0

        cabeza_actual = serpiente[0]

        nueva_x = cabeza_actual.rect.x + direccion[0]
        nueva_y = cabeza_actual.rect.y + direccion[1]

        nueva_cabeza = Segmento(nueva_x, nueva_y, True)

        # Comprobar si la cabeza alcanza la comida
        comio = nueva_cabeza.rect.colliderect(comida.rect)

        # Si no come, la cola se mueve y se elimina
        # antes de comprobar la colision con el cuerpo.
        if not comio:
            cola = serpiente.pop()
            grupo_serpiente.remove(cola)

        # Detectar choque con los limites de la ventana
        if (
            nueva_x < 0 or
            nueva_y < 0 or
            nueva_x >= ANCHO or
            nueva_y >= ALTO
        ):
            game_over = True

        # Detectar choque con el propio cuerpo
        elif pygame.sprite.spritecollideany(
            nueva_cabeza, grupo_serpiente
        ):
            game_over = True

        else:
            # Actualizar la serpiente
            cabeza_actual.image.fill(VERDE_OSCURO)

            serpiente.insert(0, nueva_cabeza)
            grupo_serpiente.add(nueva_cabeza)

            # Si comio, aumentar puntos y generar alimento
            if comio:

                puntuacion += 10

                if sonido_comer:
                    sonido_comer.play()

                comida.reubicar()

                # Evitar que el alimento aparezca sobre el cuerpo
                while pygame.sprite.spritecollideany(
                    comida, grupo_serpiente
                ):
                    comida.reubicar()

    # -------------------------------------
    # 9. DIBUJAR ELEMENTOS EN PANTALLA
    # -------------------------------------
    pantalla.fill(NEGRO)

    # Dibujar una cuadricula de fondo
    for x in range(0, ANCHO, TAM_CELDA):
        pygame.draw.line(
            pantalla, GRIS, (x, 0), (x, ALTO)
        )

    for y in range(0, ALTO, TAM_CELDA):
        pygame.draw.line(
            pantalla, GRIS, (0, y), (ANCHO, y)
        )

    # Dibujar comida y serpiente
    comida_group = pygame.sprite.Group(comida)

    comida_group.draw(pantalla)
    grupo_serpiente.draw(pantalla)

    # Mostrar puntuacion
    texto_puntos = fuente.render(
        f"Puntos: {puntuacion}",
        True,
        BLANCO
    )

    pantalla.blit(texto_puntos, (15, 15))

    # -------------------------------------
    # 10. PANTALLA DE FIN DEL JUEGO
    # -------------------------------------
    if game_over:

        texto_fin = fuente_grande.render(
            "GAME OVER",
            True,
            ROJO
        )

        texto_final = fuente.render(
            f"Puntuacion final: {puntuacion}",
            True,
            BLANCO
        )

        texto_reinicio = fuente.render(
            "Presiona R para volver a jugar",
            True,
            BLANCO
        )

        pantalla.blit(
            texto_fin,
            texto_fin.get_rect(center=(ANCHO // 2, 240))
        )

        pantalla.blit(
            texto_final,
            texto_final.get_rect(center=(ANCHO // 2, 310))
        )

        pantalla.blit(
            texto_reinicio,
            texto_reinicio.get_rect(center=(ANCHO // 2, 370))
        )

    # Actualizar la pantalla
    pygame.display.flip()

# -----------------------------------------
# 11. CERRAR PYGAME
# -----------------------------------------
pygame.quit()
