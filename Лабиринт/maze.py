from pygame import *

win_width = 1000
win_height = 800
wd = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
bck = transform.scale(image.load('background.jpg'), (win_width, win_height))
clock = time.Clock()
FPS = 30

clock.tick(FPS)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        wd.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 895:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 695:
            self.rect.y += self.speed
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 770:
            self.direction = "right"
        if self.rect.x >= win_width - 50:
            self.direction = 'left'
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw(self):
        wd.blit(self.image, (self.rect.x, self.rect.y))

player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
wall = Wall(0,0,139, 50, 0, 30, 600)
wall2 = Wall(0,0,139, 250, 400, 40, 400)
wall3 = Wall(0,0,139, 250, 0, 40, 250)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
speed = 5

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.Font(None, 70)
win = font.render('WIN!', True, (255,215,0))
lose = font.render('LOSE', True, (180,0,0))
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        wd.blit(bck, (0, 0))   
        player.reset()
        player.update()
        wall.draw()
        wall2.draw()
        wall3.draw()
        monster.reset()
        monster.update()
        final.reset()
    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3):
        finish = True
        wd.blit(lose, (400, 400))
        kick.play()
    if sprite.collide_rect(player, final):
        finish = True
        wd.blit(win, (400, 400))
        money.play()
    display.update()
