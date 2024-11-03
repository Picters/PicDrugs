import tkinter as tk
from tkinter import ttk
import pygame  # Импортируем pygame для проигрывания музыки

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PicX")
        
        # Инициализация pygame для проигрывания музыки
        pygame.mixer.init()
        
        # Установка окна на полный экран
        self.fullscreen = True
        self.root.attributes("-fullscreen", self.fullscreen)
        
        # Настройка фона
        self.root.configure(bg="black")  # Полностью черный фон
        
        # Подключение клавиши F11 для переключения полноэкранного режима
        self.root.bind("<F11>", self.toggle_fullscreen_key)
        
        # Создаем главное меню
        self.main_menu()
    
    def main_menu(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Запуск фоновой музыки для главного меню
        self.play_menu_music()
        
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
            command=self.start_loading_screen, bg="#4CAF50", fg="white",
            activebackground="#388E3C", activeforeground="white", width=20, height=2
        )
        play_button.pack(pady=20)

        # Кнопка "Выйти"
        exit_button = tk.Button(
            frame, text="Выйти", font=("Helvetica", 18),
            command=self.exit_game, bg="#E53935", fg="white",
            activebackground="#B71C1C", activeforeground="white", width=20, height=2
        )
        exit_button.pack(pady=20)
    
    def play_menu_music(self):
        # Указываем путь к файлу музыки для главного меню
        music_file = "./data/main/music.mp3"
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)  # Устанавливаем громкость
        pygame.mixer.music.play(loops=-1)  # Запускаем воспроизведение в цикле
    
    def stop_music(self):
        # Остановка музыки
        pygame.mixer.music.stop()
    
    def play_game_music(self, volume=0.1):
        # Указываем путь к файлу музыки для игры
        music_file = "./data/game/X.mp3"
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость
        pygame.mixer.music.play(loops=-1)  # Запускаем воспроизведение в цикле
    
    def start_loading_screen(self):
        # Остановка музыки меню
        self.stop_music()
        
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
        self.ask_question_1()
    
    def ask_question_1(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Вопрос "Начать тест?"
        question_label = tk.Label(self.root, text="Начать тест?", font=("Helvetica", 24), fg="white", bg="black")
        question_label.pack(expand=True)
        
        # Кнопки ДА и НЕТ
        yes_button = tk.Button(self.root, text="ДА", font=("Helvetica", 18), bg="#4CAF50", fg="white",
                               command=self.ask_question_2, width=10, height=2)
        yes_button.pack(pady=20)
        
        no_button = tk.Button(self.root, text="НЕТ", font=("Helvetica", 18), bg="#E53935", fg="white",
                              command=self.exit_game, width=10, height=2)
        no_button.pack(pady=20)
    
    def ask_question_2(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Вопрос "Вы одни?"
        question_label = tk.Label(self.root, text="Вы одни?", font=("Helvetica", 24), fg="white", bg="black")
        question_label.pack(expand=True)
        
        # Кнопки ДА и НЕТ
        yes_button = tk.Button(self.root, text="ДА", font=("Helvetica", 18), bg="#4CAF50", fg="white",
                               command=self.start_music_and_ask_question_3, width=10, height=2)
        yes_button.pack(pady=20)
        
        no_button = tk.Button(self.root, text="НЕТ", font=("Helvetica", 18), bg="#E53935", fg="white",
                              command=self.ask_question_3, width=10, height=2)
        no_button.pack(pady=20)
    
    def start_music_and_ask_question_3(self):
        # Воспроизведение музыки для игры на 10% громкости
        self.play_game_music(volume=0.1)
        self.ask_question_3()
    
    def ask_question_3(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Вопрос "Ты боишься темноты?"
        question_label = tk.Label(self.root, text="Ты боишься темноты?", font=("Helvetica", 24), fg="white", bg="black")
        question_label.pack(expand=True)
        
        # Кнопки ДА и НЕТ
        yes_button = tk.Button(self.root, text="ДА", font=("Helvetica", 18), bg="#4CAF50", fg="white",
                               command=self.increase_music_volume, width=10, height=2)
        yes_button.pack(pady=20)
        
        no_button = tk.Button(self.root, text="НЕТ", font=("Helvetica", 18), bg="#E53935", fg="white",
                              command=self.next_question, width=10, height=2)
        no_button.pack(pady=20)
    
    def increase_music_volume(self):
        # Увеличение громкости на 10%
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(min(current_volume + 0.1, 1.0))  # Максимум громкости - 100%
        self.next_question()
    
    def next_question(self):
        # Заглушка для следующего вопроса
        for widget in self.root.winfo_children():
            widget.destroy()
        
        question_label = tk.Label(self.root, text="Следующий вопрос...", font=("Helvetica", 24), fg="white", bg="black")
        question_label.pack(expand=True)
        
        # Продолжение сюжета игры...
    
    def exit_game(self):
        # Завершение игры
        self.root.quit()
    
    def toggle_fullscreen_key(self, event=None):
        # Переключение полноэкранного режима с помощью клавиши F11
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
