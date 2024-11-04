import tkinter as tk
import pygame
import random  # Для эффекта мерцания
from PIL import Image, ImageTk

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PicX")

        pygame.mixer.init()

        # Загрузка звуков
        self.click_sound = pygame.mixer.Sound("./data/game/click.mp3")
        self.click_sound.set_volume(1.0)

        self.keypress_sound = pygame.mixer.Sound("./data/game/Keyboard.mp3")
        self.keypress_sound.set_volume(0.2)

        # Музыка для игры и меню
        self.game_music_file = "./data/game/X.mp3"
        self.menu_music_file = "./data/main/music.wav"

        # Настройки окна
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        # Переменные состояния
        self.click_enabled = False
        self.escape_pressed = False
        self.escape_counter = 5
        self.escape_label = None

        # Привязки событий клавиатуры
        self.root.bind("<Escape>", self.start_escape_countdown)
        self.root.bind("<KeyRelease-Escape>", self.stop_escape_countdown)

        # Запуск главного меню
        self.main_menu()

    def play_click_sound(self):
        if self.click_enabled:
            self.click_sound.play()

    def play_keypress_sound(self, char):
        if char.isalpha() or char.isdigit():
            self.keypress_sound.play()

    def play_menu_music(self):
        pygame.mixer.music.load(self.menu_music_file)
        pygame.mixer.music.set_volume(1.0)  # Устанавливаем громкость на 100%
        pygame.mixer.music.play(loops=-1)

    def stop_menu_music(self):
        pygame.mixer.music.stop()

    def play_game_music(self):
        pygame.mixer.music.load(self.game_music_file)
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(loops=-1)

    def main_menu(self):
        # Очистка предыдущих виджетов
        for widget in self.root.winfo_children():
            widget.destroy()

        self.play_menu_music()

        # Отображение "PicX" как вопроса
        question_label = tk.Label(
            self.root,
            text="PicX\n\n1. Играть\n2. Выйти",
            font=("Courier", 24),
            fg="white",
            bg="black"
        )
        question_label.pack(pady=100)

        # Поле ввода для выбора опций
        self.input_var = tk.StringVar()
        input_entry = tk.Entry(
            self.root,
            textvariable=self.input_var,
            font=("Courier", 24),
            fg="white",
            bg="black",
            insertbackground="white",
            width=2
        )
        input_entry.pack(pady=20)
        input_entry.focus()

        # Ограничение ввода одним символом и воспроизведение звука
        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry, event))
        input_entry.bind("<Return>", lambda event: self.process_main_menu_selection())

        # Кнопка подтверждения выбора
        submit_button = tk.Button(
            self.root,
            text="OK",
            font=("Helvetica", 18),
            command=self.process_main_menu_selection
        )
        submit_button.pack(pady=10)

    def process_main_menu_selection(self):
        answer = self.input_var.get()

        if answer == "1":
            self.play_click_sound()
            self.start_game()
        elif answer == "2":
            self.play_click_sound()
            self.exit_game()
        else:
            self.show_error_screen(self.main_menu)

    def start_game(self):
        self.stop_menu_music()
        self.play_game_music()
        self.click_enabled = True
        self.show_loading_screen()  # Показ экрана загрузки перед началом вопросов

    def show_loading_screen(self):
        # Очистка экрана и показ текста "Загрузка..."
        for widget in self.root.winfo_children():
            widget.destroy()

        loading_label = tk.Label(self.root, text="Загрузка...", font=("Helvetica", 48), fg="white", bg="black")
        loading_label.pack(expand=True)

        # Через 3 секунды начать вопросы
        self.root.after(3000, self.start_game_questions)

    def start_game_questions(self):
        # Начинаем с первых вопросов
        self.ask_question("Начать тест?", "ДА", "НЕТ", self.ask_question_2, exit_on_no=True)

    def ask_question_2(self):
        self.ask_question("Вы одни?", "ДА", "НЕТ", self.ask_question_3)

    def ask_question_3(self):
        self.ask_question("Ты боишься темноты?", "ДА", "НЕТ", self.ask_question_4)

    def ask_question_4(self):
        self.ask_question("Спас бы семью если бы она была в опасности?", "ДА", "НЕТ", self.ask_question_5)

    # Новые странные вопросы начинаются здесь
    def ask_question_5(self):
        self.ask_question("Вы видели красные огоньки, когда закрывали глаза?", "ДА", "НЕТ", self.ask_question_6)

    def ask_question_6(self):
        self.ask_question("Когда вам последний раз снились звуки шагов рядом?", "ВЧЕРА", "НИКОГДА", self.ask_question_7)

    def ask_question_7(self):
        self.ask_question("Куда бы вы пошли, если бы могли идти бесконечно долго?", "НАЗАД", "ВПЕРЕД", self.ask_question_8)

    def ask_question_8(self):
        self.ask_question("Что страшнее: встретить отражение или собственную тень?", "ОТРАЖЕНИЕ", "ТЕНЬ", self.ask_question_9)

    def ask_question_9(self):
        self.ask_question("Вы чувствовали себя чужим в знакомом месте?", "ДА", "НЕТ", self.ask_question_10)

    def ask_question_10(self):
        self.ask_question("Если бы вы могли забыть что-то навсегда, что бы это было?", "ВСЕ ВОСПОМИНАНИЯ", "НИЧЕГО", self.start_end_sequence)

    def ask_question(self, question, option1, option2, next_question_callback, exit_on_no=False):
        self.current_question = question
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True)

        question_label = tk.Label(frame, text=f"{question}\n\n1. {option1}\n2. {option2}", font=("Courier", 18), fg="white", bg="black")
        question_label.pack(pady=20)

        self.input_var = tk.StringVar()
        input_entry = tk.Entry(frame, textvariable=self.input_var, font=("Courier", 18), fg="white", bg="black", insertbackground="white", width=2)
        input_entry.pack(pady=20)
        input_entry.focus()

        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry, event))

        input_entry.bind("<Return>", lambda event: self.process_answer(option1, option2, next_question_callback, exit_on_no))

        submit_button = tk.Button(
            frame, text="ОК", font=("Helvetica", 18),
            command=lambda: self.process_answer(option1, option2, next_question_callback, exit_on_no)
        )
        submit_button.pack(pady=10)

    def limit_input_length(self, entry, event):
        if len(entry.get()) > 1:
            entry.delete(1, tk.END)
        if event.char and (event.char.isalpha() or event.char.isdigit()):
            self.play_keypress_sound(event.char)

    def process_answer(self, option1, option2, next_question_callback, exit_on_no):
        answer = self.input_var.get()

        if answer == "1":
            self.show_transition(next_question_callback)
        elif answer == "2":
            if exit_on_no:  # Если на первом вопросе "НЕТ", выходим из игры
                self.exit_game()
            elif next_question_callback == self.start_end_sequence:
                self.show_dots_and_exit()  # Показывать три точки и выйти
            else:
                self.show_transition(next_question_callback)  # Показать следующий вопрос
        else:
            self.show_error_screen(lambda: self.ask_question(self.current_question, option1, option2, next_question_callback, exit_on_no))

    def show_transition(self, next_question_callback):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Отображаем черный экран на 2 секунды
        black_screen = tk.Frame(self.root, bg="black")
        black_screen.pack(fill=tk.BOTH, expand=True)
        self.root.after(2000, next_question_callback)

    def show_error_screen(self, retry_callback):
        for widget in self.root.winfo_children():
            widget.destroy()

        error_label = tk.Label(self.root, text="...", font=("Helvetica", 48), fg="white", bg="black")
        error_label.pack(expand=True)

        self.root.after(3000, retry_callback)

    def start_end_sequence(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Показ надписи "Хорошо" с громким звуком
        pygame.mixer.music.set_volume(1.0)
        final_label = tk.Label(self.root, text="Хорошо", font=("Courier", 36), fg="white", bg="black")
        final_label.pack(expand=True)

        self.root.after(1000, self.fade_out_sound_and_show_black_screen)  # Задержка в 1 секунду

    def fade_out_sound_and_show_black_screen(self):
        # Плавное уменьшение громкости до нуля
        for i in range(10):
            self.root.after(i * 100, lambda v=1 - (i * 0.1): pygame.mixer.music.set_volume(v))

        # После затухания звука показать черный экран
        self.root.after(1000, self.show_black_screen)  # После 1 секунды

    def show_black_screen(self):
        # Очистка экрана и переход на черный экран
        for widget in self.root.winfo_children():
            widget.destroy()

        black_screen = tk.Frame(self.root, bg="black")
        black_screen.pack(fill=tk.BOTH, expand=True)

        # После 2 секунд черный экран показываем мигающую полоску
        self.root.after(2000, self.show_cursor_effect)

    def show_cursor_effect(self):
        # Создаем фрейм для курсора и текста
        self.console_frame = tk.Frame(self.root, bg="black")
        self.console_frame.place(x=10, y=10)

        # Создаем мигающую полоску в верхнем левом углу внутри фрейма
        self.cursor_label = tk.Label(self.console_frame, text="_", font=("Courier", 24), fg="white", bg="black")
        self.cursor_label.pack(side='left')
        self.blink_cursor(self.cursor_label)

        # После 5 секунд показываем код подключения
        self.root.after(5000, self.show_connect_message)

    def blink_cursor(self, widget):
        def blink():
            current_color = widget.cget("fg")
            new_color = "black" if current_color == "white" else "white"
            widget.config(fg=new_color)
            widget.after(500, blink)
        blink()

    def show_connect_message(self):
        # Сообщение подключения
        connect_text = "Connect ............ "
        final_text = "Connected"

        # Удаляем курсор временно
        self.cursor_label.pack_forget()

        # Создаем лейбл для текста подключения
        self.connect_label = tk.Label(self.console_frame, text="", font=("Courier", 24), fg="white", bg="black")
        self.connect_label.pack(side='left')

        # Возвращаем курсор
        self.cursor_label.pack(side='left')

        # Начать писать код
        for i, char in enumerate(connect_text):
            self.root.after(200 * i, lambda c=char: self.connect_label.config(text=self.connect_label.cget("text") + c))

        # После завершения показа "Connected"
        total_time = 200 * len(connect_text)
        self.root.after(total_time, lambda: self.display_connected(final_text))

    def display_connected(self, final_text):
        # Обновляем текст на "Connected" зеленым цветом
        self.connect_label.config(text=final_text, fg="green")

        # Пауза перед запуском последовательности ошибки
        self.root.after(3000, self.start_error_sequence)

    def start_error_sequence(self):
        # Очистить экран
        for widget in self.root.winfo_children():
            widget.destroy()

        # Запуск мерцания
        self.flicker_start_time = self.root.after(0, self.colorful_flicker)
        # Через 3 секунды остановить мерцание и запустить ошибку
        self.root.after(3000, self.stop_flicker_and_show_error)

    def colorful_flicker(self):
        # Случайный цвет фона
        colors = ["red", "green", "blue", "yellow", "purple", "orange", "white"]
        color = random.choice(colors)
        self.root.configure(bg=color)
        self.flicker_start_time = self.root.after(100, self.colorful_flicker)

    def stop_flicker_and_show_error(self):
        # Остановить мерцание
        if self.flicker_start_time:
            self.root.after_cancel(self.flicker_start_time)
            self.flicker_start_time = None

        # Вернуть черный фон
        self.root.configure(bg="black")

        # Воспроизвести звук ошибки
        error_sound = pygame.mixer.Sound("./data/game/Error.mp3")
        error_sound.set_volume(1.0)
        error_sound.play()

        # Показать команды исправления ошибки
        self.show_error_commands()

    def show_error_commands(self):
        # Создаем фрейм для консоли
        self.console_frame = tk.Frame(self.root, bg="black")
        self.console_frame.place(x=10, y=10)

        # Мигающий курсор
        self.cursor_label = tk.Label(self.console_frame, text="_", font=("Courier", 24), fg="white", bg="black")
        self.cursor_label.pack(side='left')
        self.blink_cursor(self.cursor_label)

        # Список команд для отображения
        commands = [
            "System error detected...",
            "Attempting to recover...",
            "Loading backup files...",
            "Restoring system settings...",
            "Checking disk integrity...",
            "Recompiling core modules...",
            "Restarting essential services...",
            "Updating configuration...",
            "Clearing temporary files...",
            "Applying security patches...",
            "Finalizing recovery...",
            "Operation completed successfully."
        ]

        self.command_index = 0
        self.execute_commands(commands)

    def execute_commands(self, commands):
        if self.command_index < len(commands):
            command = commands[self.command_index]
            # Удаляем курсор временно
            self.cursor_label.pack_forget()

            # Создаем или обновляем лейбл с текстом команды
            if hasattr(self, 'command_label'):
                self.command_label.destroy()
            self.command_label = tk.Label(self.console_frame, text="", font=("Courier", 24), fg="white", bg="black")
            self.command_label.pack(anchor='w')
            self.cursor_label.pack(side='left')

            # Печатаем команду посимвольно
            for i, char in enumerate(command):
                self.root.after(200 * i, lambda c=char: self.command_label.config(text=self.command_label.cget("text") + c))
            total_time = 200 * len(command)
            # После печати команды переходим к следующей
            self.command_index += 1
            self.root.after(total_time + 500, lambda: self.execute_commands(commands))
        else:
            # После выполнения всех команд запускаем глитч эффект
            self.root.after(2000, self.start_glitch_effect)

    def start_glitch_effect(self):
        # Очистить экран
        for widget in self.root.winfo_children():
            widget.destroy()
        # Запуск глитч эффекта
        self.glitch_start_time = self.root.after(0, self.glitch_flicker)
        # Воспроизвести звук помех
        glitch_sound = pygame.mixer.Sound("./data/game/glitch.mp3")
        glitch_sound.set_volume(1.0)
        glitch_sound.play()
        # Через 2 секунды остановить глитч эффект и продолжить
        self.root.after(2000, self.stop_glitch_and_show_restored)

    def glitch_flicker(self):
        # Эффект случайного шума
        colors = ["black", "white", "gray"]
        color = random.choice(colors)
        self.root.configure(bg=color)
        self.glitch_start_time = self.root.after(50, self.glitch_flicker)

    def stop_glitch_and_show_restored(self):
        # Остановить глитч эффект
        if self.glitch_start_time:
            self.root.after_cancel(self.glitch_start_time)
            self.glitch_start_time = None
        # Сбросить фон
        self.root.configure(bg="black")
        # Показать "System is Restored"
        self.show_system_restored()

    def show_system_restored(self):
        # Воссоздаем консольный фрейм
        self.console_frame = tk.Frame(self.root, bg="black")
        self.console_frame.place(x=10, y=10)
        # Курсор
        self.cursor_label = tk.Label(self.console_frame, text="_", font=("Courier", 24), fg="white", bg="black")
        self.cursor_label.pack(side='left')
        self.blink_cursor(self.cursor_label)
        # Удаляем курсор временно
        self.cursor_label.pack_forget()
        # Отображаем "System is Restored" зелёным цветом
        self.restored_label = tk.Label(self.console_frame, text="", font=("Courier", 24), fg="green", bg="black")
        self.restored_label.pack(side='left')
        self.cursor_label.pack(side='left')
        restored_text = "System is Restored"
        for i, char in enumerate(restored_text):
            self.root.after(200 * i, lambda c=char: self.restored_label.config(text=self.restored_label.cget("text") + c))
        # После печати текста, ждём 4 секунды и продолжаем
        total_time = 200 * len(restored_text)
        self.root.after(total_time + 4000, self.start_system_startup_sequence)

    def start_system_startup_sequence(self):
        # Удаляем предыдущие лейблы
        for widget in self.console_frame.winfo_children():
            widget.destroy()
        # Курсор
        self.cursor_label = tk.Label(self.console_frame, text="_", font=("Courier", 24), fg="white", bg="black")
        self.cursor_label.pack(side='left')
        self.blink_cursor(self.cursor_label)
        # Отображаем "Starting system" оранжевым цветом
        self.cursor_label.pack_forget()
        self.starting_label = tk.Label(self.console_frame, text="", font=("Courier", 24), fg="orange", bg="black")
        self.starting_label.pack(side='left')
        self.cursor_label.pack(side='left')
        starting_text = "Starting system"
        for i, char in enumerate(starting_text):
            self.root.after(200 * i, lambda c=char: self.starting_label.config(text=self.starting_label.cget("text") + c))
        # После печати продолжаем к компонентам
        total_time = 200 * len(starting_text)
        self.root.after(total_time, self.show_components_startup)

    def show_components_startup(self):
        # Удаляем предыдущие лейблы
        for widget in self.console_frame.winfo_children():
            widget.destroy()
        # Курсор
        self.cursor_label = tk.Label(self.console_frame, text="_", font=("Courier", 24), fg="white", bg="black")
        self.cursor_label.pack(side='left')
        self.blink_cursor(self.cursor_label)
        # Список компонентов
        components = [
            "Disk C:\\......... Done",
            "System Tracing......... Done",
            "Loading drivers......... Done",
            "Initializing hardware......... Done",
            "Network services......... Done",
            "User interface......... Done",
            "Security protocols......... Done",
            "Memory check......... Done",
            "Updating registry......... Done",
            "Finalizing setup......... Done",
            "Optimizing performance......... Done",
            "Cleaning up......... Done",
            "Applying user settings......... Done",
            "Launching applications......... Done"
        ]
        # Воспроизвести звук "Repair.mp3"
        repair_sound = pygame.mixer.Sound("./data/game/Repair.mp3")
        repair_sound.set_volume(1.0)
        repair_sound.play()
        # Начинаем отображение компонентов
        self.component_index = 0
        self.display_component(components, repair_sound)

    def display_component(self, components, repair_sound):
        if self.component_index < len(components):
            component = components[self.component_index]
            # Удаляем курсор временно
            self.cursor_label.pack_forget()
            # Создаем или обновляем лейбл
            if hasattr(self, 'component_label'):
                self.component_label.destroy()
            self.component_label = tk.Label(self.console_frame, text="", font=("Courier", 24), fg="white", bg="black")
            self.component_label.pack(anchor='w')
            self.cursor_label.pack(side='left')
            # Печатаем строку компонента
            for i, char in enumerate(component):
                self.root.after(200 * i, lambda c=char: self.component_label.config(text=self.component_label.cget("text") + c))
            total_time = 200 * len(component)
            # После печати переходим к следующему компоненту
            self.component_index += 1
            self.root.after(total_time + 500, lambda: self.display_component(components, repair_sound))
        else:
            # После отображения всех компонентов
            repair_sound.stop()
            # Отображаем "System Started......."
            self.show_system_started()

    def show_system_started(self):
        # Удаляем предыдущие лейблы
        for widget in self.console_frame.winfo_children():
            widget.destroy()
        # Курсор
        self.cursor_label = tk.Label(self.console_frame, text="_", font=("Courier", 24), fg="white", bg="black")
        self.cursor_label.pack(side='left')
        self.blink_cursor(self.cursor_label)
        # Отображаем "System Started......."
        self.cursor_label.pack_forget()
        self.started_label = tk.Label(self.console_frame, text="", font=("Courier", 24), fg="white", bg="black")
        self.started_label.pack(side='left')
        self.cursor_label.pack(side='left')
        started_text = "System Started......."
        for i, char in enumerate(started_text):
            self.root.after(200 * i, lambda c=char: self.started_label.config(text=self.started_label.cget("text") + c))
        total_time = 200 * len(started_text)
        # После отображения, ждем секунду и затем черный экран
        self.root.after(total_time + 1000, self.clear_screen)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="black")
        # Выход из игры или дальнейшие действия
        self.exit_game()

    def start_escape_countdown(self, event):
        if not self.escape_pressed:
            self.escape_pressed = True
            self.escape_counter = 5
            self.update_escape_label()
            self.decrement_escape_counter()

    def stop_escape_countdown(self, event):
        self.escape_pressed = False
        if self.escape_label:
            self.escape_label.destroy()
            self.escape_label = None

    def update_escape_label(self):
        if not self.escape_label:
            self.escape_label = tk.Label(self.root, text="", font=("Helvetica", 18), fg="red", bg="black")
            self.escape_label.place(x=10, y=10)
        self.escape_label.config(text=f"Выход через {self.escape_counter}...")

    def decrement_escape_counter(self):
        if self.escape_pressed:
            if self.escape_counter > 0:
                self.escape_counter -= 1
                self.update_escape_label()
                self.root.after(1000, self.decrement_escape_counter)
            else:
                self.exit_game()

    def exit_game(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
