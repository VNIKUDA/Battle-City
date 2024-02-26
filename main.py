# Імпортування модулів та класів
import pygame, ctypes
from interface_elements import Button
from map_elements import Map
pygame.init()

# Отримання розмірів монітора
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Запис розмірів екрану у константи
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SIZE = (WIDTH, HEIGHT)

# Батьківський класс екранів
class Screen():
    # Створення об'єкту Screen
    def __init__(self, window):
        self.window = window

        # Скорочення запису функції відмальовування елементів на екрані
        self.blit = self.window.screen.blit

    # Переключення поточного екрану на цей
    def change_screen(self):
        self.window.draw = self.draw


# Класс екрана головного меню
class MenuScreen(Screen):
    # Створення об'єкта MenuScreen
    def __init__(self, window):
        super().__init__(window)

        # Задній фон меню
        self.bg = pygame.image.load('static/menu_bg.png')
        self.bg = pygame.transform.scale(self.bg, SIZE)

        # Кнопка для запуску гри та виходу з гри
        self.start = Button('static/start.png', (30, 700), (425, 170))
        self.quit = Button('static/quit.png', (30, 900), (375, 150))

        # Додавання реакцію на натискання для кожної кнопки
        self.start.add_observers_function(window.game_screen.change_screen)
        self.quit.add_observers_function(window.quit)

    # Відмальовування меню
    def draw(self):
        # Відмальовування фона
        self.blit(self.bg, (0, 0))

        # Відмальовування кнопок
        self.start.draw(self)
        self.quit.draw(self)

    # Обробник подій екрана
    def events(self, event):
        # Якщо натиснута ліва кнопка миші
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # Якщо натиснуто на старт
            if self.start.rect.collidepoint(x, y):
                self.start.notify_observers()

            # Якщо натиснуто на вихід
            elif self.quit.rect.collidepoint(x, y):
                self.quit.notify_observers()


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
        print('game')

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