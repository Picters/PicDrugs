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
        self.click_sound.set_volume(1.0)  # Громкость клика на 100%
        
        self.keypress_sound = pygame.mixer.Sound("./data/game/Keyboard.mp3")
        self.keypress_sound.set_volume(0.2)  # Громкость звука клавиш на 20%
        
        # Музыка для главного меню и игры
        self.game_music_file = "./data/game/X.mp3"
        self.menu_music_file = "./data/main/music.mp3"
        
        # Настройки окна
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        
        # Переменные для отслеживания состояния
        self.click_enabled = False
        self.escape_pressed = False
        self.escape_counter = 5
        self.escape_label = None
        
        # Обработчики клавиш
        self.root.bind("<Escape>", self.start_escape_countdown)
        self.root.bind("<KeyRelease-Escape>", self.stop_escape_countdown)
        
        # Запуск главного меню
        self.main_menu()

    def play_click_sound(self):
        if self.click_enabled:
            self.click_sound.play()

    def play_keypress_sound(self):
        self.keypress_sound.play()

    def play_menu_music(self):
        pygame.mixer.music.load(self.menu_music_file)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)

    def stop_menu_music(self):
        pygame.mixer.music.stop()

    def play_game_music(self):
        pygame.mixer.music.load(self.game_music_file)
        pygame.mixer.music.set_volume(0.03)  # Фоновая музыка на 3% громкости
        pygame.mixer.music.play(loops=-1)

    def main_menu(self):
        # Очистка окна и запуск музыки меню
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.play_menu_music()
        
        # Загрузка фона для главного меню
        bg_image = Image.open("./data/main/MainBackground.png")
        self.background_image = ImageTk.PhotoImage(bg_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)
        
        # Название игры
        title_label = tk.Label(
            self.root, text="PicX", font=("Helvetica", 48, "bold"),
            fg="white", bg="black"
        )
        title_label.pack(pady=60)

        # Стили кнопок
        button_style = {
            "font": ("Helvetica", 18, "bold"),
            "fg": "#000000",
            "bg": "#ffffff",
            "activebackground": "#354251",
            "activeforeground": "#0095ff",
            "bd": 4,
            "relief": "solid",
            "width": 20,
            "height": 2,
            "cursor": "hand2"
        }
        
        # Кнопка "Играть"
        play_button = tk.Button(
            self.root, text="Играть", command=lambda: [self.play_click_sound(), self.start_game()],
            **button_style
        )
        play_button.pack(pady=15)

        # Кнопка "Выйти"
        exit_button = tk.Button(
            self.root, text="Выйти", command=lambda: [self.play_click_sound(), self.exit_game()],
            **button_style
        )
        exit_button.pack(pady=15)

    def start_game(self):
        # Остановка музыки меню и запуск фона для игры
        self.stop_menu_music()
        self.play_game_music()
        self.click_enabled = True
        self.ask_question("Начать тест?", "ДА", "НЕТ", self.ask_question_2, exit_on_no=True)

    def ask_question(self, question, option1, option2, next_question_callback, exit_on_no=False):
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
        
        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry))
        input_entry.bind("<Key>", lambda event: self.play_keypress_sound())
        
        # Обработка нажатия клавиши Enter
        input_entry.bind("<Return>", lambda event: self.process_answer(option1, option2, next_question_callback, exit_on_no))
        
        submit_button = tk.Button(
            frame, text="ОК", font=("Helvetica", 18),
            command=lambda: self.process_answer(option1, option2, next_question_callback, exit_on_no)
        )
        submit_button.pack(pady=10)

    def limit_input_length(self, entry):
        if len(entry.get()) > 1:
            entry.delete(1, tk.END)

    def process_answer(self, option1, option2, next_question_callback, exit_on_no):
        answer = self.input_var.get()
        
        if answer == "1":
            self.show_transition(next_question_callback)
        elif answer == "2":
            if exit_on_no:
                self.exit_game()
            else:
                self.show_transition(next_question_callback)
        else:
            # Вывод сообщения об ошибке, если ввод некорректен
            self.show_error_screen(lambda: self.ask_question(question, option1, option2, next_question_callback, exit_on_no))

    def show_transition(self, next_question_callback):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.after(3000, next_question_callback)

    def show_error_screen(self, retry_callback):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        error_label = tk.Label(self.root, text="...", font=("Helvetica", 48), fg="white", bg="black")
        error_label.pack(expand=True)
        
        self.root.after(3000, retry_callback)

    def ask_question_2(self):
        self.ask_question("Вы одни?", "ДА", "НЕТ", self.ask_question_3)

    def ask_question_3(self):
        self.ask_question("Ты боишься темноты?", "ДА", "НЕТ", self.ask_question_4)

    def ask_question_4(self):
        self.ask_question("Спас бы семью если бы она была в опасности?", "ДА", "НЕТ", self.start_end_sequence)

    def start_end_sequence(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.cursor_label = tk.Label(self.root, text="_", font=("Courier", 36), fg="white", bg="black")
        self.cursor_label.pack(expand=True)
        
        self.blink_cursor(self.cursor_label)
        
        self.root.after(5000, self.show_ready_prompt)

    def blink_cursor(self, widget):
        def blink():
            current_color = widget.cget("fg")
            new_color = "black" if current_color == "white" else "white"
            widget.config(fg=new_color)
            widget.after(500, blink)
        blink()

    def show_ready_prompt(self):
        self.cursor_label.pack_forget()
        
        ready_label = tk.Label(self.root, text="Хорошо", font=("Courier", 36), fg="white", bg="black")
        ready_label.pack()
        
        self.root.after(2000, self.ask_ready_question)

    def ask_ready_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        question_label = tk.Label(self.root, text="Готов идти дальше?\n\n1. ДА\n2. НЕТ", font=("Courier", 18), fg="white", bg="black")
        question_label.pack(pady=20)
        
        self.input_var = tk.StringVar()
        input_entry = tk.Entry(self.root, textvariable=self.input_var, font=("Courier", 18), fg="white", bg="black", insertbackground="white", width=2)
        input_entry.pack(pady=20)
        input_entry.focus()
        
        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry))
        input_entry.bind("<Key>", lambda event: self.play_keypress_sound())
        
        # Обработка нажатия клавиши Enter
        input_entry.bind("<Return>", lambda event: self.process_ready_answer())
        
        submit_button = tk.Button(
            self.root, text="ОК", font=("Helvetica", 18),
            command=self.process_ready_answer
        )
        submit_button.pack(pady=10)

    def process_ready_answer(self):
        answer = self.input_var.get()
        
        if answer == "1":
            self.start_black_screen_with_sound()
        elif answer == "2":
            self.show_dots_and_black_screen()  # Изменено на черный экран вместо выхода

    def show_dots_and_black_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        dots_label = tk.Label(self.root, text="...", font=("Courier", 48), fg="white", bg="black")
        dots_label.pack(expand=True)
        
        # Через 3 секунды очищает экран и оставляет его черным
        self.root.after(3000, self.clear_screen)

    def start_black_screen_with_sound(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.cursor_label = tk.Label(self.root, text="_", font=("Courier", 36), fg="white", bg="black")
        self.cursor_label.pack(expand=True)
        
        self.blink_cursor(self.cursor_label)
        
        self.root.after(3000, self.show_final_message_with_sound)

    def show_final_message_with_sound(self):
        self.cursor_label.pack_forget()
        
        final_label = tk.Label(self.root, text="Хорошо", font=("Courier", 36), fg="white", bg="black")
        final_label.pack(expand=True)
        
        self.increase_sound()
        
        self.root.after(500, self.clear_screen)

    def increase_sound(self):
        pygame.mixer.music.load(self.game_music_file)
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(loops=-1)
        
        for i in range(1, 11):
            self.root.after(i * 300, lambda v=i: pygame.mixer.music.set_volume(v * 0.1))

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
