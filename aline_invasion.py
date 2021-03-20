#!/usr/bin/env python
# @Time: 
# @Author:童鹏
# @File:aline_invasion.py


import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from aline import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlineInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""

        # 初始化背景设置
        pygame.init()

        self.sts = Settings()
        self.screen = pygame.display.set_mode(
            (self.sts.screen_width, self.sts.screen_height))
        pygame.display.set_caption("Aline Invasion")

        self.ship = Ship(self)

        # 创建用于储存游戏统计数据的实例
        self.stats = GameStats(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_freet()
        # 创建Play按钮
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)

    def _create_freet(self):
        """ 创建外星人"""
        alien = Alien(self)
        # 创建实例计算一行外星人
        ship_height = self.ship.rect.height
        alien_width, alien_height = alien.rect.size
        space_x = self.sts.screen_width - (2*alien_width)
        numberx_aliens = space_x // (2*alien_width)
        space_y = self.sts.screen_height - (3*alien_height) - ship_height
        numbery_aliens = space_y // (2*alien_height)
        self._create_aliens(numberx_aliens, numbery_aliens)

    def _create_aliens(self, numberx_aliens, numbery_aliens):
        """创建外星人并存入编组"""
        for y_alien in range(numbery_aliens):
            for x_alien in range(numberx_aliens):
                alien = Alien(self)
                alien_width, alien_height = alien.rect.size
                alien.x = alien_width + 2*alien_width*x_alien
                alien.rect.x = alien.x
                alien.rect.y = alien_height + 2*alien_height*y_alien
                self.aliens.add(alien)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()
            self._update_aliens()
            self._update_screen()

            # 判断游戏结束
            if self.stats.ships_num <= 0:
                self.stats.game_begin = False
                break

    def _update_aliens(self):
        """更新外星人位置"""
        # 先判断是否触碰边缘向下移动
        self._aliens_dip()
        self.aliens.update()

        # 检测飞船与外星人碰撞并删除再创建新飞船
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 判断外星人是否到底部边缘并创建新飞船
        if self._check_aliens_bottom():
            self._ship_hit()

    def _check_aliens_bottom(self):
        """检测外星人是否到达底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                return True

    def _ship_hit(self):
        """响应飞船被撞到或者其他飞船击毁条件"""
        # 暂停0.5秒，飞船数量减一
        self.stats.ships_num -= 1
        self.sb.prep_ships()

        self.bullets.empty()
        self.aliens.empty()
        # 创建新的飞船
        self._create_freet()
        self.ship.create_ship()
        #
        self.stats.game_begin = False
        pygame.mouse.set_visible(True)
        # 重置游戏
        self.sts.setting_speed()
        self.stats.score = 0
        self.sb.prep_score()
        # self.play_button = Button(self, "Play")

        sleep(0.5)

    def _aliens_dip(self):
        """判断触碰屏幕"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                alien.rect.y += self.sts.drop_speed
                alien.direction *= -1

    def _update_bullet(self):
        """更新子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 删除碰撞的子弹与外星人并创建新的外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.sts.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.prep_high_score()

        if not self.aliens:
            self.stats.ship_level += 1
            self.sb.prep_level()
            self._create_freet()
            self.sts.increase_speed()

    def _check_events(self):
        """响应按键和鼠标事件"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._events_keydown(event)

            elif event.type == pygame.KEYUP:
                self._events_keyup(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_mouse(mouse_pos)

    def _check_mouse(self, mouse_pos):
        """响应鼠标事件"""
        if not self.stats.game_begin and self.play_button.rect.collidepoint(mouse_pos):
            # 重置游戏
            self.stats.reset_stats()
            self.stats.game_begin = True
            # 清空子弹和外星人
            self.aliens.empty()
            self.bullets.empty()
            # 再创建
            self._create_freet()
            self.ship.create_ship()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _events_keydown(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """按空格键创建发射子弹"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _events_keyup(self, event):
        """松开按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕图像，并切换新屏幕"""

        # 每次都重绘屏幕
        self.screen.fill(self.sts.bg_color)

        if not self.stats.game_begin:
            self.play_button.draw_button()

        else:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

        self.sb.show_score()
        # 让最近绘制的屏幕可见
        pygame.display.update()


if __name__ == '__main__':
    # 创建游戏并运行

    ai = AlineInvasion()
    ai.run_game()

