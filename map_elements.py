# Імпорт модулів
import pygame


# Клас для перешкод
class Block():
    # Створення об'єкта Block
    def __init__(self, filename, pos, size, is_breakable = False):
        # Позиція та розмір перешкоди
        self.pos = pos
        self.size = size

        # Завантаження текстури перешкоди та встановлення розміру
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, self.size)

        # Хітбокс об'єкту
        self.rect = pygame.Rect(self.pos, self.size)

        # Можливість розламування об'єкта через постріл
        self.is_breakable = is_breakable


    # Відмальовування об'єкта
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

# Клас для завантаження та конвертування схеми мапи в об'єкт
class Map():
    # Створення об'єкта Map
    def __init__(self, filename):
        # Зчитування файлу з мапою
        with open(filename, 'r') as file:
            self.file = file.readlines()

        # 
        self.map = [
            line.split()
            for line in self.file
        ]



        