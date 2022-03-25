import sys
from ProjectFiles.sprites import *
from ProjectFiles.sprites import Player

pygame.display.set_caption("Jumpman")
icon = pygame.image.load('ProjectFiles/jumpman.ico')
pygame.display.set_icon(icon)


class Game:
    def __init__(self):
        self.level = 1
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('ProjectFiles/arial.ttf', 32)
        self.intro = True
        self.play = True
        self.game_over = 2

    def createTilemap(self, maps):
        for i, row in enumerate(maps):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "L":
                    Ladder(self, j, i)
                if column == "C":
                    Coin(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "R":
                    Rope(self, j, i)

    def new(self, maps):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.ropes = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ladder = pygame.sprite.LayeredUpdates()
        self.coins = pygame.sprite.LayeredUpdates()
        self.player = Player(self, 8, 13)
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.LayeredUpdates()
        self.createTilemap(maps)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN and self.player.vel > velocity:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        self.all_sprites.update()
        if self.player.rect.y > WIN_HEIGHT:
            s = mixer.Sound("ProjectFiles/sound/fall.wav")
            s.play()
            time.sleep(0.5)
            self.player.rect.x = 256
            self.player.rect.y = 416
            self.player.game_over -= 1
            self.game_over -= 1

        if self.player.game_over > -1:
            if len(self.coins) == 0:
                self.level += 1
                if self.level > 4:
                    self.level = 2
                mixer.Sound('ProjectFiles/sound/next_level.wav').play()
                time.sleep(1)
                self.game_screen(True, self.level, 2)
                self.game_over = self.player.game_over
        if self.player.game_over == -1:
            s = mixer.Sound('ProjectFiles/sound/gameover.wav')
            s.play()
            self.game_screen(True, 1, 0)

    def show(self):
        score = self.font.render("Score :" + str(self.player.score), True, WHITE)
        level = self.font.render("Level :" + str(self.level), True, WHITE)
        Health = self.font.render("Health :" + str(self.player.game_over + 1), True, WHITE)
        score_rect = score.get_rect(x=0, y=0)
        self.screen.blit(score, score_rect)
        self.screen.blit(level, (150, 0))
        self.screen.blit(Health, (300, 0))
        pygame.display.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.add()
        self.all_sprites.draw(self.screen)
        self.show()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def intro_screen(self):
        initial = True
        self.bg = pygame.image.load("ProjectFiles/img/bg.jpg")
        title1 = self.font.render('Press Any Key', True, WHITE)
        title_rect = title1.get_rect(x=200, y=440)
        while initial:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    initial = False
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    initial = False

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(title1, title_rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def game_screen(self, intro, level, g_over):
        Play = Button(280, 210, 100, 50, WHITE, 'Play', 32)
        Play_ag = Button(230, 210, 200, 50, WHITE, 'Play again', 32)
        next_level = Button(230, 210, 200, 50, WHITE, 'Next Level', 32)
        q_button = Button(280, 245, 100, 50, WHITE, 'Quit', 32)
        Enter = [Play, q_button]
        over = [Play_ag, q_button]
        Next = [next_level, q_button]
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.playing = False
                    break
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if g_over == 2:
                    if level == 1:
                        self.bg = pygame.image.load("ProjectFiles/img/level_bg.jpg")
                        self.screen.blit(self.bg, (0, 0))
                        for i in range(len(Enter)):
                            self.screen.blit(Enter[i].image, Enter[i].rect)
                        if Play.is_pressed(mouse_pos, mouse_pressed):
                            intro = False
                            self.new(tilemap)
                    if level > 3:
                        self.bg = pygame.image.load("ProjectFiles/img/level_bg.jpg")
                        self.screen.blit(self.bg, (0, 0))
                        title1 = self.font.render('Perfect, You WON', True, RED)
                        title2 = self.font.render('Do you want to play again.', True, RED)
                        title_rect = title1.get_rect(x=200, y=90)
                        title2_rect = title2.get_rect(x=140, y=130)
                        self.screen.blit(title1, title_rect)
                        self.screen.blit(title2, title2_rect)
                    if 1 < level < 4:
                        self.bg = pygame.image.load("ProjectFiles/img/level_bg.jpg")
                        self.screen.blit(self.bg, (0, 0))
                        for i in range(len(Enter)):
                            self.screen.blit(Next[i].image, Next[i].rect)
                        title1 = self.font.render('Congrats, you have completed level '
                                                  '{}.'.format(self.level - 1), True, RED)
                        title2 = self.font.render('Press the "next level" '
                                                  'or Quit.', True, RED)
                        title_rect = title1.get_rect(x=50, y=100)
                        title2_rect = title2.get_rect(x=120, y=150)
                        self.screen.blit(title1, title_rect)
                        self.screen.blit(title2, title2_rect)
                        if next_level.is_pressed(mouse_pos, mouse_pressed):
                            if level == 2:
                                intro = False
                                self.new(tilemap2)
                            if level == 3:
                                intro = False
                                self.new(tilemap3)
                if g_over == 0:
                    self.bg = pygame.image.load("ProjectFiles/img/level_bg.jpg")
                    self.screen.blit(self.bg, (0, 0))
                    title1 = self.font.render('Game Over', True, RED)
                    title_rect = title1.get_rect(x=230, y=90)
                    self.screen.blit(title1, title_rect)
                    for i in range(len(Enter)):
                        self.screen.blit(over[i].image, over[i].rect)
                    if Play_ag.is_pressed(mouse_pos, mouse_pressed):
                        intro = False
                        self.new(tilemap)
                if q_button.is_pressed(mouse_pos, mouse_pressed):
                    intro = False
                    self.playing = False
                    break

                self.clock.tick(FPS)
                pygame.display.update()


game = Game()
game.intro_screen()
if game.running:
    game.game_screen(game.intro, game.level, game.game_over)
while game.running:
    game.main()
pygame.quit()
sys.exit()
