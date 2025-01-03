# Game main file
from ball import Ball
from brick import Brick
from ui import UIManager
from shooter import Shooter
from add_icon import AddIcon
from leaderboard import Leaderboard
from math import cos, sin, radians
import pygame
import random
import time

pygame.init()  # initialize pygame

#game setting
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1100
FPS = 60
BALL_SPEED = 20
BRICK_WIDTH, BRICK_HEIGHT = 100, 100

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) 

#initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BBTAN Game")
clock = pygame.time.Clock()
leaderboard = Leaderboard()

#initialize game objects
def  init_game():
    balls = []
    bricks = []
    add_icon = []
    level = 1
    generate_bricks(bricks, add_icon, level)
    return balls, bricks, add_icon, level

# 在第二排生成磚塊
def generate_bricks(bricks, add_icon, level):
    """每回合在第二排生成 2~3 個磚塊，耐久度等於等級"""
    new_bricks = random.randint(2, 3)
    positions = random.sample(range(7), new_bricks)
    add_icon_position = random.choice(range(7))  # 隨機選擇一個位置生成加號球
    print(f"🎯 Brick Position: {positions}")
    print(f"🎯 Add Icon Position: {add_icon_position}")
    for pos in positions:
        if pos == add_icon_position:
            continue  # 如果是加號球位置則跳過
        x = pos * (BRICK_WIDTH + 5) + 10
        y = 50  # 第二排 Y 軸位置
        strength = level  # 磚塊耐久度等於當前等級
        bricks.append(Brick(x, y, strength))
    # 生成加號球
    x = add_icon_position * (BRICK_WIDTH + 5) + 10-50+100
    y = 50+50
    add_icon.append(AddIcon(x, y))
        
# 磚塊向下移動
def move_bricks_down(bricks, add_icon):
    """將所有磚塊向下移動一格"""
    for brick in bricks:
        brick.y += BRICK_HEIGHT + 5
    for icon in add_icon:
        icon.y += BRICK_HEIGHT + 5

# 繪製底線
def draw_bottom_line(screen):
    """在最後一排磚塊下方繪製一條底線"""
    line_y = 890  # 底線的 Y 軸位置，可以根據磚塊排數調整
    pygame.draw.line(screen, WHITE, (0, line_y), (SCREEN_WIDTH, line_y), 3)

# 顯示 Game Over 畫面
def show_game_over(screen, final_score):
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text, text_rect)

    # 顯示玩家分數
    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(f"Your Score: {final_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, score_rect)

    # 玩家名稱輸入
    input_font = pygame.font.Font(None, 36)
    player_name = ""
    input_active = True  # 輸入模式啟動

    while input_active:
        screen.fill(BLACK)

        # 繪製 Game Over 和分數
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)

        # 玩家名稱輸入框
        input_text = input_font.render(f"Enter Your Name: {player_name}", True, WHITE)
        input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(input_text, input_rect)

        # 提示按鍵
        sub_font = pygame.font.Font(None, 36)
        restart_text = sub_font.render("Press Enter to Submit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    leaderboard.add_score(player_name, final_score)
                    input_active = False  # 結束名稱輸入
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 10 and event.unicode.isalnum():
                    player_name += event.unicode

    # 顯示高分榜
    scores = leaderboard.get_scores()
    leaderboard_font = pygame.font.Font(None, 36)
    y_offset = SCREEN_HEIGHT // 2 + 150
    screen.blit(leaderboard_font.render("Leaderboard:", True, WHITE), (SCREEN_WIDTH // 2 - 80, y_offset))

    for i, (name, score) in enumerate(scores):
        entry_text = leaderboard_font.render(f"{i + 1}. {name}: {score}", True, WHITE)
        screen.blit(entry_text, (SCREEN_WIDTH // 2 - 80, y_offset + 40 + i * 30))

    # 提示重新開始或退出
    restart_text = sub_font.render("Press R to Restart or Q to Quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 370))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    # 等待玩家選擇 R 或 Q
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # 重新開始遊戲
                    waiting_for_input = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    balls, bricks, add_icon, level= init_game()
    shooter = Shooter(400, 950)  # 發射人物
    ui_manager = UIManager(screen)  # UI 管理器
    angle = 90  # 初始發射角度
    ball_ready = True  # 控制小球發射狀態
    round_over = False
    has_shot = False  #檢查玩家是否已發射
    running = True
    game_over = False  # Game Over 狀態
    # 按鍵冷卻時間（毫秒）
    KEY_COOLDOWN = 70  # 200毫秒
    last_key_time = pygame.time.get_ticks()  # 記錄上次按鍵時間
    BALL_INTERVAL = 0.1  # 小球發射間隔時間（秒）
    last_ball_time = pygame.time.get_ticks()  # 記錄上次發射小球時間
    ball_index = 0  # 紀錄發射的小球數量
    first_ball_x = shooter.x  # 記錄第一顆球的落點
    while running:
        screen.fill(BLACK)

        if game_over:
            show_game_over(screen, ui_manager.score)
    

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # 按鍵冷卻邏輯
        current_time = pygame.time.get_ticks()
        # 按鍵控制邏輯
        keys = pygame.key.get_pressed()
        if current_time - last_key_time > KEY_COOLDOWN:
            if keys[pygame.K_LEFT]:
                angle += 1
                shooter.adjust_angle(-1)
                if angle > 150:
                    angle = 150
                last_key_time = current_time  # 更新冷卻時間

            if keys[pygame.K_RIGHT]:
                angle -= 1
                shooter.adjust_angle(1)
            #print(shooter.get_angle())
                if angle < 30:
                    angle = 30
                last_key_time = current_time  # 更新冷卻時間

        if keys[pygame.K_SPACE] and ball_ready and not has_shot and not round_over:
            #balls.append(Ball(400, 950, BALL_SPEED, angle))
            ball_ready = False
            has_shot = True
            #ball_shot_count = shooter.ball_count
            ball_index = 0
            last_ball_time = pygame.time.get_ticks()
            time.sleep(0.1)
            print("🎯 Ball Shot!")

        current_time = pygame.time.get_ticks()
        if has_shot and ball_index < shooter.ball_count:
            if current_time - last_ball_time >= BALL_INTERVAL:
                balls.append(Ball(shooter.x, shooter.y, BALL_SPEED, angle))
                last_ball_time = current_time  # 更新上次發射時間
                ball_index += 1  # 移到下一顆球
                #if ball_index == shooter.ball_count:
                #    first_ball_x = balls[-1].x
                #    print(f"🎯 First Ball X: {first_ball_x}")    

            

        if not keys[pygame.K_SPACE]:
            ball_ready = True
        #結束按鍵控制邏輯 key:q
        if keys[pygame.K_q]:
            running = False 

        # 更新小球邏輯
        for ball in balls:
            ball.move()
            ball.draw(screen)

            # 小球與磚塊碰撞檢測
            for brick in bricks[:]:
                if (
                    brick.x < ball.x < brick.x + brick.width and
                    brick.y < ball.y < brick.y + brick.height
                ):
                    #bricks.remove(brick)
                    brick.hit()
                    if brick.strength <= 0:
                        bricks.remove(brick)
                    ball.dy *= -1
                    ui_manager.update_score(10)  # 每擊中一個磚塊加 10 分
                    break
            # 小球與加號球碰撞檢測
            for icon in add_icon[:]:
                if icon.check_collision(ball):
                    shooter.add_ball()
                    add_icon.remove(icon)
                    print("🎯 Ball Added!")

            first_ball_x = balls[0].x
            #print(f"🎯 First Ball X: {first_ball_x}")
        # 回合邏輯
        if has_shot and all(ball.y >= 950 for ball in balls):
            round_over = True
            ui_manager.next_level()

        if round_over:
            shooter.x = first_ball_x
            move_bricks_down(bricks, add_icon)
            #shooter.add_ball()
            balls.clear()
            level += 1
            generate_bricks(bricks, add_icon, level)
            print(f"🎯 Level Up! Current Level: {level}")
            has_shot = False  # 重置發射狀態
            round_over = False

        # 繪製磚塊
        for brick in bricks:
            brick.draw(screen)
        for icon in add_icon:
            icon.draw(screen)
        draw_bottom_line(screen)
        # 繪製發射人物
        #shooter.draw(screen)
        #shooter.draw_aiming_line(screen)

        # 更新 UI
        #ui_manager.draw_score()
        #ui_manager.draw_level()
        

        # 檢查遊戲結束條件
        for brick in bricks:
            if brick.y + brick.height >= 900:
                print("🚨 A brick has reached the bottom line! Game Over!")
                #running = False
                final_score = ui_manager.score  # 獲取當前分數
                show_game_over(screen, final_score)
                game_over = True

        # 顯示 UI
        font = pygame.font.Font(None, 36)
        #angle_text = font.render(f"Angle: {angle}", True, WHITE)
        #screen.blit(angle_text, (10, 80))
        ball_count_text = font.render(f"Balls: {shooter.ball_count}", True, WHITE)
        screen.blit(ball_count_text, (300, 10))
        ui_manager.draw_score()
        ui_manager.draw_level()
        shooter.draw(screen)
        shooter.draw_aiming_line(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


# 啟動遊戲
if __name__ == "__main__":
    main()
        