import json

class GameStats:
    '''Відстежувати статистику гри'''
    def __init__(self, ai_game):
        '''Ініціалізація статистики'''
        self.settings = ai_game.settings
        self.reset_stats()
        filename = 'highscores.json'
        with open(filename) as f:
            high = json.load(f)
        self.game_active = False
        self.high_score = high

    def reset_stats(self):
        '''Ініціалізація статистики що може змінюватись впродовж гри'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1