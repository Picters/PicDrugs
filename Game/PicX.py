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
            if exit_on_no:
                self.exit_game()
            else:
                self.show_transition(next_question_callback)
        else:
            self.show_error_screen(lambda: self.ask_question(self.current_question, option1, option2, next_question_callback, exit_on_no))

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
        
        input_entry.bind("<KeyRelease>", lambda event: self.limit_input_length(input_entry, event))
        
        input_entry.bind("<Return>", lambda event: self.process_ready_answer())
        
        submit_button = tk.Button(
            self.root, text="ОК", font=("Helvetica", 18),
            command=self.process_ready_answer
        )
        submit_button.pack(pady=10)

    def process_ready_answer(self):
        answer = self.input_var.get()
        
        if answer == "1":
            self.increase_then_fade_music()
        elif answer == "2":
            self.show_dots_and_black_screen()

    def increase_then_fade_music(self):
        # Резко увеличиваем громкость, затем уменьшаем до нуля через секунду
        pygame.mixer.music.set_volume(1.0)
        self.root.after(1000, lambda: pygame.mixer.music.set_volume(0.0))
        
        # Переход к эффекту открытия глаз
        self.root.after(2000, self.open_eyes_effect)

    def show_dots_and_black_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        dots_label = tk.Label(self.root, text="...", font=("Courier", 48), fg="white", bg="black")
        dots_label.pack(expand=True)
        
        self.root.after(3000, self.clear_screen)

    def open_eyes_effect(self):
        # Эффект открытия глаз с черными полосами
        for widget in self.root.winfo_children():
            widget.destroy()

        # Верхняя и нижняя полосы
        self.top_bar = tk.Frame(self.root, bg="black", height=300)
        self.top_bar.pack(fill=tk.X)
        self.middle_frame = tk.Frame(self.root, bg="black")
        self.middle_frame.pack(fill=tk.BOTH, expand=True)
        self.bottom_bar = tk.Frame(self.root, bg="black", height=300)
        self.bottom_bar.pack(fill=tk.X)

        # Постепенное уменьшение высоты полос
        self.decrease_bar_height()

    def decrease_bar_height(self):
        # Уменьшение высоты полос для эффекта открытия глаз
        top_height = self.top_bar.winfo_height()
        bottom_height = self.bottom_bar.winfo_height()
        
        if top_height > 0 and bottom_height > 0:
            new_height = max(0, top_height - 10)
            self.top_bar.config(height=new_height)
            self.bottom_bar.config(height=new_height)
            self.root.after(50, self.decrease_bar_height)
        else:
            # После открытия глаз показать финальное изображение
            self.show_final_scene()

    def show_final_scene(self):
        # Здесь вы можете добавить изображение комнаты в пиксельном стиле
        self.middle_frame.destroy()
        final_image = Image.open("./data/game/final_scene.png")
        final_image = final_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.NEAREST)
        final_photo = ImageTk.PhotoImage(final_image)
        final_label = tk.Label(self.root, image=final_photo)
        final_label.image = final_photo  # Сохранение ссылки на изображение
        final_label.pack(expand=True, fill=tk.BOTH)

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
