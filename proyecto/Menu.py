import pygame, random

pygame.init()
screen_width = 1200
screen_height = 900

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


font = pygame.font.SysFont("arialblack", 40)

color_text = (255, 255, 255)

jugar_img = pygame.image.load('proyecto/sprites/JUGAR1.png').convert_alpha()

jugar_btn = Boton(425, 291, jugar_img, 5.25)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, color_text)
    pantalla.blit(img, (x, y))

run = True
while run:

    pantalla.fill((202, 228, 241))
    jugar_btn.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()