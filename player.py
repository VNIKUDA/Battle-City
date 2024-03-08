# Імпорт модулів
import pygame
from game_elements import Tank
pygame.init()
pygame.mixer.init()

Sound = pygame.mixer.Sound

# Клас для гравця
class Player(Tank):
    # Створення об'єкта Player
    def __init__(self, filename, pos, size, speed, procents):
        super().__init__(filename, pos, size, speed, procents)

        # Життя та патрони гравця (їх більше ніж у ворогів)
        self.health = 3
        self.bullets = 3
        self.max_bullets = self.bullets

        self.score = 0

        # Звук їзди гравця
        self.driving_sound = Sound('static/sounds/driving.mp3')
        self.driving_sound.set_volume(0.04)

        # Звуки стояння
        self.idle_sound = Sound('static/sounds/idle.mp3')
        self.idle_sound.set_volume(0.3)

        # Текстурка хп
        self.hp_texture = pygame.image.load('static/images/hp.png').convert_alpha()
        self.hp_texture = pygame.transform.scale(self.hp_texture, (self.width_procent(2.604166666666667), self.height_procent(4.62962962962963)))

        # Текстура патронів
        self.rockets_texture = pygame.image.load('static/images/rockets.png').convert_alpha()
        self.rockets_texture = pygame.transform.scale(self.rockets_texture, (self.width_procent(5.208333333333334), self.height_procent(2.314814814814815)))
        self.rockets_texture = pygame.transform.rotozoom(self.rockets_texture, 45, 1)

        self.FONT = pygame.font.Font('static/font.ttf', int(self.height_procent(5)))


    # Взаємодія з гравцем
    def interact(self, event):
        if event.type == pygame.KEYDOWN:
            # Позиція гравця
            x, y = self.pos

            # Звуки
            # Якщо натиснуто вперед або назад + вправо та вліво
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d) and (not self.is_driving and not self.is_rotating):
                pygame.mixer.Sound.stop(self.idle_sound)
                self.driving_sound.play()
            

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
     

    def update(self):
        super().update()
        if self.recharge_tick == 1:            
            self.reloading_sound.play()


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

        # Перевірка звуку їзди
        if (self.is_driving == False and self.is_rotating == False) and self.idle_sound.get_num_channels() == 0: 
            pygame.mixer.Sound.stop(self.driving_sound)
            self.idle_sound.play(-1, fade_ms=10)

        if self.health != 0 and self.score != 3000:
            # Інтерфейс здоров'я
            for x, i in enumerate(range(self.health)):
                screen.blit(self.hp_texture, (self.width_procent(99.47916666666667) - x*self.width_procent(3.6458333333333335)  - self.width_procent(2.604166666666667), self.height_procent(1.3888888888888888)))

            # Інтерфейс патронів
            for x, index in enumerate(range(self.bullets)):
                screen.blit(self.rockets_texture, (self.width_procent(0.78125) + x*self.width_procent(3.90625), self.height_procent(0.4629629629629629)))

            score = self.FONT.render(str(self.score), True, (255, 255, 255)).convert_alpha()
            pos = self.width_procent(50) - score.get_width()/2, self.height_procent(3.62962962962963) - score.get_height()/2
            
            screen.blit(score, pos)