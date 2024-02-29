import keyboard #кнопка чек

class Player():
    def __init__(self, x2, y2):
        self.x2 = x2
        self.y2 = y2
        self.direction2 = "up"

    def upravlenie(self, x, y):
        if keyboard.is_pressed('w'):
            self.x2 + 1
        if keyboard.is_pressed('s'):
            self.y2 - 1
        if keyboard.is_pressed('d'):
            self.x2 + 1
        if keyboard.is_pressed('a'):
            self.x2 - 1

    def shooot(self, x2, x1):
        pass #хз как

class EnemyTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "up"

    def move_towards_player(self, player_x, player_y):
        if player_x > self.x:
            self.direction = "right"
        elif player_x < self.x:
            self.direction = "left"
        elif player_y > self.y:
            self.direction = "down"
        elif player_y < self.y:
            self.direction = "up"

    
    def rotate_towards_direction(self, direction):
        self.direction = direction

    def move_forward(self):
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "right":
            self.x += 1

    def move_backward(self):
        if self.direction == "up":
            self.y += 1
        elif self.direction == "down":
            self.y -= 1
        elif self.direction == "left":
            self.x += 1
        elif self.direction == "right":
            self.x -= 1

    def shoot(self, player_x, player_y):
        if self.x == player_x or self.y == player_y: 
            self.rotate_towards_player(player_x, player_y) 
            print("Enemy tank shoots at player!") #логика пока такая тк я не понял как сделать фулл класс патрона и добавлять его в список патрон
        else:
            print("Enemy tank can't shoot.")

    def is_shoot(self, player_x, player_y):
        if self.x == player_x or self.y == player_y: 
            return True
        else:
            return False

enemy = EnemyTank(2, 2)
player_x, player_y = 5, 5

enemy.move_towards_player(player_x, player_y)
enemy.move_forward()
enemy.shoot(player_x, player_y)

if enemy.is_shoot(player_x, player_y):
    del enemy
