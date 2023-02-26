import pygame.font

class EazyButton:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 100, 30
        self.button_color = (0, 230, 0)
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 38)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midleft = self.screen_rect.midleft

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

