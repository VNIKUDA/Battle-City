# Імпорт модулів
import pygame
from interface_elements import Image


# Клас для перешкод
class Block():
    # Створення об'єкта Block
    def __init__(self, filename, pos, size, is_breakable = False):
        # Позиція та розмір перешкоди
        self.pos = pos
        self.size = size

        # Завантаження текстури перешкоди та встановлення розміру
        self.image = Image(filename, pos, size)

        # Хітбокс об'єкту
        self.rect = pygame.Rect(self.pos, self.size)


    # Відмальовування об'єкта
    def draw(self, screen):
        self.image.draw(screen)


# Клас для завантаження та конвертування схеми мапи в об'єкт
class Map():
    # Створення об'єкта Map
    def __init__(self, filename):
        # Зчитування файлу з мапою
        with open(filename, 'r') as file:
            self.file = file.readlines()

        # Конвертування файлу в схему мапи
        self.map = [
            line.split()
            for line in self.file
        ]

        # Створення об'єктів (перешкод) в мапі
        self.map = [
            Block('static/block.png', (x*150 + 60, y*150 + 15), (150, 150))

            for y, line in enumerate(self.map)
            for x, elem in enumerate(line)

            if elem != '.' # "." = пропуск
        ]


    # Колізія перешкод з гравцем
    def collision(self, player):
        # Перевірка колізії для кожної перешкоди
        collided = [
            block
            for block in self.map
            if (block.rect.collidepoint(player.front) and player.is_colliding == False) or (block.rect.collidepoint(player.back) and player.is_colliding == False)
        ]

        
        # Якщо колізія відбулась то дати зворотній напрям танку
        if collided != []:
            player.drive_direction *= -1

            player.is_colliding = True
            player.is_driving = True


        else:
            player.is_colliding = False

        

    # Відмальовування карти
    def draw(self, screen):
        for block in self.map:
            block.draw(screen)