import pygame
import os
import random

clock = pygame.time.Clock()
OFFSET = 10
ROJO = (255, 0, 0)
VERDE = (28, 121, 28)
AZUL = (0, 0, 255)
MARRON = (128, 64, 0)
FONDO = (5, 130, 250)

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("¡Corre Paco corre!")

# Clase Jugador omitida por simplicidad

# Clase Structure para representar las plataformas
class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + 200
            self.rect.y = random.randint(SCREEN_HEIGHT - 121 - 120, SCREEN_HEIGHT - 121)

# Función para crear plataformas de forma aleatoria
def generar_plataformas(num_plataformas):
    plataformas = pygame.sprite.Group()
    for _ in range(num_plataformas):
        x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
        y = random.randint(SCREEN_HEIGHT - 121 - 120, SCREEN_HEIGHT - 121)
        plataforma = Structure(x, y, 50, 120, 10)
        plataformas.add(plataforma)
    return plataformas

estructuras = generar_plataformas(5)  # Ajusta la cantidad de plataformas según sea necesario

jugador = Jugador(320, 700, 40, 80, 0, 0)

todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(jugador)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    choque = pygame.sprite.spritecollide(jugador, estructuras, False, pygame.sprite.collide_rect)
    if choque:
        lowest_collision_y = max([estructura.rect.top for estructura in choque])

        if jugador.rect.bottom <= lowest_collision_y + OFFSET:
            if jugador.velocity[1] > 0:
                jugador.rect.bottom = lowest_collision_y + OFFSET
                jugador.velocity[1] = 0
            jugador.is_jumping = False
        else:
            if jugador.velocity[1] > 0:
                jugador.is_jumping = True
                jugador.rect.y = lowest_collision_y - jugador.rect.height
            else:
                jugador.rect.y = lowest_collision_y + 1
                jugador.velocity[1] = 0

    if estructuras.sprites() and estructuras.sprites()[0].rect.right < 0:
        estructuras.sprites()[0].kill()
        nueva_estructura = Structure(SCREEN_WIDTH + 200, random.randint(SCREEN_HEIGHT - 121 - 120, SCREEN_HEIGHT - 121), 50, 120, 10)
        estructuras.add(nueva_estructura)

    if jugador.rect.right < 0:
        run = False

    jugador.update()
    estructuras.update()

    pantalla.fill(FONDO)

    for estructura in estructuras:
        pantalla.blit(estructura.image, estructura.rect)

    todos_los_sprites.draw(pantalla)

    pygame.draw.rect(pantalla, VERDE, pygame.Rect(0, 780, 1200, 121))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
