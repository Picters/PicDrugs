import tkinter as tk
import pygame
from PIL import Image, ImageTk

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PicX")
        
        pygame.mixer.init()
        
        # Load sounds
        self.click_sound = pygame.mixer.Sound("./data/game/click.mp3")
        self.click_sound.set_volume(1.0)
        
        self.keypress_sound = pygame.mixer.Sound("./data/game/Keyboard.mp3")
        self.keypress_sound.set_volume(0.2)
        
        # Game and menu music
        self.game_music_file = "./data/game/X.mp3"
        self.menu_music_file = "./data/main/music.wav"

        # Window settings
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        
        # State tracking variables
        self.click_enabled = False
        self.escape_pressed = False
        self.escape_counter = 5
        self.escape_label = None
        
        # Key event bindings
        self.root.bind("<Escape>", self.start_escape_countdown)
        self.root.bind("<KeyRelease-Escape>", self.stop_escape_countdown)
        
        # Start main menu
        self.main_menu()

    def play_click_sound(self):
        if self.click_enabled:
            self.click_sound.play()

    def play_keypress_sound(self, char):
        if char.isalpha() or char.isdigit():
            self.keypress_sound.play()

    def play_menu_music(self):
        pygame.mixer.music.load(self.menu_music_file)
        pygame.mixer.music.set_volume(1.0)  # Установить громкость на 100%
        pygame.mixer.music.play(loops=-1)

    def stop_menu_music(self):
        pygame.mixer.music.stop()

    def play_game_music(self):
        pygame.mixer.music.load(self.game_music_file)
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(loops=-1)

    def main_menu(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.play_menu_music()
        
        # Display "PicX" as a question
        question_label = tk.Label(
            self.root,
            text="PicX\n\n1. Играть\n2. Выйти",
            font=("Courier", 24),
            fg="white",
            bg="black"
        )
        question_label.pack(pady=100)

        # Input field for selecting options
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

        # Limit to one character and play sound for valid inputs
        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry, event))
        input_entry.bind("<Return>", lambda event: self.process_main_menu_selection())

        # OK button to confirm selection
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
                self.show_dots_and_exit()  # Показывать три точки при последнем вопросе
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
        # Создаем мигающую полоску в верхнем левом углу
        cursor_label = tk.Label(self.root, text="_", font=("Courier", 48), fg="white", bg="black")
        cursor_label.place(x=10, y=10)  # Установка положения в верхний левый угол
        self.blink_cursor(cursor_label)

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
        # Очистить экран от предыдущих виджетов
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Сообщение подключения
        connect_text = "Connect ............ "
        final_text = "Connected"
        
        label = tk.Label(self.root, text="", font=("Courier", 24), fg="white", bg="black")
        label.pack(expand=True)
        
        # Начать писать код
        for i, char in enumerate(connect_text):
            self.root.after(200 * i, lambda c=char: label.config(text=label.cget("text") + c))
        
        # После завершения показа "Connected"
        self.root.after(200 * len(connect_text), lambda: self.display_connected(final_text))

    def display_connected(self, final_text):
        # Отображаем "Connected" зеленым цветом
        label = tk.Label(self.root, text=final_text, font=("Courier", 24), fg="green", bg="black")
        label.pack(expand=True)

        # Пауза перед черным экраном
        self.root.after(3000, self.clear_screen)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="black")

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
