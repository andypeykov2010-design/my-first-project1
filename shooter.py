import pygame
import sys
import pygame.mixer
from audio_manager import AudioManager

# Цветове
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (220, 53, 69)
GREEN = (40, 167, 69)
BLUE = (0, 217, 255)
YELLOW = (255, 215, 0)
DARK_BG = (20, 20, 30)
ORANGE = (255, 140, 0)

class Wall:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2) # Бяла рамка


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


class LaserBeam:
    """Лазерен лъч с определена продължителност."""
    def __init__(self, x, y, direction, color, length=600, duration=15):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.length = length
        self.duration = duration
        self.max_duration = duration
        self.active = True
        self.width = 8
        self.glow_colors = [
            (255, 100, 100) if color == RED else (100, 100, 255),
            color,
            (255, 200, 200) if color == RED else (200, 200, 255),
        ]
    
    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
    
    def draw(self, screen):
        if not self.active:
            return
        
        end_x = self.x + self.length * self.direction
        
        # Гниещ ефект (светъл ореол)
        glow_width = int(self.width * 3 * (self.duration / self.max_duration))
        glow_color = self.glow_colors[0]
        if glow_width > 0:
            pygame.draw.line(screen, glow_color, (self.x, self.y), (end_x, self.y), glow_width)
        
        # Основния лазер
        pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, self.y), self.width)
        
        # Бял център за интензитет
        pygame.draw.line(screen, WHITE, (self.x, self.y), (end_x, self.y), 2)
        
        # Точка на начало
        pygame.draw.circle(screen, self.glow_colors[2], (int(self.x), int(self.y)), 6)


class Hero:
    def __init__(self, x, y, color, player_num, speed=6, bullet_speed=12, health=100, cooldown=20, damage=20, ammo=10, max_ammo=10):
        self.x = x
        self.y = y
        self.color = color
        self.player_num = player_num
        self.speed = speed                  
        self.bullet_speed = bullet_speed    
        self.size = 50
        self.health = health                
        self.max_health = health            
        self.damage = damage                
        self.bullets = []
        self.lasers = []
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = cooldown 
        self.ammo = ammo
        self.max_ammo = max_ammo
        
        # Лазер режим
        self.use_laser = False
        self.laser_cooldown = 10  # По-бързо презареждане за лазери
        
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
    
    def toggle_weapon(self):
        """Преключва между куршуми и лазери."""
        self.use_laser = not self.use_laser
        return self.use_laser
    
    def shoot(self, direction, audio=None):
        if self.use_laser:
            self.shoot_laser(direction)
        else:
            self.shoot_bullet(direction, audio)
    
    def shoot_bullet(self, direction, audio=None):
        """Изстрелва куршум."""
        if self.shoot_cooldown == 0 and self.ammo > 0:
            bullet = Bullet(self.x, self.y, direction, self.color, self.bullet_speed)
            self.bullets.append(bullet)
            self.shoot_cooldown = self.shoot_cooldown_max
            self.ammo -= 1
            if audio:
                audio.play_shoot()
    
    def shoot_laser(self, direction):
        """Изстрелва лазер."""
        if self.shoot_cooldown == 0:
            laser = LaserBeam(self.x, self.y, direction, self.color, length=600, duration=15)
            self.lasers.append(laser)
            self.shoot_cooldown = self.laser_cooldown

            
    
    def update_bullets(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Обновяване на куршуми
        for bullet in self.bullets:
            bullet.move()
        self.bullets = [b for b in self.bullets if b.active]
        
        # Обновяване на лазери
        for laser in self.lasers:
            laser.update()
        self.lasers = [l for l in self.lasers if l.active]
    
    def draw(self, screen):
        if self.has_image:
            screen.blit(self.image, (self.x - 50, self.y - 50))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 5, 3)
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.player_num), True, WHITE)
            screen.blit(text, (self.x - 10, self.y - 15))
        
        # Рисуване на куршуми
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # Рисуване на лазери
        for laser in self.lasers:
            laser.draw(screen)
        
        self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen):
        bar_width = 80
        font = pygame.font.Font(None, 24)
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 15
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = GREEN if self.health > 50 else ORANGE if self.health > 25 else RED
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Показване на амуниция или режим на оръжие
        if self.use_laser:
            weapon_text = font.render(f"ЛАЗЕР", True, YELLOW)
        else:
            weapon_text = font.render(f"Ammo: {self.ammo}/{self.max_ammo}", True, WHITE)
        
        text_x = self.x - weapon_text.get_width() // 2
        text_y = bar_y + 12
        screen.blit(weapon_text, (text_x, text_y))


    def check_bullet_collision(self, other_hero):
        for bullet in self.bullets:
            if bullet.active:
                distance = ((bullet.x - other_hero.x)**2 + (bullet.y - other_hero.y)**2)**0.5
                if distance < (bullet.size + other_hero.size):
                    bullet.active = False
                    other_hero.health -= self.damage
                    return True
        return False
    
    def check_laser_collision(self, other_hero):
        """Проверява дали лазер попада противника и наносява щета постоянно."""
        for laser in self.lasers:
            if laser.active:
                # Проверка дали противника е на линията на лазера
                end_x = laser.x + laser.length * laser.direction
                
                # По-голяма зона за попадение (по-лесно попадение)
                if abs(other_hero.y - laser.y) < other_hero.size + 30:  # Увеличена зона
                    # Проверка на X позиция
                    if laser.direction == 1:  # Лазер идва отляво надясно
                        if laser.x <= other_hero.x <= end_x:  # Включени краищата
                            other_hero.health -= self.damage * 0.3  # Наносява щета всеки кадър
                    else:  # Лазер идва отдясно наляво
                        if end_x <= other_hero.x <= laser.x:  # Включени краищата
                            other_hero.health -= self.damage * 0.3  # Наносява щета всеки кадър
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
    audio = AudioManager()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"⚔️ Битка - {level_name}")  # показва нивото в заглавието
    clock = pygame.time.Clock()
    
    try:
        background = pygame.image.load("images/background.jpg")
        background = pygame.transform.scale(background, (800, 600))
        has_background = True
    except:
        has_background = False
    if has_background:
        window.blit(background, (0, 0))
    else:
        if mode == "level2":
             window.fill((40, 10, 10)) # Тъмно червен фон за по-трудно ниво
        else:
            window.fill(DARK_BG)

    
    font_big = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    
    # Подаваме параметрите на двамата играчи
    player1 = Hero(100, 300, BLUE, 1, speed, bullet_speed, health, cooldown, damage)
    player2 = Hero(700, 300, RED,  2, speed, bullet_speed, health, cooldown, damage)
    
    running = True
    game_over = False
    winner = None
    show_controls = True
    controls_timer = 180
    start_time = pygame.time.get_ticks()
    TIME_LIMIT = 60
    
    while running:
        keys = pygame.key.get_pressed()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if not game_over:
                    # Преключване на оръжие
                    if e.key == pygame.K_l:
                        laser_on = player1.toggle_weapon()
                        print(f"Играч 1: {'ЛАЗЕР' if laser_on else 'КУРШУМИ'}")
                    if e.key == pygame.K_k:  # K клавиш за Player 2
                        laser_on = player2.toggle_weapon()
                        print(f"Играч 2: {'ЛАЗЕР' if laser_on else 'КУРШУМИ'}")
                    
                    # Презареждане на амуниция
                    if e.key == pygame.K_r:
                        player1.ammo = player1.max_ammo
                    if e.key == pygame.K_RETURN or e.key == pygame.K_RSHIFT:
                        player2.ammo = player2.max_ammo
                    
                    # Стрелба
                    if e.key == pygame.K_d:
                        player1.shoot(1, audio)
                    if e.key == pygame.K_LEFT:
                         if mode != "training":
                             player2.shoot(-1, audio)
        
        if not game_over:
            player1.move(keys, pygame.K_w, pygame.K_s)
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
            time_left = max(0, TIME_LIMIT - elapsed)
            if mode != "training":
                player2.move(keys, pygame.K_UP, pygame.K_DOWN)
            player1.update_bullets()
            player2.update_bullets()
            player1.check_bullet_collision(player2)
            player2.check_bullet_collision(player1)
            player1.check_laser_collision(player2)
            player2.check_laser_collision(player1)
            
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

            if time_left == 0 and not game_over:
                game_over = True
                if player1.health > player2.health:
                    winner = 1
                elif player2.health > player1.health:
                    winner = 2
                else:
                    winner = 0
        
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
        
        # показва нивото горе в средата
        lvl_text = font_small.render(f"{level_name}  |  ⏱ {time_left}s", True, YELLOW)
        window.blit(lvl_text, (800//2 - lvl_text.get_width()//2, 20))

        
        if show_controls and not game_over:
            control_bg = pygame.Surface((550, 200))
            control_bg.set_alpha(200)
            control_bg.fill(BLACK)
            window.blit(control_bg, (125, 200))
            title_ctrl = font_medium.render("КОНТРОЛИ", True, YELLOW)
            p1_move = font_small.render("Играч 1: W/S движение, D стрелба →, R презареждане, L лазер/куршуми", True, BLUE)
            p2_move = font_small.render("Играч 2: ↑ ↓ движение, ← стрелба, Enter презареждане, K лазер/куршуми", True, RED)
            window.blit(title_ctrl, (800//2 - title_ctrl.get_width()//2, 215))
            window.blit(p1_move,    (800//2 - p1_move.get_width()//2, 265))
            window.blit(p2_move,    (800//2 - p2_move.get_width()//2, 305))
        
        if game_over:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            window.blit(overlay, (0, 0))
            winner_color = BLUE if winner == 1 else RED
            if winner == 0:
                 winner_text = font_big.render("РАВЕНСТВО!", True, YELLOW)
            else:
                winner_text = font_big.render(f"ИГРАЧ {winner} ПЕЧЕЛИ!", True, winner_color)
            window.blit(winner_text, (800//2 - winner_text.get_width()//2, 250))
            restart = font_medium.render("ESC за изход", True, WHITE)
            window.blit(restart, (800//2 - restart.get_width()//2, 350))
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()