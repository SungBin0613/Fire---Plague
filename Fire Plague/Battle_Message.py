import pygame
import sys

White = (255,255,255)
Black = (0, 0, 0)
imgBtlbg = pygame.image.load("btlbg.png")
imgEnemy = None

emy_num = 0
emy_x = 0
emy_y = 0

message = [""]*10
def message():
    for i in range(10):
        message[i] = ""
def set_message():
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(10):
        message[i] = message[i+1]
    message[9] = msg

def draw_text(bg, txt, x, y, fnt, col):
    sur = fnt.render(txt, True, Black)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])
def draw_battle(bg, fnt):
    bg.blit(imgBtlbg, [0,0])
    for i in range(10):
        draw_text(bg, message[i], 600, 100 + i * 50, fnt, White)
def battle():
    global imgEnemy, emy_num, emy_y, emy_x
    emy_num += 1
    if emy_num == 5:
        emy_num = 1
    imgEnemy = pygame.image.load("enemy{0}.png".format(str(emy_num)))
    emy_y = 560 - imgEnemy.get_height() #이미지 폭으로부터 표시 위치 계산
    emy_x = 440 - imgEnemy.get_width()/2

def draw_battle(bg, fnt):
    bg.blit(imgBtlbg, [0,0]) 
    bg.blit(imgEnemy, [emy_x, emy_y])
    sur = fnt.render("enemy"+str(emy_num)+".png", True, White)
    bg.blit(sur, [360, 580])

def main():
    pygame.init()
    screen = pygame.display.set_mode((880,720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    battle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    battle()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_battle(screen, font)
        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()