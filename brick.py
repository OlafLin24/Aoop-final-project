# brick definition and collision detection
import pygame

# 顏色設定
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Brick:
    def __init__(self, x, y, strength):
        """初始化磚塊"""
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.strength = strength  # 耐久度 (被擊中次數減少)

    def draw(self, screen):
        """繪製磚塊"""
        color = RED if self.strength == 1 else BLUE
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.strength), True, WHITE)
        screen.blit(text, (self.x + self.width // 2 - 8, self.y + self.height // 2 - 12))

    def hit(self):
        """被小球擊中時減少耐久度"""
        self.strength -= 1
        return self.strength <= 0  # 如果強度小於等於0，回傳True (磚塊消失)
