import pygame
import os
###########################################################
# 기본 초기화 (반드시 해야하는 것 들)
pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption('팡')

# FPS
clock = pygame.time.Clock()

###########################################################

# 1. 사용자 게임 초기화 (배경화면, 게임이미지, 좌표, 속도, 폰트 등)

current_path = os.path.dirname(__file__)  # 현재파일의 위치 반환
image_path = os.path.join(current_path, 'images')  # images 폴더 위치 반환

# 배경만들기
background = pygame.image.load(os.path.join(image_path, 'paper2.jpg'))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

character_to_x = 0
character_speed = 0.5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, 'wep.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러발 발사 가능
weapons = []

weapon_speed = 5

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, 'ball1.png')),
    pygame.image.load(os.path.join(image_path, 'ball2.png')),
    pygame.image.load(os.path.join(image_path, 'ball3.png')),
    pygame.image.load(os.path.join(image_path, 'ball4.png'))
]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공들
balls = []
# 최초 발생하는 공,,,
balls.append({
    'pos_x': 50,
    'pos_y': 50,
    'img_idx': 0,
    'to_x': 3,
    'to_y': -6,
    'init_spd_y': ball_speed_y[0]
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# font 정의
game_font = pygame.font.Font(None, 40)
total_time = 15
start_ticks = pygame.time.get_ticks()

game_result = 'Game Over'
running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + \
                    (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            character_to_x = 0

    character_x_pos += character_to_x * dt

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  # 무기 위치를 위로

    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿앗을때 공 이동 위치 변경 (튕겨나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val['to_x'] = ball_val['to_x'] * -1

        # 세로위치
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val['to_y'] = ball_val['init_spd_y']
        else:
            ball_val['to_y'] += 0.5

        ball_val['pos_x'] += ball_val['to_x']
        ball_val['pos_y'] += ball_val['to_y']

        # 4. 충돌 처리

        # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
            break

            # 공과 무기들 충돌처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx  # 해당무기 없애기위한 값 설정
                ball_to_remove = ball_idx  # 해당 공 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 나눠짐
                if ball_img_idx < 3:
                    # 현재 공 크기의 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        'pos_x': ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y': ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        'img_idx': ball_img_idx + 1,
                        'to_x': -3,
                        'to_y': -6,
                        'init_spd_y': ball_speed_y[ball_img_idx + 1]})

                    balls.append({
                        'pos_x': ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y': ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        'img_idx': ball_img_idx + 1,
                        'to_x': 3,
                        'to_y': -6,
                        'init_spd_y': ball_speed_y[ball_img_idx + 1]})
                    break

    # 충돌된 공 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우
    if len(balls) == 0:
        game_result = 'Mission Complete'
        running = False

        # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val['pos_x']
        ball_pos_y = val['pos_y']
        ball_img_idx = val['img_idx']
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과시간계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render('Time : {}'.format(
        int(total_time - elapsed_time)), True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = 'Time Over'
        running = False

    pygame.display.update()  # 게임화면을 다시 그리기


msg = game_font.render(game_result, True, (0, 0, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()
