# Імпорт модулів
import pygame
from abc import ABC, abstractmethod

# Класс постачальника (абстрактний класс для всіх графічних елементів)
class Subject(ABC):
    # Абстрактний метод сповіщає всіх спостеріначів та виконує команду пов'язану з ними
    @abstractmethod
    def notify_observers(self):
        pass