# Імпорт модулів
import pygame


# Клас для гравця
class Player():
    # Створення об'єкта Player
    def __init__(self, filename, pos, size):
        # Розташування гравця та його розмір
        self.pos = pos
        self.size = size

        # Текстура гравця
        self.texture = pygame.image.load(filename)
        self.texture = pygame.transform.scale(self.texture, size)

        # Катринка гравця
        self.image = self.texture

        # Кут повороту, напрям повороту
        self.angle = 0
        self.rotate_direction = 1


    # Взаємодія з гравцем
    def interact(self, event):
        if event.type == pygame.KEYDOWN:
            x, y = self.pos

            # Рух гравця
            # Їздити вверх
            if event.key == pygame.K_w:
                self.pos = x, y - 5

            # Їздити вниз
            if event.key == pygame.K_s:
                self.pos = x, y + 5


            # Поворот гравця
            # Поворот вліво
            if event.key == pygame.K_a:
                self.rotate_direction = -1
                self.rotate()

            # Поворот вправо
            if event.key == pygame.K_d:
                self.rotate_direction = 1
                self.rotate()

    
    # Відмальовування гравця
    def draw(self, screen):
        screen.blit(self.image, self.pos)


    # Поворот гравця
    def rotate(self):
        self.angle += self.rotate_direction
        self.image = pygame.transform.rotozoom(self.texture, self.angle, 1)


    # Оновлення персонажа (поворот, переміщення)
    def update(self, screen):
        screen.blit(self.image, self.pos)

        # Якщо кут не 0, 90, 180, 270, 360
        print(str(self.angle / 90)[2])
        if str(self.angle / 90)[2] != '0':
            self.rotate()