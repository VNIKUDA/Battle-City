# Імпортування модулів
import pygame, ctypes
from interface_elements import Button
pygame.init()

# Отримання розмірів монітора
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Запис розмірів екрану у константи
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(0)
SIZE = (WIDTH, HEIGHT)


# Батьківський класс екранів
class Screen():
    # Створення об'єкту Screen
    def __init__(self, window):
        self.window = window

        # Скорочення запису функції відмальовування елементів на екрані
        self.blit = self.window.screen.blit

    # Переключення екрану на цей
    def change_screen(self):
        self.window.draw = self.draw


# Класс екрана головного меню
class MenuScreen(Screen):
    # Створення об'єкта MenuScreen
    def __init__(self, window):
        super().__init__(window)

    # Відмальовування меню
    def draw(self):
        pass

    # Обробник подій екрана
    def events(self, event):
        pass


# Класс екрану налаштувань
class SettingScreen(Screen):
    # Створення об'єкта SettingScreen
    def __init__(self, window):
        super().__init__(window)

    # Відмальовування налаштувань
    def draw(self):
        pass

    # Обробник подій екрана
    def events(self, event):
        pass


# Класс ігрового екрану
class GameScreen(Screen):
    # Створення об'єкта GameScreen
    def __init__(self, window):
        super().__init__(window)

    # Відмальовування гри
    def draw(self):
        pass

    # Обробник подій екрана
    def events(self, event):
        pass


# Класс вікна
class Window():
    # Створення об'єкта Window
    def __init__(self):
        # Створення екрану в повноекраному режимі
        self.screen = pygame.display.set_mode(SIZE, flags=pygame.FULLSCREEN)

        # Створення clock для встановлення частоти оновлення екрану та константи FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Змінна яка відповідає за роботу програми
        self.is_running = True

        # Cтворення всіх екранів
        self.game_screen = GameScreen(self)
        self.setting_screen = SettingScreen(self)
        self.menu_screen = MenuScreen(self)

        # Назначення функцій відмальовування екрану та обробника подій (за замовчуванням - меню)
        self.draw = self.menu_screen.draw
        self.events = self.menu_screen.events

    # Оновлення екрану
    def update_screen(self):
        pygame.display.update()
        self.clock.tick(self.FPS)

    # Закриття вікна
    def quit(self):
        self.is_running = False

# Створення вікна
win = Window()

# Головний ігровий цикл
while win.is_running == True:
    win.screen.fill((255, 255, 255))

    # Обробник подій
    for event in pygame.event.get():
        # Якщо закрито програму то вийти з головного ігрового циклу
        if event.type == pygame.QUIT:
            win.quit()

        # Обробник подій поточного екрану
        win.events(event)

    # Відмальовування поточного екрану
    win.draw() 

    # Оновлення екрану
    win.update_screen()