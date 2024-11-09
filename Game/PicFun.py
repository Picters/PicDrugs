import pygame
import sys
import os
import random
import math

# Инициализация Pygame
pygame.init()

# Получение разрешения экрана и установка полноэкранного режима
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("PicDrugs")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Часы для контроля FPS
clock = pygame.time.Clock()
FPS = 60

# Шрифты
font_size_title = int(HEIGHT * 0.1)  # Размер шрифта для заставки
font_title = pygame.font.SysFont(None, font_size_title)
font_size_info = int(HEIGHT * 0.025)  # Размер шрифта для информации
font = pygame.font.SysFont(None, font_size_info)

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y, align="center"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "center":
        textrect.center = (x, y)
    elif align == "topleft":
        textrect.topleft = (x, y)
    elif align == "topright":
        textrect.topright = (x, y)
    surface.blit(textobj, textrect)

# Функция для отображения заставки
def splash_screen():
    screen.fill(BLACK)
    draw_text("PicDrugs", font_title, WHITE, screen, WIDTH // 2, HEIGHT // 2, align="center")
    pygame.display.flip()
    pygame.time.delay(3000)  # Задержка 3 секунды

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

# Класс для эффектов
class Effect:
    def __init__(self, name, effect_func):
        self.name = name
        self.effect_func = effect_func

# Эффект кокаина
def cocaine_effect(screen, intensity):
    # Резкие мигания между красным и синим
    overlay_color = RED if random.randint(0, 1) else BLUE
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((*overlay_color, 100))
    screen.blit(overlay, (0, 0))

    # Резкое дрожание
    shake_amplitude = 15
    dx = random.randint(-shake_amplitude, shake_amplitude)
    dy = random.randint(-shake_amplitude, shake_amplitude)
    screen.blit(background_image, (dx, dy))

# Эффект марихуаны
def weed_effect(screen, intensity):
    # Зеленый тон с плавными изменениями
    overlay_color = GREEN
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    alpha_variation = random.randint(-10, 10)
    alpha = max(0, min(255, 70 + alpha_variation))  # Небольшие колебания альфа
    overlay.fill((*overlay_color, alpha))
    screen.blit(overlay, (0, 0))

    # Плавное дрожание
    shake_amplitude = 5
    shake_frequency = 120
    dx = int(shake_amplitude * math.sin((intensity / shake_frequency) * math.pi * 2))
    dy = int(shake_amplitude * math.sin((intensity / shake_frequency) * math.pi * 2))
    screen.blit(background_image, (dx, dy))

# Эффект ЛСД
def lsd_effect(screen, intensity):
    # Резкие цветовые изменения
    shift_r = random.randint(-30, 30)
    shift_g = random.randint(-15, 15)
    shift_b = random.randint(-30, 30)

    # Создание цветового сдвига
    colored_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            try:
                r, g, b = background_image.get_at((x, y))[:3]
            except IndexError:
                r, g, b = 0, 0, 0
            r = max(0, min(255, r + shift_r))
            g = max(0, min(255, g + shift_g))
            b = max(0, min(255, b + shift_b))
            pygame.draw.rect(colored_overlay, (r, g, b, 50), (x, y, 20, 20))
    screen.blit(colored_overlay, (0, 0))

    # Абстрактные узоры
    pattern_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for _ in range(30):
        radius = random.randint(5, 20)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 100)
        pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        pygame.draw.circle(pattern_surface, color, pos, radius)
    screen.blit(pattern_surface, (0, 0))

    # Резкое дрожание
    shake_amplitude = 10
    dx = random.randint(-shake_amplitude, shake_amplitude)
    dy = random.randint(-shake_amplitude, shake_amplitude)
    screen.blit(background_image, (dx, dy))

# Эффект экстази (MDMA)
def ecstasy_effect(screen, intensity):
    # Яркие мигания с разными цветами
    colors = [YELLOW, PURPLE, CYAN, ORANGE]
    overlay_color = random.choice(colors)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((*overlay_color, 120))
    screen.blit(overlay, (0, 0))

    # Пульсирующее мерцание
    pulse = int(50 * math.sin(intensity / 30))
    shake_amplitude = 10
    dx = shake_amplitude * math.sin((intensity / 60) * math.pi * 2) + pulse
    dy = shake_amplitude * math.sin((intensity / 60) * math.pi * 2) + pulse
    dx = int(dx)
    dy = int(dy)
    screen.blit(background_image, (dx, dy))

# Эффект метамфетамина
def methamphetamine_effect(screen, intensity):
    # Интенсивный красный оверлей с бликами
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((*RED, 150))
    screen.blit(overlay, (0, 0))

    # Быстрое дрожание
    shake_amplitude = 20
    dx = random.randint(-shake_amplitude, shake_amplitude)
    dy = random.randint(-shake_amplitude, shake_amplitude)
    screen.blit(background_image, (dx, dy))

    # Добавление бликов
    for _ in range(50):
        radius = random.randint(1, 3)
        color = (255, 255, 255, random.randint(50, 150))
        pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        pygame.draw.circle(screen, color, pos, radius)

# Эффект героина
def heroin_effect(screen, intensity):
    # Темный, мутный оверлей с размытием
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 180))
    screen.blit(overlay, (0, 0))

    # Медленное дрожание
    shake_amplitude = 8
    shake_frequency = 80
    dx = int(shake_amplitude * math.sin((intensity / shake_frequency) * math.pi * 2))
    dy = int(shake_amplitude * math.sin((intensity / shake_frequency) * math.pi * 2))
    screen.blit(background_image, (dx, dy))

    # Добавление мягкого свечения
    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for _ in range(100):
        radius = random.randint(2, 5)
        color = (200, 200, 200, 30)
        pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        pygame.draw.circle(glow, color, pos, radius)
    screen.blit(glow, (0, 0))

# Список доступных эффектов
effects = {
    "Нормальное зрение": None,
    "Кокаин": Effect("Кокаин", cocaine_effect),
    "Марихуана": Effect("Марихуана", weed_effect),
    "ЛСД": Effect("ЛСД", lsd_effect),
    "Экстази": Effect("Экстази", ecstasy_effect),
    "Метамфетамин": Effect("Метамфетамин", methamphetamine_effect),
    "Героин": Effect("Героин", heroin_effect),
}

# Основной цикл приложения
def main():
    splash_screen()
    active_effect = None
    current_effect_name = "Нормальное зрение"
    intensity = 0  # Для плавных эффектов

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Обработка нажатий клавиш для выбора эффекта
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    active_effect = effects["Кокаин"]
                    current_effect_name = active_effect.name if active_effect else "Нормальное зрение"
                elif event.key == pygame.K_2:
                    active_effect = effects["Марихуана"]
                    current_effect_name = active_effect.name if active_effect else "Нормальное зрение"
                elif event.key == pygame.K_3:
                    active_effect = effects["ЛСД"]
                    current_effect_name = active_effect.name if active_effect else "Нормальное зрение"
                elif event.key == pygame.K_4:
                    active_effect = effects["Экстази"]
                    current_effect_name = active_effect.name if active_effect else "Нормальное зрение"
                elif event.key == pygame.K_5:
                    active_effect = effects["Метамфетамин"]
                    current_effect_name = active_effect.name if active_effect else "Нормальное зрение"
                elif event.key == pygame.K_6:
                    active_effect = effects["Героин"]
                    current_effect_name = active_effect.name if active_effect else "Нормальное зрение"
                elif event.key == pygame.K_0:
                    active_effect = effects["Нормальное зрение"]
                    current_effect_name = "Нормальное зрение"

        # Отображение изображения фона
        screen.blit(background_image, (0, 0))

        # Применение активного эффекта
        if active_effect:
            active_effect.effect_func(screen, intensity)
            intensity += 1  # Увеличение интенсивности для анимации
        else:
            intensity = 0  # Сброс интенсивности

        # Отображение списка клавиш и их назначений (верхний левый угол)
        key_list = [
            "1: Кокаин",
            "2: Марихуана",
            "3: ЛСД",
            "4: Экстази",
            "5: Метамфетамин",
            "6: Героин",
            "0: Нормальное зрение",
            "Esc: Выход"
        ]
        for idx, key in enumerate(key_list):
            draw_text(key, font, BLACK, screen, 20, 20 + idx * (font_size_info + 5), align="topleft")

        # Отображение текущего эффекта (верхний правый угол)
        draw_text(f"Текущий эффект: {current_effect_name}", font, BLACK, screen, WIDTH - 20, 20, align="topright")

        # Отображение версии приложения (нижний левый угол)
        draw_text("Версия 1.5", font, BLACK, screen, 20, HEIGHT - 20, align="topleft")

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
