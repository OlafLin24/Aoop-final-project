# ball definition and movement
import pygame
from math import cos, sin, radians

# 顏色設定
WHITE = (255, 255, 255)

class Ball:
    def __init__(self, x, y, speed, angle):
        """初始化小球"""
        self.x = x
        self.y = y
        self.radius = 8
        self.speed = speed
        self.angle = radians(angle)
        self.dx = self.speed * cos(self.angle)
        self.dy = -self.speed * sin(self.angle)

    def move(self):
        """小球移動邏輯"""
        self.x += self.dx
        self.y += self.dy

        # 碰到牆壁時反彈
        if self.x <= 0 or self.x >= 800:  # 假設螢幕寬度為 400
            self.dx *= -1
        if self.y <= 0:
            self.dy *= -1

    def draw(self, screen):
        """繪製小球"""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def bounce(self):
        """小球反彈"""
        self.dy *= -1
