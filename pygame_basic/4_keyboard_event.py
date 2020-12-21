import pygame

pygame.init()  # 초기화작업 (반드시 필요)

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption('PYGAME')  # 게임이름

# 배경 이미지 불러오기
background = pygame.image.load(
    'C:\\Users\\joon seok\\Desktop\\Projects\\python-game\\pygame_basic\\background.png')

# 캐릭터 불러오기
character = pygame.image.load(
    'C:\\Users\\joon seok\\Desktop\\Projects\\python-game\\pygame_basic\\character.png')
character_size = character.get_rect().size  # 이미지의 크기를 구해옴
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

# 이벤트 루프
running = True  # 게임이 진행중인가?
while running:
    for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
            running = False  # 게임이 진행중이 아님

    screen.blit(background, (0, 0))  # 배경 그리기

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 그리기

    pygame.display.update()  # 게임화면을 다시 그리기

# pygame 종료
pygame.quit()
