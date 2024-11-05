import pygame
import sys

# Инициализация Pygame
pygame.init()

# Получаем разрешение экрана
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

# Настройки экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Моя Игра")

# Загрузка ресурсов
kira_image = pygame.transform.scale(pygame.image.load('./characters/Kira.png'), (50, 50))  # Измените размер по необходимости
background_music = pygame.mixer.Sound('./music/fun.mp3')
background_music.play(-1)  # Циклическое воспроизведение

# Цвета для градиента
color1 = (255, 0, 0)
color2 = (0, 0, 255)

# Персонаж
kira_x = screen_width // 2
kira_y = screen_height // 2
kira_speed = 5
jumping = False
jump_height = 10
jump_count = jump_height

# Шрифт
font = pygame.font.Font(None, 74)

# Главный цикл
def main_menu():
    while True:
        screen.fill((0, 0, 0))  # Чёрный фон

        # Создаем кнопки
        play_text = font.render("Играть", True, (255, 255, 255))
        exit_text = font.render("Выйти", True, (255, 255, 255))

        play_button_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        exit_button_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

        # Отрисовываем кнопки
        pygame.draw.rect(screen, (70, 130, 180), play_button_rect)
        pygame.draw.rect(screen, (220, 20, 60), exit_button_rect)

        screen.blit(play_text, play_button_rect)
        screen.blit(exit_text, exit_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_loop()
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_loop():
    global kira_x, kira_y, jumping, jump_count

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            kira_x -= kira_speed
        if keys[pygame.K_d]:
            kira_x += kira_speed
        if keys[pygame.K_w]:
            kira_y -= kira_speed
        if keys[pygame.K_s]:
            kira_y += kira_speed

        # Обработка прыжка
        if keys[pygame.K_SPACE] and not jumping:
            jumping = True

        if jumping:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1
                kira_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = jump_height

        # Ограничение перемещения персонажа по границам экрана
        kira_x = max(0, min(kira_x, screen_width - kira_image.get_width()))
        kira_y = max(0, min(kira_y, screen_height - kira_image.get_height()))

        # Градиентный фон
        for i in range(screen_height):
            color = (
                color1[0] * (screen_height - i) // screen_height + color2[0] * i // screen_height,
                color1[1] * (screen_height - i) // screen_height + color2[1] * i // screen_height,
                color1[2] * (screen_height - i) // screen_height + color2[2] * i // screen_height
            )
            pygame.draw.line(screen, color, (0, i), (screen_width, i))

        # Рисуем персонажа
        screen.blit(kira_image, (kira_x, kira_y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main_menu()
