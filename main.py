# Імпортування модулів та класів
import pygame, ctypes
from interface_elements import Button, Image
from game_elements import Map, Bullet, Tank
from player import Player
from enemy import spawn_enemies
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
        self.start.add_observers_function(self.restart)
        self.quit.add_observers_function(window.quit)

    def restart(self):
        Tank.tanks = []
        Bullet.bullets = []
        self.window.game_screen = GameScreen(self.window)
        self.window.game_screen.change_screen()

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
class EndScreen(Screen):
    # Створення об'єкта EndScreen
    def __init__(self, window):
        super().__init__(window)

        self.bg = Image('static/images/end_bg.png', (0, 0), SIZE)

        self.win = Image('static/images/you_win.png', (width_procent(50) - width_procent(18.22916666666667), height_procent(30) - height_procent(20.83333333333333)), (width_procent(36.45833333333333), height_procent(41.66666666666667)))
        self.lose = Image('static/images/you_lose.png', (width_procent(50) - width_procent(18.22916666666667), height_procent(30) - height_procent(20.83333333333333)), (width_procent(36.45833333333333), height_procent(41.66666666666667)))

        self.menu = Button('static/images/menu.png', (width_procent(50) - width_procent(6.510416666666667), height_procent(70) - height_procent(5.787037037037037)), (width_procent(13.02083333333333), height_procent(11.57407407407407)))
        self.restart = Button('static/images/retry.png', (width_procent(50) - width_procent(6.510416666666667), height_procent(85) - height_procent(5.787037037037037)), (width_procent(13.02083333333333), height_procent(11.57407407407407)))

        self.menu.add_observers_function(self.window.menu_screen.change_screen)
        self.restart.add_observers_function(self.window.menu_screen.restart)

        self.FONT = pygame.font.Font('static/font.ttf',  int(height_procent(5)))
        self.player = self.window.game_screen.player


    # Відмальовування налаштувань
    def draw(self):
        self.window.game_screen.draw()
        self.bg.draw(self)

        self.player = self.window.game_screen.player
        self.score = self.FONT.render(f'Score: {self.player.score}', True, (230, 230, 230)).convert_alpha()

        if self.player.score >= 3000:
            self.win.draw(self)
        elif self.player.health == 0:
            self.lose.draw(self)

        self.blit(self.score, (width_procent(50) - self.score.get_width()/2, height_procent(55) - self.score.get_height()/2))

        self.menu.draw(self)
        self.restart.draw(self)


    # Обробник подій екрана
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if self.menu.rect.collidepoint(x, y):
                self.menu.notify_observers()

            if self.restart.rect.collidepoint(x, y):
                self.restart.notify_observers()


# Класс ігрового екрану
class GameScreen(Screen):
    # Створення об'єкта GameScreen
    def __init__(self, window):
        super().__init__(window)

        # Фон 
        self.bg = Image('static/images/game_bg.png', (0, 0), SIZE)

        # Гравець
        self.player = Player('static/images/E-100.png', (width_procent(46.09375), height_procent(50)), (width_procent(3.90625), height_procent(13.888888888888888)), 3.75, (width_procent, height_procent))

        # Мапа
        self.map = Map('map.txt', SIZE, (width_procent, height_procent))


    # Відмальовування гри
    def draw(self):
        tanks = Tank.tanks
        # Якщо гравець живий
        if self.player.health > 0:
            # Спавн ворогів
            spawn_enemies(self.map, self.player)

            # Оновлення гравця (переміщення та поворот) та перевірка колізії
            self.player.update()
            self.map.collision(self.player)

            # Оновлення танків крім гравця
            tanks = tanks[:]
            tanks.remove(self.player)

            for tank in tanks:
                tank.update(self.map)

            # Оновлення пуль
            for bullet in Bullet.bullets:
                bullet.move()
                bullet.kill()

        # Якщо гравець мертвий то поміняти екран на кінцевий
        elif self.player.health == 0 and self.window.draw == self.draw:
            self.window.end_screen.change_screen()

        # Якщо гравцеь досягнув 3000 очків то перейти на кінцевий екран
        if self.player.score == 3000:
            self.player.health = 0
            self.window.end_screen.change_screen()

        # Відмальовування фону, мапи та персонажа
        self.bg.draw(self)
        self.map.draw(self)

        # Відмальовування пуль
        for bullet in Bullet.bullets:
            bullet.draw(self)

        # Відмальовування танків
        for tank in tanks:
            tank.draw(self)
            # pygame.draw.rect(self.window.screen, (0, 0, 0), tank.rect)

        if self.player.health != 0:
            self.player.draw(self)


    # Обробник подій екрана
    def events(self, event):
        self.player.interact(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.window.menu_screen.change_screen()


# Класс вікна
class Window():
    # Створення об'єкта Window
    def __init__(self):
        # Створення екрану в повноекраному режимі
        self.screen = pygame.display.set_mode(SIZE, flags = pygame.FULLSCREEN | pygame.DOUBLEBUF)

        # Назва програми та іконка
        icon = pygame.image.load('static/images/icon.png').convert_alpha()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Battle city HD Remake")

        # Створення clock для встановлення частоти оновлення екрану та константи FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Запускання фоновових звуких
        bg_sound = pygame.mixer.Sound('static\\sounds\\background.mp3')
        bg_sound.set_volume(0.1)
        bg_sound.play(-1)

        # Змінна яка відповідає за роботу програми
        self.is_running = True

        # Cтворення всіх екранів
        self.game_screen = GameScreen(self)
        self.menu_screen = MenuScreen(self)
        self.end_screen = EndScreen(self)

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