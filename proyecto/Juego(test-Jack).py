import random
import time
import pygame

ROJO = (255, 0, 0)
FONDO = (5, 130, 250)
AZUL = (0, 0, 255)
GREEN = (0, 255, 0)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.is_atacando = False 
        self.gravity = 0.33
        self.jump_strength = -10
        self.vida = 50
        self.attack_duration = 200    # Duración del ataque en milisegundos
        self.attack_timer = 0  # Temporizador para controlar la duración del ataque

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
            self.attack_timer += pygame.time.get_ticks() - self.last_update_time
            self.last_update_time = pygame.time.get_ticks()
            
            # Si el tiempo de ataque supera la duración, detener el ataque
            if self.attack_timer >= self.attack_duration:
                self.detener_ataque()
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
        if not self.is_atacando:
            self.is_atacando = True
            self.attack_timer = 0
            self.last_update_time = pygame.time.get_ticks()

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
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.aparicion_timer = random.randint(5000, 8000)  
        self.last_aparicion_time = pygame.time.get_ticks()
        self.velocity_x = -1  # Se agregó la velocidad
        self.derrotado = False 

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

class EnemigoNormal(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.image.fill(ROJO)

    def reiniciar(self):
        # Reiniciar la posición del enemigo
        self.rect.x = screen_width
        self.rect.y = 700
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False

class EnemigoEnano(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, 755)
        self.image = pygame.transform.scale(self.image, (30, 25))
        self.velocity_x = -3
        self.rect.y = 755  
        self.image.fill(GREEN)

    def reiniciar(self):
        # Reiniciar la posición del enemigo
        self.rect.x = screen_width
        self.rect.y = 755
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False

class EnemigoVolador(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.velocity_x = -2
        self.image.fill(AZUL)
        
    def reiniciar(self):
        # Reiniciar la posición del enemigo
        self.rect.x = screen_width
        self.rect.y = 700
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False


pygame.init()
screen_width = 1200
screen_height = 900
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")
jugador = Jugador(320, 240, 0, 0)

enemigos = pygame.sprite.Group()  

run = True

spawn_timer = 0
spawn_interval = 3000 

def generar_enemigo():
    # Clases de enemigos disponibles
    clases_enemigos = [EnemigoNormal, EnemigoEnano, EnemigoVolador]

    # Elije una clase de enemigo aleatoriamente
    clase_enemigo = random.choice(clases_enemigos)

    # Crea un enemigo de la clase elegida
    enemigo = clase_enemigo(screen_width, 700)

    return enemigo

font = pygame.font.Font(None, 36)
corazon_image = pygame.image.load("proyecto/sprites/cora.png")
corazon_image = pygame.transform.scale(corazon_image, (30, 30))

def mostrar_vida(surface, vida):
    vida_text = font.render(f"Vida: {vida}", True, ROJO)
    surface.blit(vida_text, (10, 10))

    x_corazon = 70
    y_corazon = 10

    for i in range(vida):
        surface.blit(corazon_image, (x_corazon, y_corazon))
        x_corazon += 35

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

    # Detección de colisiones mejorada
    colisiones = pygame.sprite.spritecollide(jugador, enemigos, False)
    if colisiones:
        if not jugador.is_atacando:
            jugador.vida -= 1  # -1 vida si toca enemigo
            print(f"¡El jugador perdió 1 vida! Vidas restantes: {jugador.vida}")
        for enemigo in colisiones:
            enemigo.derrotado = True

    # Comprobar si el jugador se queda sin vidas
    if jugador.vida <= 0:
        print("¡Juego terminado! El jugador se quedó sin vidas.")
        run = False

    jugador.update()
    enemigos.update()

    current_time = pygame.time.get_ticks()

    # Comprueba si es hora de generar un nuevo enemigo
    if current_time - spawn_timer > spawn_interval:
        enemigo = generar_enemigo()
        enemigos.add(enemigo)
        spawn_timer = current_time  

    pantalla.fill(FONDO)

    jugador.draw(pantalla)
    enemigos.draw(pantalla)

    mostrar_vida(pantalla, jugador.vida)
    pygame.display.update()

pygame.quit()