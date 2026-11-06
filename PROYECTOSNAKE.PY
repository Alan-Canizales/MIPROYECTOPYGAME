
import pygame
import random
import math
import struct

# Inicializar Pygame
pygame.init()

# Configuracion de la ventana
ANCHO = 600
ALTO = 600
TAMANO = 20

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Snake")

reloj = pygame.time.Clock()

# Colores
NEGRO = (15, 15, 20)
VERDE = (50, 200, 80)
VERDE_OSCURO = (30, 140, 60)
ROJO = (230, 60, 60)
BLANCO = (255, 255, 255)
AMARILLO = (255, 220, 50)

fuente = pygame.font.SysFont("Arial", 28)
fuente_grande = pygame.font.SysFont("Arial", 48)


# Crear sonidos sin necesitar archivos externos
def crear_sonido(frecuencia, duracion):
    try:
        frecuencia_muestreo = 22050
        muestras = int(frecuencia_muestreo * duracion)
        datos = bytearray()

        for i in range(muestras):
            tiempo = i / frecuencia_muestreo
            volumen = 0.3 * (1 - i / muestras)
            valor = int(
                32767 * volumen *
                math.sin(2 * math.pi * frecuencia * tiempo)
            )
            datos.extend(struct.pack("<h", valor))

        return pygame.mixer.Sound(buffer=bytes(datos))

    except pygame.error:
        return None


# Inicializar audio
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
    sonido_comer = crear_sonido(800, 0.12)
    sonido_perder = crear_sonido(200, 0.35)
except pygame.error:
    sonido_comer = None
    sonido_perder = None


# Clase para cada parte de la serpiente
class Segmento(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pygame.Surface((TAMANO - 2, TAMANO - 2))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect(topleft=posicion)


# Clase para la comida
class Comida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TAMANO - 2, TAMANO - 2))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.aparecer()

    def aparecer(self):
        self.rect.x = random.randrange(0, ANCHO, TAMANO)
        self.rect.y = random.randrange(0, ALTO, TAMANO)


# Crear el juego
def iniciar_juego():

    grupo_serpiente = pygame.sprite.Group()

    # Posicion inicial de la serpiente
    serpiente = [
        Segmento((300, 300)),
        Segmento((280, 300)),
        Segmento((260, 300))
    ]

    for segmento in serpiente:
        grupo_serpiente.add(segmento)

    comida = Comida()
    puntos = 0

    direccion = (TAMANO, 0)
    siguiente_direccion = direccion

    ultimo_movimiento = pygame.time.get_ticks()
    velocidad = 120

    terminado = False

    return (
        serpiente, grupo_serpiente, comida, puntos,
        direccion, siguiente_direccion,
        ultimo_movimiento, velocidad, terminado
    )


# Mostrar texto
def mostrar_texto(texto, fuente_usada, color, x, y):
    imagen = fuente_usada.render(texto, True, color)
    pantalla.blit(imagen, (x, y))


# Iniciar partida
datos = iniciar_juego()

(
    serpiente, grupo_serpiente, comida, puntos,
    direccion, siguiente_direccion,
    ultimo_movimiento, velocidad, terminado
) = datos

ejecutando = True

# Bucle principal
while ejecutando:

    reloj.tick(60)

    # Detectar eventos del teclado
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            if terminado:
                if evento.key == pygame.K_r:
                    datos = iniciar_juego()
                    (
                        serpiente, grupo_serpiente, comida, puntos,
                        direccion, siguiente_direccion,
                        ultimo_movimiento, velocidad, terminado
                    ) = datos

            else:
                # Controlar la direccion sin permitir retroceder
                if evento.key == pygame.K_UP and direccion != (0, TAMANO):
                    siguiente_direccion = (0, -TAMANO)

                elif evento.key == pygame.K_DOWN and direccion != (0, -TAMANO):
                    siguiente_direccion = (0, TAMANO)

                elif evento.key == pygame.K_LEFT and direccion != (TAMANO, 0):
                    siguiente_direccion = (-TAMANO, 0)

                elif evento.key == pygame.K_RIGHT and direccion != (-TAMANO, 0):
                    siguiente_direccion = (TAMANO, 0)

    if not terminado:

        tiempo_actual = pygame.time.get_ticks()

        # Actualizar movimiento de la serpiente
        if tiempo_actual - ultimo_movimiento >= velocidad:

            ultimo_movimiento = tiempo_actual
            direccion = siguiente_direccion

            nueva_cabeza = serpiente[0].rect.copy()
            nueva_cabeza.x += direccion[0]
            nueva_cabeza.y += direccion[1]

            # Comprobar si comio la comida
            comio = nueva_cabeza.colliderect(comida.rect)

            # Comprobar colision con las paredes
            if (
                nueva_cabeza.left < 0 or
                nueva_cabeza.right > ANCHO or
                nueva_cabeza.top < 0 or
                nueva_cabeza.bottom > ALTO
            ):
                terminado = True

            # Comprobar colision con el cuerpo
            cuerpo_a_revisar = serpiente[1:]

            if not comio:
                cuerpo_a_revisar = cuerpo_a_revisar[:-1]

            for segmento in cuerpo_a_revisar:
                if nueva_cabeza.colliderect(segmento.rect):
                    terminado = True

            if not terminado:

                # Agregar nueva cabeza
                nueva_cabeza_sprite = Segmento(nueva_cabeza.topleft)
                serpiente.insert(0, nueva_cabeza_sprite)
                grupo_serpiente.add(nueva_cabeza_sprite)

                # Si no comio, quitar la ultima parte
                if not comio:
                    cola = serpiente.pop()
                    grupo_serpiente.remove(cola)

                else:
                    puntos += 10

                    if sonido_comer:
                        sonido_comer.play()

                    # Buscar una posicion libre para la comida
                    while True:
                        comida.aparecer()

                        ocupado = any(
                            comida.rect.colliderect(segmento.rect)
                            for segmento in serpiente
                        )

                        if not ocupado:
                            break

            if terminado and sonido_perder:
                sonido_perder.play()

    # Dibujar pantalla
    pantalla.fill(NEGRO)

    # Dibujar serpiente y comida
    grupo_serpiente.draw(pantalla)
    pantalla.blit(comida.image, comida.rect)

    # Mostrar puntuacion
    mostrar_texto(
        f"Puntos: {puntos}",
        fuente,
        BLANCO,
        10,
        10
    )

    # Mostrar pantalla de Game Over
    if terminado:

        mostrar_texto(
            "GAME OVER",
            fuente_grande,
            ROJO,
            165,
            240
        )

        mostrar_texto(
            f"Puntuacion final: {puntos}",
            fuente,
            BLANCO,
            180,
            310
        )

        mostrar_texto(
            "Presiona R para reiniciar",
            fuente,
            AMARILLO,
            150,
            370
        )

    pygame.display.flip()

# Cerrar Pygame
pygame.quit()
