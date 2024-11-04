import tkinter as tk
import pygame
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
        pygame.mixer.music.set_volume(1.0)  # Установить громкость на 100%
        pygame.mixer.music.play(loops=-1)

    def stop_menu_music(self):
        pygame.mixer.music.stop()

    def main_menu(self):
        # Очистка экрана и запуск главного меню
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.play_menu_music()
        
        question_label = tk.Label(
            self.root,
            text="PicX\n\n1. Играть\n2. Выйти",
            font=("Courier", 24),
            fg="white",
            bg="black"
        )
        question_label.pack(pady=100)

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

        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry, event))
        input_entry.bind("<Return>", lambda event: self.process_main_menu_selection())

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
            self.start_game()
        elif answer == "2":
            self.exit_game()

    def start_game(self):
        self.stop_menu_music()
        pygame.mixer.music.load(self.game_music_file)
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(loops=-1)
        self.show_loading_screen()

    def show_loading_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        loading_label = tk.Label(self.root, text="Загрузка...", font=("Helvetica", 48), fg="white", bg="black")
        loading_label.pack(expand=True)

        self.root.after(3000, self.start_game_questions)

    def start_game_questions(self):
        # Начинаем с первых вопросов
        self.ask_question("Начать тест?", "ДА", "НЕТ", self.ask_question_2)

    def ask_question_2(self):
        self.ask_question("Вы одни?", "ДА", "НЕТ", self.ask_question_3)

    def ask_question_3(self):
        self.ask_question("Ты боишься темноты?", "ДА", "НЕТ", self.ask_question_4)

    def ask_question_4(self):
        self.ask_question("Спас бы семью если бы она была в опасности?", "ДА", "НЕТ", self.ask_question_5)

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

    def ask_question(self, question, option1, option2, next_question_callback):
        # Показ вопроса и вариантов ответа
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
        input_entry.bind("<Return>", lambda event: self.process_answer(option1, option2, next_question_callback))
        
        submit_button = tk.Button(
            frame, text="ОК", font=("Helvetica", 18),
            command=lambda: self.process_answer(option1, option2, next_question_callback)
        )
        submit_button.pack(pady=10)

    def limit_input_length(self, entry, event):
        if len(entry.get()) > 1:
            entry.delete(1, tk.END)
        if event.char and (event.char.isalpha() or event.char.isdigit()):
            self.play_keypress_sound(event.char)

    def process_answer(self, option1, option2, next_question_callback):
        answer = self.input_var.get()
        
        if answer == "1":
            self.show_transition(next_question_callback)
        elif answer == "2":
            self.exit_game()
        else:
            self.show_error_screen(lambda: self.ask_question(self.current_question, option1, option2, next_question_callback))

    def show_transition(self, next_question_callback):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Отображаем черный экран на 3 секунды
        black_screen = tk.Frame(self.root, bg="black")
        black_screen.pack(fill=tk.BOTH, expand=True)
        self.root.after(3000, next_question_callback)

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
        
        self.root.after(1000, self.fade_out_sound_and_show_cursor)

    def fade_out_sound_and_show_cursor(self):
        # Плавное уменьшение громкости до нуля
        for i in range(10):
            self.root.after(i * 100, lambda v=1 - (i * 0.1): pygame.mixer.music.set_volume(v))
        self.root.after(1000, self.show_cursor_effect)

    def show_cursor_effect(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Создаем мигающую пикающую полоску
        cursor_label = tk.Label(self.root, text="_", font=("Courier", 48), fg="white", bg="black")
        cursor_label.pack(expand=True)
        self.blink_cursor(cursor_label)

    def blink_cursor(self, widget):
        def blink():
            current_color = widget.cget("fg")
            new_color = "black" if current_color == "white" else "white"
            widget.config(fg=new_color)
            widget.after(500, blink)
        blink()

    def exit_game(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
