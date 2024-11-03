import tkinter as tk
from tkinter import ttk
import time

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моя Игра")
        
        # Установка окна на полный экран
        self.fullscreen = True
        self.root.attributes("-fullscreen", self.fullscreen)
        
        # Основное меню
        self.main_menu()
    
    def main_menu(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Название игры
        title_label = tk.Label(self.root, text="Название Игры", font=("Helvetica", 24))
        title_label.pack(pady=20)
        
        # Кнопка "Играть"
        play_button = tk.Button(self.root, text="Играть", font=("Helvetica", 18), command=self.start_loading_screen)
        play_button.pack(pady=10)
        
        # Кнопка "Настройки"
        settings_button = tk.Button(self.root, text="Настройки", font=("Helvetica", 18), command=self.settings_menu)
        settings_button.pack(pady=10)
    
    def settings_menu(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок настроек
        settings_label = tk.Label(self.root, text="Настройки", font=("Helvetica", 24))
        settings_label.pack(pady=20)
        
        # Флажок "Полноэкранный режим"
        self.fullscreen_var = tk.BooleanVar(value=self.fullscreen)
        fullscreen_checkbox = tk.Checkbutton(self.root, text="Полноэкранный режим", font=("Helvetica", 18),
                                             variable=self.fullscreen_var, command=self.toggle_fullscreen)
        fullscreen_checkbox.pack(pady=10)
        
        # Кнопка "Назад"
        back_button = tk.Button(self.root, text="Назад", font=("Helvetica", 18), command=self.main_menu)
        back_button.pack(pady=10)
    
    def toggle_fullscreen(self):
        # Переключение полноэкранного режима
        self.fullscreen = self.fullscreen_var.get()
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def start_loading_screen(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Черный экран с надписью "Загрузка..."
        self.root.configure(bg="black")
        loading_label = tk.Label(self.root, text="Загрузка...", font=("Helvetica", 24), fg="white", bg="black")
        loading_label.pack(expand=True)
        
        # Задержка на 5 секунд перед началом игры
        self.root.after(5000, self.start_game)
    
    def start_game(self):
        # Заглушка для начала игры
        self.root.configure(bg="black")
        for widget in self.root.winfo_children():
            widget.destroy()
        
        game_label = tk.Label(self.root, text="Игра началась! (сюжетное развитие...)", font=("Helvetica", 18), fg="white", bg="black")
        game_label.pack(expand=True)
        
        # В этом месте в дальнейшем будет добавлена логика самой игры

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
