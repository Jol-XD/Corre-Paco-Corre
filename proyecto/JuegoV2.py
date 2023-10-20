import random
import time
import pygame
import sys

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

screen_width = 1200
screen_height = 900
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("¡Corre Paco corre!")

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

def salir_del_juego():
    pygame.quit()
    sys.exit()

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

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    pantalla.blit(img, (x, y))

def mostrar_menu():
    global menu_activo, juego_activo, puntuacion, tiempo_ultimo_punto

    menu_activo = True
    juego_activo = False
    puntuacion = 0
    tiempo_ultimo_punto = 0

    # Restablece la posición del jugador
    jugador.rect.x = 320
    jugador.rect.y = 240
    jugador.velocity = [0, 0]
    jugador.vida = 5

    # Restablece la posición de las estructuras
    estructuras.empty()
    for _ in range(1):
        nueva_estructura = Estructura(random.randint(screen_width, screen_width + 200), 50, 120, 10)
        estructuras.add(nueva_estructura)

    # Reinicia el tiempo de aparición de los enemigos
    spawn_timer = 0

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


class Jugador(pygame.sprite.Sprite):
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
        self.tipo = None  # Nuevo atributo para el tipo de enemigo
        self.image = pygame.Surface((40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.velocity_x = -3
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

    def reiniciar(self):
        # Reiniciar la posición del enemigo
        self.rect.x = screen_width
        self.rect.y = 700
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False

        # Crear un nuevo enemigo de ese tipo
        nuevo_enemigo = self.tipo(screen_width, 700)
        self.image.fill(nuevo_enemigo.image.get_at((0, 0)))  # Pinta el fondo del nuevo enemigo con el color del tipo
        self.velocity_x = nuevo_enemigo.velocity_x

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
        self.velocity_x = -6
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
        self.velocity_x = -5
        self.image.fill(AZUL)
        
    def reiniciar(self):
        # Reiniciar la posición del enemigo
        self.rect.x = screen_width
        self.rect.y = 700
        self.aparicion_timer = random.randint(5000, 8000)
        self.last_aparicion_time = pygame.time.get_ticks()
        self.derrotado = False

tiempo_ultimo_punto = 0 
puntuacion = 0
tipos_enemigos = [EnemigoNormal, EnemigoEnano, EnemigoVolador]

def actualizar_puntuacion():
    global puntuacion
    global tiempo_ultimo_punto

    tiempo_actual = pygame.time.get_ticks()

    # Comprueba si ha pasado al menos 10 segundos desde el último punto sumado
    if tiempo_actual - tiempo_ultimo_punto >= 5000:  # 10000 milisegundos = 10 segundos
        puntuacion += 1
        tiempo_ultimo_punto = tiempo_actual  # Actualiza el tiempo del último punto sumado 

    puntuacion_texto = font.render(f"Puntuación: {puntuacion}", True, GREEN)
    puntuacion_rect = puntuacion_texto.get_rect()
    puntuacion_rect.topright = (screen_width - 10, 10)
    pantalla.blit(puntuacion_texto, puntuacion_rect.topleft)


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


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if juego_activo:
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
                    puntuacion += 5  # Suma 10 puntos
                    print("¡Enemigo derrotado!")

        colisiones = pygame.sprite.spritecollide(jugador, enemigos, False)
        if colisiones:
            if not jugador.is_atacando:
                jugador.vida -= 1  # -1 vida si toca enemigo
                print(f"¡El jugador perdió 1 vida! Vidas restantes: {jugador.vida}")
            for enemigo in colisiones:
                enemigo.derrotado = True

        choque = pygame.sprite.spritecollide(jugador, estructuras, False)
        if choque:
            estructura_colisionada = choque[0]  # Obtén la primera estructura con la que ha colisionado
            if jugador.rect.right > estructura_colisionada.rect.left:
                jugador.rect.right = estructura_colisionada.rect.left

        if jugador.rect.right < 0:
            print("¡Juego terminado! Se salió de la pantalla.")
            juego_activo = False
            menu_activo = True

    # Comprobar si el jugador se queda sin vidas
        if jugador.vida <= 0:
            print("¡Juego terminado! El jugador se quedó sin vidas.")
            juego_activo = False
            menu_activo = True


        # Mueve la verificación del evento de cerrar la ventana aquí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        jugador.update()
        enemigos.update()
        estructuras.update()

        current_time = pygame.time.get_ticks()

        # Comprueba si es hora de generar un nuevo enemigo
        if current_time - spawn_timer > spawn_interval:
            enemigo = generar_enemigo()
            enemigos.add(enemigo)
            spawn_timer = current_time  

        pantalla.fill(FONDO)

        for estructura in estructuras:
            pygame.draw.rect(pantalla, MARRON, estructura.rect)

        jugador.draw(pantalla)
        enemigos.draw(pantalla)
        pygame.draw.rect(pantalla, SUELO, pygame.Rect(0, 780, 1200, 500))

        mostrar_vida(pantalla, jugador.vida)
        actualizar_puntuacion()
        pygame.display.update()
        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Limitar los FPS a 60

    elif menu_activo:
        mostrar_menu()

# Mueve la salida del juego fuera del bucle del juego
pygame.quit()
sys.exit()
