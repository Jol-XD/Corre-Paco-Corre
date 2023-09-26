import random
import time

import pygame

ROJO = (255, 0, 0)
FONDO = (5, 130, 250)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.position = (x, y)
        self.velocity = (velocity_x, velocity_y)
        
    def update(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, 10)

    def salto(self):
        self.velocity = (1, self.velocity[0])

pygame.init()
screen_width = 800
screen_height = 600
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")
jugador = Jugador(320, 240, 0, 0)

run = True

while run:
    pantalla.fill(FONDO)
    pygame.draw.rect(pantalla, (28, 133, 45), (0, 500, 800, 200))
    
    pygame.draw.rect(pantalla, ROJO, (250, 300, 100, 200))

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jugador.salto()
                #pantalla.fill(FONDO)
                #pygame.draw.rect(pantalla, (28, 133, 45), (0, 500, 800, 200))
                #pygame.draw.rect(pantalla, ROJO, (250, 200, 100, 200))
                print("salto")
        
    jugador.update()

    pantalla.fill(FONDO)

    jugador.draw(pantalla)
                
    pygame.display.update()
    

pygame.quit()