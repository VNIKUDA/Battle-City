# Імпорт модулів
import pygame
from interface_elements import Image
pygame.init()
pygame.mixer.init()

Sound = pygame.mixer.Sound

# Математичний модуль
module = lambda num: num if num >= 0 else -num

# Нормалізувати кут повороту (від -360 до 360)
def normalise_angle(angle):
    if angle >= 360:
        angle = angle - 360
    elif angle <= -360:
        angle = angle + 360

    return angle


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

# Класс снаряда
class Bullet():
    # Список патронів
    bullets = []

    # Створення об'єкта Bullet
    def __init__(self, pos, size, tank):
        # Позиція та розмір снаряда
        self.pos = pos
        self.size = size

        # Вектор руху снаряда та її швидкість
        x_offset, y_offset = tank.vector
        self.direction = (x_offset, y_offset) if tank.drive_direction == 1 else (-x_offset, -y_offset)
        self.x_speed, self.y_speed = tank.x_speed * 2, tank.y_speed * 2

        # Танк який вистрілив
        self.tank = tank

        # Текстура снаряда
        self.texture = pygame.image.load('static/images/rocket.png').convert_alpha()
        self.texture = pygame.transform.scale(self.texture, size)
        self.texture = pygame.transform.rotozoom(self.texture, tank.angle, 1)

        # Оновлений розмір (через поворот текстури)
        self.size = self.texture.get_size()

        # Хітбокс
        self.rect = pygame.Rect(self.pos, self.size)

        # Звук вибуху
        self.boom_sound = Sound('static/sounds/boom.mp3')
        self.boom_sound.set_volume(0.2)

        # Додавання до списку снарядів
        Bullet.bullets.append(self)

    # Відмальовування снаряда
    def draw(self, screen):
        # Розмір та позиція
        x, y = self.pos
        w, h = self.size

        # Координати текстури
        pos = x - w/2, y - h/2

        # Відмальовування текстури
        screen.blit(self.texture, pos)

    # Переміщення снаряда
    def move(self):
        # Позиція
        x, y = self.pos

        # Вектор руху
        x_offset, y_offset = self.direction

        # Нові координати
        self.pos = x + (x_offset * self.x_speed), y + (y_offset * self.y_speed)

        # Оновлення хітбокса
        self.rect = pygame.Rect(self.pos, self.size)

    # Перевірка на колізію для знищення
    def kill(self):
        # Перевірка для всіх танків
        for tank in Tank.tanks:
            # Якщо снаряд попав в танк і це не той танк що вистрілив снарядом
            if self.rect.colliderect(tank.rect) and tank != self.tank:
                # Зменшити здоров'я
                tank.health -= 1

                # Програти звук вибуху від попадання
                self.boom_sound.play()

                self.tank.score += 100

                # Видалення снаряда
                Bullet.bullets.remove(self)
                del self

                # Якщо танк мертвий то видалити з програми
                if tank.health == 0:
                    Tank.tanks.remove(tank)
                    del tank

                # Вийти з циклу
                break
                    

# Клас танка
class Tank():
    tanks = []
    # Створення об'єкта Tank
    def __init__(self, filename, pos, size, speed, procents):
        # Розташування гравця та його розмір
        self.pos = pos
        self.size = size

        self.width_procent, self.height_procent = procents

        # Хітбокс
        x, y = self.pos
        w, h = self.size
        self.block = Block('static/images/block.png', (x - w/2, y - h/2), (h, h))
        # self.rect = pygame.Rect((x - w/2, y - h/2), self.size)
        self.rect = self.block.rect

        # Життя та nпатрони танка
        self.health = 1
        self.bullets = 1
        self.max_bullets = self.bullets

        # Перезарядка
        self.recharge_tick = 0

        # Швидкість гравця
        self.speed = speed
        self.x_speed, self.y_speed = self.width_procent(speed/19.2), self.height_procent(speed/10.8)

        # Текстура гравця
        self.texture = pygame.image.load(filename).convert_alpha()
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
        
        self.back = (x, y + h/2)
        self.front = (x, y - h/2)

        # Змінна яка перевіряє чи є колізія між гравцем та перешкодою на мапі
        self.is_colliding = False

        # Звук пострілу
        self.shooting_sound = Sound('static/sounds/shoot.mp3')
        self.shooting_sound.set_volume(0.5)

        # Звук перезарядки
        self.reloading_sound = Sound('static/sounds/reload.wav')
        self.reloading_sound.set_volume(0.5)

        # Балли
        self.score = 0

        Tank.tanks.append(self)

    # Рух граіця
    def move(self):
        x, y = self.pos
        w, h = self.size



        # Визначення вектора руху
        # Якщо кут дорівнює нулю то вектор руху буде вверх
        if self.angle == 0:
            self.vector = 0, -1 * (self.drive_direction * self.y_speed)

            # Колізія
            self.back = (x, y + h/2 - self.y_speed*2.5)
            self.front = (x, y - h/2 + self.y_speed*2.5)

        # Якщо кут дорівнює -270 або 90 то вектор руху вліво
        elif self.angle in (-270, 90):
            self.vector = -1 * (self.drive_direction * self.x_speed), 0

            # Колізія
            self.back = (x + w/2 - self.x_speed*2.5, y)
            self.front = (x - w/2 + self.x_speed*2.5, y)

        # Якщо модуль кута дорівнює -180 то вектор руху вниз
        elif module(self.angle) == 180:
            self.vector = 0, self.y_speed * self.drive_direction

            # Колізія
            self.back = (x, y - h/2 + self.y_speed*2.5)
            self.front = (x, y + h/2 - self.y_speed*2.5)

        # Якщо модуль кута дорівнює 90 то вектор руху вправо
        elif self.angle in (-90, 270):
            self.vector = self.x_speed * self.drive_direction, 0

            # Колізія
            self.back = (x - w/2 + self.x_speed*2.5, y)
            self.front = (x + w/2 - self.x_speed*2.5, y)

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
            self.vector = 0, -1 * (self.drive_direction * self.y_speed)

            # Колізія
            self.back = (x, y + h/2 - self.y_speed*2.5)
            self.front = (x, y - h/2 + self.y_speed*2.5)

        # Якщо кут дорівнює -270 або 90 то вектор руху вліво
        elif self.angle in (-270, 90):
            self.vector = -1 * (self.drive_direction * self.x_speed), 0

            # Колізія
            self.back = (x + w/2 - self.x_speed*2.5, y)
            self.front = (x - w/2 + self.x_speed*2.5, y)

        # Якщо модуль кута дорівнює -180 то вектор руху вниз
        elif module(self.angle) == 180:
            self.vector = 0, self.y_speed * self.drive_direction

            # Колізія
            self.back = (x, y - h/2 + self.y_speed*2.5)
            self.front = (x, y + h/2 - self.y_speed*2.5)

        # Якщо модуль кута дорівнює 90 то вектор руху вправо
        elif self.angle in (-90, 270):
            self.vector = self.x_speed * self.drive_direction, 0

            # Колізія
            self.back = (x - w/2 + self.x_speed*2.5, y)
            self.front = (x + w/2 - self.x_speed*2.5, y)

        
        # Анімація руху
        # Якщо позиція гравця не вирівнина по сітці
        x_digits = str(round((x-self.width_procent(7.03125)) / self.width_procent(7.8125), 2))[-1]
        y_digits = str(round((y-self.height_procent(8.333333333333332)) / self.height_procent(13.888888888888888), 2))[-1]

        if (x_digits != '0' or y_digits != '0') and (self.is_driving == True):
            self.move()
        else:
            self.is_driving = False


        # Перезарядка патронів
        if self.bullets < self.max_bullets:
            self.recharge_tick += 0.01

            if self.recharge_tick >= 1:
                self.bullets += 1
                self.recharge_tick = 0

        # Оновлення хітбокса танку
        self.block = Block('static/images/block.png', (x - h/2, y - h/2), (h, h))
        self.rect = self.block.rect


    # Вистріл
    def shoot(self):
        self.shooting_sound.play()
        size = self.width_procent(1.3020833333333335), self.height_procent(4.62962962962963)
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

    # Колізія перешкод з танком
    def collision(self, tank):
        # Перевірка колізії для кожної перешкоди
        tank_collided = [
            block
            for block in self.map
            if (block.rect.collidepoint(tank.front) and tank.is_colliding == False) or (block.rect.collidepoint(tank.back) and tank.is_colliding == False)
        ]

        tanks = Tank.tanks[:]
        tanks.remove(tank)
        tank_rects_collided = [tank_.block for tank_ in tanks if (tank_.block.rect.collidepoint(tank.front) and tank.is_colliding == False) or (tank_.block.rect.collidepoint(tank.back) and tank.is_colliding == False)] 


        bullet_collided = [
            bullet

            for block in self.map
            for bullet in Bullet.bullets

            if block.rect.colliderect(bullet.rect)
        ]


        # Якщо снаряд попав в блок то знищити та запустити звук вибуху
        for bullet in bullet_collided:
            Bullet.bullets.remove(bullet)
            bullet.boom_sound.play()
            del bullet

        
        # Якщо колізія відбулась то дати зворотній напрям танку
        if tank_collided != [] or tank_rects_collided:
            tank.drive_direction *= -1
            for i in range(2):
                tank.move()

            tank.is_colliding = True

        # Якщо колізії не відбулось
        else:
            tank.is_colliding = False
       

    # Відмальовування карти
    def draw(self, screen):
        for block in self.map:
            block.draw(screen)