import random
import pygame
import os

ROJO = (255, 0, 0)
FONDO = (5, 130, 250)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False  
        self.gravity = 0.33
        self.jump_strength = -10

        # Cargar los cuadros individuales de la animación desde un archivo GIF
        self.animacion = []
        for i in range(1,8):  # Cambia el número según la cantidad de cuadros en tu GIF
            frame = pygame.image.load(os.path.join("proyecto","sprites", "corre", f"corre{i}.PNG"))
            frame = pygame.transform.scale(frame, (100, 120))
            self.animacion.append(frame)

        self.indice_animacion = 0  # Índice actual de la animación
        self.image = self.animacion[self.indice_animacion]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tiempo_animacion = 100  # Tiempo de espera entre cuadros
        self.ultimo_cambio = pygame.time.get_ticks()

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
                self.rect.y = 735
                self.velocity[1] = 0

        # Actualizar la animación
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion)
            self.image = self.animacion[self.indice_animacion]
            self.ultimo_cambio = tiempo_actual

    def salto(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = self.jump_strength

    def agacharse(self):
        if not self.is_agachado:
            self.is_agachado = True
            self.rect.height = 40
            self.rect.y += 40

    def levantarse(self):
        if self.is_agachado:
            self.is_agachado = False
            self.rect.height = 80
            self.rect.y -= 40

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

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
