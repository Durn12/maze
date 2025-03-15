import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        previous_x = self.rect.x
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
        collision_occured = False
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                collision_occured = True
                break
            
        if collision_occured:
            self.rect.x = previous_x
            self.direction = 'right' if self.direction == 'left' else 'left'
            
        else:
            if self.rect.x <= 50:
                self.direction = "right"
            if self.rect.x >= win_width - 50:
                self.direction = "left"



class Wall(pygame.sprite.Sprite):
    def __init__(self, thickness, color, wall_x, wall_y, length, is_vertical, type_wall=None, name=None):
        super().__init__()
        self.thickness = thickness
        self.color = color
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.is_vertical = is_vertical
        self.length = length
        self.type_wall = type_wall
        self.name = name
        if is_vertical:
            self.width = thickness
            self.height = length
        else:
            self.width = length
            self.height = thickness
            
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
    def draw_wall(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

def create_walls(walls_list):
    wall_objects = []
    
    for wall_params in walls_list:
        wall = Wall(
            thickness = wall_params[0],
            color = wall_params[1],
            wall_x = wall_params[2],
            wall_y = wall_params[3],
            length = wall_params[4],
            is_vertical = wall_params[5],
            type_wall = wall_params[6],
            name = wall_params[7],
        )
        wall_objects.append(wall)
    return wall_objects

WALL_WHITE = (255, 255, 255)
WALL_RED = (255, 0, 0)
WALL_GREEN = (0, 255, 0)
WALL_BLUE = (0, 0, 255)
WALL_BLACK = (0, 0, 0)
walls_list = [
    [20, WALL_WHITE, 200, 40, 600, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 200, 800, 500, False, 'barricada', 'правая нижняя горизонтальная стена'],
    [20, WALL_WHITE, 320, 810, 150, True, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 500, 810, 100, True, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 520, 880, 120, False, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 640, 640, 260, True, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 420, 540, 270, True, 'baricada', 'левая стена'],
    
    [20, WALL_WHITE, 200, 40, 600, False, 'barricada', 'левая стена'],
    [20, WALL_WHITE, 200, 400, 500, False, 'barricada', 'правая нижняя горизонтальная стена'],
    [20, WALL_WHITE, 320, 410, 150, True, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 500, 410, 100, True, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 520, 480, 120, False, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 640, 240, 260, True, 'baricada', 'левая стена'],
    [20, WALL_WHITE, 420, 140, 270, True, 'baricada', 'левая стена']
]
walls = create_walls(walls_list)
WIN = (255, 215, 0)
LOSE = (180, 0, 0)
win_width = 1000
win_height = 1000
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Лабиринт")
background = pygame.transform.scale(pygame.image.load('background1.png'), (win_width, win_height))

player = Player('ship1.png', 5, win_height - 80, 4)
monster1 = Enemy('ship2.png', win_width - 80, 280, 2)
monster2 = Enemy('ship2.png', win_width - 80, 580, 10)
monster3 = Enemy('ship2.png', win_width - 780, 480, 8)
monster4 = Enemy('ship2.png', win_width - 800, 680, 6)
monster5 = Enemy('ship2.png', win_width - 800, 280, 5)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

monsters = [monster1, monster2, monster3, monster4, monster5]
finals = [final]

game_over = False
clock = pygame.time.Clock()
FPS = 100
finish = False

pygame.font.init()
font = pygame.font.SysFont('Arial', 70)

win = font.render('YOU WIN!', True, WIN)
lose = font.render('YOU LOSE', True, LOSE)

pygame.mixer.init()
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()

money = pygame.mixer.Sound('money.ogg')
kick = pygame.mixer.Sound('kick.ogg')

def end_game(end = None):
    global finish
    finish = True
    if end == win:
        money.play()
        window.blit(win, (500, 500))
    elif end == lose:
        kick.play()
        window.blit(lose, (500, 500))
        

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        
        for wall in walls:
            wall.draw_wall(window)
            if pygame.sprite.collide_rect(player, wall):
                end_game(lose)
        for monster in monsters:
            monster.update()
            monster.reset()
            if pygame.sprite.collide_rect(player, monster1):
                end_game(lose)
        for final in finals:
            final.reset()
            if pygame.sprite.collide_rect(player, final):
                end_game(win)
        
    
    pygame.display.update()
    clock.tick(FPS)
