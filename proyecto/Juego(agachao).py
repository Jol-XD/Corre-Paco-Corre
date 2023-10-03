import random
import time
import pygame

ROJO = (255, 0, 0)
FONDO = (5, 130, 250)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 40)  # Tamaño del rectángulo del jugador
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.jump_strength = -10
        self.gravity = 0.33

        self.image = pygame.image.load("proyecto/sprites/pibe_palo.png")  
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.velocity[1] += self.gravity

        if self.velocity[1] > 3.5:
            self.velocity[1] = 3.5

        if not self.is_jumping:
            self.velocity[1] += self.gravity

        if self.rect.y >= 600 - 10:
            self.is_jumping = False
            self.rect.y = 600 - 10
            self.velocity[1] = 0

    def salto(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = self.jump_strength

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Dibuja la imagen en lugar del rectángulo

pygame.init()
screen_width = 1200
screen_height = 900
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")
jugador = Jugador(320, 240, 0, 0)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jugador.salto()
                print("salto")

    jugador.update()

    pantalla.fill(FONDO)

    jugador.draw(pantalla)

    pygame.display.update()

pygame.quit()
