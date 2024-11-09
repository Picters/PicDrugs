import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Демонстрация эффектов наркотических веществ на зрение")

# Загрузка изображения фона
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
background_path = os.path.join(ASSETS_DIR, 'room.jpg')

try:
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Не удалось загрузить изображение фона: {e}")
    pygame.quit()
    sys.exit()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Часы для контроля FPS
clock = pygame.time.Clock()
FPS = 60

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Класс для эффектов
class Effect:
    def __init__(self, name, duration, effect_func):
        self.name = name
        self.duration = duration
        self.effect_func = effect_func

# Эффект кокаина
def cocaine_effect(screen, intensity):
    # Мигание между красным и синим
    if intensity % 10 < 5:
        overlay_color = (255, 0, 0)  # Красный
    else:
        overlay_color = (0, 0, 255)  # Синий
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(overlay_color)
    screen.blit(overlay, (0, 0))
    
    # Дрожание
    shake_offset = 5
    dx = (pygame.time.get_ticks() % (2 * shake_offset)) - shake_offset
    dy = (pygame.time.get_ticks() % (2 * shake_offset)) - shake_offset
    temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surface.fill((255, 255, 255, 0))
    font = pygame.font.SysFont(None, 36)
    draw_text("Эффект кокаина: Изменение зрения", font, BLACK, temp_surface, WIDTH // 2 + dx, HEIGHT // 2 + dy)
    screen.blit(temp_surface, (dx, dy))

# Эффект марихуаны
def weed_effect(screen, intensity):
    # Добавление зеленого тона и легкое дрожание
    overlay_color = (0, 255, 0)  # Зеленый
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(50)
    overlay.fill(overlay_color)
    screen.blit(overlay, (0, 0))
    
    # Легкое дрожание
    shake_offset = 2
    dx = (pygame.time.get_ticks() % (2 * shake_offset)) - shake_offset
    dy = (pygame.time.get_ticks() % (2 * shake_offset)) - shake_offset
    temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surface.fill((255, 255, 255, 0))
    font = pygame.font.SysFont(None, 36)
    draw_text("Эффект марихуаны: Изменение восприятия", font, BLACK, temp_surface, WIDTH // 2 + dx, HEIGHT // 2 + dy)
    screen.blit(temp_surface, (dx, dy))

# Эффект ЛСД
def lsd_effect(screen, intensity):
    # Изменение цветов и абстрактные узоры
    for i in range(0, WIDTH, 50):
        for j in range(0, HEIGHT, 50):
            color = ((i + intensity) % 255, (j + intensity) % 255, (i + j) % 255)
            pygame.draw.rect(screen, color, (i, j, 50, 50))
    
    # Добавление текста
    font = pygame.font.SysFont(None, 36)
    draw_text("Эффект ЛСД: Галлюцинации и искажения", font, BLACK, screen, WIDTH // 2, HEIGHT // 2)

# Список доступных эффектов
effects = {
    "Нормальное зрение": None,
    "Кокаин": Effect("Кокаин", 300, cocaine_effect),
    "Марихуана": Effect("Марихуана", 300, weed_effect),
    "ЛСД": Effect("ЛСД", 300, lsd_effect),
}

# Основной цикл приложения
def main():
    font = pygame.font.SysFont(None, 36)
    active_effect = None
    effect_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Обработка нажатий клавиш для выбора эффекта
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    active_effect = effects["Кокаин"]
                    effect_timer = active_effect.duration if active_effect else 0
                elif event.key == pygame.K_2:
                    active_effect = effects["Марихуана"]
                    effect_timer = active_effect.duration if active_effect else 0
                elif event.key == pygame.K_3:
                    active_effect = effects["ЛСД"]
                    effect_timer = active_effect.duration if active_effect else 0
                elif event.key == pygame.K_0:
                    active_effect = effects["Нормальное зрение"]
                    effect_timer = 0

        # Отображение изображения фона
        screen.blit(background_image, (0, 0))

        # Применение активного эффекта
        if active_effect and effect_timer > 0:
            active_effect.effect_func(screen, effect_timer)
            effect_timer -= 1
            if effect_timer <= 0:
                active_effect = None
        else:
            # Отображение статичного текста выбора
            draw_text("Выберите эффект:", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
            draw_text("1: Кокаин", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("2: Марихуана", font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
            draw_text("3: ЛСД", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
            draw_text("0: Нормальное зрение", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 100)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
