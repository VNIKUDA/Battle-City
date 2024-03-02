# Імпорт модулів
import pygame
import time

# Математичний модуль
module = lambda num: num if num >= 0 else -num 

# Нормалізувати кут повороту (від -360 до 360)
def normalise_angle(angle):
    if angle >= 360:
        angle = angle - 360
    elif angle <= -360:
        angle = angle + 360

    return angle

class Bullet():
    bullets = []

    def __init__(self, pos, size, tank):
        self.pos = pos
        self.size = size

        x_offset, y_offset = tank.vector
        self.direction = (x_offset, y_offset) if tank.drive_direction == 1 else (-x_offset, -y_offset)

        self.speed = tank.speed
        self.tank = tank

        self.texture = pygame.image.load('static/rocket.png')
        self.texture = pygame.transform.scale(self.texture, size)
        self.texture = pygame.transform.rotozoom(self.texture, tank.angle, 1)

        self.size = self.texture.get_size()

        self.rect = pygame.Rect(self.pos, self.size)

        Bullet.bullets.append(self)

    def draw(self, screen):
        x, y = self.pos
        w, h = self.size

        pos = x - w/2, y - h/2

        screen.blit(self.texture, pos)

    def move(self):
        x, y = self.pos

        x_offset, y_offset = self.direction

        self.pos = x + (x_offset * self.speed), y + (y_offset * self.speed)

        self.rect = pygame.Rect(self.pos, self.size)

    def kill(self):
        for tank in Tank.tanks:
            if self.rect.colliderect(tank.rect) and tank != self.tank:
                Tank.tanks.remove(tank)
                Bullet.bullets.remove(self)

                del tank
                del self


# Клас танка
class Tank():
    tanks = []
    # Створення об'єкта Tank
    def __init__(self, filename, pos, size, speed):
        # Розташування гравця та його розмір
        self.pos = pos
        self.size = size

        # Хітбокс
        self.rect = pygame.Rect(self.pos, self.size)

        # Життя та патрони гравця
        self.health = 3
        self.bullets = 3

        # Перезарядка
        self.recharge_tick = 0

        # Швидкість гравця
        self.speed = speed

        # Текстура гравця
        self.texture = pygame.image.load(filename)
        self.texture = pygame.transform.scale(self.texture, size)
        self.texture = pygame.transform.rotozoom(self.texture, 180, 1)

        # Катринка гравця
        self.image = self.texture

        # Розмір картинки (для виправлення багу при повороті)
        self.size = self.image.get_size()

        # Кут повороту, напрям повороту
        self.angle = 0
        self.rotate_direction = 1
        self.is_rotating = False # повертається

        # Вуктор руху та напрям руху (назад або вперед)
        self.vector = (0, 0) 
        self.drive_direction = 1
        self.is_driving = False # їздить

        # Перед та зад танка для перевірки колізії з перешкодами
        x, y = self.pos
        w, h = self.size
        self.back = (x, y + h/2)
        self.front = (x, y - h/2)

        # Змінна яка перевіряє чи є колізія між гравцем та перешкодою на мапі
        self.is_colliding = False

        Tank.tanks.append(self)

    # Рух граіця
    def move(self):
        x, y = self.pos
        w, h = self.size

        # Визначення вектора руху
        # Якщо кут дорівнює нулю то вектор руху буде вверх
        if self.angle == 0:
            self.vector = 0, -1 * (self.drive_direction * self.speed)

            # Колізія
            self.back = (x, y + h/2 - self.speed/2)
            self.front = (x, y - h/2 + self.speed/2)

        # Якщо кут дорівнює -270 або 90 то вектор руху вліво
        elif self.angle in (-270, 90):
            self.vector = -1 * (self.drive_direction * self.speed), 0

            # Колізія
            self.back = (x + w/2 - self.speed/2, y)
            self.front = (x - w/2 + self.speed/2, y)

        # Якщо модуль кута дорівнює -180 то вектор руху вниз
        elif module(self.angle) == 180:
            self.vector = 0, self.speed * self.drive_direction

            # Колізія
            self.back = (x, y - h/2 + self.speed/2)
            self.front = (x, y + h/2 - self.speed/2)

        # Якщо модуль кута дорівнює 90 то вектор руху вправо
        elif self.angle in (-90, 270):
            self.vector = self.speed * self.drive_direction, 0

            # Колізія
            self.back = (x - w/2 + self.speed/2, y)
            self.front = (x + w/2 - self.speed/2, y)

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
    def update(self):
        # Позиція та розмір
        x, y = self.pos
        w, h = self.size

        # Оновлення хітбокса танку
        self.rect = pygame.Rect(self.pos, self.size)
        

        # Анімація повороту
        # Якщо при діленні поточного кута поворота на 90 результат має соті (тобто не ціле число)
        digits = str(round(module(self.angle / 90), 2))[2:4] # соті результату 
        if digits[-1] != '0' and self.is_rotating:
            self.rotate()
        else:
            self.is_rotating = False

        # Визначення вектора руху
        # Якщо кут дорівнює нулю то вектор руху буде вверх
        if self.angle == 0:
            self.vector = 0, -1 * (self.drive_direction * self.speed)

            # Колізія
            self.back = (x, y + h/2 - self.speed/2)
            self.front = (x, y - h/2 + self.speed/2)

        # Якщо кут дорівнює -270 або 90 то вектор руху вліво
        elif self.angle in (-270, 90):
            self.vector = -1 * (self.drive_direction * self.speed), 0

            # Колізія
            self.back = (x + w/2 - self.speed/2, y)
            self.front = (x - w/2 + self.speed/2, y)

        # Якщо модуль кута дорівнює -180 то вектор руху вниз
        elif module(self.angle) == 180:
            self.vector = 0, self.speed * self.drive_direction

            # Колізія
            self.back = (x, y - h/2 + self.speed/2)
            self.front = (x, y + h/2 - self.speed/2)

        # Якщо модуль кута дорівнює 90 то вектор руху вправо
        elif self.angle in (-90, 270):
            self.vector = self.speed * self.drive_direction, 0

            # Колізія
            self.back = (x - w/2 + self.speed/2, y)
            self.front = (x + w/2 - self.speed/2, y)

        
        # Анімація руху
        # Якщо позиція гравця не вирівнина по сітці
        x_digits = str(round((x-135) / 150, 2))[-1]
        y_digits = str(round((y-90) / 150, 2))[-1]

        if (x_digits != '0' or y_digits != '0') and (self.is_driving == True):
            self.move()
        else:
            self.is_driving = False


        # Перезарядка патронів
        if self.bullets < 3:
            self.recharge_tick += 0.012

            if self.recharge_tick >= 1:
                self.bullets += 1
                self.recharge_tick = 0


    def shoot(self):
        size = 25, 50
        Bullet(self.pos, size, self)
        self.bullets -= 1

    # Відмальовування гравця
    def draw(self, screen):
        # Розмір та позиція 
        w, h = self.image.get_size()
        x, y = self.pos

        self.size = self.image.get_size()

        # Вираховування позиції гравця з вирівнюванням по центру (для анімації повороту) 
        pos = x - w/2, y - h/2

        # Відмальовування текстури гравця
        screen.blit(self.image, pos)

# Клас для гравця
class Player(Tank):
    # Створення об'єкта Player
    def __init__(self, filename, pos, size, speed):
        super().__init__(filename, pos, size, speed)

        # Текстурка хп
        self.hp_texture = pygame.image.load('static/hp.png')
        self.hp_texture = pygame.transform.scale(self.hp_texture, (50, 50))

        # Текстура патронів
        self.rockets_texture = pygame.image.load('static/rockets.png')
        self.rockets_texture = pygame.transform.scale(self.rockets_texture, (100, 25))
        self.rockets_texture = pygame.transform.rotozoom(self.rockets_texture, 45, 1)

    # Взаємодія з гравцем
    def interact(self, event):
        if event.type == pygame.KEYDOWN:
            # Позиція гравця
            x, y = self.pos

            # Вистріл
            if event.key == pygame.K_SPACE and (not self.is_rotating and not self.is_driving and not self.is_colliding) and self.bullets > 0:
                self.shoot()

            # Рух гравця
            # Їздити вверх
            if event.key == pygame.K_w and (not self.is_rotating and not self.is_driving and not self.is_colliding):
                self.drive_direction = 1
                self.move()
                self.is_driving = True

            # Їздити вниз
            if event.key == pygame.K_s and (not self.is_rotating and not self.is_driving and not self.is_colliding):
                self.drive_direction = -1
                self.move()
                self.is_driving = True


            # Поворот гравця
            # Поворот вліво
            if event.key == pygame.K_a and (not self.is_rotating and not self.is_driving and not self.is_colliding):
                self.rotate_direction = 1
                self.rotate()
                self.is_rotating = True

            # Поворот вправо
            if event.key == pygame.K_d and (not self.is_rotating and not self.is_driving and not self.is_colliding):
                self.rotate_direction = -1
                self.rotate()
                self.is_rotating = True

    # Відмальовування гравця
    def draw(self, screen):
        # Розмір та позиція 
        w, h = self.image.get_size()
        x, y = self.pos

        self.size = self.image.get_size()

        # Вираховування позиції гравця з вирівнюванням по центру (для анімації повороту) 
        pos = x - w/2, y - h/2

        # Відмальовування текстури гравця
        screen.blit(self.image, pos)

        # Інтерфейс здоров'я
        for x, i in enumerate(range(self.health)):
            screen.blit(self.hp_texture, (1700 + x*70, 15))

        # Інтерфейс патронів
        for x, index in enumerate(range(self.bullets)):
            screen.blit(self.rockets_texture, (15+x*75, 5))