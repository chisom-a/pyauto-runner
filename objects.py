# Copyright 2026 Chisom Anaemeribe
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pygame #, pprint <-- For debugging
from game_values import *

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
        self.image = pygame.image.load(os.path.join(IMG_DIR, 'blob.png'))
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
            img = pygame.image.load(os.path.join(IMG_DIR, 'platform_x.png'))
        else:
            img = pygame.image.load(os.path.join(IMG_DIR, 'platform_y.png'))
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
        img = pygame.image.load(os.path.join(IMG_DIR, 'lava.png'))
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(IMG_DIR, 'coin.png'))
        self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(IMG_DIR, 'exit.png'))
        self.image = pygame.transform.scale(img, (TILE_SIZE, int(TILE_SIZE * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
