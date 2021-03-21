import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """管理单个外星人"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.sts

        # 加载外星人图像并设置rect属性
        self.image = pygame.image.load('images/alien2.png')
        self.rect = self.image.get_rect()

        # 初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 记录外星人精准水平位置
        self.x = float(self.rect.x)

        # 判断单个外星人的左右移动1为右移-1为左移
        self.direction = 1

    def check_edges(self):
        """判断外星人是否碰到屏幕边缘，就返回True"""
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            return True

    def update(self):
        """更新外星人水平位置"""
        self.x += (self.setting.alien_speed * self.direction)
        self.rect.x = float(self.x)



