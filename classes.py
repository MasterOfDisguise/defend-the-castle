__author__ = 'Simon'
from config import *


class Castle(pygame.sprite.Sprite):

    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.surface = self.manager.surface
        self.image = pygame.image.load("castle.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = width*3/4
        self.rect.y = height*3/4

    def draw(self):
        self.surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, manager, speed, health):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.speed = speed
        self.health = health
        self.surface = self.manager.surface
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

    def move(self):
        if not pygame.sprite.collide_rect(self, self.manager.castle):
            self.rect.x += self.speed


class Upgrade(pygame.sprite.Sprite):

    def __init__(self, manager, x, y, image, effect):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.effect = effect

    def activate_effect(self):
        if self.effect == 'damage_up':
            saved_data["damage"] += 1
            saved_data["upgrade_price"] *= 2


class GameScreen():

    def __init__(self, manager):
        self.manager = manager
        self.surface = self.manager.surface
        self.castle = Castle(self.manager)
        self.enemies = pygame.sprite.Group()
        self.money_counter = eztext.Input(maxlength=45, color=(255, 255, 255), prompt='money: '+str(self.manager.money))
        self.damage = saved_data['damage']
        self.timer = 0

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for enemy in self.enemies:
                if enemy.rect.collidepoint(x, y):
                    enemy.health -= self.damage
                    if enemy.health <= 0:
                        enemy.kill()
                        self.manager.money += 100
        if event.type == pygame.KEYDOWN:
            self.manager.end_game()

    def draw(self):
        self.castle.draw()
        self.enemies.draw(self.surface)

    def update(self):

        self.timer += 1
        if self.timer >= 100:
            enemy = Enemy(self, 1, 2)
            self.enemies.add(enemy)
            self.timer = 0
        for enemy in self.enemies:
            enemy.move()


class MainMenu():

    def __init__(self, manager):
        self.manager = manager
        self.surface = self.manager.surface
        self.button1 = eztext.Input(maxlength=45, color=white, prompt='play')
        self.button1.set_pos(width/2, height*1/4)
        self.button2 = eztext.Input(maxlength=45, color=white, prompt='shop')
        self.button2.set_pos(width/2, height*3/4)

    def draw(self):
        self.button1.draw(self.surface)
        self.button2.draw(self.surface)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 400 <= x <= 440 and 160 <= y <= 170:
                self.manager.screen = GameScreen(self.manager)
            if 400 <= x <= 450 and 455 <= y <= 475:
                self.manager.screen = Shop(self.manager)

    def update(self):
        pass


class Shop():

    def __init__(self, manager):
        self.manager = manager
        self.surface = self.manager.surface
        self.button = eztext.Input(maxlength=45, color=white, prompt='main menu')
        self.button.set_pos(width-150, 0)
        self.upgrades = pygame.sprite.Group()
        self.init_upgrades()

    def draw(self):
        self.button.draw(self.surface)
        self.upgrades.draw(self.surface)

    def init_upgrades(self):
        upgrade = Upgrade(self.manager, 50, 155, 'dmg upgrade.png', 'damage_up')
        self.upgrades.add(upgrade)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 650 <= x <= 765 and y <= 20:
                self.manager.screen = MainMenu(self.manager)
            for upgrade in self.upgrades:
                if upgrade.rect.collidepoint(x, y):
                    if self.manager.money >= saved_data['upgrade_price']:
                        self.manager.money -= saved_data['upgrade_price']
                        upgrade.activate_effect()

    def update(self):
        pass


class Game():

    def __init__(self, surface):
        self.surface = surface
        self.money = int(saved_data['money'])
        self.screen = MainMenu(self)
        self.money_counter = eztext.Input(maxlength=45, color=white, prompt='money: '+str(self.money))

    def draw(self):
        self.screen.draw()
        self.money_counter.draw(self.surface)

    def handle_events(self, event):
        self.screen.handle_events(event)

    def end_game(self):
        saved_data['money'] = self.money
        f = open('saved_data', 'w')
        json_string = json.dumps(saved_data)
        f.write(json_string)
        f.close()
        sys.exit(0)

    def update(self):
        self.money_counter = eztext.Input(maxlength=45, color=white, prompt='money: '+str(self.money))
        self.screen.update()