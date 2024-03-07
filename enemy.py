# Імпорт
from player import Tank
from random import randint


# Клас ворога
class Enemy(Tank):
    # Створення об'єкта Enemy
    def __init__(self, filename, pos, size, speed, procents):
        super().__init__(filename, pos, size, speed, procents)

        self.path = []


# Спавн ворога
def spawn_enemy(map, player):
    width_procent, height_procent = player.width_procent, player.height_procent

    player_x, player_y = player.pos

    player_x_index = int(str((player_x - width_procent(7.03125)) / width_procent(7.8125)).split('.')[0])
    player_y_index = int(str((player_y - height_procent(8.333333333333333)) / height_procent(13.888888888888888)).split('.')[0])

    player_x_area = [index for index in range(player_x_index - 1, player_x_index + 2) if index >= 0 and index <= 11]
    player_y_area = [index for index in range(player_y_index - 1, player_y_index + 2) if index >= 0 and index <= 6]

    map = [(int(str((block.rect.x + block.rect.w/2 - width_procent(3.125)) / width_procent(7.8125)).split('.')[0]), int(str((block.rect.y + block.rect.h/2 - height_procent(1.3888888888888888)) / height_procent(13.888888888888888)).split('.')[0])) for block in map.map][3:]

    tanks = [(int(str((tank.rect.x - width_procent(7.03125)) / width_procent(7.8125)).split('.')[0]), int(str((tank.rect.y - height_procent(8.333333333333333)) / height_procent(13.888888888888888)).split('.')[0])) for tank in Tank.tanks]

    x, y = randint(0, 11), randint(0, 6)
    while (x in player_x_area and y in player_y_area) or (x, y) in map or (x, y) in tanks:
        x, y = randint(0, 11), randint(0, 6)


    pos = width_procent(7.03125) + x * width_procent(7.8125), height_procent(8.333333333333333) + y * height_procent(13.888888888888888)

    Enemy('static/images/Tiger-II.png', pos, (width_procent(3.90625), height_procent(13.888888888888888)), 3, (width_procent, height_procent))

# Спавн ворогів
def spawn_enemies(map, player):
    # Якщо кількість танків менше 4 (3 вороги + гравець)
    if len(Tank.tanks) < 4:
        
        spawn_enemy(map, player)

