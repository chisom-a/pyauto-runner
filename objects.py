import os.path, pygame #, pprint <-- For debugging
from game_values import *

#Getting directory where script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    
    def draw(self, screen: pygame.Surface):
        action = False

        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            #checks if left mouse button is pressed
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        #checks if left mouse button has let go
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(script_dir, 'assets/img/blob.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50: 
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, move_x: int, move_y: int, is_user_tile=False):
        pygame.sprite.Sprite.__init__(self)
        if move_x == 1:
            img = pygame.image.load(os.path.join(script_dir, 'assets/img/platform_x.png'))
        else:
            img = pygame.image.load(os.path.join(script_dir, 'assets/img/platform_y.png'))
        if is_user_tile:
            img.fill(USER_TILE_COLOR_RGBA, special_flags=pygame.BLEND_RGBA_ADD)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y
    
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50: 
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(script_dir, 'assets/img/lava.png'))
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(script_dir, 'assets/img/coin.png'))
        self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(script_dir, 'assets/img/exit.png'))
        self.image = pygame.transform.scale(img, (TILE_SIZE, int(TILE_SIZE * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
