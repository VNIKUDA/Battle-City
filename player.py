# Імпорт модулів
import pygame

# Математичний модуль
module = lambda num: num if num >= 0 else -num 

# Нормалізувати кут повороту (від -360 до 360)
def normalise_angle(angle):
    if angle >= 360:
        angle = angle - 360
    elif angle <= -360:
        angle = angle + 360

    return angle


# Клас танка
class Tank():
    # Створення об'єкта Tank
    def __init__(self, filename, pos, size):
        pass


# Клас для гравця
class Player():
    # Створення об'єкта Player
    def __init__(self, filename, pos, size, speed = 1):
        # Розташування гравця та його розмір
        self.pos = pos
        self.size = size

        # Швидкість гравця
        self.speed = speed

        # Текстура гравця
        self.texture = pygame.image.load(filename)
        self.texture = pygame.transform.scale(self.texture, size)
        self.texture = pygame.transform.rotozoom(self.texture, 180, 1)

        # Катринка гравця
        self.image = self.texture

        # Кут повороту, напрям повороту
        self.angle = 0
        self.rotate_direction = 1
        self.is_rotating = False # повертається

        # Вуктор руху та напрям руху (назад або вперед)
        self.vector = (0, 0) 
        self.drive_direction = 1
        self.is_driving = False # їздить

    # Взаємодія з гравцем
    def interact(self, event):
        if event.type == pygame.KEYDOWN:
            # Позиція гравця
            x, y = self.pos

            # Рух гравця
            # Їздити вверх
            if event.key == pygame.K_w and not self.is_rotating:
                self.drive_direction = 1
                self.move()
                self.is_driving = True

            # Їздити вниз
            if event.key == pygame.K_s and not self.is_rotating:
                self.drive_direction = -1
                self.move()
                self.is_driving = True


            # Поворот гравця
            # Поворот вліво
            if event.key == pygame.K_a and not self.is_driving:
                self.rotate_direction = 1
                self.rotate()
                self.is_rotating = True

            # Поворот вправо
            if event.key == pygame.K_d and not self.is_driving:
                self.rotate_direction = -1
                self.rotate()
                self.is_rotating = True

    
    # Відмальовування гравця
    def draw(self, screen):
        # Розмір та позиція 
        w, h = self.image.get_size()
        x, y = self.pos

        # Вираховування позиції гравця з вирівнюванням по центру (для анімації повороту) 
        pos = x - w/2, y - h/2

        # Відмальовування текстури гравця
        screen.blit(self.image, pos)


    # Рух граіця
    def move(self):
        # Визначення вектора руху
        # Якщо кут дорівнює нулю то вектор руху буде вверх
        if self.angle == 0:
            self.vector = 0, -1 * (self.drive_direction * self.speed)

        # Якщо кут дорівнює -270 або 90 то вектор руху вліво
        elif self.angle in (-270, 90):
            self.vector = -1 * (self.drive_direction * self.speed), 0

        # Якщо модуль кута дорівнює -180 то вектор руху вниз
        elif module(self.angle) == 180:
            self.vector = 0, self.speed * self.drive_direction

        # Якщо модуль кута дорівнює 90 то вектор руху вправо
        elif self.angle in (-90, 270):
            self.vector = self.speed * self.drive_direction, 0

        # Позиція та вектор
        x, y = self.pos
        x_offset, y_offset = self.vector

        # Переміщення
        self.pos = x + x_offset, y + y_offset


    # Поворот гравця
    def rotate(self):
        self.angle += self.speed/2 * self.rotate_direction
        self.angle = normalise_angle(self.angle)

        self.image = pygame.transform.rotozoom(self.texture, self.angle, 1)


    # Оновлення персонажа (поворот, переміщення)
    def update(self, screen):
        # Анімація повороту
        # Якщо при діленні поточного кута поворота на 90 результат має соті (тобто не ціле число)
        digits = str(round(module(self.angle / 90), 2))[2:4] # соті результату 
        if digits[-1] != '0' and self.is_rotating:
            self.rotate()
        else:
            self.is_rotating = False

        
        # Анімація руху
        # Якщо позиція гравця не вирівнина по сітці
        x, y = self.pos

        x_digits = str(round((x-135) / 150, 2))[-1]
        y_digits = str(round((y-90) / 150, 2))[-1]

        if (x_digits != '0' or y_digits != '0') and self.is_driving:
            self.move()
        else:
            self.is_driving = False


        # Відмальовування текстури
        self.draw(screen)