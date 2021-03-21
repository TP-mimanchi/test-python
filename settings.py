
class Settings:
    """储存游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""

        # 屏幕设置(像素，颜色)
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 5, 5)

        # 飞船速度(像素个数),数量
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 子弹设置(速度，大小，颜色)
        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_height = 8
        self.bullet_color = (200, 10, 10)

        # 外星人设置
        self.alien_speed = 0.5
        self.drop_speed = 90
        self.alien_points = 100

        # 游戏节奏
        self.speed_scale = 1.3

    def setting_speed(self):
        """开始速度"""
        self.alien_speed = 0.5
        self.bullet_speed = 0.5
        self.ship_speed = 1.5

    def increase_speed(self):
        """增加速度"""
        self.alien_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.ship_speed *= self.speed_scale