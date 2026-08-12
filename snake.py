import math
import random
import os
import pygame
import tkinter as tk
from tkinter import messagebox

# Window dimensions (expanded height to fit a top score bar)
width = 500
height = 550
play_height = 500  # Actual game grid height

cols = 25
rows = 20

# High Score File Handling
SCORE_FILE = "highscore.txt"

def load_high_score():
    if not os.path.exists(SCORE_FILE):
        return 0
    try:
        with open(SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (ValueError, IOError):
        return 0

def save_high_score(new_score):
    current_high = load_high_score()
    if new_score > current_high:
        try:
            with open(SCORE_FILE, "w") as f:
                f.write(str(new_score))
        except IOError:
            pass

# Themes Dictionary Configuration
THEMES = {
    "Classic Dark": {
        "bg": (0, 0, 0),
        "grid": (40, 40, 40),
        "snake": (255, 0, 0),
        "snack": (0, 255, 0),
        "bar": (40, 40, 40)
    },
    "Retro Neon": {
        "bg": (15, 15, 35),
        "grid": (45, 45, 75),
        "snake": (0, 255, 255),
        "snack": (255, 0, 127),
        "bar": (30, 30, 60)
    },
    "Matrix Green": {
        "bg": (5, 20, 5),
        "grid": (15, 50, 15),
        "snake": (0, 255, 60),
        "snack": (255, 255, 0),
        "bar": (10, 35, 10)
    }
}

# Global active theme tracker
current_theme_name = "Classic Dark"

class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=None):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny 
        self.color = color if color else THEMES[current_theme_name]["snake"]

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        draw_color = self.color if self.color != (255,0,0) else THEMES[current_theme_name]["snake"]
        
        # Offset y-coordinates by 50 pixels to account for the top bar
        pygame.draw.rect(surface, draw_color, (i*dis+1, j*dis+51, dis-2, dis-2))
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
        self.head = cube(pos, color=color)
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
        self.head = cube(pos, color=self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]), color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]), color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1), color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1), color=self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(score, high_score):
    global win, s, snack, current_theme_name
    theme = THEMES[current_theme_name]
    
    win.fill(theme["bg"])
    
    # Draw Top Score Bar Background
    pygame.draw.rect(win, theme["bar"], (0, 0, width, 50))
    
    # Render Score & High Score Text on Top Bar
    font = pygame.font.SysFont('arial', 20)
    score_label = font.render(f"Score: {score}  |  High Score: {high_score}", True, (255, 255, 255))
    win.blit(score_label, (20, 15))
    
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()


def drawGrid(w, rows, surface):
    global current_theme_name
    theme = THEMES[current_theme_name]
    sizeBtwn = w // rows
    x = 0
    y = 50  # Offset grid lines below the score bar
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, theme["grid"], (x, 50),(x, w + 50))
        pygame.draw.line(surface, theme["grid"], (0, y),(w, y))


def randomSnack(rows, item):
    global current_theme_name
    theme = THEMES[current_theme_name]
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
    """Displays the main menu with start options, difficulty, and theme selectors."""
    global win, current_theme_name
    clock = pygame.time.Clock()
    
    modes = ["Easy", "Medium", "Hard"]
    current_mode_idx = 0
    
    theme_names = list(THEMES.keys())
    current_theme_idx = theme_names.index(current_theme_name)
    
    high_score = load_high_score()
    
    while True:
        win.fill((20, 20, 20))
        
        title_font = pygame.font.SysFont('arial', 40, bold=True)
        option_font = pygame.font.SysFont('arial', 20)
        
        # Title
        title_label = title_font.render("SNAKE GAME", True, (255, 0, 0))
        win.blit(title_label, (width//2 - title_label.get_width()//2, 80))
        
        # High Score on Menu
        hs_font = pygame.font.SysFont('arial', 18)
        hs_label = hs_font.render(f"All-Time High Score: {high_score}", True, (255, 215, 0))
        win.blit(hs_label, (width//2 - hs_label.get_width()//2, 135))
        
        # Start Game Button
        start_rect = pygame.Rect(width//2 - 120, 185, 240, 40)
        pygame.draw.rect(win, (0, 200, 0), start_rect, border_radius=8)
        start_label = option_font.render("START GAME", True, (255, 255, 255))
        win.blit(start_label, (width//2 - start_label.get_width()//2, 193))
        
        # Difficulty Mode Bar
        mode_rect = pygame.Rect(width//2 - 120, 240, 240, 40)
        pygame.draw.rect(win, (70, 70, 70), mode_rect, border_radius=8)
        mode_label = option_font.render(f"Mode: {modes[current_mode_idx]}", True, (255, 255, 255))
        win.blit(mode_label, (width//2 - mode_label.get_width()//2, 248))
        
        # Theme Selector Bar
        theme_rect = pygame.Rect(width//2 - 120, 295, 240, 40)
        pygame.draw.rect(win, (70, 70, 70), theme_rect, border_radius=8)
        theme_label = option_font.render(f"Theme: {theme_names[current_theme_idx]}", True, (255, 255, 255))
        win.blit(theme_label, (width//2 - theme_label.get_width()//2, 303))
        
        # Instructions
        hint_font = pygame.font.SysFont('arial', 15)
        hint_label = hint_font.render("Click option bars to cycle settings", True, (150, 150, 150))
        win.blit(hint_label, (width//2 - hint_label.get_width()//2, 355))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    current_theme_name = theme_names[current_theme_idx]
                    speeds = {"Easy": 10, "Medium": 20, "Hard": 40}
                    return speeds[modes[current_mode_idx]]
                elif mode_rect.collidepoint(event.pos):
                    current_mode_idx = (current_mode_idx + 1) % len(modes)
                elif theme_rect.collidepoint(event.pos):
                    current_theme_idx = (current_theme_idx + 1) % len(theme_names)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_theme_name = theme_names[current_theme_idx]
                    speeds = {"Easy": 10, "Medium": 20, "Hard": 40}
                    return speeds[modes[current_mode_idx]]

        clock.tick(15)


def gameOverScreen(score, high_score):
    """Displays the game over screen with score, restart, main menu, and exit options."""
    global win
    clock = pygame.time.Clock()
    
    while True:
        win.fill((20, 20, 20))
        
        title_font = pygame.font.SysFont('arial', 38, bold=True)
        score_font = pygame.font.SysFont('arial', 20)
        option_font = pygame.font.SysFont('arial', 18)
        
        title_label = title_font.render("GAME OVER", True, (255, 0, 0))
        win.blit(title_label, (width//2 - title_label.get_width()//2, 85))
        
        score_label = score_font.render(f"Total Score: {score}", True, (255, 255, 255))
        win.blit(score_label, (width//2 - score_label.get_width()//2, 140))
        
        hs_label = score_font.render(f"High Score: {high_score}", True, (255, 215, 0))
        win.blit(hs_label, (width//2 - hs_label.get_width()//2, 170))
        
        # Restart Button
        restart_rect = pygame.Rect(width//2 - 120, 220, 240, 38)
        pygame.draw.rect(win, (0, 150, 255), restart_rect, border_radius=8)
        restart_label = option_font.render("RESTART GAME", True, (255, 255, 255))
        win.blit(restart_label, (width//2 - restart_label.get_width()//2, 228))
        
        # Main Menu Button
        menu_rect = pygame.Rect(width//2 - 120, 270, 240, 38)
        pygame.draw.rect(win, (200, 140, 0), menu_rect, border_radius=8)
        menu_label = option_font.render("MAIN MENU", True, (255, 255, 255))
        win.blit(menu_label, (width//2 - menu_label.get_width()//2, 278))
        
        # Exit Button
        exit_rect = pygame.Rect(width//2 - 120, 320, 240, 38)
        pygame.draw.rect(win, (200, 0, 0), exit_rect, border_radius=8)
        exit_label = option_font.render("EXIT", True, (255, 255, 255))
        win.blit(exit_label, (width//2 - exit_label.get_width()//2, 328))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                elif menu_rect.collidepoint(event.pos):
                    return "menu"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"

        clock.tick(15)


def main():
    global s, snack, win
    pygame.init()
    pygame.mixer.init()
    
    eat_sound = None
    game_over_sound = None
    try:
        if os.path.exists("eat.wav"):
            eat_sound = pygame.mixer.Sound("eat.wav")
        if os.path.exists("gameover.wav"):
            game_over_sound = pygame.mixer.Sound("gameover.wav")
    except Exception:
        pass

    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    while True:
        # Show start screen to pick settings/mode and return the speed
        game_speed = startScreen()

        running_session = True
        while running_session:
            theme = THEMES[current_theme_name]
            s = snake(theme["snake"], (10,10))
            s.addCube()
            snack = cube(randomSnack(rows, s), color=theme["snack"])
            
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
                    if eat_sound:
                        eat_sound.play()
                    snack = cube(randomSnack(rows, s), color=theme["snack"])
                    
                # Self Collision Check
                for x in range(len(s.body)):
                    if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                        flag = False
                        break
                            
                if flag:
                    current_high = load_high_score()
                    redrawWindow(score, current_high)
            
            if game_over_sound:
                game_over_sound.play()

            save_high_score(score)
            final_high = load_high_score()
            
            # Action choice from Game Over screen ("restart" or "menu")
            action = gameOverScreen(score, final_high)
            
            if action == "menu":
                running_session = False  # Breaks inner loop to go back to startScreen()
                game_speed = startScreen()  # Re-opens the start screen menu loop
            elif action != "restart":
                break

main()