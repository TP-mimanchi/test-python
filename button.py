import pygame.font

class Button:
    """创建标签矩形按钮"""

    def __init__(self, ai_game, msg):
        """初始化按钮"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 初始化按钮属性（宽度，高度，颜色，字体颜色，字体形式与大小）
        self.width, self.height = 200, 50
        self.color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮并设置位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 创建按钮中的文本并设置位置
        self.msg_image = self.font.render(msg, True, self.text_color, self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """在屏幕绘制矩形按钮，再填充文本"""
        self.screen.fill(self.color, self.rect)
        # 向矩型传递图像以及相关联的rect
        self.screen.blit(self.msg_image, self.msg_image_rect)