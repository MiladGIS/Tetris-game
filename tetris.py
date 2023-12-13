import pygame
import random

colors = [
    (0, 0, 0),
    (10, 20, 60),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    figures = [
        [[6, 7], [3, 6]],
        [[1, 2, 5], [0, 1, 3]],
        [[5, 7, 8], [3, 6, 7]],
        [[0, 3, 6], [6, 7, 8]],
        [[8]], 
        [[0, 2, 4, 6, 8]],
        [[0, 4, 8], [2, 4, 6]],
        [[1, 2, 4, 6, 7], [0, 3, 4, 5, 8], [2, 3, 4, 5, 6], [0, 1, 4, 7, 8]]
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
        
    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
   

class Tetris:
    level = 2
    score = 0
    hieghst_score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(0, 3)

    def intersects(self):
        intersection = False
        for i in range(3):
            for j in range(3):
                if i * 3 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            i + self.figure.y < 0 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.width):
            zeros = 0
            for j in range(self.height):
                if self.field[j][i] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.height):
                        self.field[j][i1] = self.field[j][i1 - 1]
        self.score += lines
        my_file = open('score.txt','r+')
        lines = my_file.readlines()
        a = ""
        for line in lines:
            for c in line:
                if c.isdigit() == True:
                    a += str(c)
        if int(a) < self.score:
            my_file.truncate(0)
            my_file.seek(0)
            my_file.write('Highest score is: ' + str(self.score))
            self.hieghst_score = self.score
        else:
            self.hieghst_score = int(a)
        my_file.close()

    def go_space(self):
        while not self.intersects():
            self.figure.x += 1
        self.figure.x -= 1
        self.freeze()

    def go_down(self):
        self.figure.x += 1
        if self.intersects():
            self.figure.x -= 1
            self.freeze()

    def freeze(self):
        for i in range(3):
            for j in range(3):
                if i * 3 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dy):
        old_y = self.figure.y
        self.figure.y += dy
        if self.intersects():
            self.figure.y = old_y

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation



# Initialize the game engine
pygame.init()

size = (600, 300)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Create text file
my_file = open('score.txt','w+')
my_file.write('Highest score is: ' + str(0))
my_file.close() 

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(10, 20)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.go_side(-1)
            if event.key == pygame.K_DOWN:
                game.go_side(1)
            if event.key == pygame.K_LEFT:
                game.rotate()
            if event.key == pygame.K_RIGHT:
                game.go_space()
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(10, 20)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill((255,255,255))

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, (128, 128, 128),
                             [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(3):
            for j in range(3):
                p = i * 3 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("  Score: " + str(game.score) + "    " + "  Hieghst Score: " + str(game.hieghst_score),
                       True, (0,0,0))
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [size[0] / 5, size[1] / 3])
        screen.blit(text_game_over1, [size[0] / 5 + size[0] / 100, size[1] / 2])

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()