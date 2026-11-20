
import pygame
import os
import random
import math
import struct

# --------------------------------------------------
# 1. INICIALIZAR PYGAME Y AUDIO
# --------------------------------------------------
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

# --------------------------------------------------
# 2. CONFIGURACION DE LA VENTANA
# --------------------------------------------------
ANCHO = 600
ALTO = 600
TAMANO = 20

COLUMNAS = ANCHO // TAMANO
FILAS = ALTO // TAMANO

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake - Proyecto Multimedia")

reloj = pygame.time.Clock()

# --------------------------------------------------
# 3. COLORES Y FUENTES
# --------------------------------------------------
BLANCO = (255, 255, 255)
VERDE = (0, 200, 0)
ROJO = (220, 30, 30)
NEGRO = (0, 0, 0)
GRIS = (150, 150, 150)

fuente = pygame.font.SysFont("Arial", 25)
fuente_grande = pygame.font.SysFont("Arial", 45)

# --------------------------------------------------
# 4. RUTA DE LA CARPETA MEDIA
# --------------------------------------------------
carpeta_media = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Media"
)

# --------------------------------------------------
# 5. CARGAR IMAGENES
# --------------------------------------------------
archivos_imagenes = [
    "images.jfif",
    "images (1).jfif",
    "images (2).jfif"
]

imagenes = []

for archivo in archivos_imagenes:
    ruta = os.path.join(carpeta_media, archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(
            imagen,
            (ANCHO, ALTO)
        )
        imagenes.append(imagen)

    except pygame.error as error:
        print(f"Error al cargar {archivo}: {error}")
        pygame.quit()
        raise SystemExit

    except FileNotFoundError:
        print(f"No se encontro la imagen: {ruta}")
        pygame.quit()
        raise SystemExit

# --------------------------------------------------
# 6. CARGAR MUSICA DE FONDO
# --------------------------------------------------
ruta_musica = os.path.join(
    carpeta_media,
    "sonido circus videojuego.mp3"
)

try:
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

except pygame.error as error:
    print("Error al cargar la musica:", error)
    pygame.quit()
    raise SystemExit

# --------------------------------------------------
# 7. CREAR EFECTOS DE SONIDO
# --------------------------------------------------
def crear_sonido(frecuencia, duracion):

    frecuencia_muestreo = 22050
    muestras = int(frecuencia_muestreo * duracion)

    datos = bytearray()

    for i in range(muestras):

        tiempo = i / frecuencia_muestreo

        valor = int(
            10000 * math.sin(
                2 * math.pi * frecuencia * tiempo
            )
        )

        datos.extend(struct.pack("<h", valor))

    return pygame.mixer.Sound(buffer=bytes(datos))


sonido_comer = crear_sonido(800, 0.12)
sonido_perder = crear_sonido(200, 0.35)

# --------------------------------------------------
# 8. VARIABLES DE LAS IMAGENES
# --------------------------------------------------
indice_imagen = 0
tiempo_cambio = 3000
ultimo_cambio = pygame.time.get_ticks()

# Capa oscura para mejorar la visibilidad
capa_oscura = pygame.Surface((ANCHO, ALTO))
capa_oscura.set_alpha(110)
capa_oscura.fill(NEGRO)

# --------------------------------------------------
# 9. FUNCION PARA DIBUJAR LA CUADRICULA
# --------------------------------------------------
def dibujar_cuadricula():

    # Lineas verticales
    for columna in range(COLUMNAS + 1):

        x = columna * TAMANO

        pygame.draw.line(
            pantalla,
            GRIS,
            (x, 0),
            (x, ALTO),
            1
        )

    # Lineas horizontales
    for fila in range(FILAS + 1):

        y = fila * TAMANO

        pygame.draw.line(
            pantalla,
            GRIS,
            (0, y),
            (ANCHO, y),
            1
        )

# --------------------------------------------------
# 10. GENERAR COMIDA
# --------------------------------------------------
def generar_comida(serpiente):

    while True:

        x = random.randrange(0, ANCHO, TAMANO)
        y = random.randrange(0, ALTO, TAMANO)

        if (x, y) not in serpiente:
            return (x, y)

# --------------------------------------------------
# 11. INICIAR O REINICIAR EL JUEGO
# --------------------------------------------------
def iniciar_juego():

    serpiente = [
        (300, 300),
        (280, 300),
        (260, 300)
    ]

    direccion = (TAMANO, 0)

    comida = generar_comida(serpiente)

    puntos = 0
    intervalo_movimiento = 120

    game_over = False

    return (
        serpiente,
        direccion,
        comida,
        puntos,
        intervalo_movimiento,
        game_over
    )


(
    serpiente,
    direccion,
    comida,
    puntos,
    intervalo_movimiento,
    game_over
) = iniciar_juego()

ultimo_movimiento = pygame.time.get_ticks()

# --------------------------------------------------
# 12. BUCLE PRINCIPAL
# --------------------------------------------------
ejecutando = True

while ejecutando:

    tiempo_actual = pygame.time.get_ticks()

    # ----------------------------------------------
    # CAMBIAR IMAGEN CADA 3 SEGUNDOS
    # ----------------------------------------------
    if tiempo_actual - ultimo_cambio >= tiempo_cambio:

        indice_imagen = (
            indice_imagen + 1
        ) % len(imagenes)

        ultimo_cambio = tiempo_actual

    # ----------------------------------------------
    # DETECTAR EVENTOS DEL TECLADO
    # ----------------------------------------------
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

            if game_over and evento.key == pygame.K_r:

                (
                    serpiente,
                    direccion,
                    comida,
                    puntos,
                    intervalo_movimiento,
                    game_over
                ) = iniciar_juego()

                ultimo_movimiento = pygame.time.get_ticks()

                # Volver a reproducir la musica
                pygame.mixer.music.play(-1)

            if not game_over:

                if evento.key == pygame.K_UP:

                    if direccion != (0, TAMANO):
                        direccion = (0, -TAMANO)

                elif evento.key == pygame.K_DOWN:

                    if direccion != (0, -TAMANO):
                        direccion = (0, TAMANO)

                elif evento.key == pygame.K_LEFT:

                    if direccion != (TAMANO, 0):
                        direccion = (-TAMANO, 0)

                elif evento.key == pygame.K_RIGHT:

                    if direccion != (-TAMANO, 0):
                        direccion = (TAMANO, 0)

    # ----------------------------------------------
    # MOVIMIENTO DE LA SERPIENTE
    # ----------------------------------------------
    if not game_over:

        if tiempo_actual - ultimo_movimiento >= intervalo_movimiento:

            ultimo_movimiento = tiempo_actual

            cabeza_x, cabeza_y = serpiente[0]

            nueva_cabeza = (
                cabeza_x + direccion[0],
                cabeza_y + direccion[1]
            )

            # Detectar colision con las paredes
            if (
                nueva_cabeza[0] < 0
                or nueva_cabeza[0] >= ANCHO
                or nueva_cabeza[1] < 0
                or nueva_cabeza[1] >= ALTO
            ):

                game_over = True

            # Detectar colision con el cuerpo
            elif nueva_cabeza in serpiente[:-1]:

                game_over = True

            else:

                serpiente.insert(0, nueva_cabeza)

                # Comprobar si comio la comida
                if nueva_cabeza == comida:

                    puntos += 10

                    sonido_comer.play()

                    comida = generar_comida(serpiente)

                else:

                    serpiente.pop()

            # Reproducir sonido al perder
            if game_over:

                pygame.mixer.music.stop()
                sonido_perder.play()

    # ----------------------------------------------
    # DIBUJAR FONDO
    # ----------------------------------------------
    pantalla.blit(
        imagenes[indice_imagen],
        (0, 0)
    )

    pantalla.blit(
        capa_oscura,
        (0, 0)
    )

    # ----------------------------------------------
    # DIBUJAR CUADRICULA
    # ----------------------------------------------
    dibujar_cuadricula()

    # ----------------------------------------------
    # DIBUJAR SERPIENTE
    # ----------------------------------------------
    for x, y in serpiente:

        pygame.draw.rect(
            pantalla,
            VERDE,
            (x, y, TAMANO - 2, TAMANO - 2)
        )

    # ----------------------------------------------
    # DIBUJAR COMIDA
    # ----------------------------------------------
    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            comida[0],
            comida[1],
            TAMANO - 2,
            TAMANO - 2
        )
    )

    # ----------------------------------------------
    # MOSTRAR PUNTUACION
    # ----------------------------------------------
    texto_puntos = fuente.render(
        f"Puntos: {puntos}",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_puntos,
        (10, 10)
    )

    # ----------------------------------------------
    # PANTALLA GAME OVER
    # ----------------------------------------------
    if game_over:

        texto_final = fuente_grande.render(
            "GAME OVER",
            True,
            ROJO
        )

        texto_reinicio = fuente.render(
            "Presiona R para reiniciar",
            True,
            BLANCO
        )

        texto_salir = fuente.render(
            "Presiona ESC para salir",
            True,
            BLANCO
        )

        pantalla.blit(
            texto_final,
            (
                ANCHO // 2 - texto_final.get_width() // 2,
                220
            )
        )

        pantalla.blit(
            texto_reinicio,
            (
                ANCHO // 2 - texto_reinicio.get_width() // 2,
                300
            )
        )

        pantalla.blit(
            texto_salir,
            (
                ANCHO // 2 - texto_salir.get_width() // 2,
                340
            )
        )

    # ----------------------------------------------
    # ACTUALIZAR PANTALLA
    # ----------------------------------------------
    pygame.display.flip()

    reloj.tick(60)

# --------------------------------------------------
# 13. CERRAR PYGAME
# --------------------------------------------------
pygame.mixer.music.stop()
pygame.quit()
