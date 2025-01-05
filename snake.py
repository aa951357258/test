import pygame
import random
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    filename=f'snake_game_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 初始化 Pygame
pygame.init()
logging.info("游戏初始化成功")

# 设置游戏窗口
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 蛇的设置
snake_block = 20
snake_speed = 15
snake_x = window_width // 2
snake_y = window_height // 2
snake_dx = 0
snake_dy = 0
snake_body = []
snake_length = 1

# 食物设置
food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block

# 分数
score = 0

# 设置游戏时钟
clock = pygame.time.Clock()

# 显示分数
def show_score():
    font = pygame.font.SysFont(None, 50)
    score_text = font.render(f"得分: {score}", True, WHITE)
    window.blit(score_text, [10, 10])

# 游戏主循环
running = True
logging.info("游戏开始")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("游戏结束")
        
        # 键盘控制
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_dx != snake_block:
                snake_dx = -snake_block
                snake_dy = 0
                logging.debug("向左移动")
            elif event.key == pygame.K_RIGHT and snake_dx != -snake_block:
                snake_dx = snake_block
                snake_dy = 0
                logging.debug("向右移动")
            elif event.key == pygame.K_UP and snake_dy != snake_block:
                snake_dx = 0
                snake_dy = -snake_block
                logging.debug("向上移动")
            elif event.key == pygame.K_DOWN and snake_dy != -snake_block:
                snake_dx = 0
                snake_dy = snake_block
                logging.debug("向下移动")

    # 移动蛇
    snake_x += snake_dx
    snake_y += snake_dy

    # 检查边界碰撞
    if snake_x >= window_width or snake_x < 0 or snake_y >= window_height or snake_y < 0:
        running = False
        logging.info(f"游戏结束 - 撞墙 - 最终得分: {score}")

    # 更新蛇身
    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_body.append(snake_head)
    if len(snake_body) > snake_length:
        del snake_body[0]

    # 检查自身碰撞
    for segment in snake_body[:-1]:
        if segment == snake_head:
            running = False
            logging.info(f"游戏结束 - 自身碰撞 - 最终得分: {score}")

    # 检查是否吃到食物
    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
        snake_length += 1
        score += 10
        logging.info(f"得分增加 - 当前得分: {score}")

    # 绘制游戏画面
    window.fill(BLACK)
    
    # 绘制食物
    pygame.draw.rect(window, RED, [food_x, food_y, snake_block, snake_block])
    
    # 绘制蛇
    for segment in snake_body:
        pygame.draw.rect(window, GREEN, [segment[0], segment[1], snake_block, snake_block])
    
    # 显示分数
    show_score()
    
    # 更新显示
    pygame.display.update()
    
    # 控制游戏速度
    clock.tick(snake_speed)

# 退出游戏
pygame.quit() 