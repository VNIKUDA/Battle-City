# Імпорт модулів
import pygame
from interface_elements import Image
from player import Bullet
pygame.init()


# Клас для перешкод
class Block():
    # Створення об'єкта Block
    def __init__(self, filename, pos, size):
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
    def __init__(self, filename, window_size, procents):
        # Розмір вікна
        self.SIZE = window_size
        self.WIDTH, self.HEIGHT = self.SIZE

        # Проценти від ширини та висоти вікна
        width_procent, height_procent = procents

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
            Block('static/images/block.png', (x*width_procent(7.8125) + width_procent(3.125), y*height_procent(13.888888888888888) + height_procent(1.3888888888888888)), (width_procent(7.8125), height_procent(13.888888888888888)))

            for y, line in enumerate(self.map)
            for x, elem in enumerate(line)

            if elem != '.' # "." = пропуск
        ]

        # Кордони мапи
        borders = [
            Block('static/images/nothing.png', (0, 0), (self.WIDTH, height_procent(1.3888888888888888))), # верхній блок мапи
            Block('static/images/nothing.png', (0, 0), (width_procent(3.125), self.HEIGHT)), # лівий блок мапи
            Block('static/images/nothing.png', (0, self.HEIGHT - height_procent(1.3888888888888888)), (self.WIDTH, height_procent(1.3888888888888888))), # нижній блок мапи
            Block('static/images/nothing.png', (self.WIDTH - width_procent(3.125), 0), (width_procent(3.125), self.HEIGHT)) # правий блок мапи
        ]
    
        # Додання кордонів мапи до мапи
        self.map = borders + self.map


    # Колізія перешкод з гравцем
    def collision(self, player):
        # Перевірка колізії для кожної перешкоди
        player_collided = [
            block
            for block in self.map
            if (block.rect.collidepoint(player.front) and player.is_colliding == False) or (block.rect.collidepoint(player.back) and player.is_colliding == False)
        ]

        bullet_collided = [
            bullet

            for block in self.map
            for bullet in Bullet.bullets

            if block.rect.colliderect(bullet.rect)
        ]


        for bullet in bullet_collided:
            Bullet.bullets.remove(bullet)
            del bullet

        
        # Якщо колізія відбулась то дати зворотній напрям танку
        if player_collided != []:
            player.drive_direction *= -1
            player.move()

            player.is_colliding = True

        # Якщо колізії не відбулось
        else:
            player.is_colliding = False
       

    # Відмальовування карти
    def draw(self, screen):
        for block in self.map:
            block.draw(screen)