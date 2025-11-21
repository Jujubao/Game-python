import pgzrun
import sys
from pygame import Rect # Única exceção permitida

# --- CONFIGURAÇÕES ---
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Test Final"

# Estados do Jogo
game_state = 'menu'  # Pode ser 'menu' ou 'game'
music_on = True

# Física
GRAVITY = 1
JUMP_POWER = -16
SPEED = 5

# --- CLASSE BOTÃO (Para o Menu) ---
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.color = color
    
    def draw(self):
        # Desenha o retângulo do botão
        screen.draw.filled_rect(self.rect, self.color)
        # Desenha o texto centralizado
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color="white")

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- CLASSE JOGADOR ---
class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.on_ground = False
        
        # Sprites
        self.idle_sprites = ["p1_idle"]
        self.walk_sprites = ["p1_walk1", "p1_walk2"]
        self.current_frame = 0
        self.facing_right = True
        
        self.actor = Actor(self.idle_sprites[0])
        self.actor.pos = (x, y)
        
        # Hitbox ajustada
        self.rect = Rect(x, y, 40, 60)

    def update(self, platforms):
        dx = 0
        is_moving = False

        # Controles
        if keyboard.left:
            dx = -SPEED
            self.facing_right = False
            is_moving = True
        elif keyboard.right:
            dx = SPEED
            self.facing_right = True
            is_moving = True

        # Pulo
        if keyboard.up and self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False
            # SOM DE PULO
            # Proteção para o som de pulo
            if music_on:
                try:
                    sounds.jump.play()
                except:
                    pass # Se der erro, apenas ignora e continua o jogo

        # Movimento e Gravidade
        self.x += dx
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Colisão com Plataformas
        self.rect.midbottom = (self.x, self.y)
        self.on_ground = False
        
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.velocity_y > 0: # Caindo
                    self.y = plat.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.rect.bottom = plat.top

        # Atualiza Visual
        self.actor.pos = (self.x, self.y - (self.actor.height/2) + 5)
        self.animate(is_moving)

    def animate(self, is_moving):
        if is_moving:
            sprites = self.walk_sprites
            speed = 0.2
        else:
            sprites = self.idle_sprites
            speed = 0.1

        self.current_frame += speed
        if self.current_frame >= len(sprites):
            self.current_frame = 0

        self.actor.image = sprites[int(self.current_frame)]
        self.actor.flip_x = not self.facing_right

    def draw(self):
        self.actor.draw()
        
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.velocity_y = 0

# --- CLASSE INIMIGO ---
class Enemy:
    def __init__(self, x, y, distance):
        self.start_x = x
        self.x = x
        self.y = y
        self.max_distance = distance
        self.speed = 2
        self.direction = 1 
        
        self.sprites = ["enemy_walk1", "enemy_walk2"]
        self.current_frame = 0
        
        self.actor = Actor(self.sprites[0])
        self.actor.pos = (x, y)
        self.rect = Rect(x, y, 40, 40)

    def update(self):
        self.x += self.speed * self.direction
        if self.x > self.start_x + self.max_distance: self.direction = -1
        elif self.x < self.start_x: self.direction = 1
            
        self.rect.center = (self.x, self.y)
        self.actor.pos = (self.x, self.y)
        self.animate()

    def animate(self):
        self.current_frame += 0.1
        if self.current_frame >= len(self.sprites): self.current_frame = 0
        self.actor.image = self.sprites[int(self.current_frame)]
        self.actor.flip_x = (self.direction < 0)

    def draw(self):
        self.actor.draw()

# --- INICIALIZAÇÃO ---

# Instâncias do Menu
btn_start = Button(300, 200, 200, 50, "Start Game", "green")
btn_music = Button(300, 280, 200, 50, "Music: ON", "blue")
btn_exit = Button(300, 360, 200, 50, "Exit", "red")

# Instâncias do Jogo
hero = Player(100, 300)
platforms = [
    Rect(0, 550, 800, 50),
    Rect(200, 450, 200, 20),
    Rect(500, 350, 200, 20),
    Rect(50, 250, 100, 20)
]
enemies = [
    Enemy(200, 425, 150),
    Enemy(400, 525, 200)
]

# --- LOOP PRINCIPAL PGZERO ---

def update():
    if game_state == 'game':
        hero.update(platforms)
        for enemy in enemies:
            enemy.update()
            if hero.rect.colliderect(enemy.rect):
                print("Dano! Resetando...")
                hero.reset()

def draw():
    screen.clear()
    
    if game_state == 'menu':
        screen.fill((30, 30, 30)) # Fundo escuro pro menu
        screen.draw.text("PLATFORMER ADVENTURE", center=(400, 100), fontsize=50, color="yellow")
        btn_start.draw()
        btn_music.draw()
        btn_exit.draw()
        
    elif game_state == 'game':
        screen.fill((135, 206, 235)) # Céu azul
        for plat in platforms:
            screen.draw.filled_rect(plat, (100, 60, 20))
        for enemy in enemies:
            enemy.draw()
        hero.draw()

# --- INTERAÇÃO COM MOUSE (Para o Menu) ---
def on_mouse_down(pos):
    global game_state, music_on
    
    if game_state == 'menu':
        if btn_start.is_clicked(pos):
            game_state = 'game'
            
            # Tenta tocar a música, mas não fecha se der erro
            if music_on:
                try:
                    music.play('bg_music.wav')
                except Exception as e:
                    print(f"ERRO DE SOM: Não foi possível tocar a música.")
                    print(f"Detalhe do erro: {e}")
                
        elif btn_music.is_clicked(pos):
            music_on = not music_on
            if music_on:
                btn_music.text = "Music: ON"
                # music.unpause() # Opcional
            else:
                btn_music.text = "Music: OFF"
                music.stop() # Para a música se desligar
                
        elif btn_exit.is_clicked(pos):
            sys.exit()

pgzrun.go()