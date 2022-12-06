import pygame
import sys
import random
from pygame.locals import *
import pygame_menu
# 색 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLINK = [(224, 255, 255), (192, 240, 255), (128, 224, 255), (64, 192, 255), (128, 224, 255), (192, 240, 255)] #깜빡임 색

# 이미지 로딩
imgTitle = pygame.image.load("타이틀 사진.jpg")
imgWall = pygame.image.load("TEST_LONG_WALL.png")
imgWall2 = pygame.image.load("TEST_SHORT_WALL.png")
imgDark = pygame.image.load("dark.png")
imgPara = pygame.image.load("TEST_PARA.png")
imgBtlBG = pygame.image.load("전투 배경.png")
imgEnemy = pygame.image.load("enemy2.png")
imgItem = [
    pygame.image.load("potion.png"),
    pygame.image.load("blaze_gem.png"),
    pygame.image.load("spoiled.png"),
    pygame.image.load("apple.png"),
    pygame.image.load("meat.png"),
    pygame.image.load("DBSImage.png"),
    pygame.image.load("Lightning_Icon.png"),
    pygame.image.load("blizard_icon.png")
]
imgFloor = [
    pygame.image.load("TEST_FLOOR.png"),
    pygame.image.load("상자.png"),
    pygame.image.load("고치 대체 버전.png"),
    pygame.image.load("stairs.png")
]
imgPlayer = [
    pygame.image.load("mychr0.png"),
    pygame.image.load("mychr1.png"),
    pygame.image.load("mychr2.png"),
    pygame.image.load("mychr3.png"),
    pygame.image.load("mychr4.png"),
    pygame.image.load("mychr5.png"),
    pygame.image.load("mychr6.png"),
    pygame.image.load("mychr7.png"),
    pygame.image.load("mychr8.png")
]
imgEffect = [
    pygame.image.load("at-1.gif"),
    pygame.image.load("effect_b.png"),
    pygame.image.load("Lightning.png")
]
imgLightening = [
    pygame.image.load("lightening1.png"),
    pygame.image.load("lightening2.png"),
    pygame.image.load("lightening3.png"),
    pygame.image.load("lightening4.png")
]
imgRLightening = [
    pygame.image.load("lightening red1.png"),
    pygame.image.load("lightening red2.png"),
    pygame.image.load("lightening red3.png")
]
imgDBS = [
    pygame.image.load("DBS1.png"),
    pygame.image.load("DBS2.png"),
]

# 변수 선언
speed = 1 
idx = True #유저 상태 결정
tmr = 0
floor = 0 #얼마나 이동했는지
fl_max = 1 #길 끝 도착
welcome = 0
ADD = 0
maze = []
typ = 0 #몬스터 관련 스탯
#플레이어 관련 상태 및 현황
pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0
pl_lifemax = 0
pl_life = 0
pl_str = 0
pl_luc = 10
pl_mana = 200 #마나
food = 0
potion = 0
blazegem = 0
treasure = 0
#적 관련 상태 및 현황
emy_name = ""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0
#퀘스트
pl_goal = 0
kill_score = 0
stack = 0
#기타
dmg_eff = 0
btl_cmd = 0
MIMIC = 0
#스킬
Skill_1 = False
Skill_2 = False
Skill_3 = False

COMMAND = ["[A] Attack", "[P]otion", "[B]laze gem", "[R]un", None, None, None]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food +20", "Food +100", "Get Skill : Double Slash!!","Get Skill : Lightning!!", "Get Skill : Blizard"]
EMY_NAME = [
    "Blue Mush", "Green slime", "Insect Warrior", "Tri-dragon", "Goblinn",
    "Ifrit", "Hydra", "RingLeader", "MIMIC", "Hell"
]

MAZE_W = 15
MAZE_H = 15

for i in range(MAZE_H):
    maze.append([0] * MAZE_W)
DUNGEON_W = MAZE_W * 3
DUNGEON_H = MAZE_H * 3
dungeon = []
def basic_MAP():
    for y in range(DUNGEON_H):
        dungeon.append([0] * DUNGEON_W)
    return
basic_MAP()
def make_dungeon():  # 던전 자동 생성
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]
    # 테두리 벽
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H - 1][x] = 1
    for y in range(1, MAZE_H - 1):
        maze[y][0] = 1
        maze[y][MAZE_W - 1] = 1
    # 가운데를 아무것도 없는 상태로 만듬
    for y in range(1, MAZE_H - 1):
        for x in range(1, MAZE_W - 1):
            maze[y][x] = 0
    # 기둥
    for y in range(2, MAZE_H - 2, 2):
        for x in range(2, MAZE_W - 2, 2):
            maze[y][x] = 1
    # 기둥에서 상하좌우로 벽 생성
    for y in range(2, MAZE_H - 2, 2):
        for x in range(2, MAZE_W - 2, 2):
            d = random.randint(0, 3)
            if x > 2:  # 2열부터 왼쪽에는 벽을 생성하지 않음
                d = random.randint(0, 2)
            maze[y + YP[d]][x + XP[d]] = 1

    # 미로에서 던전 생성
    # 전체를 벽으로
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    # 방과 통로 배치
    for y in range(1, MAZE_H - 1):
        for x in range(1, MAZE_W - 1):
            dx = x * 3
            dy = y * 3
            if maze[y][x] == 0:
                if random.randint(0, 99) < 20:  # 방 생성
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy + ry][dx + rx] = 0
                else:  # 통로 생성
                    dungeon[dy][dx] = 0
                    if maze[y - 1][x] == 0: dungeon[dy - 1][dx] = 0
                    if maze[y + 1][x] == 0: dungeon[dy + 1][dx] = 0
                    if maze[y][x - 1] == 0: dungeon[dy][dx - 1] = 0
                    if maze[y][x + 1] == 0: dungeon[dy][dx + 1] = 0
                    

            

def draw_dungeon(bg, fnt):  # 던전 표시
    bg.fill(BLACK)
    for y in range(-4, 4):
        for x in range(-4, 5):
            X = (x + 5) * 80
            Y = (y + 4) * 80
            dx = pl_x + x
            dy = pl_y + y
            try:
                if 0 < dx and dx < DUNGEON_W and 0 < dy and dy < DUNGEON_H:
                    if dungeon[dy][dx] <= 3:
                        bg.blit(imgFloor[dungeon[dy][dx]], [X, Y])
                    if ( dy + 1 <= DUNGEON_H and dx+1 <= DUNGEON_W and dy -1 >= 0 and dx -1 >= 0 ):
                        if dungeon[dy][dx] == 9:
                            if (dungeon[dy + 1][dx] == 9 or dungeon[dy-1][dx] ==9 or dungeon[dy][dx+1] == 9 or dungeon[dy][dx -1] == 9):
                                if (dungeon[dy-1][dx] <=3 or dungeon[dy+1][dx] <= 3 or dungeon[dy][dx+1] <= 3 or dungeon[dy][dx -1] <= 3):
                                        bg.blit(imgWall, [X, Y - 40])
                                        if dy >= 1 and dungeon[dy - 1][dx] == 9:
                                            bg.blit(imgWall2, [X, Y - 80])
                        if (dungeon[dy][dx] == 9):
                            if (dungeon[dy + 1][dx] <= 3 and dungeon[dy-1][dx] <= 3 and dungeon[dy][dx+1] <= 3 and dungeon[dy][dx -1] <= 3):
                                bg.blit(imgWall, [X, Y - 40])
                                if dy >= 1 and dungeon[dy - 1][dx] == 9:
                                    bg.blit(imgWall2, [X, Y - 80])
            except:
                pass
            if x == 0 and y == 0:  # 주인공 캐릭터 표시
                bg.blit(imgPlayer[pl_a], [X, Y - 40])
    bg.blit(imgDark, [0, 0])  # 네 모서리가 어두운 이미지 겹침
    draw_para(bg, fnt)  # 주인공 능력치 표시

def put_event():  # 길에 이벤트 배치
    global pl_x, pl_y, pl_d, pl_a
    # 계단 배치
    while True:
        x = random.randint(3, DUNGEON_W - 4)
        y = random.randint(3, DUNGEON_H - 4)
        if (dungeon[y][x] == 0):
            for ry in range(-1, 2):  # 계단 주변을 길로 만듬
                for rx in range(-1, 2):
                    dungeon[y + ry][x + rx] = 0
            dungeon[y][x] = 3
            break
    # 보물 상자와 누에고치 배치
    for i in range(60):
        x = random.randint(3, DUNGEON_W - 4)
        y = random.randint(3, DUNGEON_H - 4)
        if (dungeon[y][x] == 0):
            dungeon[y][x] = random.choice([1, 2, 2, 2, 2])
    # 플레이어 초기 위치
    while True:
        pl_x = random.randint(3, DUNGEON_W - 4)
        pl_y = random.randint(3, DUNGEON_H - 4)
        if (dungeon[pl_y][pl_x] == 0):
            break
    pl_d = 1
    pl_a = 2

def quest_reward(): #퀘스트 보상 목록
    global food, kill_score, pl_goal
    if kill_score == pl_goal :
        food += pl_goal * 10
def quest_accept(): #퀘스트 주기
    global kill_score, pl_goal, stack
    pl_goal = random.randint(1 + stack,3 + stack)
quest_accept()
def move_player(key):  # 주인공 이동
    global idx, tmr, pl_x, pl_y, pl_d, pl_a, pl_life, food, potion, blazegem, treasure, Skill_1, Skill_2, Skill_3, COMMAND, MIMIC

    if dungeon[pl_y][pl_x] == 1:  # 보물상자에 닿음
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,5,5,5,6,6,7,7,8,8])   #5는 스킬 1 /  6는 스킬 2 / 7은 스킬 3
        if treasure == 0:
            potion = potion + 1
        if treasure == 1:
            blazegem = blazegem + 1
        if treasure == 2:
            food = int(food / 2)
        idx = 3
        tmr = 0
        if treasure == 5:
            Skill_1 = True
            COMMAND[4] = "[1] Double Slash"
        if treasure == 6:
            Skill_2 = True
            COMMAND[5] = "[2] Lightning"
        if treasure == 7:
            Skill_3 = True
            COMMAND[6] = "[3] Blizard"
        if treasure == 8: #미믹 코드
            MIMIC = True
            idx = 10
            tmr = 0
        return
    if dungeon[pl_y][pl_x] == 2:  # 누에고치에 닿음
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 100)
        if r < 35:  # 식량
            treasure = random.choice([3, 3, 3, 4, 4])
            if treasure == 3: food = food + 20
            if treasure == 4: food = food + 100
            idx = 3
            tmr = 0
        else:  # 적 출현
            idx = 10
            tmr = 0
        return
    if dungeon[pl_y][pl_x] == 3:  # 계단에 닿음
        idx = 2
        tmr = 0
        return

    # 방향 키로 상하좌우 이동
    x = pl_x
    y = pl_y
    if key[K_UP] == 1:
        pl_d = 0
        if dungeon[pl_y - 1][pl_x] != 9:
            pl_y = pl_y - 1
    if key[K_DOWN] == 1:
        pl_d = 1
        if dungeon[pl_y + 1][pl_x] != 9:
            pl_y = pl_y + 1
    if key[K_LEFT] == 1:
        pl_d = 2
        if dungeon[pl_y][pl_x - 1] != 9:
            pl_x = pl_x - 1
    if key[K_RIGHT] == 1:
        pl_d = 3
        if dungeon[pl_y][pl_x + 1] != 9:
            pl_x = pl_x + 1
    pl_a = pl_d * 2
    if pl_x != x or pl_y != y:  # 이동 시 식량 및 체력 계산
        pl_a = pl_a + tmr % 2  # 이동 시 걷기 애니메이션
        if food > 0:
            food = food - 1
        else:
            pl_life = pl_life - 5
            if pl_life <= 0:
                pl_life = 0
                pygame.mixer.music.stop()
                idx = 9
                tmr = 0

def draw_text(bg, txt, x, y, fnt, col):  # 그림자 포함한 문자 표시
    sur = fnt.render(txt, True, BLACK) #원래 좌표보다 아래쪽에 검은색 글자 표시
    bg.blit(sur, [x + 1, y + 2])
    sur = fnt.render(txt, True, col)#원래 좌표 글자 표시
    bg.blit(sur, [x, y])

def draw_para(bg, fnt):  # 주인공 능력 표시
    global pl_mana
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if pl_life < 10 and tmr % 2 == 0: col = RED
    draw_text(bg, "{}/{}".format(pl_life, pl_lifemax), X + 128, Y + 6, fnt, col)
    draw_text(bg, str(pl_str), X + 128, Y + 33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr % 2 == 0: col = RED
    draw_text(bg, str(food), X + 128, Y + 60, fnt, col)
    draw_text(bg, str(potion), X + 266, Y + 6, fnt, WHITE)
    draw_text(bg, str(blazegem), X + 266, Y + 33, fnt, WHITE)
    draw_text(bg, str(pl_luc), X+200, Y+60, fnt, WHITE)
    draw_text(bg, "MP " + str(pl_mana), X + 230, Y + 60, fnt, WHITE )
def init_battle():  # 전투 시작 준비
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, MIMIC, typ
    if MIMIC == True:
        typ = 8
    if mob_stack == 10:
        typ = 2
    if mob_stack == 25:
        typ = 5
    if mob_stack == 50:
        typ = 9
    else:
        typ = random.randint(0, floor)
    if floor >= 10:
        if MIMIC == True:
            typ = 8
        if mob_stack == 10:
            typ = 2
        if mob_stack == 25:
            typ = 5
        if mob_stack == 50:
            typ = 9
        else:
            typ = random.randint(0, 8)
    lev = random.randint(1, floor)
    imgEnemy = pygame.image.load("enemy" + str(typ) + ".png")
    if mob_stack == 10 or mob_stack == 25:
        emy_name = "Forced "+EMY_NAME[typ] + " LV" + str(lev)
    else:
        emy_name = EMY_NAME[typ] + " LV" + str(lev)
    if mob_stack == 10 or mob_stack == 25:
        emy_lifemax = (60 * (typ + 1) + (lev - 1) * 10) * 3
    elif mob_stack == 50:
        emy_lifemax = (60 * (typ + 1) + (lev - 1) * 10) * 6
    else:
        emy_lifemax = 60 * (typ + 1) + (lev - 1) * 10
    emy_life = emy_lifemax
    if mob_stack == 10 or mob_stack == 25:
        emy_str = (int(emy_lifemax / 8))
    elif mob_stack == 50:
        emy_str = int(emy_lifemax / 8) * 2
    else:
        emy_str = int(emy_lifemax / 8)
    emy_x = 440 - imgEnemy.get_width() / 2
    emy_y = 560 - imgEnemy.get_height()

def draw_bar(bg, x, y, w, h, val, ma):  # 적 체력 표시 게이지
    pygame.draw.rect(bg, WHITE, [x - 2, y - 2, w + 4, h + 4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0, 128, 255), [x, y, w * val / ma, h])

def draw_battle(bg, fnt):  # 전투 화면 표시
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_life > 0 and emy_blink % 2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y + emy_step])
    draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)
    if emy_blink > 0:
        emy_blink = emy_blink - 1
    for i in range(10):  # 전투 메시지 표시
        draw_text(bg, message[i], 600, 100 + i * 50, fnt, WHITE)
    draw_para(bg, fnt)  # 주인공 능력 표시

def battle_command(bg, fnt, key):  # 커맨드 입력 및 표시
    global btl_cmd, Skill_1, Skill_2, Skill_3
    ent = False
    if key[K_a]:  # A 키
        btl_cmd = 0
        ent = True
    if key[K_p]:  # P 키
        btl_cmd = 1
        ent = True
    if key[K_b]:  # B 키
        btl_cmd = 2
        ent = True
    if key[K_r]:  # R 키
        btl_cmd = 3
        ent = True
    if Skill_1 == True:
        if key[K_1]:
            btl_cmd = 4
            ent = True
    if Skill_2 == True:
        if key[K_2]:
            btl_cmd = 5
            ent = True
    if Skill_3 == True:
        if key[K_3]:
            btl_cmd = 6
            ent = True
    

    if key[K_UP] and btl_cmd > 0:  # ↑ 키
        btl_cmd -= 1
    if key[K_DOWN] and btl_cmd < 3:  # ↓ 키
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        c = WHITE
        if btl_cmd == i: c = BLINK[tmr % 6]
        draw_text(bg, COMMAND[i], 20, 360 + i * 60, fnt, c)
        if Skill_1 == True:
            draw_text(bg, COMMAND[4],20, 180, fnt, c)
        if Skill_2 == True:
            draw_text(bg, COMMAND[5], 20, 240, fnt, c)
        if Skill_3 == True:
            draw_text(bg, COMMAND[6], 20, 300, fnt, c)
    return ent

# 전투 메시지 표시 처리
message = [""] * 10
def init_message():
    for i in range(10):
        message[i] = ""

def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(9):
        message[i] = message[i + 1]
    message[9] = msg 


def main():  # 메인 처리
    global speed, idx, tmr, floor, fl_max, welcome, typ, mob_stack
    global pl_a, pl_lifemax, pl_life, pl_str, food, potion, blazegem, pl_goal, kill_score, stack, pl_luc, pl_mana
    global emy_life, emy_step, emy_blink, dmg_eff, imgLightening, imgRLightening
    dmg = 0
    lif_p = 0
    str_p = 0
    mob_stack = 0
    pygame.init()
    pygame.display.set_caption("Fire Plague")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fontS = pygame.font.Font(None, 30)   


    se = [  # 효과음 및 징글
        pygame.mixer.Sound("Chapter12_sound_ohd_se_attack.ogg"),
        pygame.mixer.Sound("Chapter12_sound_ohd_se_blaze.ogg"),
        pygame.mixer.Sound("Chapter12_sound_ohd_se_potion.ogg"),
        pygame.mixer.Sound("Chapter12_sound_ohd_jin_gameover.ogg"),
        pygame.mixer.Sound("Chapter12_sound_ohd_jin_levup.ogg"),
        pygame.mixer.Sound("Chapter12_sound_ohd_jin_win.ogg"),
        pygame.mixer.Sound("DBS_Sound.mp3"),
        pygame.mixer.Sound("라이트닝 효과음.wav"),
        pygame.mixer.Sound("Blizard_Sound.mp3")
    ]

    def start_the_game():
        global idx
        idx = 0
        pygame.display.update()
        return idx 
    menu = pygame_menu.Menu('Welcome', 400, 300,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.text_input('Name :', default='LOGUE')
    menu.add.button('Play', start_the_game) 
    menu.add.button('Quit', pygame_menu.events.EXIT)      

    menu.mainloop(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed = speed + 1
                    if speed == 4:
                        speed = 1
            if idx == True:
                if event.type == MOUSEBUTTONDOWN:
                    idx = 0

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        if idx == 0:  # 타이틀 화면
            if tmr == 1:
                pygame.mixer.music.load("메인 타이틀.mp3")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [0, 0])
            if fl_max >= 2: #스테이지 표시
                draw_text(screen, "You reached floor {}.".format(fl_max), 300, 460, font, CYAN)
            draw_text(screen, "Press Space Key", 320, 560, font, BLINK[tmr % 6])
            if key[K_SPACE] == 1:
                make_dungeon()
                put_event()
                floor = 1
                welcome = 15
                pl_lifemax = 300
                pl_life = pl_lifemax
                pl_str = 100
                food = 300
                potion = 0
                blazegem = 0
                idx = 1
                pygame.mixer.music.load("필드.mp3")
                pygame.mixer.music.play(-1)
            pygame.display.update()
        elif idx == 1:  # 플레이어 이동
            move_player(key)
            draw_dungeon(screen, fontS)
            draw_text(screen, "floor {} ({},{})".format(floor, pl_x, pl_y), 60, 40, fontS, WHITE)
            draw_text(screen, "QUEST : Kill The Monster {0}/{1} REWARD : food {2}".format(kill_score, pl_goal,pl_goal*10), 60 , 100, fontS, WHITE)
            if welcome > 0:
                welcome = welcome - 1
                draw_text(screen, "Welcome to floor {}.".format(floor), 300, 180, font, CYAN)

        elif idx == 2:  # 화면 전환
            draw_dungeon(screen, fontS)
            if 1 <= tmr and tmr <= 5:
                h = 80 * tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720 - h, 880, h])
            if tmr == 5:
                floor = floor + 1
                if floor > fl_max:
                    fl_max = floor
                welcome = 15
                basic_MAP()
                make_dungeon()
                put_event()
            if 6 <= tmr and tmr <= 9:
                h = 80 * (10 - tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720 - h, 880, h])
            if tmr == 10:
                idx = 1

        elif idx == 3:  # 아이템 입수 혹은 함정
            draw_dungeon(screen, fontS)
            screen.blit(imgItem[treasure], [320, 220])
            draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
            if tmr == 10:
                idx = 1

        elif idx == 9:  # 게임 오버
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                pl_a = PL_TURN[tmr % 4]
                if tmr == 30: pl_a = 8  # 쓰러진 그림
                draw_dungeon(screen, fontS)
            elif tmr == 31:
                se[3].play()
                draw_text(screen, "You died.", 360, 240, font, RED)
                draw_text(screen, "Game over.", 360, 380, font, RED)
            elif tmr == 100:
                idx = 0
                tmr = 0

        elif idx == 10:  # 전투 시작
            if tmr == 1:
                pygame.mixer.music.load("전투 배경음.wav")
                pygame.mixer.music.play(-1)
                init_battle()
                init_message()
            elif tmr <= 4:
                bx = (4 - tmr) * 220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name + " appear!", 300, 200, font, WHITE)
            else:
                idx = 11
                tmr = 0

        elif idx == 11:  # 플레이어 턴(입력 대기)
            draw_battle(screen, fontS)
            if tmr == 1: set_message("Your turn.")
            if battle_command(screen, font, key) == True:
                if btl_cmd == 0:
                    idx = 12
                    tmr = 0
                if btl_cmd == 1 and potion > 0:
                    idx = 20
                    tmr = 0
                if btl_cmd == 2 and blazegem > 0:
                    idx = 21
                    tmr = 0
                if btl_cmd == 3:
                    idx = 14
                    tmr = 0
                if btl_cmd == 4:
                    pl_mana -= 20
                    if pl_mana <= 0 :
                        set_message("Not Enough Mana")
                        idx = 10
                    if pl_mana > 0:
                        idx = 30
                        tmr = 0
                if btl_cmd == 5:
                    pl_mana -= 40
                    if pl_mana <= 0 :
                        set_message("Not Enough Mana")
                        idx = 10
                    if pl_mana > 0:
                        idx = 31
                        tmr = 0
                if btl_cmd == 6:
                    pl_mana -= 80
                    if pl_mana <= 0 :
                        set_message("Not Enough Mana")
                        idx = 10
                    if pl_mana > 0:
                        idx = 32
                        tmr = 0

        elif idx == 12:  # 플레이어 공격
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You attack!")
                se[0].play()
                dmg = pl_str + random.randint(0, 9) + pl_luc
            if 2 <= tmr and tmr <= 4:
                screen.blit(imgEffect[0], [emy_x, emy_y])
            if tmr == 5:
                emy_blink = 5
                set_message(str(dmg) + "pts of damage!")
            if tmr == 11:
                emy_life = emy_life - dmg
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0

        elif idx == 13:  # 적 턴, 적 공격
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Enemy turn.")
            if tmr == 5:
                set_message(emy_name + " attack!")
                se[0].play()
                emy_step = 30
            if tmr == 9:
                dmg = emy_str + random.randint(0, 9)
                set_message(str(dmg) + "pts of damage!")
                dmg_eff = 5
                emy_step = 0
            if tmr == 15:
                pl_life = pl_life - dmg
                if pl_life < 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0
            if tmr == 20:
                idx = 11
                tmr = 0

        elif idx == 14:  # 도망 가능한가?
            draw_battle(screen, fontS)
            if tmr == 1: set_message("...")
            if tmr == 2: set_message("......")
            if tmr == 3: set_message(".........")
            if tmr == 4: set_message("............")
            if tmr == 5:
                if random.randint(0, 99) < 60:
                    idx = 22
                else:
                    set_message("You failed to flee.")
            if tmr == 10:
                idx = 13
                tmr = 0

        elif idx == 15:  # 패배
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("You lose.")
            if tmr == 11:
                idx = 9
                tmr = 29

        elif idx == 16:  # 승리
            draw_battle(screen, fontS)
            if tmr == 1:
                kill_score += 1
                set_message("You win!")
                pl_luc = 0
                pygame.mixer.music.stop()
                se[5].play()
                if kill_score == pl_goal :
                    quest_reward()
                    stack += 1
                    kill_score = 0
                    quest_accept()
            if tmr == 28:
                idx = 22
                if random.randint(0, emy_lifemax) > random.randint(0, pl_lifemax):
                    idx = 17
                    tmr = 0
            if mob_stack != 50:
                mob_stack += 1

        elif idx == 17:  # 레벨업
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Level up!")
                se[4].play()
                lif_p = random.randint(10, 20)
                str_p = random.randint(5, 10)
                pl_luc = random.randint(0,5)
            if tmr == 21:
                set_message("Max life + " + str(lif_p))
                pl_lifemax = pl_lifemax + lif_p
            if tmr == 26:
                set_message("Str + " + str(str_p))
                pl_str = pl_str + str_p
            if tmr == 31:
                 set_message("Luc + " + str(pl_luc))
            if tmr == 50:
                idx = 22

        elif idx == 20:  # Potion
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Potion!")
                se[2].play()
            if tmr == 6:
                pl_life = pl_lifemax
                potion = potion - 1
            if tmr == 11:
                idx = 13
                tmr = 0

        elif idx == 21:  # Blaze gem
            draw_battle(screen, fontS)
            img_rz = pygame.transform.rotozoom(imgEffect[1], 30 * tmr, (12 - tmr) / 8)
            X = 440 - img_rz.get_width() / 2
            Y = 360 - img_rz.get_height() / 2
            screen.blit(img_rz, [X, Y])
            if tmr == 1:
                set_message("Blaze gem!")
                se[1].play()
            if tmr == 6:
                blazegem = blazegem - 1
            if tmr == 11:
                dmg = 250
                idx = 12
                tmr = 4

        elif idx == 22:  # 전투 종료
            if typ != 9:
                pygame.mixer.music.load("필드.mp3")
                pygame.mixer.music.play(-1)
                idx = 1
                pl_mana = 200
            if typ == 9:
                pygame.mixer.music.load("메인 타이틀.mp3")
                pygame.mixer.music.play(-1)
                ending = pygame.image.load("엔딩.png")
                screen.blit(ending, [0,0])
                if key[K_SPACE] == 1:
                    idx = 0
        elif idx == 30: # 스킬 1 - 두번 베기
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Double Slash!")
            if tmr == 2:
                se[6].play()
            if tmr >= 3 and tmr <= 8:
                screen.blit(imgDBS[0], [emy_x, emy_y])
                pygame.display.update()
            if tmr >= 5 and tmr <= 10:
                screen.blit(imgDBS[1], [emy_x, emy_y])
                pygame.display.update()
            if tmr == 11 :
                idx = 12
                tmr = 4
                dmg = (pl_str + pl_luc) * 2 
            continue
        
        elif idx == 31: # 스킬 2 - 라이트닝
            draw_battle(screen, fontS)
            if tmr == 1:
                se[7].play()
                set_message("Lightening!")
            if tmr >= 1 and tmr <= 4:
                screen.blit(imgLightening[0], [emy_x - 50,emy_y])
                screen.blit(imgRLightening[0], [emy_x - 50, emy_y])
                pygame.display.update()
            if tmr >= 3 and tmr <= 8:
                screen.blit(imgLightening[1], [emy_x - 50,emy_y])
                screen.blit(imgRLightening[0], [emy_x - 50, emy_y])
                pygame.display.update()
            if tmr >= 5 and tmr <= 9:
                screen.blit(imgLightening[2], [emy_x - 50,emy_y])
                screen.blit(imgRLightening[1], [emy_x - 50, emy_y])
                pygame.display.update()
            if tmr >= 7 and tmr <= 11:
                screen.blit(imgLightening[3], [emy_x - 50,emy_y])
                screen.blit(imgRLightening[2], [emy_x - 50, emy_y])
                pygame.display.update()   
            if tmr == 12:
                idx = 12
                tmr = 4
                dmg = 200
            continue

        elif idx == 32: #스킬 3 - Blizard
            draw_battle(screen, fontS)
            BEffect = pygame.image.load("blizard_effect.png")
            if tmr == 2:
                se[8].play()
            if tmr >= 1 and tmr <= 10:
                if imgEnemy.get_width() == 300 and imgEnemy.get_height() == 400:
                    screen.blit(BEffect, [emy_x, emy_y])
                    pygame.display.update()
                else:
                    screen.blit(BEffect, [emy_x, emy_y - 100])
            if tmr == 12:
                idx = 12
                tmr = 4
                dmg = 500
            continue
        draw_text(screen, "[S]peed " + str(speed), 740, 40, fontS, WHITE)

        pygame.display.update()
        clock.tick(4 + 2 * speed)

if __name__ == '__main__':
    main()