import random
import pgzrun
import time

WIDTH = 800
HEIGHT = 600
TITLE = "Proyecto Kodland"
FPS = 30

# Menú--------------------------------------
fondo = Actor("background_menu")
start = Actor("start", (WIDTH/2, 280))
Exit = Actor("exit", (WIDTH/2, 350))
menu = Actor("menu", (WIDTH/2, HEIGHT/2))
Menu = True
Game = False
score = 0
altura_maxima = 600
#-----------------------------------------------
# Player---------------------------------------------------
walk_right = [f"walk_right_{i}.png" for i in range(9)]
walk_left = [f"walk_left_{i}.png" for i in range(9)]
jump_right = [f"jump_right_{i}.png" for i in range(13)]
jump_left = [f"jump_left_{i}.png" for i in range(13)]
idle_right = [f"idle_right_{i}.png" for i in range(3)]
idle_left = [f"idle_left_{i}.png" for i in range(3)]
player = Actor(idle_right[0], (400, 500))
current_frame = 0
frame_duration = 10
frame_counter = 0
moving_right = False
moving_left = False
jumping = False
direction = "right"
JUMP_SPEED = -10
initial_player_x = WIDTH/2
initial_player_y = 500
GRAVITY = 0.8
MAX_FALL_SPEED = 15
MOVE_SPEED = 5
velocity_y = 0
on_ground = False
balas = 10
bomb = 10
lives = 3
shoot = False
bullets = []
last_shot_time = 0
last_bomb_time = 0
SHOOT_DELAY = 0.25
BOMB_DELAY = 0.5
BULLET_SPEED = 7
#---------------------------------------------------------------------------------------------------
# Mapa----------------------------------------------------------------------------------------------
TORRES = []
plataformas = []
altura_torres = 0
zona1 = Actor("pinchos",(WIDTH/2,595))
zona3 = Actor("pinchosr",(WIDTH/2,10))
FONDO = Actor("fondoo0")
BASE = Actor("base",(WIDTH/2,580))
transition_active = False
transition_alpha = 0
TRANSITION_SPEED = 5
BOTON = False
start_hover = False
exit_hover = False
#----------------extras---------------------
TOWER_SCROLL_MULTIPLIER = 0.3
respawn_animation = False
respawn_frames = 0
RESPAWN_DURATION = 30 
menu_music_playing = False
#-----------------------------------------------------------------------------------------------------
def check_platform_collision():
    global on_ground, velocity_y, player
    on_ground = False

    # Check base collision first
    if player.colliderect(BASE):
        if velocity_y >= 0:
            player.y = BASE.top  # Set player position to top of base
            on_ground = True
            velocity_y = 0
            return True

    # Then check other platforms
    for plataforma in plataformas:
        if player.colliderect(plataforma):
            if velocity_y >= 0:
                player.y = plataforma.top
                on_ground = True
                velocity_y = 0

                if not getattr(plataforma, "checked", False):
                    plataforma.checked = True
                    destruir_plataforma(plataforma)
                return True
        else:
            plataforma.checked = False
        
    return False

def create_bullet():
    bullet = Actor('bullet')
    bullet.x = player.x + (20 if direction == "right" else -20)
    bullet.y = player.y - 1
    if direction == "left":
        bullet.angle = 180
    bullets.append({
        'actor': bullet,
        'speed': BULLET_SPEED if direction == "right" else -BULLET_SPEED
    })

def update_bullets():
    for bullet in bullets[:]:
        bullet['actor'].x += bullet['speed']
        if bullet['actor'].x < 0 or bullet['actor'].x > WIDTH:
            bullets.remove(bullet)

def player_update():
    global moving_right, moving_left, jumping, direction, velocity_y, on_ground, balas, bomb, shoot
    global last_shot_time, last_bomb_time

    moving_right = False
    moving_left = False

    if keyboard.right:
        player.x += MOVE_SPEED
        moving_right = True
        direction = "right"
    elif keyboard.left:
        player.x -= MOVE_SPEED
        moving_left = True
        direction = "left"

    current_time = time.time()
    if keyboard.x and shoot and balas > 0 and current_time - last_shot_time >= SHOOT_DELAY:
        shoot = False
        balas -= 1
        create_bullet()
        last_shot_time = current_time

    elif keyboard.x and shoot and balas == 0 and current_time - last_shot_time >= SHOOT_DELAY:
        shoot = False
        sounds.gun_empty.set_volume(0.2)
        sounds.gun_empty.play()
        last_shot_time = current_time
    shoot = True

    if keyboard.r and bomb > 0 and current_time - last_bomb_time >= BOMB_DELAY:
        bomb -= 1
        last_bomb_time = current_time

    player.x = max(0, min(player.x, WIDTH - player.width))

    if on_ground and keyboard.space:
        velocity_y = JUMP_SPEED
        jumping = True
        on_ground = False

    velocity_y = min(velocity_y + GRAVITY, MAX_FALL_SPEED)
    player.y += velocity_y

    check_platform_collision()
    
    if on_ground:
        jumping = False

def update_animations_player():
    global current_frame, frame_counter

    frame_counter += 1
    if frame_counter >= frame_duration:
        frame_counter = 0
        current_frame = (current_frame + 1) % 9
        
        if jumping:
            player.image = jump_right[current_frame % 13] if direction == "right" else jump_left[current_frame % 13]
        elif moving_right:
            player.image = walk_right[current_frame]
        elif moving_left:
            player.image = walk_left[current_frame]
        else:
            player.image = idle_right[current_frame % 3] if direction == "right" else idle_left[current_frame % 3]

def new_torre():
    global altura_torres
    x = WIDTH / 2
    y = HEIGHT - (70 * (altura_torres + 1))

    tower = Actor("secondary_tower", (x, y))
    TORRES.append(tower)
    
    num_plataformas = random.choice([1, 2])
    for i in range(num_plataformas):
        plataforma_x = tower.x + (50 * (i * 2 - 1))
        plataforma_y = tower.y - 20 + random.choice([-10, 10])
        plataforma = Actor("platform", (plataforma_x, plataforma_y))
        plataformas.append(plataforma)
    
    altura_torres += 1

def torres():
    global TORRES, plataformas
    scroll_speed = 0

    if jumping:
        scroll_speed = abs(velocity_y) * TOWER_SCROLL_MULTIPLIER

    BASE.y += scroll_speed

    for tower in TORRES:
        tower.y += scroll_speed

    for plataforma in plataformas:
        plataforma.y += scroll_speed

    TORRES = [tower for tower in TORRES if tower.y < HEIGHT + tower.height]
    plataformas[:] = [plataforma for plataforma in plataformas if plataforma.y < HEIGHT + plataforma.height]

def update():
    global transition_alpha, transition_active, Menu, Game, menu_music_playing
    
    if Menu and not transition_active:
        if not menu_music_playing:
            sounds.sound_menu.set_volume(0.2)
            sounds.sound_menu.play(loops=-1) 
            menu_music_playing = True
    
    muerte()
    
    if transition_active:
        transition_alpha = min(255, transition_alpha + TRANSITION_SPEED)
        if transition_alpha >= 255:
            Menu = False
            Game = True 
            setup_initial_towers() 
            transition_active = False
            transition_alpha = 0
            
    if Game:
        handle_respawn()
        if not respawn_animation:
            player_update()
        update_bullets()
        update_platform()
        actualizar_score(player.y)
        update_animations_player()
        torres()
        pinchos()
        muerte()
        if keyboard.space and on_ground:
            new_torre()

def draw():
    global score, balas, bomb, lives
    if Menu:
        draw_menu()
        if transition_active:
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, transition_alpha))
    elif Game:
        draw_game()
        zona1.draw()
        BASE.draw()

        for torre in TORRES:
            torre.draw()
        
        for plataforma in plataformas:
            if not hasattr(plataforma, "should_blink") or plataforma.should_blink:
                plataforma.draw()

        for bullet in bullets:
            bullet['actor'].draw()
        zona3.draw()
        dibujar_menu(score,balas,bomb,lives,True)
        player.draw()

def draw_menu():
    fondo.draw()
    menu.draw()
    start.draw()
    Exit.draw()

def draw_game():
    screen.fill((0, 0, 0))
    FONDO.draw()

def on_mouse_move(pos):
    global BOTON
    if Menu:
        if start.collidepoint(pos):
            if not BOTON:
                BOTON = True
                start.image = "darkened_start"
                sounds.select.set_volume(0.1)
                sounds.select.play()
        else:
            start.image = "start"

        if Exit.collidepoint(pos):
            if not BOTON:
                BOTON = True
                Exit.image = "darkened_exit"
                sounds.select.set_volume(0.1)
                sounds.select.play()
        else:
            Exit.image = "exit"
            
        if not start.collidepoint(pos) and not Exit.collidepoint(pos):
            BOTON = False

def on_mouse_up(pos, button):
    global Menu, Game, transition_active
    if Menu and not transition_active:
        sounds.sound_menu.set_volume(0.2)
        sounds.sound_menu.play(loops=-1)
        if start.collidepoint(pos):
            sounds.sound_menu.stop()
            transition_active = True
            reset_game()
        elif Exit.collidepoint(pos):
            exit()

        start.image = "start"
        Exit.image = "exit"

def setup_initial_towers():
    global altura_torres
    altura_torres = 0
    for _ in range(100):
        new_torre()

def obtener_ancho_char(char):
    LETTER_WIDTH = 12
    NUMBER_WIDTH = 16
    NUMBER_ONE_WIDTH = 9
    DOSP_WIDTH = 3
    if char == ':':
        return DOSP_WIDTH
    if char.isdigit():
        return NUMBER_ONE_WIDTH if char == '1' else NUMBER_WIDTH
    return LETTER_WIDTH

def dibujar_texto(texto, x, y, espacio=2):
    LETTER_WIDTH = 12
    VALID_CHARS = set('abcdefghijklmnopqrstuvwxyz0123456789: ')
    current_x = x
    texto = texto.lower()
    
    for char in texto:
        if char not in VALID_CHARS:
            continue
        if char == ' ':
            current_x += LETTER_WIDTH + espacio
            continue
        try:
            if char == ':':
                screen.blit('dosP', (current_x, y))
            else:
                screen.blit(f'char/{char}', (current_x, y))
        except:
            pass 
        current_x += obtener_ancho_char(char) + espacio

def dibujar_menu(score, balas, bombs, lives, show_up):
    dibujar_texto(f"score {score}", 10, 10)
    dibujar_texto(f"arms {balas}", 10, 40)
    dibujar_texto(f"bombs {bombs}", 10, 70)
    dibujar_texto(f"lives {lives}", 10, 100)
    if show_up:
        dibujar_texto("up", WIDTH - 50, 10)

def actualizar_score(pos_y_jugador):
    global score, altura_maxima
    if pos_y_jugador < altura_maxima:
        diferencia_altura = altura_maxima - pos_y_jugador
        altura_maxima = pos_y_jugador
        score += 10 + diferencia_altura * 0

def pinchos():
    global lives, respawn_animation, respawn_frames
    if player.colliderect(zona1) or player.colliderect(zona3):
        if lives > 0 and not respawn_animation:
            lives -= 1
            respawn_animation = True
            respawn_frames = 0

def muerte():
    global lives,Menu,Game
    if lives == 0:
        Menu = True
        Game = False
        reset_game()

def destruir_plataforma(plataforma):
    if not hasattr(plataforma, "time_to_destroy"):
        plataforma.time_to_destroy = 2.0
        plataforma.start_time = time.time()
        plataforma.should_blink = True

def update_platform():
    global plataformas
    current_time = time.time()
    
    for plataforma in plataformas[:]:
        if hasattr(plataforma, "time_to_destroy"):
            elapsed_time = current_time - plataforma.start_time
            
            if elapsed_time >= 1.0:
                plataforma.should_blink = (elapsed_time * 5) % 1 > 0.5
            
            if elapsed_time >= 2.0:
                plataformas.remove(plataforma)

def draw_plataformas():
    for plataforma in plataformas:
        if getattr(plataforma, "visible", True):
            plataforma.draw()

def handle_respawn():
    global respawn_animation, respawn_frames
    if respawn_animation:
        respawn_frames += 1
        start_x = player.x
        start_y = player.y
        target_x = WIDTH/2
        target_y = HEIGHT/2
        
        progress = min(respawn_frames / RESPAWN_DURATION, 1.0)
        player.x = start_x + (target_x - start_x) * progress
        player.y = start_y + (target_y - start_y) * progress
        
        if respawn_frames >= RESPAWN_DURATION:
            respawn_animation = False
            player.x = target_x
            player.y = target_y

def reset_game():
    global score, altura_maxima, TORRES, plataformas, player, altura_torres
    global balas, bomb, lives, velocity_y, on_ground
    
    player.x = initial_player_x
    player.y = initial_player_y
    velocity_y = 0
    on_ground = False
    
    balas = 10
    bomb = 15
    lives = 3
    
    score = 0
    altura_maxima = 600
    
    TORRES.clear()
    plataformas.clear()
    altura_torres = 0

pgzrun.go()