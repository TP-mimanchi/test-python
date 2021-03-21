class GameStats:
    """记录游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.sts

        self.game_begin = False
        self.reset_stats()
        # 统计分数
        self.score = 0
        self.high_score = 0

        # 等级
        self.ship_level = 1

    def reset_stats(self):
        """统计游戏期间的信息"""
        self.ships_num = self.settings.ship_limit
