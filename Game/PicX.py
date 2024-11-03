import tkinter as tk
import pygame

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PicX")
        
        # Инициализация pygame для воспроизведения музыки и звуков
        pygame.mixer.init()
        
        # Загрузка звука клика
        self.click_sound = pygame.mixer.Sound("./data/game/click.mp3")
        self.click_sound.set_volume(1.0)  # Установка громкости на 100%
        
        # Установка только полноэкранного режима
        self.root.attributes("-fullscreen", True)
        
        # Настройка фона
        self.root.configure(bg="black")  # Полностью черный фон
        
        # Переменные для отслеживания состояния удержания Escape
        self.escape_pressed = False
        self.escape_counter = 5
        self.escape_label = None
        
        # Привязка события нажатия и удержания клавиши Escape
        self.root.bind("<Escape>", self.start_escape_countdown)
        self.root.bind("<KeyRelease-Escape>", self.stop_escape_countdown)
        
        # Привязка события клика мыши для воспроизведения звука
        self.root.bind("<Button-1>", self.play_click_sound)
        
        # Создаем главное меню
        self.main_menu()

    def play_click_sound(self, event=None):
        # Воспроизведение звука клика
        self.click_sound.play()

    def main_menu(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Рамка для центровки контента
        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True)
        
        # Название игры
        title_label = tk.Label(
            frame, text="PicX", font=("Helvetica", 48, "bold"),
            fg="white", bg="black"
        )
        title_label.pack(pady=40)
        
        # Кнопка "Играть"
        play_button = tk.Button(
            frame, text="Играть", font=("Helvetica", 18),
            command=self.start_loading_screen,
            bg="#4CAF50", fg="white", activebackground="#388E3C",
            activeforeground="white", width=20, height=2
        )
        play_button.pack(pady=20)

        # Кнопка "Выйти"
        exit_button = tk.Button(
            frame, text="Выйти", font=("Helvetica", 18),
            command=self.exit_game,
            bg="#E53935", fg="white", activebackground="#B71C1C",
            activeforeground="white", width=20, height=2
        )
        exit_button.pack(pady=20)

    def start_loading_screen(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Черный экран с надписью "Загрузка..."
        loading_label = tk.Label(self.root, text="Загрузка...", font=("Helvetica", 24), fg="white", bg="black")
        loading_label.pack(expand=True)
        
        # Задержка на 5 секунд перед началом теста
        self.root.after(5000, self.start_game)
    
    def start_game(self):
        # Начало первого вопроса
        self.ask_question("Начать тест?", "ДА", "НЕТ", self.ask_question_2)
    
    def ask_question(self, question, option1, option2, next_question_callback):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()

        # Фрейм для командной строки
        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True)
        
        # Вопрос
        question_label = tk.Label(frame, text=f"{question}\n\n1. {option1}\n2. {option2}", font=("Courier", 18), fg="white", bg="black")
        question_label.pack(pady=20)
        
        # Поле для ввода ответа
        self.input_var = tk.StringVar()
        input_entry = tk.Entry(frame, textvariable=self.input_var, font=("Courier", 18), fg="white", bg="black", insertbackground="white", width=2)
        input_entry.pack(pady=20)
        input_entry.focus()
        
        # Мигающая полоска в поле ввода
        self.blink_cursor(input_entry)
        
        # Кнопка для подтверждения ответа
        submit_button = tk.Button(
            frame, text="ОК", font=("Helvetica", 18),
            command=lambda: self.process_answer(option1, option2, next_question_callback)
        )
        submit_button.pack(pady=10)
    
    def process_answer(self, option1, option2, next_question_callback):
        answer = self.input_var.get()
        
        # Проверка ответа
        if answer == "1":
            self.show_transition(next_question_callback)
        elif answer == "2":
            if option2 == "НЕТ" and next_question_callback == self.end_game_screen:
                self.ask_question("Хочешь поиграть?", "ДА", "НЕТ", self.end_game_screen)
            else:
                self.show_transition(next_question_callback)
        else:
            self.show_error_screen(lambda: self.ask_question("Начать тест?", "ДА", "НЕТ", self.ask_question_2))
    
    def show_error_screen(self, retry_callback):
        # Очистка окна и показ сообщения об ошибке
        for widget in self.root.winfo_children():
            widget.destroy()
        
        error_label = tk.Label(self.root, text="...", font=("Helvetica", 48), fg="white", bg="black")
        error_label.pack(expand=True)
        
        # Задержка на 5 секунд перед повтором вопроса
        self.root.after(5000, retry_callback)

    def show_transition(self, next_question_callback):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Черный экран на 3 секунды
        self.root.after(3000, next_question_callback)

    def ask_question_2(self):
        self.ask_question("Вы одни?", "ДА", "НЕТ", self.ask_question_3)

    def ask_question_3(self):
        self.ask_question("Ты боишься темноты?", "ДА", "НЕТ", self.ask_question_4)

    def ask_question_4(self):
        self.ask_question("Спас бы семью если бы она была в опасности?", "ДА", "НЕТ", self.end_game_screen)

    def end_game_screen(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Черный экран с мигающей полоской
        end_label = tk.Label(self.root, text="_", font=("Courier", 36), fg="white", bg="black")
        end_label.pack(expand=True)
        
        # Мигающая полоска
        self.blink_cursor(end_label)
    
    def blink_cursor(self, widget):
        def blink():
            current_color = widget.cget("fg")
            new_color = "black" if current_color == "white" else "white"
            widget.config(fg=new_color)
            widget.after(500, blink)
        blink()
    
    def start_escape_countdown(self, event):
        if not self.escape_pressed:
            self.escape_pressed = True
            self.escape_counter = 5  # Сброс обратного отсчета
            self.update_escape_label()
            self.decrement_escape_counter()

    def stop_escape_countdown(self, event):
        self.escape_pressed = False
        if self.escape_label:
            self.escape_label.destroy()  # Удаляем обратный отсчет, если клавиша отпущена

    def update_escape_label(self):
        # Обновляем или создаем метку обратного отсчета
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
                self.exit_game()  # Закрываем игру, если обратный отсчет до нуля

    def exit_game(self):
        # Завершение игры
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
