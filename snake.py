import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Window dimensions (expanded height to fit a top score bar)
width = 500
height = 550
play_height = 500  # Actual game grid height

cols = 25
rows = 20

class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny 
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        # Offset y-coordinates by 50 pixels to account for the top bar
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+51, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8+50)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8+50)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake():
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(score):
    global win, s, snack
    win.fill((0,0,0))
    
    # Draw Top Score Bar Background
    pygame.draw.rect(win, (40, 40, 40), (0, 0, width, 50))
    
    # Render Score Text on Top Bar
    font = pygame.font.SysFont('arial', 25)
    score_label = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_label, (20, 12))
    
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 50  # Offset grid lines below the score bar
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (40,40,40), (x, 50),(x, w + 50))
        pygame.draw.line(surface, (40,40,40), (0, y),(w, y))


def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(0, rows)
        y = random.randrange(0, rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)


def startScreen():
    """Displays the main menu with a start option and difficulty selector bar."""
    global win
    clock = pygame.time.Clock()
    modes = ["Easy", "Medium", "Hard"]
    current_mode_idx = 0
    
    while True:
        win.fill((20, 20, 20))
        
        title_font = pygame.font.SysFont('arial', 45, bold=True)
        option_font = pygame.font.SysFont('arial', 22)
        
        # Title
        title_label = title_font.render("SNAKE GAME", True, (255, 0, 0))
        win.blit(title_label, (width//2 - title_label.get_width()//2, 120))
        
        # Start Game Button
        start_rect = pygame.Rect(width//2 - 120, 230, 240, 45)
        pygame.draw.rect(win, (0, 200, 0), start_rect, border_radius=8)
        start_label = option_font.render("START GAME", True, (255, 255, 255))
        win.blit(start_label, (width//2 - start_label.get_width()//2, 240))
        
        # Difficulty Mode Bar (Placed below Start button)
        mode_rect = pygame.Rect(width//2 - 120, 290, 240, 45)
        pygame.draw.rect(win, (70, 70, 70), mode_rect, border_radius=8)
        mode_text = f"Mode: {modes[current_mode_idx]}"
        mode_label = option_font.render(mode_text, True, (255, 255, 255))
        win.blit(mode_label, (width//2 - mode_label.get_width()//2, 300))
        
        # Instruction text for changing mode
        hint_font = pygame.font.SysFont('arial', 16)
        hint_label = hint_font.render("(Click mode bar to change)", True, (150, 150, 150))
        win.blit(hint_label, (width//2 - hint_label.get_width()//2, 340))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    speeds = {"Easy": 10, "Medium": 20, "Hard": 40}
                    return speeds[modes[current_mode_idx]]
                elif mode_rect.collidepoint(event.pos):
                    current_mode_idx = (current_mode_idx + 1) % len(modes)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    speeds = {"Easy": 10, "Medium": 20, "Hard": 40}
                    return speeds[modes[current_mode_idx]]

        clock.tick(15)


def gameOverScreen(score):
    """Displays the game over screen with final score, restart, and exit options."""
    global win
    clock = pygame.time.Clock()
    
    while True:
        win.fill((20, 20, 20))
        
        title_font = pygame.font.SysFont('arial', 40, bold=True)
        score_font = pygame.font.SysFont('arial', 28)
        option_font = pygame.font.SysFont('arial', 22)
        
        title_label = title_font.render("GAME OVER", True, (255, 0, 0))
        win.blit(title_label, (width//2 - title_label.get_width()//2, 120))
        
        score_label = score_font.render(f"Total Score: {score}", True, (255, 255, 255))
        win.blit(score_label, (width//2 - score_label.get_width()//2, 190))
        
        restart_rect = pygame.Rect(width//2 - 120, 270, 240, 45)
        pygame.draw.rect(win, (0, 150, 255), restart_rect, border_radius=8)
        restart_label = option_font.render("RESTART GAME", True, (255, 255, 255))
        win.blit(restart_label, (width//2 - restart_label.get_width()//2, 280))
        
        exit_rect = pygame.Rect(width//2 - 120, 335, 240, 45)
        pygame.draw.rect(win, (200, 0, 0), exit_rect, border_radius=8)
        exit_label = option_font.render("EXIT", True, (255, 255, 255))
        win.blit(exit_label, (width//2 - exit_label.get_width()//2, 345))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return True  # Directly restart the game loop
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        clock.tick(15)


def main():
    global s, snack, win
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    # Show start screen once at the very beginning to pick the mode & start
    game_speed = startScreen()

    while True:
        s = snake((255,0,0), (10,10))
        s.addCube()
        snack = cube(randomSnack(rows, s), color=(0,255,0))
        
        score = 0
        flag = True
        clock = pygame.time.Clock()
        
        while flag:
            pygame.time.delay(50)
            clock.tick(game_speed)
            s.move()
            headPos = s.head.pos
            
            # Border Collision Check
            if headPos[0] >= rows or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0:
                flag = False

            # Eating Snack Check
            if s.body[0].pos == snack.pos:
                s.addCube()
                score += 1
                snack = cube(randomSnack(rows, s), color=(0,255,0))
                
            # Self Collision Check
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                    flag = False
                    break
                        
            if flag:
                redrawWindow(score)
        
        # When dead, show Game Over menu
        should_restart = gameOverScreen(score)
        if not should_restart:
            break

main()