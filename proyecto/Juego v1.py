import pygame, random

ROJO = (255, 0, 0)

pygame.init()
screen_width = 800
screen_height = 600
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hola")

pygame.draw.rect(pantalla, ROJO, (100, 100, 100, 50))

run = True
while run:
    pantalla.fill((5, 130, 250))
    pygame.draw.rect(pantalla, ROJO, (300, 350, 200, 100))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()


pygame.quit()