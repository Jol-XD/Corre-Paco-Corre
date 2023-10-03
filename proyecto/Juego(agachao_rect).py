import random
import time
import pygame

ROJO = (255, 0, 0)
FONDO = (5, 130, 250)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity_x, velocity_y):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.gravity = 0.33
        self.jump_strength = -10

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

    def agacharse(self):
        if not self.is_agachado:
            self.is_agachado = True
            self.rect.height = 40
            self.rect.y += 0

    def levantarse(self):
        if self.is_agachado:
            self.is_agachado = False
            self.rect.height = 80
            self.rect.y -= 0 


    def draw(self, surface):
        pygame.draw.rect(surface, ROJO, self.rect)

pygame.init()
screen_width = 1200
screen_height = 900
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")
jugador = Jugador(320, 240, 40, 80, 0, 0)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jugador.salto()
                print("salto")
            if event.key == pygame.K_DOWN:
                jugador.agacharse()
                print("agachado")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                jugador.levantarse()
                print("levantado")

    jugador.update()

    pantalla.fill(FONDO)

    jugador.draw(pantalla)

    pygame.display.update()

pygame.quit()
