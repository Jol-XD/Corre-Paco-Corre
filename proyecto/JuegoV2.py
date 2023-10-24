import random
import time
import pygame
import sys

# Define colores
MENU = (202, 228, 241)
FONDO = (5, 130, 250)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GREEN = (0, 255, 0)
NEGRO = (0, 0, 0)
MARRON = (128, 64, 0)
SUELO = (28, 121, 28)

clock = pygame.time.Clock()
pygame.init()

# Configuración de la pantalla
screen_width = 1200
screen_height = 900
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")

# Clase para manejar botones
class Boton():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale (image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

# Función para salir del juego
def salir_del_juego():
    pygame.quit()
    sys.exit()

# Carga de imágenes para los botones
jugar_img = pygame.image.load('proyecto/sprites/JUGAR1.png').convert_alpha()
jugar_presionado_img = pygame.image.load('proyecto/sprites/jugar02.png').convert_alpha()
salir_img = pygame.image.load('proyecto/sprites/SALIR1.png').convert_alpha()
salir_presionado_img = pygame.image.load('proyecto/sprites/salir002.png').convert_alpha()
No_img = pygame.image.load('proyecto/sprites/no.png').convert_alpha()
Si_img = pygame.image.load('proyecto/sprites/si.png').convert_alpha()

jugar_btn = Boton(445, 391, jugar_img, 5.25)
salir_btn = Boton(446, 525, salir_img, 5.25)
yes_btn = Boton(350, 400, Si_img, 5.25)
no_btn = Boton(675, 400, No_img, 5.25)

menu_activo = True
juego_activo = False

# Función para mostrar un mensaje de salida
def mostrar_mensaje_salida():
    pantalla.fill((202, 228, 241))
    mensaje = "¿Enserio deseas salir del juego?"
    font = pygame.font.SysFont("arialblack", 40)
    draw_text(mensaje, font, (255, 255, 255), 270, 300)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_btn.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif no_btn.rect.collidepoint(event.pos):
                    return False

        yes_btn.draw()
        no_btn.draw()
        pygame.display.update()

# Función para dibujar texto en la pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    pantalla.blit(img, (x, y))

# Función para mostrar el menú principal
def mostrar_menu():
    global menu_activo, juego_activo, puntuacion, tiempo_ultimo_punto

    menu_activo = True
    juego_activo = False
    puntuacion = 0
    tiempo_ultimo_punto = 0

    jugador.rect.x = 320
    jugador.rect.y = 700
    jugador.velocity = [0, 0]
    jugador.vida = 5

    # Restablece la posición de las estructuras
    estructuras.empty()

    # Agregar un enemigo al principio del juego de manera aleatoria
    enemigos.empty()
    tipos_enemigos = [EnemigoNormal, EnemigoVolador] #falta EnemigoEnano
    enemigo_inicial = random.choice(tipos_enemigos)
    nuevo_enemigo = enemigo_inicial(screen_width, 700)
    enemigos.add(nuevo_enemigo)

    for _ in range(1):
        nueva_estructura = Estructura(random.randint(screen_width, screen_width + 200), 50, 120, 10)
        estructuras.add(nueva_estructura)


    while menu_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if jugar_btn.rect.collidepoint(event.pos):
                    jugar_btn.clicked = True
                if salir_btn.rect.collidepoint(event.pos):
                    salir_btn.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                if jugar_btn.clicked:
                    menu_activo = False
                    juego_activo = True
                    jugar_btn.clicked = False
                if salir_btn.clicked:
                    salir_btn.clicked = False
                    if mostrar_mensaje_salida():
                        run = False

        if jugar_btn.clicked:
            jugar_btn.image = pygame.transform.scale(jugar_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))
        else:
            jugar_btn.image = pygame.transform.scale(jugar_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))

        if salir_btn.clicked:
            salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))
        else:
            salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))

        pantalla.fill(MENU)
        jugar_btn.draw()
        salir_btn.draw()
        pygame.display.update()

class jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.is_atacando = False 
        self.gravity = 1.1
        self.jump_strength = -20
        self.vida = 5
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

        if self.velocity[1] > 10:
            self.velocity[1] = 10

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
        self.velocity_x = -3
        self.derrotado = False

    def update(self):
        self.rect.x += self.velocity_x

        if self.rect.right < 0 or self.derrotado:
            self.reiniciar()

    def reiniciar(self):
        self.rect.x = screen_width
        self.rect.y = 700
        self.velocity_x = -3
        self.derrotado = False

class EnemigoNormal(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.image.fill(ROJO)
        self.velocidad_inicial = -3
        self.velocidad = self.velocidad_inicial

    def reiniciar(self):
        super().reiniciar()
        self.velocity_x = self.velocidad

#class EnemigoEnano(Enemigo):
#    def __init__(self, x, y):
#        super().__init__(x, 755)
#        self.image = pygame.transform.scale(self.image, (30, 25))
#        self.velocity_x = -6
#        self.rect.y = 755
#       self.image.fill(GREEN)
#        self.velocidad_inicial = -6
#       self.velocidad = self.velocidad_inicial

#    def reiniciar(self):
#        super().reiniciar()
#        self.velocity_x = self.velocidad

class EnemigoVolador(Enemigo):
    def __init__(self, x, y,):
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.velocity_x = -5
        self.image.fill(AZUL)
        self.velocidad_inicial = -5
        self.velocidad = self.velocidad_inicial
    def reiniciar(self):
        super().reiniciar()
        self.velocity_x = self.velocidad
        

jugador = jugador(320, 700, 0, 0)
enemigos = pygame.sprite.Group()  
spawn_timer = 0
spawn_interval = 3000 
enemigo_en_pantalla = False
enemigo_actual = None
ultima_clase_enemigo = None
ultimo_tipo_enemigo = None
ultimo_enemigo_derrotado = False


def generar_enemigo():
    global enemigo_en_pantalla, ultima_clase_enemigo, ultimo_tipo_enemigo, ultimo_enemigo_derrotado
    if not enemigo_en_pantalla and ultimo_enemigo_derrotado:
        enemigo_en_pantalla = True
        # Clases de enemigos disponibles
        clases_enemigos = [EnemigoNormal, EnemigoVolador] #EnemigoEnano falta

        while True:
            # Elije una clase de enemigo aleatoriamente
            clase_enemigo = random.choice(clases_enemigos)

            # Comprueba si el tipo del enemigo es diferente al anterior
            if clase_enemigo != ultimo_tipo_enemigo:
                ultimo_tipo_enemigo = clase_enemigo
                ultima_clase_enemigo = clase_enemigo
                # Crea un enemigo de la clase elegida
                enemigo = clase_enemigo(screen_width, 700)
                return enemigo
    return None

font = pygame.font.SysFont("arialblack", 40) 
puntuacion = 0
tiempo_ultimo_punto = 0

def actualizar_puntuacion():
    global puntuacion
    global tiempo_ultimo_punto

    tiempo_actual = pygame.time.get_ticks()

    # Comprueba si ha pasado al menos 10 segundos desde el último punto sumado
    if tiempo_actual - tiempo_ultimo_punto >= 1000:
        puntuacion += 1
        tiempo_ultimo_punto = tiempo_actual  # Actualiza el tiempo del último punto sumado

    puntuacion_texto = font.render(f"Puntuación: {puntuacion}", True, GREEN)
    puntuacion_rect = puntuacion_texto.get_rect()
    puntuacion_rect.topright = (screen_width - 10, 10)
    pantalla.blit(puntuacion_texto, puntuacion_rect.topleft)

sprite_caja2 = pygame.image.load("proyecto/sprites/structuras/structure1(small).png").convert_alpha()
class Estructura(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.image = sprite_caja2
        self.rect = pygame.Rect(x, 0, width, height)  
        self.velocity = velocity
    
    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = screen_width + 200
            stucture_sel = random.randint(1, 2)
            if stucture_sel==1:
                self.rect.y = screen_height- self.rect.height - 100
            elif stucture_sel==2:
                self.rect.y = 720 - self.rect.height
            self.velocity += 0.25

estructuras = pygame.sprite.Group()

for _ in range(1):
    nueva_estructura = Estructura(random.randint(screen_width, screen_width + 200), 50, 120, 10)
    estructuras.add(nueva_estructura)

font = pygame.font.Font(None, 36)
corazon_image = pygame.image.load("proyecto/sprites/cora.png")
corazon_image = pygame.transform.scale(corazon_image, (30, 30))

# Función para mostrar la vida del jugador
def mostrar_vida(surface, vida):
    vida_text = font.render(f"Vida: {vida}", True, ROJO)
    surface.blit(vida_text, (10, 10))

    x_corazon = 70
    y_corazon = 10

    for i in range(vida):
        surface.blit(corazon_image, (x_corazon, y_corazon))
        x_corazon += 35

has_muerto_image = pygame.image.load("proyecto/sprites/has_muerto.png")
has_muerto_image = pygame.transform.scale(has_muerto_image, (500, 300))

# Función para mostrar un mensaje de muerte
def mostrar_mensaje_muerte(surface):
    global run

    surface.blit(has_muerto_image, (350, 200))
    pygame.display.update()

    muerto = True
    while muerto:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                muerto = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                muerto = False

def reiniciar_juego():
    global puntuacion
    global tiempo_ultimo_punto
    global juego_activo
    global menu_activo

    # Reinicia las variables globales
    puntuacion = 0
    tiempo_ultimo_punto = pygame.time.get_ticks()
    juego_activo = False
    menu_activo = True
    
    # Elimina todos los enemigos y estructuras
    enemigos.empty()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if juego_activo:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jugador.salto()
                if event.key == pygame.K_DOWN:
                    jugador.agacharse()
                if event.key == pygame.K_SPACE:
                    jugador.atacar()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    jugador.levantarse()
                if event.key == pygame.K_SPACE:
                    jugador.detener_ataque()

            if jugador.attack_rect:
                for enemigo in enemigos:
                    if jugador.attack_rect.colliderect(enemigo.rect):
                        enemigo.derrotado = True
                        puntuacion += 5
                        print("¡Enemigo derrotado!")
                        ultimo_enemigo_derrotado = True  # Indicar que el último enemigo fue derrotado

    colisiones = pygame.sprite.spritecollide(jugador, enemigos, False)
    if colisiones:
        if not jugador.is_atacando:
            jugador.vida -= 1
            print(f"¡El jugador perdió 1 vida! Vidas restantes: {jugador.vida}")
        for enemigo in colisiones:
            enemigo.derrotado = True
            puntuacion += 5
            print("¡Enemigo derrotado!")
            ultimo_enemigo_derrotado = True  # Indicar que el último enemigo fue derrotado

    # Restablecer el tipo del último enemigo si se derrotó
    if ultimo_enemigo_derrotado:
        ultima_clase_enemigo = None

    choque = pygame.sprite.spritecollide(jugador, estructuras, False)
    if choque:
        estructura_colisionada = choque[0]
        if jugador.rect.right > estructura_colisionada.rect.left:
            jugador.rect.right = estructura_colisionada.rect.left

    if jugador.rect.right < 0:
        print("¡Juego terminado! Se salió de la pantalla.")
        juego_activo = False
        menu_activo = True
        reiniciar_juego()

    if jugador.vida <= 0:
        print("¡Juego terminado! El jugador se quedó sin vidas.")
        juego_activo = False
        menu_activo = True
        reiniciar_juego()

    jugador.update()

    enemigo_actual = generar_enemigo()  # Generar un nuevo enemigo en cada iteración
    if enemigo_actual:
        enemigo_actual.update()

    if not enemigo_en_pantalla and ultimo_enemigo_derrotado:
        enemigo_actual = generar_enemigo()
        if enemigo_actual:
            enemigo_en_pantalla = True
            ultimo_enemigo_derrotado = False  # Restablecer el valor

    enemigos.update()
    estructuras.update()

    current_time = pygame.time.get_ticks()

# Aumenta la velocidad de los enemigos en función del tiempo transcurrido

    pantalla.fill(FONDO)

    for estructura in estructuras:
        pygame.draw.rect(pantalla, MARRON, estructura.rect)

    jugador.draw(pantalla)
    enemigos.draw(pantalla)
    pygame.draw.rect(pantalla, SUELO, pygame.Rect(0, 780, 1200, 500))

    mostrar_vida(pantalla, jugador.vida)
    actualizar_puntuacion()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

    if menu_activo:
        mostrar_menu()

pygame.quit()
sys.exit()