import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Класс для керування кораблем'''
    def __init__(self, ai_game):
        super().__init__()
        '''Ініціалізація корабля'''
        self.screen = ai_game.screen # Зберігаємо екран щоб до нього було зручно звертатись
        self.screen_rect = self.screen.get_rect() # Щоб потім правильно розташувати корабель
        self.settings = ai_game.settings # Отримуєм доступ до налаштувань

        self.image = pygame.image.load('images/pixel ship1000.bmp') # Load the ship image
        self.rect = self.image.get_rect() # Робим корабель прямокутником

        self.rect.midbottom = self.screen_rect.midbottom # Розташовуєм корабель

        self.x = float(self.rect.x)  # Змінна яка містить дробові координати

        self.moving_right = False # Індикатор руху
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x # Оновлюєм rect.х з self.x

    def blitme(self):
        ''' Метод який малюэ корабель'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def train_mode(self):
        self.rect.midleft = self.screen_rect.left
        self.y = float(self.rect.y)
