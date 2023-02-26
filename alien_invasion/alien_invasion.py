import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from eazy_button import EazyButton
from hard_button import HardButton
from scoreboard import Scoreboard
from alien_bullets import AlienBullets


class AlienInvasion:
    '''Загальний клас для керування гри'''
    def __init__(self):
        ''' Game initialization'''
        pygame.init() # Initialization pygame
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Create a size of window
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invasion') # Set the main caption in window
        # Створити екземпляр для збереження ігрової статистики
        self.stats = GameStats(self)

        # Створити екземпляр для збереження ігрової статистики та табло на екрані
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # Атрибут який створює ігровий список
        self.alien = Alien(self)
        self.alien_bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Create a play button
        self.play_button = Button(self, 'Play')
        self.eazy_button = EazyButton(self, 'Eazy')
        self.hard_button = HardButton(self, 'Hard')

    def run_game(self):
        '''Метод відповідальний за процесс гри'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()
                self._update_alien_bullets()
            self._update_screen()

    def _check_events(self):
        # Create a event dispetcher
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Exit from sys module
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_eazy_button(mouse_pos)
                self._check_hard_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        '''Розпочати нову гру коли клристувач натисне кнопку'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dinamic_settings()
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _check_eazy_button(self, mouse_pos):
        button_clicked = self.eazy_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 0.3
            self.settings.initialize_dinamic_settings()
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


    def _check_hard_button(self, mouse_pos):
        button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 0.8
            self.settings.initialize_dinamic_settings()
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()




    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True

        # озбавитись прибульців та куль
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()



        # Create new fleet and centralize a ship
        self._create_fleet()
        self.ship.center_ship()

        # nahui cursor
        pygame.mouse.set_visible(False)



    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
            self._fire_alien_bullet()
        if event.key == pygame.K_p:
            self._start_game()
            self.settings.initialize_dinamic_settings()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_q:
            sys.exit()

    def _create_fleet(self):
        '''Метод який створює інопланетний флот'''
        alien = Alien(self) # Create an atribute
        alien_width, alien_height = alien.rect.size
        avaible_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaible_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        avaible_space_y = (self.settings.screen_height - (2 * alien_height) - ship_height)
        number_rows = avaible_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)  # Fill window with custom color
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score() # Намалювати інформацію про рахунок

        # Draw a play button
        if not self.stats.game_active:
            self.play_button.draw_button()
        if not self.stats.game_active:
            self.eazy_button.draw_button()
        if not self.stats.game_active:
            self.hard_button.draw_button()
        pygame.display.flip()  # Перемалювання екрану на кожній іттерації циклу

    def _update_bullets(self):
        '''Метод відповідальний за оновлення куль'''
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.bottom >= 1000:
                self.alien_bullets.remove(alien_bullet)


    def _check_bullet_alien_collision(self):
        # Перевіряємо чи зіткнулись прямокутники кулі та прибульця
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)

            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty() # Видаляємо старі кулі
            self.alien_bullets.empty()
            self._create_fleet() # Створюєм новий флот
            self.settings.increase_speed()

            # Збільшити рівень
            self.stats.level += 1
            self.sb.prep_level()


    def _update_alien(self):
        '''Метод відповідальний за пересування прибульців'''
        self._check_fleet_edges()
        self.aliens.update()
        # Шукати зіткнення прибульців і корабля
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        '''Реагує на те чи досяг флот краю екрана'''
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Метод відповідальний за зміну напрямку'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _fire_bullet(self):
        '''Метод відповідальний за постріли'''
        if len(self.bullets) < self.settings.bullets_alowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_alien_bullet(self):
        new_bullet = AlienBullets(self)
        self.alien_bullets.add(new_bullet)

    def _ship_hit(self):
        '''Реагувати на зіткнення прибульців з кораблем'''
        if self.stats.ships_left > 0:
            # Зменшити ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Позбавитись надлишку прибульців та куль
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Створити новий флот та відцентрувати корабель
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        # Pause
        sleep(0.5)

    def _check_aliens_bottom(self):
        '''Перевірити чи не досяг прибулець низу екрана'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Зреагувати ніби підбито корабель
                self._ship_hit()
                break





if __name__ == '__main__': # Створення екземпляру гри та її запуск
    ai = AlienInvasion()
    ai.run_game()


