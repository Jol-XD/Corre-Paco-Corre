import pygame
import os
import sys

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

def cambiar_a_juego():
    os.system("proyecto/Juego.py")

def salir_del_juego():
    pygame.quit()
    sys.exit()

jugar_img = pygame.image.load('proyecto/sprites/JUGAR1.png').convert_alpha()
jugar_presionado_img = pygame.image.load('proyecto/sprites/jugar02.png').convert_alpha()
salir_img = pygame.image.load('proyecto/sprites/SALIR1.png').convert_alpha()
salir_presionado_img = pygame.image.load('proyecto/sprites/salir002.png').convert_alpha()
<<<<<<< HEAD
No_img = pygame.image.load('proyecto/sprites/no.png').convert_alpha()
=======
No_img = pygame.image.load('proyecto/sprites/X.png').convert_alpha()
>>>>>>> 8a0925e64d8f304e86eb3e1ab7138db605fc56a3
Si_img = pygame.image.load('proyecto/sprites/si.png').convert_alpha()

jugar_btn = Boton(445, 391, jugar_img, 5.25)
salir_btn = Boton(446, 525, salir_img, 5.25)
yes_btn = Boton(350, 400, Si_img, 2)
no_btn = Boton(600, 400, No_img, 2)

def mostrar_mensaje_salida():
    pantalla.fill((202, 228, 241))
    mensaje = "¿Enserio deseas salir del juego?"
    font = pygame.font.SysFont("arialblack", 40)
    draw_text(mensaje, font, (255, 255, 255), 325, 300)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_btn.rect.collidepoint(event.pos):
                    return True
                elif no_btn.rect.collidepoint(event.pos):
                    return False

        yes_btn.draw()
        no_btn.draw()
        pygame.display.update()

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
            if salir_btn.rect.collidepoint(event.pos):
                salir_btn.clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if jugar_btn.clicked:
                jugar_btn.clicked = False
                cambiar_a_juego()
            if salir_btn.clicked:
                salir_btn.clicked = False
                if mostrar_mensaje_salida():
                    run = False

    if jugar_btn.clicked:
        jugar_btn.image = pygame.transform.scale(jugar_presionado_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))
    else:
        jugar_btn.image = pygame.transform.scale(jugar_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))

    if salir_btn.clicked:
        salir_btn.image = pygame.transform.scale(salir_presionado_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))
    else:
        salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))

    jugar_btn.draw()
    salir_btn.draw()

    pygame.display.update()

pygame.quit()
