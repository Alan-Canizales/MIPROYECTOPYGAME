
import pygame
import os

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la ventana
ANCHO = 1280
ALTO = 720

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Presentacion Multimedia - Pygame")

# Rutas de los archivos
carpeta_media = os.path.join(os.path.dirname(__file__), "Media")

# Cargar imágenes
# Cargar imágenes
imagenes = [
    pygame.image.load(os.path.join(carpeta_media, "images.jfif")),
    pygame.image.load(os.path.join(carpeta_media, "images (1).jfif")),
    pygame.image.load(os.path.join(carpeta_media, "images (2).jfif"))
]

# Ajustar imágenes al tamaño de la ventana
imagenes = [
    pygame.transform.scale(imagen, (ANCHO, ALTO))
    for imagen in imagenes
]

# Cargar y reproducir música
ruta_musica = os.path.join(carpeta_media, "sonido circus videojuego.mp3")

pygame.mixer.music.load(ruta_musica)
pygame.mixer.music.play(-1)

# Variables para controlar las imágenes
indice_imagen = 0
tiempo_cambio = 3000  # 3 segundos
ultimo_cambio = pygame.time.get_ticks()

# Control de FPS
reloj = pygame.time.Clock()

# Bucle principal
ejecutando = True

while ejecutando:

    # Detectar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # Obtener tiempo actual
    tiempo_actual = pygame.time.get_ticks()

    # Cambiar imagen automáticamente
    if tiempo_actual - ultimo_cambio >= tiempo_cambio:

        indice_imagen = (indice_imagen + 1) % len(imagenes)

        ultimo_cambio = tiempo_actual

    # Dibujar imagen de fondo
    screen.blit(imagenes[indice_imagen], (0, 0))

    # Actualizar pantalla
    pygame.display.flip()

    # Mantener 60 FPS
    reloj.tick(60)

# Finalizar Pygame
pygame.mixer.music.stop()
pygame.quit()
