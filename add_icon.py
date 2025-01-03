import pygame

# 顏色
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


class AddIcon:
    def __init__(self, x, y):
        """初始化加號球"""
        self.x = x
        self.y = y
        self.radius = 15  # 加號球的大小
        self.color = GREEN
        self.image = pygame.image.load("images/jerry.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def draw(self, screen):
        """繪製加號球"""
        #pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # 繪製加號標誌
        #pygame.draw.line(screen, WHITE, (self.x - 5, self.y), (self.x + 5, self.y), 2)
        #pygame.draw.line(screen, WHITE, (self.x, self.y - 5), (self.x, self.y + 5), 2)
        # from rat.jpg
        #add_icon = pygame.image.load("images/rat.jpg")
        screen.blit(self.image, (self.x-15, self.y-15))


    def check_collision(self, ball):
        """檢查與小球的碰撞"""
        distance = ((self.x - ball.x)**2 + (self.y - ball.y)**2)**0.5
        return distance <= self.radius + ball.radius
