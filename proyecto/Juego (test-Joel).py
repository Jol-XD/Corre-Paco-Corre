import random
import time
import pygame
import os

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

# Define the player class
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity_x, velocity_y):
        super().__init__()
        original_image = pygame.image.load(os.path.join("proyecto", "sprites", "pibe_palo.png")).convert_alpha()
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.gravity = 1.1
        self.jump_strength = -20
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.velocity[1] += self.gravity

        if self.velocity[1] > 10:
            self.velocity[1] = 10

        if not self.is_jumping:
            self.velocity[1] += self.gravity

        if self.rect.y >= 700:
            self.is_jumping = False
            if not self.is_agachado:
                self.rect.y = 700
                self.velocity[1] = 0
            else:
                self.rect.y = 740
                self.velocity[1] = 0

    def salto(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = self.jump_strength

    def agacharse(self):
        if not self.is_agachado:
            self.is_agachado = True
            self.rect.height = 40
            self.rect.y = self.rect.y + 50

    def levantarse(self):
        if self.is_agachado:
            self.is_agachado = False
            self.rect.height = 80
            self.rect.y -= 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity):
        super().__init__()
        self.image = pygame.image.load(os.path.join("proyecto", "sprites", "structuras", "structure1(big).png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + self.get_height()
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)

    def get_height(self):
        return self.rect.height

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + 200
            self.velocity += 1

class Suelo(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Crea la instancia de la clase Suelo
suelo = Suelo(0, SCREEN_HEIGHT - suelo_height, suelo_image)

# Agrégala al grupo de sprites
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(suelo)

estructuras = pygame.sprite.Group()

for _ in range(1):
    nueva_estructura = Structure(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), 0, 50, 120, 10)
    nueva_estructura.rect.y = SCREEN_HEIGHT - nueva_estructura.get_height() - 121
    estructuras.add(nueva_estructura)

run = True
perder = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jugador.salto()
                print("salto")
            if event.key == pygame.K_DOWN and not jugador.is_jumping:
                jugador.agacharse()
                print("agachado")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                jugador.levantarse()
                print("levantado")

    choque = pygame.sprite.spritecollide(jugador, estructuras, False, pygame.sprite.collide_mask)
    if choque:
        lowest_collision_y = max([estructura.rect.top for estructura in choque])

        if jugador.rect.bottom <= lowest_collision_y + OFFSET:
            if jugador.velocity[1] > 0:
                jugador.rect.bottom = lowest_collision_y + OFFSET
                jugador.velocity[1] = 0
            jugador.is_jumping = False
        else:
            # Si el jugador está descendiendo, dejarlo atravesar la plataforma
            if jugador.velocity[1] > 0:
                jugador.is_jumping = True
                jugador.rect.y = lowest_collision_y - jugador.rect.height
            else:
                # Si el jugador está subiendo, detenerlo
                jugador.rect.y = lowest_collision_y + 1
                jugador.velocity[1] = 0

    if jugador.rect.right < 0:
        run = False

    jugador.update()
    estructuras.update()

    pantalla.fill(FONDO)

    for estructura in estructuras:
        pantalla.blit(estructura.image, estructura.rect)

    jugador.draw(pantalla)

    pygame.draw.rect(pantalla, VERDE, pygame.Rect(0, 780, 1200, 121))

    todos_los_sprites.draw(pantalla)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()