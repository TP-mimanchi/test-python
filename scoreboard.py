import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """显示分数"""

    def __init__(self, ai_game):
        """初始化信息"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.sts
        self.stats = ai_game.stats

        # 显示的字体设置
        self.text_color = (255, 255, 255)
        self.text_font = pygame.font.SysFont(None, 25)

        # 准备图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """显示飞窜数量"""
        self.ships = Group()
        for number in range(self.stats.ships_num):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship.rect.width * number
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        """显示文本图像"""
        round_score = round(self.stats.score, -1)
        score_str = "{:,}".format(round_score)
        self.score_image = self.text_font.render(score_str, True, self.text_color)

        # 显示在屏幕右上角
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = self.screen_rect.top + 20

    def prep_high_score(self):
        """显示历史最高"""
        if self.stats.high_score < self.stats.score:
            self.stats.high_score = self.stats.score
        round_score = round(self.stats.high_score, -1)
        score_str = "{:,}".format(round_score)
        st = f"Height Score:{score_str}"
        self.high_score_image = self.text_font.render(st, True, self.text_color)

        # 显示
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.top = self.screen_rect.top
        self.high_score_image_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        """显示等级"""
        level_str = f"Level:{self.stats.ship_level}"
        self.level_image = self.text_font.render(level_str, True, self.text_color)

        # 显示
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.top = self.screen_rect.top + 40
        self.level_image_rect.right = self.screen_rect.right - 20

    def show_score(self):
        """显示分数"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)



