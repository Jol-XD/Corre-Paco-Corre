import pygame

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
        self.clicked = False

    def draw(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

jugar_img = pygame.image.load('proyecto/sprites/JUGAR1.png').convert_alpha()
jugar_presionado_img = pygame.image.load('proyecto/sprites/jugar02.png').convert_alpha()
salir_img = pygame.image.load('proyecto/sprites/SALIR1.png').convert_alpha()

jugar_btn = Boton(425, 291, jugar_img, 5.25)
salir_btn = Boton(440, 425, salir_img, 5.25)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    pantalla.blit(img, (x, y))

run = True
while run:
    pantalla.fill((202, 228, 241))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if jugar_btn.rect.collidepoint(event.pos):
                jugar_btn.clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            jugar_btn.clicked = False

    if jugar_btn.clicked:
        jugar_btn.image = pygame.transform.scale(jugar_presionado_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))
    else:
        jugar_btn.image = pygame.transform.scale(jugar_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))

    jugar_btn.draw()
    salir_btn.draw()

    pygame.display.update()

pygame.quit()
