import pygame

# Inicializar Pygame
pygame.init()

# Definir constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Tamaño de cada celda en píxeles
ANCHO_CELDA = 50

# Definir la clase para los sprites
class Platform(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((ANCHO_CELDA, ANCHO_CELDA))
        if self.tipo == 1:
            self.image.fill((255, 0, 0))  # Rojo para cajas
        elif self.tipo == 2:
            self.image.fill((0, 0, 255))  # Azul para pinchos
        else:
            self.image.fill((0, 0, 0))  # Negro para otros tipos
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Inicializar la ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Juego con Sprites')

# Definir el nivel como una lista de listas con números
nivel = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0],
    [2, 2, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Crear un grupo para los sprites
sprites_group = pygame.sprite.Group()

# Crear sprites basados en el nivel
for fila in range(len(nivel)):
    for columna in range(len(nivel[fila])):
        tipo = nivel[fila][columna]
        if tipo != 0:
            sprite = Platform(tipo, columna * ANCHO_CELDA, fila * ANCHO_CELDA)
            sprites_group.add(sprite)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lógica del juego aquí

    # Dibujar los sprites
    screen.fill((0, 0, 0))  # Limpiar la pantalla
    sprites_group.draw(screen)

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
