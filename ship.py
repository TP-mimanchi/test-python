import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船"""

    def __init__(self, ai_game):
        """初始化飞船属性并设置位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.sts

        # 加载飞船图像并获取外接矩形
        self.image = pygame.image.load('images/ship1.png')
        self.rect = self.image.get_rect()

        # 对于飞船将它放于底部
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # 飞船移动
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动方向调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def create_ship(self):
        """创建飞船并居于底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)