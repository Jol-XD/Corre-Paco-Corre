import random
import pygame
import sys
import os
import math

# Define colores
MENU = (202, 228, 241)
FONDO = (5, 130, 250)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GREEN = (0, 255, 0)
NEGRO = (0, 0, 0)
MARRON = (128, 64, 0)
SUELO = (28, 121, 28)
BLANCO = (255, 255, 255)

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


#Titulo
titulo = pygame.image.load('sprites/titulos/nombre18.png').convert_alpha()
titulo= pygame.transform.scale(titulo, (500, 400))
titulo2 = pygame.image.load('sprites/titulos/nombre20.png').convert_alpha()
titulo2= pygame.transform.scale(titulo2, (500, 400))

# Carga de imágenes para los botones
jugar_img = pygame.image.load('sprites/botones/JUGAR1.png').convert_alpha()
jugar_presionado_img = pygame.image.load('sprites/botones/jugar02.png').convert_alpha()
salir_img = pygame.image.load('sprites/botones/SALIR1.png').convert_alpha()
salir_presionado_img = pygame.image.load('sprites/botones/salir002.png').convert_alpha()
salir_img2 = pygame.image.load('sprites/botones/salirnoche.png').convert_alpha()
salir_presionado_img2 = pygame.image.load('sprites/botones/salirnoche0.png').convert_alpha()
No_img = pygame.image.load('sprites/botones/no.png').convert_alpha()
Si_img = pygame.image.load('sprites/botones/si.png').convert_alpha()

jugar_btn = Boton(445, 540, jugar_img, 5.25)
salir_btn = Boton(446, 670, salir_img, 5.25)
salir_btn2 = Boton(446, 670, salir_img2, 5.25)
yes_btn = Boton(350, 400, Si_img, 5.25)
no_btn = Boton(675, 400, No_img, 5.25)

menu_activo = True
juego_activo = False

# Función para mostrar un mensaje de salida
def mostrar_mensaje_salida():
    pantalla.fill((201, 228, 241))
    mensaje = "¿Enserio deseas salir del juego?"
    font = pygame.font.SysFont("arialblack", 50)
    draw_text(mensaje, font, (255, 255, 255), 315, 300)

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

#Background
# Definir las velocidades para cada capa.
class Bg_menu1:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.speeds = [0.5, 0.10, 0.15, 0.20, 0.25]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 5):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_menu", "Clouds 5", f"{i}.png")).convert_alpha()
            
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)

                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0
bg_m1 = Bg_menu1(pantalla, screen_width, screen_height)

class Bg_menu2:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.speeds = [0.02, 0.05, 0.08, 0.11]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 4):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_menu", "Clouds 3", f"{i}.png")).convert_alpha()
            
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)

                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0
bg_m2 = Bg_menu2(pantalla, screen_width, screen_height)

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
    jugador.vida = 3

    # Restablece la posición de las estructuras
    estructura1.empty()
    enemigos.empty()
    
    numero_enemigo = random.randint(1, 3)  # Elegir un número aleatorio entre 1 y 3

    # Asignar el tipo de enemigo en función del número aleatorio
    if numero_enemigo == 1:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 2:
        tipo_enemigo = EnemigoVolador
    else:
        tipo_enemigo = EnemigoEnano
    nuevo_enemigo = tipo_enemigo(screen_width, 700)
    nuevo_enemigo.numero = numero_enemigo  
    enemigos.add(nuevo_enemigo)

    for _ in range(1):
            nueva_estructura = Estructura1(random.randint(screen_width, screen_width + 200), 50, 120, 10)
            estructura1.add(nueva_estructura)

    while menu_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if jugar_btn.rect.collidepoint(event.pos):
                    jugar_btn.clicked = True
                    jugar_btn.image = pygame.transform.scale(jugar_presionado_img, (int(jugar_presionado_img.get_width() * 5.25), int(jugar_presionado_img.get_height() * 5.25)))
                if salir_btn.rect.collidepoint(event.pos):
                    salir_btn.clicked = True
                    salir_btn.image = pygame.transform.scale(salir_presionado_img, (int(salir_presionado_img.get_width() * 5.25), int(salir_presionado_img.get_height() * 5.25)))

            if event.type == pygame.MOUSEBUTTONUP:
                if jugar_btn.clicked:
                    menu_activo = False
                    juego_activo = True
                    jugar_btn.clicked = False
                    cambiar_fondo_aleatorio()
                    jugar_btn.image = pygame.transform.scale(jugar_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))
                if salir_btn.clicked:
                    salir_btn.clicked = False
                    if mostrar_mensaje_salida():
                        run = False
                        salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))

            if event.type == pygame.MOUSEMOTION:
                # Restablecer el estado del botón si el mouse se mueve fuera del botón
                if not salir_btn.rect.collidepoint(event.pos):
                    salir_btn.clicked = False
                    salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))
                if not jugar_btn.rect.collidepoint(event.pos):
                    jugar_btn.clicked = False
                    jugar_btn.image = pygame.transform.scale(jugar_img, (int(jugar_img.get_width() * 5.25), int(jugar_img.get_height() * 5.25)))
        bg_m1.draw_bg()
        pantalla.blit(titulo, (350, 50))
        jugar_btn.draw()
        salir_btn.draw()
        pygame.display.update()

def mostrar_menu_pausa():
    global pausa

    pausa = True


    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if salir_btn.rect.collidepoint(event.pos):
                    salir_btn.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                if salir_btn.clicked:
                    salir_btn.clicked = False
                    if mostrar_mensaje_salida():
                        run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausa = False

        if salir_btn.clicked:
            salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))
        else:
            salir_btn.image = pygame.transform.scale(salir_img, (int(salir_img.get_width() * 5.25), int(salir_img.get_height() * 5.25)))


        bg_m2.draw_bg()
        pantalla.blit(titulo2, (350, 50))
        salir_btn.draw()
        mensaje = "Pulsa Esc para renudar"
        font = pygame.font.SysFont("arialblack", 50)
        draw_text(mensaje, font, (255, 255, 255), 410, 600)
    
        pygame.display.flip()

pausa = False

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        self.velocity = [velocity_x, velocity_y]
        self.is_jumping = False
        self.is_agachado = False
        self.is_atacando = False
        self.gravity = 1.1
        self.jump_strength = -20
        self.vida = 3
        self.attack_duration = 200
        self.attack_timer = 250
        self.attack = None
        self.space_pressed = False
        self.animacion_ataque_terminada = True
        self.ultimo_cambio = pygame.time.get_ticks()
        self.attack_start_time = 0

        self.animacion = []
        for i in range(1, 7):
            frame = pygame.image.load(os.path.join( "sprites", "corre", f"corre{i}.PNG"))
            frame = pygame.transform.scale(frame, (75, 100))
            self.animacion.append(frame)

        self.animacion_salto = []
        for i in range(1, 7):
            frame = pygame.image.load(os.path.join( "sprites", "salto", f"salto{i}.png"))
            frame = pygame.transform.scale(frame, (50, 100))
            self.animacion_salto.append(frame)

        self.animacion_agacharse = []
        for i in range(1, 9):
            frame = pygame.image.load(os.path.join( "sprites", "agachar", f"seagacha{i}.png"))
            frame = pygame.transform.scale(frame, (40, 45))
            self.animacion_agacharse.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tiempo_animacion = 100

    def cambiar_animacion_ataque(self):
        if not self.is_atacando and not self.is_jumping and not self.is_agachado:
            self.space_pressed = True
            self.animacion_ataque_terminada = False
            self.atacar()

    def detener_ataque(self):
        if self.is_atacando:
            self.is_atacando = False
            self.restablecer_animacion()
            self.attack = None  # Limpiar la instancia de ataque
            self.animacion_ataque_terminada = True

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.velocity[1] += self.gravity


        if self.velocity[1] > 10:
            self.velocity[1] = 10

        if not self.is_jumping:
            self.velocity[1] += self.gravity

        if self.rect.y >= 688:
            self.is_jumping = False
            if not self.is_agachado:
                self.rect.y = 688
                self.velocity[1] = 0
            else:
                self.rect.y = 735
                self.velocity[1] = 0

        if self.is_atacando:
            self.attack_timer += pygame.time.get_ticks() - self.ultimo_cambio
            self.ultimo_cambio = pygame.time.get_ticks()

            if self.attack_timer >= self.attack_duration:
                self.detener_ataque()
        else:
            # Cambiar a la animación de correr solo si no está saltando ni agachado
            if not self.is_jumping and not self.is_agachado:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
                    self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion)
                    self.image = self.animacion[self.indice_animacion]
                    self.ultimo_cambio = tiempo_actual

        if self.is_agachado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_agacharse)
                self.image = self.animacion_agacharse[self.indice_animacion]
                self.ultimo_cambio = tiempo_actual
        elif self.is_jumping:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_salto)
                self.image = self.animacion_salto[self.indice_animacion]
                self.ultimo_cambio = tiempo_actual
        else:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion)
                self.image = self.animacion[self.indice_animacion]
                self.ultimo_cambio = tiempo_actual

    def restablecer_animacion(self):
        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

    def salto(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = self.jump_strength

    def agacharse(self):
        if not self.is_agachado and (not self.is_jumping or (self.is_jumping and 650 <= self.rect.y <= 700)):
            self.is_agachado = True
            self.image = self.animacion_agacharse[0]
            self.rect.height = 40
            self.rect.y += 0

    def levantarse(self):
        if self.is_agachado:
            self.is_agachado = False
            self.rect.height = 80
            self.rect.y -= 0
            self.restablecer_animacion()

    def atacar(self):
        if not self.is_atacando:
            self.is_atacando = True
            self.attack_timer = 0
            self.attack_start_time = pygame.time.get_ticks()

            # Crear una instancia de la clase Attack
            self.attack = Attack(self.rect.x + 50, self.rect.y + 20)


    def restablecer_animacion(self):
        if not self.is_jumping and not self.is_agachado:
            # Restablecer la animación original de correr
            self.animacion = []
            for i in range(1, 7):
                frame = pygame.image.load(os.path.join( "sprites", "corre", f"corre{i}.PNG"))
                frame = pygame.transform.scale(frame, (75, 100))
                self.animacion.append(frame)


    def detener_ataque(self):
            if self.is_atacando:
                self.is_atacando = False
                self.attack = None  # Limpiar la instancia de ataque
                self.animacion_ataque_terminada = True

                # Switch back to the running animation
                self.animacion = []
                for i in range(1, 7):
                    frame = pygame.image.load(os.path.join( "sprites", "corre", f"corre{i}.PNG"))
                    frame = pygame.transform.scale(frame, (75, 100))
                    self.animacion.append(frame)

                # Set the current frame to the one where the attack animation left off
                elapsed_time = pygame.time.get_ticks() - self.attack_start_time
                frames_per_attack = 8  # Assuming 8 frames in the attack animation
                self.indice_animacion = (elapsed_time // self.tiempo_animacion) % frames_per_attack
                self.image = self.animacion[self.indice_animacion]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        if self.attack:
            self.attack.draw(surface)

class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, width=60, height=50):
        super().__init__()

        # Carga la imagen
        original_image = pygame.image.load('sprites/atack/atack.png')  # Ajusta la ruta de la imagen

        # Escala la imagen al tamaño deseado
        self.image = pygame.transform.scale(original_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        # Dibuja la imagen en la superficie
        surface.blit(self.image, self.rect.topleft)

vel_enemigos = -2 

class EnemigoNormal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.numero = 1, 4
        self.animacion = []  # Lista de la animación principal

        # Carga de la animación principal
        for i in range(2, 6):
            frame = pygame.image.load(os.path.join( "sprites", "esqueleto", "run", f"run_{i}.png"))
            frame = pygame.transform.scale(frame, (60, 80))
            self.animacion.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]  # Inicialmente en la animación principal

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.velocidad_inicial = vel_enemigos
        self.velocity_x = self.velocidad_inicial
        self.velocidad = self.velocidad_inicial
        self.derrotado = False 
        self.ultimo_cambio = pygame.time.get_ticks()
        self.tiempo_animacion = 200

    def update(self):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion)
            self.image = self.animacion[self.indice_animacion]
            self.ultimo_cambio = tiempo_actual

        self.rect.x += self.velocity_x

    def reiniciar(self):
        self.rect.x = screen_width
        self.rect.y = 700
        self.velocity_x = self.velocidad_inicial
        self.derrotado = False
        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

class EnemigoVolador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.numero = 2, 5
        self.animacion = []  # Lista de la animación principal

        # Carga de la animación principal
        for i in range(1, 8):
            frame = pygame.image.load(os.path.join( "sprites", "vuela_ojo", f"vuelo_{i}.png"))
            frame = pygame.transform.scale(frame, (70, 60))
            self.animacion.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]  # Inicialmente en la animación principal

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 680 
        self.velocidad_inicial = vel_enemigos - 1
        self.velocity_x = self.velocidad_inicial
        self.velocidad = self.velocidad_inicial
        self.derrotado = False 
        self.ultimo_cambio = pygame.time.get_ticks()
        self.tiempo_animacion = 100

    def update(self):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion)
            self.image = self.animacion[self.indice_animacion]
            self.ultimo_cambio = tiempo_actual

        self.rect.x += self.velocity_x

    def reiniciar(self):
        self.rect.x = screen_width
        self.rect.y = 680
        self.velocity_x = self.velocidad_inicial
        self.derrotado = False
        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

class EnemigoEnano(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.numero = 3, 6
        self.animacion = []  # Lista de la animación principal

        # Carga de la animación principal
        for i in range(1, 4):
            frame = pygame.image.load(os.path.join( "sprites", "goblin", f"run{i}.png"))
            frame = pygame.transform.scale(frame, (40, 40))
            self.animacion.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]  # Inicialmente en la animación principal

        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = 740
        self.velocidad_inicial = vel_enemigos -2
        self.velocity_x = self.velocidad_inicial
        self.velocidad = self.velocidad_inicial
        self.derrotado = False
        self.ultimo_cambio = pygame.time.get_ticks()
        self.tiempo_animacion = 100

    def update(self):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion)
            self.image = self.animacion[self.indice_animacion]
            self.ultimo_cambio = tiempo_actual

        self.rect.x += self.velocity_x

    def reiniciar(self):
        self.rect.x = screen_width
        self.rect.y = 740
        self.velocity_x = self.velocidad_inicial
        self.derrotado = False
        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

enemigos_derrotados = []
tiempo_transcurrido = 0


jugador = Jugador(320, 700, 0, 0)
enemigos = pygame.sprite.Group()  
spawn_timer = 0
spawn_interval = 3000

def generar_enemigo():
    global vel_enemigos
    numero_enemigo = random.randint(1, 9)

    if numero_enemigo == 1:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 2:
        tipo_enemigo = EnemigoVolador
    elif numero_enemigo == 4:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 5:
        tipo_enemigo = EnemigoVolador
    elif numero_enemigo == 7:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 8:
        tipo_enemigo = EnemigoVolador
    else:
        tipo_enemigo = EnemigoEnano

    if not vel_enemigos >= 45:
        vel_enemigos -= 0.5
    nuevo_enemigo = tipo_enemigo(screen_width, 700)
    nuevo_enemigo.numero = numero_enemigo
    enemigos.add(nuevo_enemigo)
    print(f"¡Apareció un enemigo número {numero_enemigo}!")

font = pygame.font.SysFont("arialblack", 40) 
puntuacion = 0
tiempo_ultimo_punto = 0

def actualizar_puntuacion():
    global puntuacion
    global tiempo_ultimo_punto

    tiempo_actual = pygame.time.get_ticks()

    # Comprueba si ha pasado al menos 10 segundos desde el último punto sumado
    if tiempo_actual - tiempo_ultimo_punto >= 50:
        puntuacion += 1
        tiempo_ultimo_punto = tiempo_actual  # Actualiza el tiempo del último punto sumado

    puntuacion_texto = font.render(f"Puntuación: {puntuacion}", True, GREEN)
    puntuacion_rect = puntuacion_texto.get_rect()
    puntuacion_rect.topright = (screen_width - 10, 10)
    pantalla.blit(puntuacion_texto, puntuacion_rect.topleft)


sprite_caja1 = pygame.image.load("sprites/structuras/cajas-a.png").convert_alpha()
sprite_caja2 = pygame.image.load("sprites/structuras/cajas-p.png").convert_alpha()
class Estructura1(pygame.sprite.Sprite):
    def __init__(self, x, width, height, velocity):
        super().__init__()
        self.image1 = pygame.image.load("sprites/structuras/cajas-a.png").convert_alpha()  # Cambia "ruta_de_tu_textura.jpg" con la ruta de tu textura
        self.image1 = pygame.transform.scale(self.image1, (width, height))
        self.image2 = pygame.image.load("sprites/structuras/cajas-p.png").convert_alpha()  # Cambia "ruta_de_tu_textura.jpg" con la ruta de tu textura
        self.image2 = pygame.transform.scale(self.image2, (width, height))
        self.image = self.image1
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.velocity = velocity
        self.structure_sel = None

    def update(self):
        global screen_width
        screen_width = pantalla.get_width()
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.rect.x = screen_width + 200
            self.structure_sel = random.randint(1, 3)
            if self.structure_sel == 1:
                if self.image == self.image2:
                    self.image = self.image1
                self.rect.y = screen_height - self.rect.height - 100
            elif self.structure_sel == 2:
                if self.image == self.image2:
                    self.image = self.image1
                self.rect.y = 720 - self.rect.height
            elif self.structure_sel == 3:
                if self.image == self.image1:
                    self.image = self.image2
                self.rect.y = screen_height - self.rect.height - 100
            if not self.velocity >= 40:
                self.velocity += 0.25
        pantalla.blit(self.image, self.rect)

estructure = Estructura1(x=100, width=50, height=50, velocity=5)

estructura1 = pygame.sprite.Group()    

font = pygame.font.Font(None, 36)
corazon_image = pygame.image.load("sprites/cora.png")
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

has_muerto_image = pygame.image.load("sprites/titulos/has_muerto.png")
has_muerto_image = pygame.transform.scale(has_muerto_image, (500, 300))

muerto = False

surface = pygame.display.set_mode((screen_width, screen_height ))

# Función para mostrar un mensaje de muerte
def mostrar_mensaje_muerte(surface):
    global run
    pantalla.fill(NEGRO)
    surface.blit(has_muerto_image, (350, 80))
    
    # Dibujar la puntuación actual del jugador con fuente Arial Black
    font = pygame.font.SysFont("arialblack", 40)
    texto_puntuacion = font.render(f"Puntuación: {puntuacion}", True, BLANCO)
    texto_puntuacion_rect = texto_puntuacion.get_rect()
    texto_puntuacion_rect.topleft = (500, 600)  # Ajusta la posición del mensaje de puntuación
    surface.blit(texto_puntuacion, texto_puntuacion_rect)

    # Dibujar un mensaje en la pantalla con un tamaño de fuente de 50
    font_mensaje = pygame.font.SysFont("arialblack", 45)
    texto = font_mensaje.render("Presiona cualquier tecla para volver al menú", True, BLANCO)
    texto_rect = texto.get_rect()
    texto_rect.topleft = (295, 700)  
    surface.blit(texto, texto_rect)
    
    pygame.display.update()

    muerto = True
    while muerto:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                muerto = False
            if event.type == pygame.KEYDOWN:
                muerto = False

class Bg_juego1:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.45, 0.55]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 4):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_1", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

class Bg_juego2:
    scrolls = 0
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.55, 0.55, 0.57]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_7", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

class Bg_juego3:
    scrolls = 0
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.55, 0.58, 0.61]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_8", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

class Bg_juego4:
    scrolls = 0
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.55, 0.55, 0.60]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_6", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

class Bg_juego5:
    scrolls = 0
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.55, 0.60,]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 5):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_4", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

class Bg_juego6:
    scrolls = 0
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.55, 0.60,]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 5):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_3", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

class Bg_juego7:
    scrolls = 0
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.bg_speed = 1  # Velocidad adicional para el fondo

        self.speeds = [0.25, 0.35, 0.55, 0.58, 0.60]
        self.scrolls = [0] * len(self.speeds)

        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(os.path.join( "sprites", "bg_juego", "Ocean_5", f"{i}.png")).convert_alpha()
            # Calculate the corresponding width to maintain the aspect ratio
            aspect_ratio = bg_image.get_width() / bg_image.get_height()
            bg_width = int(self.screen_height * aspect_ratio)
            
            # Resize the image to the calculated width and screen_height
            bg_image = pygame.transform.scale(bg_image, (bg_width, self.screen_height))
            
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()

        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

    def draw_bg(self):
        for i, (image, speed) in enumerate(zip(self.bg_images, self.speeds)):
            for x in range(0, self.tiles):
                position = (x * self.bg_width + self.scrolls[i], 0)
                self.screen.blit(image, position)

                # Actualiza el desplazamiento para cada capa.
                self.scrolls[i] -= speed

                if abs(self.scrolls[i]) > self.bg_width:
                    self.scrolls[i] = 0

    def reset_scroll(self):
        self.scrolls = [0] * len(self.speeds)

bg1 = Bg_juego1(pantalla, screen_width, screen_height)
bg2 = Bg_juego2(pantalla, screen_width, screen_height)
bg3 = Bg_juego3(pantalla, screen_width, screen_height)
bg4 = Bg_juego4(pantalla, screen_width, screen_height)
bg5 = Bg_juego5(pantalla, screen_width, screen_height)
bg6 = Bg_juego6(pantalla, screen_width, screen_height)
bg7 = Bg_juego7(pantalla, screen_width, screen_height)
current_bg = random.choice([bg1, bg2, bg3, bg4, bg5, bg6, bg7])

def cambiar_fondo_aleatorio():
    global current_bg
    current_bg = random.choice([bg1, bg2, bg3, bg4, bg5, bg6, bg7])
    current_bg.reset_scroll()
    print(f"Fondo cambiado a: {current_bg}")

def reiniciar_juego():
    global puntuacion, tiempo_ultimo_punto, juego_activo, menu_activo, scrolls, vel_enemigos
    # Reinicia las variables globales
    puntuacion = 0
    tiempo_ultimo_punto = pygame.time.get_ticks()
    juego_activo = False
    menu_activo = True
    scrolls = 0
    vel_enemigos = -2

    # Elimina todos los enemigos
    enemigos.empty()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if juego_activo:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mostrar_menu_pausa()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jugador.salto()
                if event.key == pygame.K_DOWN:
                    jugador.agacharse()
                if event.key == pygame.K_SPACE and not jugador.is_atacando: 
                    jugador.atacar()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    jugador.levantarse()

    jugador.update()
    estructura1.update()
    # Actualiza la posición de los enemigos
    for enemigo in enemigos.sprites():
        enemigo.update()

        # Verifica si el enemigo está fuera de la pantalla (lado derecho o izquierdo)
        if enemigo.rect.right < 0 or enemigo.rect.left > screen_width:
            enemigo.derrotado = True
            enemigos_derrotados.append(enemigo)
            print("¡Enemigo salió de la pantalla!")
            generar_enemigo()

    # Elimina los enemigos derrotados del grupo de enemigos
    for enemigo in enemigos_derrotados:
        enemigos.remove(enemigo)

    enemigos_derrotados = []

    # Colisiones y lógica del juego
    colisiones_jugador_enemigos = pygame.sprite.spritecollide(jugador, enemigos, False)
    if colisiones_jugador_enemigos:
        for enemigo in colisiones_jugador_enemigos:
            jugador.vida -= 1
            print(f"¡El jugador perdió 1 vida! Vidas restantes: {jugador.vida}")
            for enemigo in colisiones_jugador_enemigos:
                if not enemigo.derrotado:
                    enemigo.derrotado = True
                    enemigos_derrotados.append(enemigo)
                    print("¡Enemigo derrotado!")
                    generar_enemigo()

    # Colisiones del ataque del jugador con los enemigos
    if jugador.is_atacando and jugador.attack:
        colisiones_ataque_enemigos = pygame.sprite.spritecollide(jugador.attack, enemigos, False)
        if colisiones_ataque_enemigos:
            for enemigo in colisiones_ataque_enemigos:
                if not enemigo.derrotado:
                    enemigo.derrotado = True
                    enemigos_derrotados.append(enemigo)
                    print("¡Enemigo derrotado!")
                    generar_enemigo()

    if jugador.rect.right < 0:
        print("¡Juego terminado! Se salió de la pantalla.")
        mostrar_mensaje_muerte(surface)
        juego_activo = False
        menu_activo = True
        reiniciar_juego()

    if jugador.vida <= 0:
        print("¡Juego terminado! El jugador se quedó sin vidas.")
        mostrar_mensaje_muerte(surface)
        juego_activo = False
        menu_activo = True
        reiniciar_juego()

    choque = pygame.sprite.spritecollide(jugador, estructura1, False)
    if choque:
        estructura_colisionada = choque[0]
        if estructura_colisionada.structure_sel == 3:
            jugador.vida -= 3
        elif jugador.rect.right > estructura_colisionada.rect.left:
            jugador.rect.right = estructura_colisionada.rect.left
        elif jugador.rect.left < estructura_colisionada.rect.right:
            jugador.rect.left = estructura_colisionada.rect.right

    current_bg.draw_bg()
    jugador.draw(pantalla)
    estructura1.draw(pantalla)
    enemigos.draw(pantalla)

    mostrar_vida(pantalla, jugador.vida)
    actualizar_puntuacion()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

    if menu_activo:
        mostrar_menu()

pygame.quit()
