import pygame
import sys

# Константы
SCREEN_TITLE = "Современная Игра"

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
        image = pygame.image.load(path)
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
        self.background_music.set_volume(0.5)
        self.background_music.play(-1)

        # Персонаж
        self.kira_rect = self.kira_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - self.kira_image.get_height() // 2))
        self.kira_speed = 5
        self.kira_vel_y = 0
        self.gravity = 0.5
        self.is_jumping = False

        # Состояние игры
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = 'menu'

        # FPS настройки
        self.fps_options = [5, 30, 60, 90, 120, 144, 180, 240, 480]
        self.fps = 60  # Текущий FPS
        self.show_fps_menu = False  # Показывать ли выпадающее меню FPS

        # Цвета для градиента
        self.gradient_surface = self.create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (30, 30, 30), (70, 70, 70))

        # Создаем кнопки главного меню с современным дизайном
        self.create_menu_buttons()

    def create_gradient_surface(self, width, height, start_color, end_color):
        """Создает поверхность с вертикальным градиентом."""
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
        """Создает кнопки главного меню с современным дизайном."""
        self.play_button = pygame.Rect(0, 0, 250, 80)
        self.play_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        self.settings_button = pygame.Rect(0, 0, 300, 50)
        self.settings_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

        self.exit_button = pygame.Rect(0, 0, 250, 80)
        self.exit_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)

        # Шрифт для меню
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
                elif self.settings_button.collidepoint(event.pos):
                    self.show_fps_menu = not self.show_fps_menu
                elif self.exit_button.collidepoint(event.pos):
                    self.running = False
                elif self.show_fps_menu:
                    # Проверяем, на какую опцию FPS нажал пользователь
                    for idx, option in enumerate(self.fps_options):
                        option_rect = pygame.Rect(
                            self.settings_button.left,
                            self.settings_button.bottom + idx * 40,
                            self.settings_button.width,
                            40
                        )
                        if option_rect.collidepoint(event.pos):
                            self.fps = option
                            self.show_fps_menu = False
                            break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def menu_draw(self):
        SCREEN.blit(self.gradient_surface, (0, 0))

        # Отрисовка заголовка игры
        title_text = self.font.render("Моя Современная Игра", True, (200, 200, 200))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250))
        SCREEN.blit(title_text, title_rect)

        # Отрисовка кнопок
        pygame.draw.rect(SCREEN, (50, 150, 200), self.play_button, border_radius=15)
        pygame.draw.rect(SCREEN, (50, 50, 50), self.settings_button, border_radius=10)
        pygame.draw.rect(SCREEN, (200, 50, 50), self.exit_button, border_radius=15)

        play_text = self.menu_font.render("Играть", True, (255, 255, 255))
        settings_text = self.menu_font.render(f"Кадры в секунду - {self.fps}", True, (255, 255, 255))
        exit_text = self.menu_font.render("Выйти", True, (255, 255, 255))

        play_text_rect = play_text.get_rect(center=self.play_button.center)
        settings_text_rect = settings_text.get_rect(center=self.settings_button.center)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)

        SCREEN.blit(play_text, play_text_rect)
        SCREEN.blit(settings_text, settings_text_rect)
        SCREEN.blit(exit_text, exit_text_rect)

        # Отрисовка выпадающего меню FPS
        if self.show_fps_menu:
            for idx, option in enumerate(self.fps_options):
                option_rect = pygame.Rect(
                    self.settings_button.left,
                    self.settings_button.bottom + idx * 40,
                    self.settings_button.width,
                    40
                )
                pygame.draw.rect(SCREEN, (70, 70, 70), option_rect)
                fps_option_text = self.menu_font.render(f"{option}", True, (255, 255, 255))
                fps_option_rect = fps_option_text.get_rect(center=option_rect.center)
                SCREEN.blit(fps_option_text, fps_option_rect)

        pygame.display.flip()

    def game_events(self):
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
                if event.key == pygame.K_SPACE and not self.is_jumping:
                    self.is_jumping = True
                    self.kira_vel_y = -10

    def game_update(self):
        # Обновление позиции персонажа
        if self.keys[pygame.K_a]:
            self.kira_rect.x -= self.kira_speed
        if self.keys[pygame.K_d]:
            self.kira_rect.x += self.kira_speed

        # Обработка прыжка и гравитации
        self.kira_vel_y += self.gravity
        self.kira_rect.y += self.kira_vel_y

        if self.kira_rect.bottom >= SCREEN_HEIGHT:
            self.kira_rect.bottom = SCREEN_HEIGHT
            self.is_jumping = False
            self.kira_vel_y = 0

        # Ограничение перемещения персонажа по границам экрана
        if self.kira_rect.left < 0:
            self.kira_rect.left = 0
        if self.kira_rect.right > SCREEN_WIDTH:
            self.kira_rect.right = SCREEN_WIDTH

    def game_draw(self):
        SCREEN.blit(self.gradient_surface, (0, 0))
        SCREEN.blit(self.kira_image, self.kira_rect)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
