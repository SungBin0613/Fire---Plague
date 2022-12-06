import pygame
import sys
import random

Cyan = (0, 255, 255)
Gray = (96, 96, 96)

Maze_W = 11
Maze_H = 9
maze = []

for y in range(Maze_H):
    maze.append([0]*Maze_W)

def make_maze():
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    #주변 벽
    for x in range(Maze_W):
        maze[0][x] = 1
        maze[Maze_H - 1][x] = 1
    for y in range(Maze_H):
        maze[y][0] = 1
        maze[y][Maze_W -1] = 1

    #안이 빈 상태
    for y in range(1, Maze_H-1):
        for x in range(1, Maze_W -1):
            maze[y][x] = 0
    
    #기둥
    for y in range(2, Maze_H -2, 2):
        for x in range(2, Maze_W -2 , 2):
            maze[y][x] = 1
    
    #기둥에서 상하좌우로 벽 생성
    for y in range(2, Maze_H -2, 2):
        for x in range(2, Maze_W-2, 2):
            d = random.randint(0,3)
            if x>2:
                d = random.randint(0,2)
            maze[y+YP[d]][x+XP[d]] = 1

def main():
    pygame.init()
    pygame.display.set_caption("미로 자동 생성기")
    screen = pygame.display.set_mode((540, 540))
    clock = pygame.time.Clock()

    make_maze()

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                make_maze()

        for y in range(Maze_H):
            for x in range(Maze_W):
                W = 48
                H = 48
                X = x*W
                Y = y*H #크기 지정

                if maze[y][x] == 0: #0이면 통로
                    pygame.draw.rect(screen, Cyan, [X,Y,W,H])
                if maze[y][x] == 1: #1이면 벽
                    pygame.draw.rect(screen, Gray, [X,Y,W,H])
                
        pygame.display.update()
        clock.tick(2)
if __name__ == '__main__':
    main()
pygame.quit()
sys.exit()



