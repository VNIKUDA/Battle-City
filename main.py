# Імпортування модулів та класів
import pygame, ctypes
from interface_elements import Button, Image
from map_elements import Map
from player import Player, Bullet, Tank
pygame.init()
pygame.mixer.init()

# Отримання розмірів монітора
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Запис розмірів монітора у константи
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SIZE = (WIDTH, HEIGHT)

# Проценти в пікселі
width_procent = lambda num: num * WIDTH/100
height_procent = lambda num: num * HEIGHT/100

# Дозволенні взаємодії з програмою (для оптимізації)
allowed_events = [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT]
pygame.event.set_allowed(allowed_events)

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
        self.window.events = self.events


# Класс екрана головного меню
class MenuScreen(Screen):
    # Створення об'єкта MenuScreen
    def __init__(self, window):
        super().__init__(window)

        # Задній фон меню та лого
        self.bg = Image('static/images/menu_bg.png', (0, 0), SIZE)
        self.logo = Image('static/images/logo.png', (width_procent(0.5208333333333334), height_procent(-2.7777777777777777)), (width_procent(15.625), height_procent(37.03703703703704)))

        # Кнопка для запуску гри та виходу з гри
        self.start = Button('static/images/start.png', (width_procent(1.5625), height_procent(64.81481481481481)), (width_procent(22.135416666666668), height_procent(15.74074074074074)))
        self.quit = Button('static/images/quit.png', (width_procent(1.5625), height_procent(83.33333333333333)), (width_procent(19.53125), height_procent(13.888888888888888)))

        # Додавання реакцію на натискання для кожної кнопки
        self.start.add_observers_function(window.game_screen.change_screen)
        self.quit.add_observers_function(window.quit)

    # Відмальовування меню
    def draw(self):
        # Відмальовування фона та лого
        self.bg.draw(self)
        self.logo.draw(self)

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

        # Фон 
        self.bg = Image('static/images/game_bg.png', (0, 0), SIZE)

        # Гравець
        self.player = Player('static/images/E-100.png', (width_procent(46.09375), height_procent(50)), (width_procent(3.90625), height_procent(13.888888888888888)), 3.75, (width_procent, height_procent))

        Tank('static/images/Tiger-II.png', (width_procent(46.09375), height_procent(8.333333333333332)), (width_procent(3.90625), height_procent(13.88888888888889)), 3, (width_procent, height_procent))

        # Мапа
        self.map = Map('map.txt', SIZE, (width_procent, height_procent))


    # Відмальовування гри
    def draw(self):
        # Оновлення гравця (переміщення та поворот) та перевірка колізії
        self.player.update()
        self.map.collision(self.player)

        # Відмальовування фону, мапи та персонажа
        self.bg.draw(self)
        self.map.draw(self)

        self.player.draw(self)

        tanks = Tank.tanks[:]
        tanks.remove(self.player)

        for tank in tanks:
            tank.draw(self)
            

        for bullet in Bullet.bullets:
            bullet.move()
            bullet.kill()
            bullet.draw(self)


    # Обробник подій екрана
    def events(self, event):
        self.player.interact(event)


# Класс вікна
class Window():
    # Створення об'єкта Window
    def __init__(self):
        # Створення екрану в повноекраному режимі
        self.screen = pygame.display.set_mode(SIZE, flags = pygame.FULLSCREEN | pygame.DOUBLEBUF)

        # Створення clock для встановлення частоти оновлення екрану та константи FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Запускання фоновових звуких
        pygame.mixer.Sound('static/sounds/background.mp3').play(-1).set_volume(0.1)

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

        pygame.display.set_caption(str(self.clock.get_fps()))

    # Закриття вікна
    def quit(self):
        self.is_running = False

# Створення вікна
win = Window()

# Головний ігровий цикл
while win.is_running == True:
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