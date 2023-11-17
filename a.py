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

#Define al jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity_x, velocity_y):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.gravity = 1.1
        self.jump_strength = -20
        self.image = pygame.image.load(os.path.join("proyecto", "sprites", "pibe_palo.png"))
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

    # Nueva sección para manejar colisiones laterales
        estructura_colisionada = pygame.sprite.spritecollideany(self, estructuras, pygame.sprite.collide_mask)
        if estructura_colisionada:
            if self.velocity[0] > 0:
                self.rect.right = estructura_colisionada.rect.left
            elif self.velocity[0] < 0:
                self.rect.left = estructura_colisionada.rect.right

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
        pygame.draw.rect(surface, ROJO, self.rect)
                
class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity):
        super().__init__()
        self.image = pygame.image.load(os.path.join("proyecto", "sprites", "structuras", "cajas-a.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + self.get_height()
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)
        self.es_plataforma = False

    def get_height(self):
        return self.rect.height

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + 200
            self.velocity += 1

        # Detección de colisiones laterales
        choque_lateral = pygame.sprite.collide_rect(jugador, self)
        if choque_lateral:
            if jugador.velocity[0] > 0:
                jugador.rect.right = self.rect.left
            elif jugador.velocity[0] < 0:
                jugador.rect.left = self.rect.right

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity):
        super().__init__()
        self.image = pygame.image.load(os.path.join("proyecto", "sprites", "structuras", "cajas-a.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + self.get_height()
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)
        self.es_plataforma = True  # Nuevo atributo

    def get_height(self):
        return self.rect.height

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + 200
            self.velocity += 1

jugador = Jugador(320, 240, 40, 80, 0, 0)

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
            if event.key == pygame.K_UP and not jugador.is_jumping or (not jugador.is_jumping and pygame.sprite.spritecollide(jugador, estructuras, False)):
                jugador.salto()
                print("salto")
            if event.key == pygame.K_DOWN:
                jugador.agacharse()
                print("agachado")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                jugador.levantarse()
                print("levantado")

    # Detección de colisiones
    # Detección de colisiones
    choque = pygame.sprite.spritecollideany(jugador, estructuras, pygame.sprite.collide_mask)
    if choque and choque.es_plataforma:
        estructura_colisionada = choque
        if jugador.rect.bottom <= estructura_colisionada.rect.top + OFFSET:
            jugador.rect.bottom = estructura_colisionada.rect.top + OFFSET
            jugador.velocity[1] = 0
            jugador.is_jumping = False
            
    if jugador.rect.right < 0:
        run = False

    jugador.update()
    estructuras.update()

    pantalla.fill(FONDO)

    for estructura in estructuras:
        pantalla.blit(estructura.image, estructura.rect)

    jugador.draw(pantalla)

    pygame.draw.rect(pantalla, VERDE, pygame.Rect(0, 780, 1200, 121))

    pygame.display.flip()  # Actualizar la pantalla
    clock.tick(60)  # Limitar los FPS a 60

    pygame.display.update()

pygame.quit()