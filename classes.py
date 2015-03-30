__author__ = 'Simon'
from config import *


class Castle(pygame.sprite.Sprite):

    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.surface = self.manager.surface
        self.image = pygame.image.load("castle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect()
        self.rect.x = width*3/4
        self.rect.y = height*3/4

    def draw(self):
        self.surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, manager, speed, health, damage):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.speed = speed
        self.health = health
        self.damage = damage
        self.surface = self.manager.surface
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500
        self.timer = 0
        self.timer_speed = 1

    def move(self):
        self.rect.x += self.speed
        if pygame.sprite.collide_rect(self, self.manager.castle):
            self.speed = 0
            self.attack()

    def attack(self):
        self.timer += self.timer_speed
        if self.timer <= 40:
            self.image = pygame.image.load("enemy.png").convert_alpha()
        elif self.timer == 50:
            self.image = pygame.image.load("enemy_attack1.png").convert_alpha()
        elif self.timer == 60:
            self.image = pygame.image.load("enemy_attack2.png").convert_alpha()
        elif self.timer == 70:
            self.image = pygame.image.load("enemy_attack3.png").convert_alpha()
        elif self.timer == 80:
            self.image = pygame.image.load("enemy_attack4.png").convert_alpha()
        if self.timer == 80:
            self.timer_speed *= -1
            if pygame.sprite.collide_rect(self, self.manager.castle):
                self.manager.life -= self.damage
                self.manager.health_bar_width -= self.manager.pixels_per_life*self.damage
        if self.timer == 0:
            self.timer_speed *= -1

    def update(self):
        self.move()
        if self.health <= 0:
            self.kill()
            self.manager.manager.money += 100


class Turret(pygame.sprite.Sprite):

    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.surface = self.manager.surface
        self.image = pygame.image.load("turret.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.manager.castle.rect.x
        self.rect.y = self.manager.castle.rect.y + 50
        self.fire_counter = 1000
        self.count = 0
        self.target = False

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def fire(self):
        self.count += 1*saved_data["turret_level"]
        target_list = []
        for enemy in self.manager.enemies:
            target_list.append(enemy)
        if self.count >= self.fire_counter:
            self.image = pygame.image.load("turret fire.png").convert_alpha()
            self.target = random.choice(target_list)
            self.target.health -= 1*saved_data["turret_level"]
            self.count = 0

    def update(self):
        self.image = pygame.image.load("turret.png").convert_alpha()
        self.fire()


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
        if self.effect == 'life_up':
            saved_data["life"] *= 2
            saved_data["upgrade_price"] *= 2


class GameScreen():

    def __init__(self, manager):
        self.manager = manager
        self.surface = self.manager.surface
        self.castle = Castle(self.manager)
        self.life = saved_data["life_max"]
        self.health_bar_width = 200
        self.pixels_per_life = self.health_bar_width/float(self.life)
        self.enemies = pygame.sprite.Group()
        self.turret = Turret(self)
        self.money_counter = eztext.Input(maxlength=45, color=white, prompt='money: '+str(self.manager.money))
        self.button = eztext.Input(maxlength=45, color=white, prompt='main menu')
        self.button.set_pos(width-120, 0)
        self.damage = saved_data['damage']
        self.timer = 0

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for enemy in self.enemies:
                if enemy.rect.collidepoint(x, y):
                    enemy.health -= self.damage
            if x >= width-120 and y <= 20:
                self.manager.screen = MainMenu(self.manager)
        if event.type == pygame.KEYDOWN:
            self.manager.end_game()

    def draw(self):
        self.castle.draw()
        self.turret.draw()
        self.enemies.draw(self.surface)
        self.button.draw(self.surface)
        health_bar = pygame.draw.rect(self.surface, red, (self.castle.rect.x, self.castle.rect.y-40, 200, 20), 0)
        health_bar2 = pygame.draw.rect(self.surface, green, (self.castle.rect.x, self.castle.rect.y-40, self.health_bar_width, 20), 0)

    def update(self):
        self.timer += 1
        if self.timer >= 100:
            enemy = Enemy(self, 1, 2, 1)
            self.enemies.add(enemy)
            self.timer = 0
        self.enemies.update()
        self.turret.update()
        if self.life <= 0:
            self.manager.end_game()


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
        upgrade1 = Upgrade(self.manager, 150, 155, 'life upgrade.png', 'life_up')
        self.upgrades.add(upgrade)
        self.upgrades.add(upgrade1)

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