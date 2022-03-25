import time
import pygame
import pygame as pg
from ProjectFiles.config import *
from pygame import mixer

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.score = 0
        self.x = x * TILESIZE * 2
        self.y = y * TILESIZE * 2
        self.width = TILESIZE * 1.5
        self.height = TILESIZE * 1.5
        self.player_speed = PLAYER_SPEED
        self.vel = 0
        self.acc = vec(0, 0)
        player_img = pg.image.load("ProjectFiles/img/jumpman.gif")
        self.image = pg.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(player_img, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pos = vec(self.rect.x, self.rect.y)
        self.game_over = 2

    def update(self):
        if self.game_over != -1:
            self.movement()
            self.rect.x += self.acc.x
            self.collide('x')
            self.rect.y += self.acc.y
            self.collide("y")
            if self.rect.y < 0:
                self.rect.y = 0
            self.calculate_score()

    def movement(self):
        speed = PLAYER_SPEED
        hits = pg.sprite.spritecollide(self, self.game.ladder, False)
        self.image = pygame.image.load("ProjectFiles/img/jumpman.gif")
        if hits:
            self.vel = 0
            self.image = pygame.image.load("ProjectFiles/img/jumpman_stairs.gif")
        keys = pg.key.get_pressed()
        self.acc = vec(0, 0)
        if keys[pg.K_LEFT] and self.rect.x >= PLAYER_SPEED - 1:
            self.acc.x -= speed
            self.image = pg.image.load("ProjectFiles/img/jumpman_move_left.gif")
        if keys[pg.K_RIGHT] and self.rect.x < WIN_WIDTH - self.width - PLAYER_SPEED + 1:
            self.acc.x += speed
            self.image = pg.image.load("ProjectFiles/img/jumpman_move_right.gif")
        if pg.key.get_pressed()[pg.K_UP]:
            self.acc.y -= speed
        if pg.key.get_pressed()[pg.K_DOWN]:
            self.acc.y += speed
        if not hits:
            self.vel += 1
            if self.vel > 10:
                self.vel = 10
            self.acc.y += self.vel

    def collide(self, direction):
        if direction == "x":
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.acc.x > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.acc.x < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.acc.y > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.acc.y < 0:
                    self.rect.y = hits[0].rect.bottom
        if pygame.sprite.spritecollide(self, self.game.enemies, True):
            self.game_over -= 1
            if self.game_over >= 0:
                s = mixer.Sound("ProjectFiles/sound/fall.wav")
                s.play()
                self.image = pygame.image.load("ProjectFiles/img/jumpman_dead.gif")
            if self.game_over == -1:
                self.image = pygame.image.load("ProjectFiles/img/jumpman_dead.gif")
                s = mixer.Sound("ProjectFiles/sound/gameover.wav")
                s.play()
                self.game.level = 1
        if pygame.sprite.spritecollide(self, self.game.ropes, False):
            self.vel = 0
            self.acc.y -= 3
            self.image = pygame.image.load("ProjectFiles/img/jumpman_rope.png")

    def calculate_score(self):
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        if hits:
            s = mixer.Sound('ProjectFiles/sound/coins.wav')
            s.play()
            self.score += 1

    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        self.rect.y -= 2
        if len(hits) > 0 or self.rect.bottom >= WIN_HEIGHT:
            s = mixer.Sound('ProjectFiles/sound/jump.wav')
            s.play()
            self.vel = velocity


class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        block_img = pg.image.load("ProjectFiles/img/platform.png")
        self.image = pg.Surface([16, 16])
        self.image.set_colorkey(BLACK)
        self.image.blit(block_img, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ladder(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LADDER_LAYER
        self.groups = self.game.all_sprites, self.game.ladder
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        block_img = pg.image.load("ProjectFiles/img/stair.gif")
        self.image = pg.Surface([32, 32])
        self.image.set_colorkey(BLACK)
        self.image.blit(block_img, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, content, fontsize):
        self.font = pygame.font.Font('ProjectFiles/arial.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)

        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.coins
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        block_img = pg.image.load("ProjectFiles/img/coin.png")
        self.image = pg.Surface([16, 16])
        self.image.set_colorkey(BLACK)
        self.image.blit(block_img, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.acc = vec(0, 0)
        block_img = pg.image.load("ProjectFiles/img/bird.gif")
        self.image = pg.Surface([16, 16])
        self.image.blit(block_img, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.move()
        self.rect.x += self.acc.x
        self.rect.y += self.acc.y

    def move(self):
        speed = PLAYER_SPEED - 1
        self.acc = vec(0, 0)
        moveright = True

        if moveright:
            if self.game.level == 1:
                if self.rect.y == WIN_HEIGHT - 16:
                    self.rect.y = 0

                if self.rect.x < 0:
                    self.rect.x = 640

                if self.rect.x > 640:
                    self.rect.x = 0

                if self.rect.y < 120:
                    self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                    self.acc.x += speed

                if 120 <= self.rect.y < 240:
                    self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                    self.acc.x -= speed

                if 240 <= self.rect.y < 360:
                    self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                    self.acc.x += speed

                if self.rect.y >= 360:
                    self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                    self.acc.x -= speed

            if self.game.level == 2:
                self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                if self.rect.x < 0:
                    self.rect.x = 640

                if self.rect.x > 640:
                    self.rect.x = 0

                if self.rect.y == WIN_HEIGHT - 16:
                    self.rect.y = 10

                if self.rect.y == 0:
                    self.rect.y = WIN_HEIGHT - 10

                self.acc.x += speed
                self.acc.y += speed

            if self.game.level == 3:
                if self.rect.y == WIN_HEIGHT - 16:
                    self.rect.y = 10

                if self.rect.x < 0:
                    self.rect.x = 640

                if self.rect.x > 640:
                    self.rect.x = 0

                if 0 <= self.rect.x <= 160:

                    if 0 < self.rect.y < 120:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 120 <= self.rect.y < 240:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                    if 240 <= self.rect.y < 360:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 360 <= self.rect.y < 480:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                if 160 < self.rect.x <= 320:

                    if 0 <= self.rect.y < 120:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 120 <= self.rect.y < 240:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                    if 240 <= self.rect.y < 360:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 360 <= self.rect.y < 480:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                if 320 < self.rect.x <= 480:

                    if 0 < self.rect.y < 120:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 120 <= self.rect.y < 240:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                    if 240 <= self.rect.y < 360:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 360 <= self.rect.y < 480:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                if self.rect.x >= 480:

                    if 0 < self.rect.y < 120:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 120 <= self.rect.y < 240:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed

                    if 240 <= self.rect.y < 360:
                        self.image = pg.image.load("ProjectFiles/img/bird_right.gif")
                        self.acc.x += speed
                        self.acc.y += speed

                    if 360 <= self.rect.y < 480:
                        self.image = pg.image.load("ProjectFiles/img/bird_left.gif")
                        self.acc.x -= speed
                        self.acc.y += speed


class Rope(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.ropes
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        block_img = pg.image.load("ProjectFiles/img/rope.jpg")
        self.image = pg.Surface([16, 16])
        self.image.set_colorkey(BLACK)
        self.image.blit(block_img, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
