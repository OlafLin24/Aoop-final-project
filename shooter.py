import pygame
from math import radians, cos, sin

# 顏色設定
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
class Shooter:
    def __init__(self, x, y):
        """初始化發射人物"""
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.angle = 90  # 初始發射角度
        self.image = None
        self.ball_count = 1  # 初始球數量為1

        # 嘗試載入圖片，若失敗則使用預設形狀
        try:
            self.image = pygame.image.load("images/tom.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except FileNotFoundError:
            self.image = None

    def draw(self, screen):
        """繪製發射人物"""
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, -self.angle)
            rect = rotated_image.get_rect(center=(self.x, self.y))
            screen.blit(rotated_image, rect.topleft)
        else:
            # 如果沒有圖片，使用三角形作為替代
            points = [
                (self.x, self.y - 20),  # 上方頂點
                (self.x - 20, self.y + 20),  # 左下角
                (self.x + 20, self.y + 20)   # 右下角
            ]
            pygame.draw.polygon(screen, WHITE, points)

    def draw_aiming_line(self, screen):
        """繪製發射輔助線"""
        # 計算輔助線的終點
        length = 1200  # 輔助線長度
        end_x = self.x + length * cos(radians(180 - self.angle))
        end_y = self.y - length * sin(radians(180 - self.angle))
        #print(self.angle)
        # 繪製輔助線
        pygame.draw.line(screen, GREEN, (self.x, self.y), (end_x, end_y), 2)
        # 輔助線終點標記
        pygame.draw.circle(screen, GREEN, (int(end_x), int(end_y)), 5)

    def adjust_angle(self, delta):
        """調整發射角度"""
        self.angle += delta
        if self.angle < 30:
            self.angle = 30
        if self.angle > 150:
            self.angle = 150

    def get_angle(self):
        """返回發射角度"""
        return self.angle
    def add_ball(self, count=1):
        """增加持有的球數量"""
        self.ball_count += count
