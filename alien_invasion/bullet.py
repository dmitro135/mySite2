import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Клас для керування кулями'''
    def __init__(self, ai_game):
        super().__init__() # Успадкування значень Sprite
        self.screen = ai_game.screen # Передаєм значення екрану
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height) # Створюєм прямоутник
        self.rect.midtop = ai_game.ship.rect.midtop # Розташовуєм прямокутник

        self.y = float(self.rect.y)

    def update(self):
        '''Метод який оновлює значення координат кулі'''
        self.y -= self.settings.bullet_speed # Update values
        self.rect.y = self.y # Присвоюєм значенню rect значення x


    def draw_bullet(self):
        '''Метод який малює кулю'''
        pygame.draw.rect(self.screen, self.color, self.rect)

