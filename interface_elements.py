# Імпорт модулів
import pygame
from abc import ABC, abstractmethod

# Класс графічного елемента (абстрактний класс для всіх графічних елементів)
class GraphElement(ABC):
    # Абстрактний метод який додає функцію спостерігача
    @abstractmethod
    def add_observers_function(self, function):
        pass

    # Абстрактний метод виконує команди спостерігачів 
    @abstractmethod
    def notify_observers(self):
        pass


# Класс кнопки
class Button(GraphElement):
    # Cтворення об'єкта Button
    def __init__(self, pos, filename):
        # Список функцій спостерігачів
        self.observers_functions = []

        # Текстура кнопки
        self.image = pygame.image.load(filename)
        
        # Створення rect для відстеження натискання на цю кнопку та встановлення позиції rect-а
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    # Додавання функції яка буде запущена при натискані на кнопку
    def add_observers_function(self, function):
        self.observers_functions.append(function)

    # Запуск функцій в self.observers_functions
    def notify_observers(self):
        for function in self.observers_functions:
            function()