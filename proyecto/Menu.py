import pygame, random

pygame.init()
screen_width = 800
screen_height = 600

pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")


class Boton():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def draw(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

juego_inicio = False

font = pygame.font.SysFont("arialblack", 40)

color_text = (255, 255, 255)

play_img = pygame.image.load('proyecto/boton_play.png').convert_alpha()

play_btn = Boton(450, 200, play_img, 0.18)



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, color_text)
    pantalla.blit(img, (x, y))

run = True
while run:

    pantalla.fill((202, 228, 241))

    if juego_inicio == True:
        play_btn.draw()
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