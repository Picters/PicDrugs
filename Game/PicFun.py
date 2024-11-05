import pygame
import sys
import random
import math

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

        self.background_music = load_sound('./music/fun.mp3')
        self.background_music.set_volume(0.1)  # Установить громкость фоновой музыки на 0.1
        self.background_music.play(-1)

        # Загрузка голосовых фраз
        self.voice_sounds = []
        for i in range(1, 6):  # Удален voice6
            voice_sound = load_sound(f'./music/voice{i}.mp3')
            voice_sound.set_volume(1.0)  # Установить громкость на 100%
            self.voice_sounds.append(voice_sound)

        # Загрузка звука "grab"
        self.grab_sound = load_sound('./music/grab.mp3')
        self.grab_sound.set_volume(1.0)  # Установить громкость на 100%
        self.grab_sound_channel = None  # Канал для воспроизведения grab_sound

        # Загрузка звука "scream"
        self.scream_sound = load_sound('./music/scream.mp3')
        self.scream_sound.set_volume(1.0)
        self.scream_sound_channel = None  # Канал для воспроизведения scream_sound

        # Загрузка изображения мусорки
        self.trash_image = load_image('./png/trash.png')
        self.trash_rect = self.trash_image.get_rect(topright=(SCREEN_WIDTH, 0))

        # Персонаж
        self.kira_rect = self.kira_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - self.kira_image.get_height() // 2))
        self.kira_speed = 5
        self.kira_vel_x = random.choice([-self.kira_speed, self.kira_speed])
        self.kira_vel_y = 0
        self.kira_angle = 0  # Угол поворота персонажа
        self.kira_angular_velocity = 0
        self.gravity = 0.5
        self.is_dragged = False

        # Таймер для голосовых фраз
        self.voice_timer = pygame.time.get_ticks()

        # Состояние игры
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = 'menu'

        # FPS настройки
        self.fps = 60  # Текущий FPS

        # Цвета для градиента
        self.gradient_surface = self.create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (30, 30, 30), (70, 70, 70))

        # Создаем кнопки главного меню с современным дизайном
        self.create_menu_buttons()

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
                elif self.exit_button.collidepoint(event.pos):
                    self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def menu_draw(self):
        SCREEN.blit(self.gradient_surface, (0, 0))

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.kira_rect.collidepoint(event.pos):
                    self.is_dragged = True
                    self.mouse_offset = pygame.math.Vector2(self.kira_rect.center) - pygame.math.Vector2(event.pos)
                    self.kira_vel_x = 0
                    self.kira_vel_y = 0
                    self.kira_angular_velocity = 0
                    # Начать воспроизведение grab.mp3 циклично
                    self.grab_sound_channel = self.grab_sound.play(-1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_dragged:
                    self.is_dragged = False
                    # Остановить воспроизведение grab.mp3
                    if self.grab_sound_channel is not None:
                        self.grab_sound_channel.stop()
                        self.grab_sound_channel = None
                    # Проверить, отпущен ли персонаж над мусоркой
                    if self.kira_rect.colliderect(self.trash_rect):
                        # Остановить фоновую музыку
                        self.background_music.stop()
                        # Залить экран черным
                        SCREEN.fill((0, 0, 0))
                        pygame.display.flip()
                        # Проиграть scream.mp3 с плавным затуханием
                        self.scream_sound_channel = self.scream_sound.play()
                        # Плавное затухание крика
                        for volume in range(100, -1, -1):
                            self.scream_sound.set_volume(volume / 100.0)
                            pygame.time.delay(50)  # Настроить для желаемой скорости затухания
                        # Остановить звук
                        self.scream_sound_channel.stop()
                        pygame.time.delay(500)  # Небольшая пауза перед выходом
                        pygame.quit()
                        sys.exit()
                    else:
                        # Если не над мусоркой, продолжить обычное поведение
                        self.kira_vel_x = random.choice([-self.kira_speed, self.kira_speed])
                        self.kira_vel_y = -10
                        self.kira_angular_velocity = random.uniform(-5, 5)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'

    def game_update(self):
        current_time = pygame.time.get_ticks()
        if not self.is_dragged:
            if current_time - self.voice_timer >= 10000:  # 10 секунд
                self.voice_timer = current_time
                voice_sound = random.choice(self.voice_sounds)
                voice_sound.play()

        if self.is_dragged:
            # Перетаскивание персонажа мышью с вращением
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_pos = pygame.math.Vector2(mouse_x, mouse_y) + self.mouse_offset
            self.kira_rect.center = new_pos
            # Вращение персонажа при перетаскивании
            self.kira_angular_velocity += 0.1  # Можно настроить чувствительность вращения
            self.kira_angle += self.kira_angular_velocity

            # Проверка наведения на мусорку
            if self.kira_rect.colliderect(self.trash_rect):
                # Если scream.mp3 не воспроизводится, начать воспроизведение
                if self.scream_sound_channel is None or not self.scream_sound_channel.get_busy():
                    self.scream_sound_channel = self.scream_sound.play(-1)
            else:
                # Если персонаж не над мусоркой, остановить scream.mp3
                if self.scream_sound_channel is not None and self.scream_sound_channel.get_busy():
                    self.scream_sound_channel.stop()
        else:
            # Убедиться, что scream.mp3 остановлен, если персонаж не перетаскивается
            if self.scream_sound_channel is not None and self.scream_sound_channel.get_busy():
                self.scream_sound_channel.stop()

            # Автономное движение
            self.kira_vel_y += self.gravity
            self.kira_rect.y += self.kira_vel_y

            self.kira_rect.x += self.kira_vel_x

            # Вращение персонажа из-за гравитации
            self.kira_angular_velocity += self.kira_vel_x * 0.01
            self.kira_angular_velocity *= 0.99  # Сопротивление вращению
            self.kira_angle += self.kira_angular_velocity

            # Изменение направления при достижении границ
            if self.kira_rect.left <= 0:
                self.kira_rect.left = 0
                self.kira_vel_x *= -1
            if self.kira_rect.right >= SCREEN_WIDTH:
                self.kira_rect.right = SCREEN_WIDTH
                self.kira_vel_x *= -1

            if self.kira_rect.top <= 0:
                self.kira_rect.top = 0
                self.kira_vel_y *= -1

            if self.kira_rect.bottom >= SCREEN_HEIGHT:
                self.kira_rect.bottom = SCREEN_HEIGHT
                self.kira_vel_y = -self.kira_vel_y * 0.8  # Потеря энергии при отскоке
                if abs(self.kira_vel_y) < 1:
                    self.kira_vel_y = 0

    def game_draw(self):
        SCREEN.blit(self.gradient_surface, (0, 0))
        # Отрисовка мусорки
        SCREEN.blit(self.trash_image, self.trash_rect)

        # Поворот персонажа
        rotated_image = pygame.transform.rotate(self.kira_image, self.kira_angle)
        new_rect = rotated_image.get_rect(center=self.kira_rect.center)
        SCREEN.blit(rotated_image, new_rect)

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
