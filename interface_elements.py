# Імпорт модулів
import pygame
from abc import ABC, abstractmethod

# Класс графічного елемента (абстрактний класс для всіх інтерактивних елементів)
class GraphElement(ABC):
    # Абстрактний метод який додає функцію спостерігача
    @abstractmethod
    def add_observers_function(self, function):
        pass

    # Абстрактний метод виконує команди спостерігачів 
    @abstractmethod
    def notify_observers(self):
        pass


# Класс картинки
class Image():
    # Створення об'єкта Image
    def __init__(self, filename, pos, size):
        # Розмір та позиція картинки
        self.pos = pos
        self.size = size

        # Завантажування картинка та вставновлення її розміру
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, self.size)


    # Відмальовування картинки
    def draw(self, screen):
        screen.blit(self.image, self.pos)

# Класс кнопки
class Button(GraphElement):
    # Cтворення об'єкта Button
    def __init__(self, filename, pos, size, text = None):
        # Список функцій спостерігачів
        self.observers_functions = []

        # Розмір та позиція кнопки
        self.size = size
        self.pos = pos

        # Текстура кнопки
        self.image = Image(filename, self.pos, self.size)
        
        # Створення поле для відстеження натискання на цю кнопку
        self.rect = pygame.Rect(self.pos, self.size)

        # Текст кнопки (якщо не введено то None)
        self.text = text

    # Відмальовування кнопки
    def draw(self, screen):
        # Просто відмальовування кнопки
        self.image.draw(screen)

        # Якщо в кнопці є текст
        if self.text:
            # Змінні для ширини, висоти та x, y координат
            width, height = self.size
            x0, y0 = self.pos
            
            # Створення зображення тексту
            text = pygame.font.Font(None, 30).render(self.text, True, (0, 0, 0))

            # Обчислення координат тексту (вирівнювання по центру)
            pos = x0 + (width/2 - text.get_width()/2), y0 + (height/2 - text.get_height()/2)

            # Відмальовування тексту
            screen.blit(text, pos)

    # Додавання функції яка буде запущена при натискані на кнопку
    def add_observers_function(self, function):
        self.observers_functions.append(function)

    # Запуск функцій в self.observers_functions
    def notify_observers(self):
        for function in self.observers_functions:
            function()