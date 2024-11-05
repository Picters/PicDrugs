import pygame
import sys
import random

# Константы
SCREEN_TITLE = "PicFun"

# Инициализация Pygame
pygame.init()

# Получаем разрешение экрана
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Настройки экрана
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Загрузка ресурсов с проверкой ошибок
def load_image(path):
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить изображение: {path}")
        sys.exit()

def load_sound(path):
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error as e:
        print(f"Не удалось загрузить звук: {path}")
        sys.exit()

class Game:
    def __init__(self):
        # Шрифт
        self.font = pygame.font.Font(None, 74)

        # Загрузка ресурсов
        self.kira_image_original = load_image('./characters/Kira.png')
        self.kira_image = pygame.transform.scale(self.kira_image_original, (150, 150))

        # Увеличиваем размер henrybaby в два раза
        self.henrybaby_image_original = load_image('./characters/henrybaby.png')
        self.henrybaby_image = pygame.transform.scale(self.henrybaby_image_original, (60, 60))  # Размер 60x60 пикселей

        self.background_music = load_sound('./music/fun.mp3')
        self.background_music.set_volume(0.1)
        self.background_music.play(-1)

        # Загрузка звуков
        self.grab_sound = load_sound('./music/grab.mp3')
        self.grab_sound.set_volume(1.0)

        self.scream_sound = load_sound('./music/scream.mp3')
        self.scream_sound.set_volume(1.0)

        # Загрузка голосовых фраз
        self.voice_sounds = []
        for i in range(1, 6):
            voice_sound = load_sound(f'./music/voice{i}.mp3')
            voice_sound.set_volume(1.0)
            self.voice_sounds.append(voice_sound)

        # Загрузка и уменьшение изображения мусорки
        self.trash_image_original = load_image('./png/trash.png')
        self.trash_image = pygame.transform.scale(self.trash_image_original, (50, 50))
        self.trash_rect = self.trash_image.get_rect(topright=(SCREEN_WIDTH, 0))

        # Персонаж
        self.kira_rect = self.kira_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - self.kira_image.get_height() // 2))
        self.kira_speed = 3
        self.kira_vel_x = random.choice([-self.kira_speed, self.kira_speed])
        self.kira_vel_y = 0
        self.gravity = 0.5
        self.is_dragged = False

        # Создание каналов для звуков
        self.voice_channel = pygame.mixer.Channel(1)
        self.grab_channel = pygame.mixer.Channel(2)
        self.scream_channel = pygame.mixer.Channel(3)

        # Таймеры
        self.move_timer = pygame.time.get_ticks()
        self.voice_timer = pygame.time.get_ticks()
        self.jump_timer = pygame.time.get_ticks()  # Инициализация jump_timer

        # Инициализация переменной для хранения предыдущей позиции мыши
        self.prev_mouse_pos = None

        # Состояние игры
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = 'menu'

        # Список для henrybaby
        self.henrybabies = []

        # Флаг для генерации henrybaby бесконечно
        self.spawn_henrybabies = False

        # Цвета для градиента
        self.gradient_surface = self.create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (30, 30, 30), (70, 70, 70))

        # FPS настройки
        self.fps = 60

        # Создаем кнопки главного меню
        self.create_menu_buttons()

        # Красная кнопка
        self.red_button = pygame.Rect(10, 10, 20, 20)
        self.red_button_visible = False  # Флаг видимости красной кнопки

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
                    self.red_button_visible = True  # Делаем красную кнопку видимой
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

    def trigger_henrybabies(self):
        self.background_music.stop()  # Остановить фоновую музыку
        self.scream_channel.play(self.scream_sound)  # Проиграть scream.mp3
        self.spawn_henrybabies = True  # Начать бесконечное появление henrybabies

        # Ждем 2 секунды и затем выходим из игры
        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.USEREVENT + 1:
                # Останавливаем scream и выходим из игры
                self.scream_channel.stop()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.kira_rect.collidepoint(event.pos):
                    self.is_dragged = True
                    self.mouse_offset = pygame.math.Vector2(self.kira_rect.center) - pygame.math.Vector2(event.pos)
                    self.kira_vel_x = 0
                    self.kira_vel_y = 0
                    self.grab_channel.play(self.grab_sound, loops=-1)
                elif self.red_button_visible and self.red_button.collidepoint(event.pos):
                    self.trigger_henrybabies()  # Обработка нажатия на красную кнопку

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_dragged:
                    self.is_dragged = False
                    self.grab_channel.stop()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    current_mouse_pos = pygame.math.Vector2(mouse_x, mouse_y)
                    # Вычисление скоростей броска
                    if self.prev_mouse_pos is not None:
                        delta = current_mouse_pos - self.prev_mouse_pos
                        self.kira_vel_x = delta.x * 0.2
                        self.kira_vel_y = delta.y * 0.2
                    self.prev_mouse_pos = None
                    if self.kira_rect.colliderect(self.trash_rect):
                        self.background_music.stop()
                        self.voice_channel.stop()
                        self.grab_channel.stop()
                        # Затемнение экрана
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
                        # Остановить все звуки, кроме scream
                        pygame.mixer.stop()
                        self.scream_channel.play(self.scream_sound)
                        # Плавное затухание scream
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
                    self.red_button_visible = False  # Скрываем красную кнопку при возвращении в меню

    def game_update(self):
        current_time = pygame.time.get_ticks()

        # Проверка столкновения с мусоркой для проигрывания scream.mp3
        if self.kira_rect.colliderect(self.trash_rect):
            if not self.scream_channel.get_busy():
                self.scream_channel.play(self.scream_sound)
        else:
            if self.scream_channel.get_busy():
                self.scream_channel.stop()

        # Генерация henrybaby бесконечно
        if self.spawn_henrybabies:
            # Создаем нескольких henrybaby каждый кадр
            for _ in range(5):
                henry_rect = self.henrybaby_image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
                self.henrybabies.append(henry_rect)

        # Обновление позиции henrybaby
        for henry_rect in self.henrybabies:
            henry_rect.y += 2  # Движение вниз

        # Удаляем henrybaby, которые вышли за пределы экрана
        self.henrybabies = [henry_rect for henry_rect in self.henrybabies if henry_rect.y < SCREEN_HEIGHT]

        if current_time - self.voice_timer >= 10000:
            self.voice_timer = current_time
            if not self.voice_channel.get_busy():
                voice_sound = random.choice(self.voice_sounds)
                self.voice_channel.play(voice_sound)

        if self.is_dragged:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_pos = pygame.math.Vector2(mouse_x, mouse_y) + self.mouse_offset
            self.kira_rect.center = new_pos
            self.prev_mouse_pos = pygame.math.Vector2(mouse_x, mouse_y)
        else:
            # Физика замедления при броске
            self.kira_vel_x *= 0.98  # Коэффициент трения по горизонтали
            self.kira_vel_y *= 0.98  # Коэффициент трения по вертикали

            self.kira_vel_y += self.gravity
            self.kira_rect.y += self.kira_vel_y
            self.kira_rect.x += self.kira_vel_x

            # Изменение направления при достижении границ
            if self.kira_rect.left <= 0:
                self.kira_rect.left = 0
                self.kira_vel_x *= -1
            if self.kira_rect.right >= SCREEN_WIDTH:
                self.kira_rect.right = SCREEN_WIDTH
                self.kira_vel_x *= -1

            if self.kira_rect.bottom >= SCREEN_HEIGHT:
                self.kira_rect.bottom = SCREEN_HEIGHT
                self.kira_vel_y = -self.kira_vel_y * 0.5  # Потеря энергии при отскоке
                if abs(self.kira_vel_y) < 1:
                    self.kira_vel_y = 0

            # Автономное движение
            if current_time - self.move_timer >= random.randint(2000, 5000):
                self.move_timer = current_time
                self.kira_vel_x = random.choice([-self.kira_speed, self.kira_speed])

            # Автономный прыжок
            if current_time - self.jump_timer >= random.randint(3000, 7000):
                self.jump_timer = current_time
                if self.kira_rect.bottom >= SCREEN_HEIGHT:
                    self.kira_vel_y = -10

    def game_draw(self):
        SCREEN.blit(self.gradient_surface, (0, 0))
        SCREEN.blit(self.trash_image, self.trash_rect)
        SCREEN.blit(self.kira_image, self.kira_rect)

        # Отрисовка henrybaby
        for henry_rect in self.henrybabies:
            SCREEN.blit(self.henrybaby_image, henry_rect)

        # Рисуем красную кнопку, если она видима
        if self.red_button_visible:
            pygame.draw.rect(SCREEN, (255, 0, 0), self.red_button)

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
