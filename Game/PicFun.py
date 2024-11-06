import pygame
import sys
import random
import os

SCREEN_TITLE = "PicFun"

pygame.init()

infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

CHARACTERS_DIR = 'characters'
IMAGES_DIR = 'images'
SFX_DIR = 'sfx'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_image(path):
    try:
        image = pygame.image.load(resource_path(path)).convert_alpha()
        return image
    except pygame.error:
        print(f"Не удалось загрузить изображение: {path}")
        sys.exit()

def load_sound(path):
    try:
        sound = pygame.mixer.Sound(resource_path(path))
        return sound
    except pygame.error:
        print(f"Не удалось загрузить звук: {path}")
        sys.exit()

class Game:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.kira_image_original = load_image(os.path.join(CHARACTERS_DIR, 'Kira.png'))
        self.kira_image = pygame.transform.scale(self.kira_image_original, (150, 150))
        self.background_music = load_sound(os.path.join(SFX_DIR, 'fun.mp3'))
        self.background_music.set_volume(0.1)
        self.background_music.play(-1)
        self.grab_sound = load_sound(os.path.join(SFX_DIR, 'grab.mp3'))
        self.grab_sound.set_volume(1.0)
        self.scream_sound = load_sound(os.path.join(SFX_DIR, 'scream.mp3'))
        self.scream_sound.set_volume(1.0)
        self.voice_sounds = [load_sound(os.path.join(SFX_DIR, f'voice{i}.mp3')) for i in range(1, 6)]
        for voice in self.voice_sounds:
            voice.set_volume(1.0)
        self.trash_image_original = load_image(os.path.join(IMAGES_DIR, 'trash.png'))
        self.trash_image = pygame.transform.scale(self.trash_image_original, (30, 30))
        self.trash_rect = self.trash_image.get_rect(topleft=(10, 10))
        self.kira_rect = self.kira_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - self.kira_image.get_height() // 2))
        self.kira_speed = 3
        self.kira_vel_x = random.choice([-self.kira_speed, self.kira_speed])
        self.kira_vel_y = 0
        self.gravity = 0.5
        self.is_dragged = False
        self.voice_channel = pygame.mixer.Channel(1)
        self.grab_channel = pygame.mixer.Channel(2)
        self.scream_channel = pygame.mixer.Channel(3)
        self.voiserubka_sound = load_sound(os.path.join(SFX_DIR, 'voiserubka.mp3'))
        self.voiserubka_channel = pygame.mixer.Channel(4)
        self.move_timer = pygame.time.get_ticks()
        self.voice_timer = pygame.time.get_ticks()
        self.jump_timer = pygame.time.get_ticks()
        self.prev_mouse_pos = None
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = 'menu'
        self.gradient_surface = self.create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (30, 30, 30), (70, 70, 70))
        self.fps = 60
        self.create_menu_buttons()
        self.arrow_image = load_image(os.path.join(IMAGES_DIR, 'arrow.png'))
        self.arrow_image = pygame.transform.scale(self.arrow_image, (40, 40))
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_rect.topright = (SCREEN_WIDTH - 10, 10)
        self.panel_width = 300
        self.panel_height = SCREEN_HEIGHT
        self.panel_color = (100, 100, 100)
        self.panel_surface = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        self.panel_rect = self.panel_surface.get_rect()
        self.panel_rect.left = SCREEN_WIDTH
        self.panel_open = False
        self.panel_animating = False
        self.panel_animation_speed = 20
        self.panel_font = pygame.font.Font(None, 50)
        self.panel_title = self.panel_font.render("Tools", True, (255, 255, 255))
        self.panel_title_rect = self.panel_title.get_rect(center=(self.panel_width // 2, 30))
        self.rubka_image_original = load_image(os.path.join(IMAGES_DIR, 'rubka.png'))
        self.rubka_image = pygame.transform.scale(self.rubka_image_original, (50, 50))
        self.rubka_square_size = 70
        self.rubka_square_color = (255, 165, 0)
        self.rubka_square_rect = pygame.Rect(20, 80, self.rubka_square_size, self.rubka_square_size)
        self.grinder_visible = False
        self.grinder_image_original = load_image(os.path.join(IMAGES_DIR, 'rubka.png'))
        self.grinder_image = pygame.transform.scale(self.grinder_image_original, (self.kira_image.get_width() * 2, self.kira_image.get_height() * 2))
        self.grinder_rect = self.grinder_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    
    def create_gradient_surface(self, width, height, start_color, end_color):
        gradient = pygame.Surface((width, height))
        for y in range(height):
            ratio = y / height
            color = (
                int(start_color[0] * (1 - ratio) + end_color[0] * ratio),
                int(start_color[1] * (1 - ratio) + end_color[1] * ratio),
                int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            )
            pygame.draw.line(gradient, color, (0, y), (width, y))
        return gradient
    
    def create_menu_buttons(self):
        self.play_button = pygame.Rect(0, 0, 250, 80)
        self.play_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.exit_button = pygame.Rect(0, 0, 250, 80)
        self.exit_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
        self.menu_font = pygame.font.Font(None, 60)
    
    def toggle_panel(self):
        if not self.panel_animating:
            self.panel_animating = True
            self.panel_open = not self.panel_open
    
    def run(self):
        while self.running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_draw()
            elif self.state == 'game':
                self.game_events()
                self.game_update()
                self.game_draw()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()
    
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    self.state = 'game'
                elif self.exit_button.collidepoint(event.pos):
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def menu_draw(self):
        SCREEN.fill((0, 0, 0))
        title_text = self.font.render("PicFun", True, (200, 200, 200))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        SCREEN.blit(title_text, title_rect)
        pygame.draw.rect(SCREEN, (50, 150, 200), self.play_button, border_radius=15)
        pygame.draw.rect(SCREEN, (200, 50, 50), self.exit_button, border_radius=15)
        play_text = self.menu_font.render("Играть", True, (255, 255, 255))
        exit_text = self.menu_font.render("Выйти", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=self.play_button.center)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)
        SCREEN.blit(play_text, play_text_rect)
        SCREEN.blit(exit_text, exit_text_rect)
        pygame.display.flip()
    
    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT + 1:
                self.scream_channel.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.kira_rect.collidepoint(event.pos):
                    if not self.grinder_visible:
                        self.is_dragged = True
                        self.mouse_offset = pygame.math.Vector2(self.kira_rect.center) - pygame.math.Vector2(event.pos)
                        self.kira_vel_x = 0
                        self.kira_vel_y = 0
                        self.grab_channel.play(self.grab_sound, loops=-1)
                elif self.arrow_rect.collidepoint(event.pos):
                    self.toggle_panel()
                elif self.panel_open:
                    relative_pos = (event.pos[0] - self.panel_rect.x, event.pos[1] - self.panel_rect.y)
                    if self.rubka_square_rect.collidepoint(relative_pos):
                        self.grinder_visible = not self.grinder_visible
                        if self.grinder_visible:
                            self.voiserubka_channel.play(self.voiserubka_sound, loops=-1)
                            self.background_music.stop()
                            self.grab_channel.stop()
                            self.voice_channel.stop()
                            self.scream_channel.stop()
                        else:
                            self.voiserubka_channel.stop()
                            self.background_music.play(-1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_dragged:
                    self.is_dragged = False
                    self.grab_channel.stop()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    current_mouse_pos = pygame.math.Vector2(mouse_x, mouse_y)
                    if self.prev_mouse_pos is not None:
                        delta = current_mouse_pos - self.prev_mouse_pos
                        self.kira_vel_x = delta.x * 0.2
                        self.kira_vel_y = delta.y * 0.2
                    self.prev_mouse_pos = None
                    if self.kira_rect.colliderect(self.trash_rect):
                        self.scream_channel.play(self.scream_sound)
                        self.background_music.stop()
                        self.voice_channel.stop()
                        self.grab_channel.stop()
                        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                        fade_surface.fill((0, 0, 0))
                        for alpha in range(0, 256, 5):
                            fade_surface.set_alpha(alpha)
                            SCREEN.blit(self.gradient_surface, (0, 0))
                            SCREEN.blit(self.trash_image, self.trash_rect)
                            SCREEN.blit(self.kira_image, self.kira_rect)
                            SCREEN.blit(fade_surface, (0, 0))
                            pygame.display.flip()
                            pygame.time.delay(30)
                        pygame.mixer.stop()
                        for volume in range(100, -1, -1):
                            self.scream_channel.set_volume(volume / 100.0)
                            pygame.time.delay(50)
                        self.scream_channel.stop()
                        pygame.time.delay(500)
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
    
    def game_update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.voice_timer >= 10000:
            self.voice_timer = current_time
            if not self.voice_channel.get_busy() and not self.grinder_visible:
                voice_sound = random.choice(self.voice_sounds)
                self.voice_channel.play(voice_sound)
        if self.is_dragged:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_pos = pygame.math.Vector2(mouse_x, mouse_y) + self.mouse_offset
            self.kira_rect.center = new_pos
            self.prev_mouse_pos = pygame.math.Vector2(mouse_x, mouse_y)
            if self.grinder_visible and self.kira_rect.colliderect(self.grinder_rect):
                if self.kira_vel_x > 0:
                    self.kira_rect.right = self.grinder_rect.left
                elif self.kira_vel_x < 0:
                    self.kira_rect.left = self.grinder_rect.right
                if self.kira_vel_y > 0:
                    self.kira_rect.bottom = self.grinder_rect.top
                    self.kira_vel_y = 0
                elif self.kira_vel_y < 0:
                    self.kira_rect.top = self.grinder_rect.bottom
                    self.kira_vel_y = 0
        else:
            self.kira_vel_x *= 0.98
            self.kira_vel_y *= 0.98
            self.kira_vel_y += self.gravity
            self.kira_rect.y += self.kira_vel_y
            self.kira_rect.x += self.kira_vel_x
            if self.grinder_visible and self.kira_rect.colliderect(self.grinder_rect):
                if self.kira_vel_x > 0:
                    self.kira_rect.right = self.grinder_rect.left
                    self.kira_vel_x = 0
                elif self.kira_vel_x < 0:
                    self.kira_rect.left = self.grinder_rect.right
                    self.kira_vel_x = 0
                if self.kira_vel_y > 0:
                    self.kira_rect.bottom = self.grinder_rect.top
                    self.kira_vel_y = 0
                elif self.kira_vel_y < 0:
                    self.kira_rect.top = self.grinder_rect.bottom
                    self.kira_vel_y = 0
            if self.kira_rect.left <= 0:
                self.kira_rect.left = 0
                self.kira_vel_x *= -1
            if self.kira_rect.right >= SCREEN_WIDTH:
                self.kira_rect.right = SCREEN_WIDTH
                self.kira_vel_x *= -1
            if self.kira_rect.bottom >= SCREEN_HEIGHT:
                self.kira_rect.bottom = SCREEN_HEIGHT
                self.kira_vel_y = -self.kira_vel_y * 0.5
                if abs(self.kira_vel_y) < 1:
                    self.kira_vel_y = 0
            if current_time - self.move_timer >= random.randint(2000, 5000):
                self.move_timer = current_time
                self.kira_vel_x = random.choice([-self.kira_speed, self.kira_speed])
            if current_time - self.jump_timer >= random.randint(3000, 7000):
                self.jump_timer = current_time
                if self.kira_rect.bottom >= SCREEN_HEIGHT:
                    self.kira_vel_y = -10
        if self.panel_animating:
            if self.panel_open:
                if self.panel_rect.left > SCREEN_WIDTH - self.panel_width:
                    self.panel_rect.x -= self.panel_animation_speed
                    if self.panel_rect.left <= SCREEN_WIDTH - self.panel_width:
                        self.panel_rect.left = SCREEN_WIDTH - self.panel_width
                        self.panel_animating = False
            else:
                if self.panel_rect.left < SCREEN_WIDTH:
                    self.panel_rect.x += self.panel_animation_speed
                    if self.panel_rect.left >= SCREEN_WIDTH:
                        self.panel_rect.left = SCREEN_WIDTH
                        self.panel_animating = False
            target_x = SCREEN_WIDTH - self.panel_width - 10 - self.arrow_rect.width if self.panel_open else SCREEN_WIDTH - 10 - self.arrow_rect.width
            current_x = self.arrow_rect.x
            if current_x < target_x:
                self.arrow_rect.x += min(self.panel_animation_speed, target_x - current_x)
            elif current_x > target_x:
                self.arrow_rect.x -= min(self.panel_animation_speed, current_x - target_x)
    
    def game_draw(self):
        SCREEN.blit(self.gradient_surface, (0, 0))
        SCREEN.blit(self.trash_image, self.trash_rect)
        SCREEN.blit(self.kira_image, self.kira_rect)
        self.panel_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.panel_surface, self.panel_color, (0, 0, self.panel_width, self.panel_height), border_radius=20)
        self.panel_surface.blit(self.panel_title, self.panel_title_rect)
        pygame.draw.rect(self.panel_surface, self.rubka_square_color, self.rubka_square_rect)
        if self.grinder_visible:
            pygame.draw.rect(self.panel_surface, (0, 0, 255), self.rubka_square_rect, 3)
        else:
            pygame.draw.rect(self.panel_surface, (0, 0, 0), self.rubka_square_rect, 3)
        rubka_x = self.rubka_square_rect.left + (self.rubka_square_rect.width - self.rubka_image.get_width()) // 2
        rubka_y = self.rubka_square_rect.top + (self.rubka_square_rect.height - self.rubka_image.get_height()) // 2
        self.panel_surface.blit(self.rubka_image, (rubka_x, rubka_y))
        if self.grinder_visible:
            SCREEN.blit(self.grinder_image, self.grinder_rect)
        SCREEN.blit(self.panel_surface, self.panel_rect)
        SCREEN.blit(self.arrow_image, self.arrow_rect)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
