# Імпорт модулів
import pygame
from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def notify_observers(self):
        pass