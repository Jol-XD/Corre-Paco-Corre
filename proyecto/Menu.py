import pygame, random

pygame.init()
screen_width = 800
screen_height = 600

pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

juego_inicio = False

font = pygame.font.SysFont("arialblack", 40)

color_text = (255, 255, 255)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, color_text)
    pantalla.blit(img, (x, y))


run = True
while run:

    pantalla.fill((202, 228, 241))

    if juego_inicio == True:
        pass
    else:
        draw_text("Pulsa Espacio para Comenzar", font, color_text, 70, 250)



    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                juego_inicio = True
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()