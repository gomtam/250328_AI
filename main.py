import pygame
import random
import time
import os

# 게임 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 게임 화면 설정
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('스네이크 게임')

# 게임 속도 설정
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# 폰트 설정 - 한글 지원 폰트 사용
# 시스템에 설치된 기본 폰트 사용 (맑은 고딕, 굴림, 등)
try:
    # Windows 환경
    if os.name == 'nt':
        font_style = pygame.font.SysFont("malgun gothic", 25)  # 맑은 고딕
        score_font = pygame.font.SysFont("malgun gothic", 35)
    # Mac 환경
    elif os.name == 'posix':
        font_style = pygame.font.SysFont("AppleGothic", 25)
        score_font = pygame.font.SysFont("AppleGothic", 35)
    # 기타 환경
    else:
        # 기본 폰트 사용
        font_style = pygame.font.SysFont(None, 25)
        score_font = pygame.font.SysFont(None, 35)
except:
    # 폰트 로드 실패 시 기본 폰트 사용
    font_style = pygame.font.SysFont(None, 25)
    score_font = pygame.font.SysFont(None, 35)

def your_score(score):
    value = score_font.render("점수: " + str(score), True, BLACK)
    game_display.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, GREEN, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [width / 6, height / 3])

def gameLoop():
    game_over = False
    game_close = False

    # 뱀 초기 위치
    x1 = width / 2
    y1 = height / 2

    # 초기 방향 (정지 상태)
    x1_change = 0
    y1_change = 0
    
    # 현재 이동 방향 (초기값은 정지 상태)
    # 0: 정지, 1: 오른쪽, 2: 왼쪽, 3: 위, 4: 아래
    current_direction = 0

    # 뱀 길이 리스트
    snake_List = []
    Length_of_snake = 1

    # 음식 위치 랜덤 생성
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            game_display.fill(WHITE)
            message("게임오버! 다시하기: C 종료하기: Q", RED)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_direction != 1:  # 오른쪽으로 이동 중이 아닐 때만 왼쪽으로 이동 가능
                    x1_change = -snake_block
                    y1_change = 0
                    current_direction = 2
                elif event.key == pygame.K_RIGHT and current_direction != 2:  # 왼쪽으로 이동 중이 아닐 때만 오른쪽으로 이동 가능
                    x1_change = snake_block
                    y1_change = 0
                    current_direction = 1
                elif event.key == pygame.K_UP and current_direction != 4:  # 아래로 이동 중이 아닐 때만 위로 이동 가능
                    y1_change = -snake_block
                    x1_change = 0
                    current_direction = 3
                elif event.key == pygame.K_DOWN and current_direction != 3:  # 위로 이동 중이 아닐 때만 아래로 이동 가능
                    y1_change = snake_block
                    x1_change = 0
                    current_direction = 4

        # 경계에 닿았는지 확인
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # 뱀 위치 업데이트
        x1 += x1_change
        y1 += y1_change
        game_display.fill(WHITE)
        pygame.draw.rect(game_display, RED, [foodx, foody, snake_block, snake_block])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 자기 자신과 충돌했는지 확인
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # 음식을 먹었는지 확인
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop() 