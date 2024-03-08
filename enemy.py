# Імпорт
from player import Tank
from random import randint
from heapq import heappush, heappop

# Класс ворога
class Enemy(Tank):
    def __init__(self, pos, size, speed, procents):
        self.textures = [
            'KV-2.png',
            'M-6.png',
            'VK-3601h.png',
            'Tiger-II.png'
        ]

        texture = self.textures[randint(0, 3)]
        filename = f'static/images/{texture}'

        super().__init__(filename, pos, size, speed, procents)
        super().update()


    def update(self, map):
        
        if self.is_driving == False and self.is_rotating == False and self.is_colliding == False:
            action = randint(0, 2)

            if action == 0:
                self.rotate_direction = [1, -1][randint(0, 1)]
                self.rotate()
                self.is_rotating = True

            elif action == 1:
                self.drive_direction = [1, -1][randint(0, 1)]
                self.move()
                self.is_driving = True

            elif action == 2:
                if self.bullets > 0:
                    self.shoot()

        super().update()
        map.collision(self)

# Спавн ворога
def spawn_enemy(map, player):
    # Функції для форматування процентів в пікселі
    width_procent, height_procent = player.width_procent, player.height_procent

    # Позиція гравця
    player_x, player_y = player.pos

    # Індекс гравця по горизонталі та вертикалі
    player_x_index = int(str((player_x - width_procent(7.03125)) / width_procent(7.8125)).split('.')[0])
    player_y_index = int(str((player_y - height_procent(8.333333333333333)) / height_procent(13.888888888888888)).split('.')[0])

    # Зона біля гравця, в якій не можна спавнити ворога
    player_x_area = [index for index in range(player_x_index - 1, player_x_index + 2) if index >= 0 and index <= 11]
    player_y_area = [index for index in range(player_y_index - 1, player_y_index + 2) if index >= 0 and index <= 6]

    # Координати елементів мапи в індексах
    map = [(int(str((block.rect.x + block.rect.w/2 - width_procent(3.125)) / width_procent(7.8125)).split('.')[0]), int(str((block.rect.y + block.rect.h/2 - height_procent(1.3888888888888888)) / height_procent(13.888888888888888)).split('.')[0])) for block in map.map][3:]

    # Координати танківв індексах
    tanks = [(int(str((tank.rect.x  + tank.rect.w/2 - width_procent(7.03125)) / width_procent(7.8125)).split('.')[0]), int(str((tank.rect.y + tank.rect.h/2 - height_procent(8.333333333333333)) / height_procent(13.888888888888888)).split('.')[0]) if int(str((tank.rect.y + tank.rect.h/2 - height_procent(8.333333333333333)) / height_procent(13.888888888888888)).split('.')[0]) == 0 else int(str((tank.rect.y + tank.rect.h/2 - height_procent(8.333333333333333)) / height_procent(13.888888888888888)).split('.')[0]) + 1)  for tank in Tank.tanks]

    # Рандомний спавн ворога
    x, y = randint(0, 11), randint(0, 6)

    # Поки позиція ворога є в забороненій зоні
    while (x in player_x_area and y in player_y_area) or (x, y) in map or (x, y) in tanks:
        x, y = randint(0, 11), randint(0, 6)

    # Координати ворога
    pos = width_procent(7.03125) + x * width_procent(7.8125), height_procent(8.333333333333333) + y * height_procent(13.888888888888888)

    # Створення ворога
    Enemy(pos, (width_procent(3.90625), height_procent(13.888888888888888)), 3, (width_procent, height_procent))

# Спавн ворогів
def spawn_enemies(map, player):
    # Якщо кількість танків менше  (3 вороги + гравець)
    max_num_of_tanks = int(str(player.score / 300).split('.')[0])
    if len(Tank.tanks) < 2 + max_num_of_tanks:
        # Створити ворога
        spawn_enemy(map, player)

