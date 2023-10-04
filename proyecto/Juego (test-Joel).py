import random
import time
import pygame

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
FONDO = (5, 130, 250)

#Define al jugador
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
        pygame.draw.rect(surface, ROJO, self.rect)

class Estructura(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.rect = pygame.Rect(x, SCREEN_HEIGHT - height, width, height)
        self.velocity = velocity

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
            self.rect.y = SCREEN_HEIGHT - self.rect.height



pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("¡Corre Paco corre!")
jugador = Jugador(320, 240, 40, 80, 0, 0)

estructuras = pygame.sprite.Group()
for _ in range(1):  # Genera inicialmente 5 estructuras
    nueva_estructura = Estructura(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), 50, 200, 5)
    estructuras.add(nueva_estructura)

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
    estructuras.update()

    pantalla.fill(FONDO)

    for estructura in estructuras:
        pygame.draw.rect(pantalla, VERDE, estructura.rect)

    jugador.draw(pantalla)

    pygame.display.update()

pygame.quit()
