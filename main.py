# Імпортування модулів
import pygame, ctypes
pygame.init()

# Отримання розмірів монітора
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(0)
SIZE = (WIDTH, HEIGHT)

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

    # Відмальовування екрану
    def draw(self):
        pass

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

    # Оновлення екрану
    win.update_screen()