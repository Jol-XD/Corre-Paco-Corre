import random
import time
import pygame
import sys
import os

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
    estructuras.empty()
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

def mostrar_menu_pausa():
    global pausa

    pausa = True

    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausa = False

        pantalla.fill(MENU)
        # Agrega aquí los elementos específicos del menú de pausa
        pygame.display.update()

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
        self.attack_timer = 0
        self.ultimo_cambio = pygame.time.get_ticks()

        self.animacion = []
        for i in range(1, 7):
            frame = pygame.image.load(os.path.join("proyecto", "sprites", "corre", f"corre{i}.PNG"))
            frame = pygame.transform.scale(frame, (75, 100))
            self.animacion.append(frame)

        self.animacion_salto = []
        for i in range(1, 7):
            frame = pygame.image.load(os.path.join("proyecto", "sprites", "salto", f"salto{i}.png"))
            frame = pygame.transform.scale(frame, (50, 100))
            self.animacion_salto.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tiempo_animacion = 100

        self.image_crouch = pygame.image.load("proyecto/sprites/palo_agacha.png")
        self.image_crouch = pygame.transform.scale(self.image_crouch, (40, 40))

        self.attack_rect = None

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
            self.attack_rect = pygame.Rect(self.rect.x + 50, self.rect.y + 30, 60, 15)
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

        if self.is_jumping:
            self.image = self.animacion_salto[self.indice_animacion]

    def salto(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = self.jump_strength

    def agacharse(self):
        if not self.is_agachado and (not self.is_jumping or (self.is_jumping and 650 <= self.rect.y <= 700)):
            self.is_agachado = True
            self.image = self.image_crouch
            self.rect.height = 40
            self.rect.y += 0

    def levantarse(self):
        if self.is_agachado:
            self.is_agachado = False
            self.rect.height = 80
            self.rect.y -= 0 

    def atacar(self):
        if not self.is_atacando:
            self.is_atacando = True
            self.attack_timer = 0
            self.ultimo_cambio = pygame.time.get_ticks()
            self.restablecer_animacion()  # Agregado para restablecer la animación al atacar

    def restablecer_animacion(self):
        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]

    def detener_ataque(self):
        self.is_atacando = False
        self.restablecer_animacion()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        if self.is_atacando and self.attack_rect:
            pygame.draw.rect(surface, ROJO, self.attack_rect)

class EnemigoNormal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.numero = 1, 4
        self.animacion = []  # Lista de la animación principal

        # Carga de la animación principal
        for i in range(2, 6):
            frame = pygame.image.load(os.path.join("proyecto", "sprites", "esqueleto", "run", f"run_{i}.png"))
            frame = pygame.transform.scale(frame, (60, 80))
            self.animacion.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]  # Inicialmente en la animación principal

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.velocity_x = -4
        self.velocidad_inicial = -4
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

        if self.rect.right < 0 or self.derrotado:
            self.reiniciar()

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
            frame = pygame.image.load(os.path.join("proyecto", "sprites", "vuela_ojo", f"vuelo_{i}.png"))
            frame = pygame.transform.scale(frame, (70, 60))
            self.animacion.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]  # Inicialmente en la animación principal

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 680 
        self.velocity_x = -5
        self.velocidad_inicial = -5
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

        if self.rect.right < 0 or self.derrotado:
            self.reiniciar()

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
            frame = pygame.image.load(os.path.join("proyecto", "sprites", "goblin", f"run{i}.png"))
            frame = pygame.transform.scale(frame, (40, 40))
            self.animacion.append(frame)

        self.indice_animacion = 0
        self.image = self.animacion[self.indice_animacion]  # Inicialmente en la animación principal

        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = 740
        self.velocity_x = -6
        self.velocidad_inicial = -6
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

        if self.rect.right < 0 or self.derrotado:
            self.reiniciar()

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
    numero_enemigo = random.randint(1, 9)

    if numero_enemigo == 1:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 2:
        tipo_enemigo = EnemigoVolador
    if numero_enemigo == 4:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 5:
        tipo_enemigo = EnemigoVolador
    if numero_enemigo == 7:
        tipo_enemigo = EnemigoNormal
    elif numero_enemigo == 8:
        tipo_enemigo = EnemigoVolador
    else:
        tipo_enemigo = EnemigoEnano

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
                if event.key == pygame.K_SPACE:
                    jugador.detener_ataque()


    jugador.update()
    enemigos.update()
    estructuras.update()

    # Colisiones y lógica del juego
    colisiones = pygame.sprite.spritecollide(jugador, enemigos, False)
    if colisiones:
        for enemigo in colisiones:
            if not jugador.is_atacando:
                jugador.vida -= 1
                print(f"¡El jugador perdió 1 vida! Vidas restantes: {jugador.vida}")
            for enemigo in colisiones:
                if not enemigo.derrotado:
                    enemigo.derrotado = True
                    enemigos_derrotados.append(enemigo)
                    print("¡Enemigo derrotado!")
                    generar_enemigo()

        # Elimina los enemigos derrotados del grupo de enemigos
        for enemigo in enemigos_derrotados:
            enemigos.remove(enemigo)

        enemigos_derrotados = [] 

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

    choque = pygame.sprite.spritecollide(jugador, estructuras, False)
    if choque:
        estructura_colisionada = choque[0]
        if jugador.rect.right > estructura_colisionada.rect.left:
            jugador.rect.right = estructura_colisionada.rect.left
        elif jugador.rect.left < estructura_colisionada.rect.right:
            jugador.rect.left = estructura_colisionada.rect.right

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
