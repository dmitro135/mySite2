import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''Клас відповідальний за прибульців'''
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien1000.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height # Початкове місце появи дорівнює числу його висоти і ширини

        self.x = float(self.rect.x)

    def update(self):
        '''Метод відповідальний за оновлення координат флоту'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def _check_edges(self):
        '''Метод відповідальний за контроль кордонів'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True





