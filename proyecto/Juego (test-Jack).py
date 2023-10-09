import random
import time
import pygame

ROJO = (255, 0, 0)
FONDO = (5, 130, 250)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.is_atacando = False 
        self.gravity = 0.33
        self.jump_strength = -10

        # Imágenes del jugador
        self.image_stand = pygame.image.load("proyecto/sprites/pibe_palo.png")
        self.image_crouch = pygame.image.load("proyecto/sprites/palo_agacha.png")
        
        self.image_stand = pygame.transform.scale(self.image_stand, (40, 80))
        self.image_crouch = pygame.transform.scale(self.image_crouch, (40, 40))

        self.image = self.image_stand
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.attack_rect = None  # Rectángulo de ataque del jugador

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

        # Actualizar la posición del rectángulo de ataque
        if self.is_atacando:
            self.attack_rect = pygame.Rect(self.rect.x + 40, self.rect.y + 30, 40, 15)
        else:
            self.attack_rect = None

    def salto(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = self.jump_strength

    def agacharse(self):
        if not self.is_agachado:
            self.is_agachado = True
            self.image = self.image_crouch
            self.rect.height = 40
            self.rect.y += 0

    def levantarse(self):
        if self.is_agachado:
            self.is_agachado = False
            self.image = self.image_stand
            self.rect.height = 80
            self.rect.y -= 0

    def atacar(self):
        self.is_atacando = True

    def detener_ataque(self):
        self.is_atacando = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        # Dibujar el rectángulo de ataque si está activo
        if self.is_atacando and self.attack_rect:
            pygame.draw.rect(surface, ROJO, self.attack_rect)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = -2  # Velocidad de movimiento del enemigo
        self.aparicion_timer = random.randint(5000, 8000)  # Timer para la aparición aleatoria
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False  # Variable para rastrear si el enemigo ha sido derrotado

    def reiniciar(self):
        # Reiniciar la posición del enemigo fuera de la pantalla
        self.rect.x = screen_width
        self.rect.y = 700
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False  # Reiniciar el estado de derrota

    def update(self):
        # Mover el enemigo hacia adelante
        self.rect.x += self.velocity_x

        # Verificar si el enemigo ha salido completamente de la pantalla o ha sido derrotado
        if self.rect.right < 0 or self.derrotado:
            self.reiniciar()
        # Verificar si es hora de aparecer en una nueva posición aleatoria
        current_time = pygame.time.get_ticks()
        if current_time - self.last_aparicion_time > self.aparicion_timer:
            self.reiniciar()

pygame.init()
screen_width = 1200
screen_height = 900
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")
jugador = Jugador(320, 240, 0, 0)

enemigos = pygame.sprite.Group()  # Grupo para almacenar enemigos
enemigo = Enemigo(screen_width, random.randint(700, 700))  # Crear un enemigo fuera de la pantalla
enemigos.add(enemigo) 

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
            if event.key == pygame.K_SPACE:
                jugador.atacar()
                print("ataque")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                jugador.levantarse()
                print("levantado")
            if event.key == pygame.K_SPACE:
                jugador.detener_ataque()

    if jugador.attack_rect:
        for enemigo in enemigos:
            if jugador.attack_rect.colliderect(enemigo.rect):
                enemigo.derrotado = True  # Marcar al enemigo como derrotado en lugar de eliminarlo
                print("¡Enemigo derrotado!")

                
    jugador.update()
    enemigos.update()

    pantalla.fill(FONDO)

    jugador.draw(pantalla)
    enemigos.draw(pantalla)

    pygame.display.update()

pygame.quit()
