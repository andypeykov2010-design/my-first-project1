import pygame
import sys

# Цветове
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (220, 53, 69)
GREEN = (40, 167, 69)
BLUE = (0, 217, 255)
YELLOW = (255, 215, 0)
DARK_BG = (20, 20, 30)
ORANGE = (255, 140, 0)

class Bullet:
    def __init__(self, x, y, direction, color, speed=12):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed          # ← НОВО: приема speed
        self.size = 8
        self.color = color
        self.active = True
    
    def move(self):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > 800:
            self.active = False
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 3)


class Hero:
    def __init__(self, x, y, color, player_num, speed=6, bullet_speed=12, health=100, cooldown=20, damage=20):
        self.x = x
        self.y = y
        self.color = color
        self.player_num = player_num
        self.speed = speed                  #НОВО
        self.bullet_speed = bullet_speed    #НОВО
        self.size = 50
        self.health = health                #НОВО
        self.max_health = health            #НОВО
        self.damage = damage                #НОВО
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = cooldown  #НОВО
        
        try:
            self.image = pygame.image.load(f"images/hero{player_num}.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
            self.has_image = True
        except:
            self.has_image = False
    
    def move(self, keys, up_key, down_key):
        if keys[up_key]:
            self.y -= self.speed
        if keys[down_key]:
            self.y += self.speed
        self.y = max(self.size, min(self.y, 600 - self.size))
    
    def shoot(self, direction):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.x, self.y, direction, self.color, self.bullet_speed)  # ← подава bullet_speed
            self.bullets.append(bullet)
            self.shoot_cooldown = self.shoot_cooldown_max  #НОВО
    
    def update_bullets(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        for bullet in self.bullets:
            bullet.move()
        self.bullets = [b for b in self.bullets if b.active]
    
    def draw(self, screen):
        if self.has_image:
            screen.blit(self.image, (self.x - 50, self.y - 50))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 5, 3)
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.player_num), True, WHITE)
            screen.blit(text, (self.x - 10, self.y - 15))
        
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen):
        bar_width = 80
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 15
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = GREEN if self.health > 50 else ORANGE if self.health > 25 else RED
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    def check_bullet_collision(self, other_hero):
        for bullet in self.bullets:
            if bullet.active:
                distance = ((bullet.x - other_hero.x)**2 + (bullet.y - other_hero.y)**2)**0.5
                if distance < (bullet.size + other_hero.size):
                    bullet.active = False
                    other_hero.health -= self.damage
                    return True
        return False


def start_game(mode="level1"):

    if mode == "training":
        speed, bullet_speed, health, cooldown, damage = 4, 8, 200, 30, 10
        level_name = "Тренировка"
    elif mode == "level1":
        speed, bullet_speed, health, cooldown, damage = 6, 12, 100, 20, 20
        level_name = "Ниво 1"
    elif mode == "level2":
        speed, bullet_speed, health, cooldown, damage = 9, 18, 70, 10, 30
        level_name = "Ниво 2"

    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"⚔️ Битка - {level_name}")  # показва нивото в заглавието
    clock = pygame.time.Clock()
    
    try:
        background = pygame.image.load("images/background.jpg")
        background = pygame.transform.scale(background, (800, 600))
        has_background = True
    except:
        has_background = False
    
    font_big = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    
    #НОВО: подаваме параметрите на двамата играчи
    player1 = Hero(100, 300, BLUE, 1, speed, bullet_speed, health, cooldown, damage)
    player2 = Hero(700, 300, RED,  2, speed, bullet_speed, health, cooldown, damage)
    
    running = True
    game_over = False
    winner = None
    show_controls = True
    controls_timer = 180
    
    while running:
        keys = pygame.key.get_pressed()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if not game_over:
                    if e.key == pygame.K_d:
                        player1.shoot(1)
                    if e.key == pygame.K_LEFT:
                        player2.shoot(-1)
        
        if not game_over:
            player1.move(keys, pygame.K_w, pygame.K_s)
            player2.move(keys, pygame.K_UP, pygame.K_DOWN)
            player1.update_bullets()
            player2.update_bullets()
            player1.check_bullet_collision(player2)
            player2.check_bullet_collision(player1)
            
            if player1.health <= 0:
                game_over = True
                winner = 2
            elif player2.health <= 0:
                game_over = True
                winner = 1
            
            if show_controls and controls_timer > 0:
                controls_timer -= 1
                if controls_timer == 0:
                    show_controls = False
        
        if has_background:
            window.blit(background, (0, 0))
        else:
            window.fill(DARK_BG)
        
        player1.draw(window)
        player2.draw(window)
        
        p1_text = font_medium.render(f"Играч 1: {player1.health}HP", True, RED)
        window.blit(p1_text, (20, 20))
        p2_text = font_medium.render(f"Играч 2: {player2.health}HP", True, BLUE)
        window.blit(p2_text, (800 - p2_text.get_width() - 20, 20))
        
        #НОВО: показва нивото горе в средата
        lvl_text = font_small.render(level_name, True, YELLOW)
        window.blit(lvl_text, (800//2 - lvl_text.get_width()//2, 20))
        
        if show_controls and not game_over:
            control_bg = pygame.Surface((450, 160))
            control_bg.set_alpha(200)
            control_bg.fill(BLACK)
            window.blit(control_bg, (175, 220))
            title_ctrl = font_medium.render("КОНТРОЛИ", True, YELLOW)
            p1_move = font_small.render("Играч 1: W/S движение, D стрелба →", True, BLUE)
            p2_move = font_small.render("Играч 2: ↑ ↓ движение, ← стрелба", True, RED)
            window.blit(title_ctrl, (800//2 - title_ctrl.get_width()//2, 240))
            window.blit(p1_move,    (800//2 - p1_move.get_width()//2, 290))
            window.blit(p2_move,    (800//2 - p2_move.get_width()//2, 325))
        
        if game_over:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            window.blit(overlay, (0, 0))
            winner_color = BLUE if winner == 1 else RED
            winner_text = font_big.render(f"ИГРАЧ {winner} ПЕЧЕЛИ!", True, winner_color)
            window.blit(winner_text, (800//2 - winner_text.get_width()//2, 250))
            restart = font_medium.render("ESC за изход", True, WHITE)
            window.blit(restart, (800//2 - restart.get_width()//2, 350))
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
   