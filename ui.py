# player interface and score board
import pygame

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class UIManager:
    def __init__(self, screen):
        """初始化 UI 管理器"""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 50)
        self.score = 0
        self.level = 1

    def update_score(self, points):
        """更新分數"""
        self.score += points

    def next_level(self):
        """提升關卡"""
        self.level += 1

    def draw_score(self):
        """顯示分數"""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def draw_level(self):
        """顯示關卡"""
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (150, 10))

    def show_start_message(self):
        """顯示開始訊息"""
        start_text = self.large_font.render("Press Space to Start!", True, WHITE)
        self.screen.blit(start_text, (self.screen.get_width() // 2 - start_text.get_width() // 2, 
                                      self.screen.get_height() // 2 - start_text.get_height() // 2))

    def show_game_over(self):
        """顯示遊戲結束訊息"""
        game_over_text = self.large_font.render("Game Over", True, WHITE)
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2,
                                          self.screen.get_height() // 2 - game_over_text.get_height() // 2))
