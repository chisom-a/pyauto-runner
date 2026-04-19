#!/usr/bin/env python3

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

#import pprint <-- For debugging
import pygame, pickle
from pygame import mixer
from scripts.game_values import *
from scripts.objects import *
from sys import exit #Terminates the program

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

pygame.init() #Needed to initialize the game

#Load app icon
icon_img = pygame.image.load(os.path.join(IMG_DIR, 'app_icon.png'))
pygame.display.set_icon(icon_img)

#Game fonts
try:
    default_font = pygame.font.SysFont('Bauhaus 93', 70)
    score_font = pygame.font.SysFont('Bauhaus 93', 30)
except:
    default_font = pygame.font.SysFont('freesansbold', 70)
    score_font = pygame.font.SysFont('freesansbold', 30)

#Information on game's state
game_state = State.MAIN_MENU
level = 0
score = 0
#For tiles_placed and each element list in MAX_TILES_PLACED,
#   index 0: Green tiles placed
#   index 1: Green horizontal platforms placed
#   index 2: Green vertical platforms placed
MAX_TILES_PLACED = ( #Store max tiles you can place in each level
    (5, 0, 0),
    (2, 0, 0),
    (0, 2, 0),
    (0, 1, 1),
    (0, 3, 0),
    (0, 2, 1),
    (0, 0, 4),
    (4, 0, 0),
    (0, 0, 4),
    (1, 1, 1)
)
tiles_placed = [0, 0, 0]
tile_to_place = 0

clock = pygame.time.Clock() #Used for frame rate
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BKG_COLOR)
pygame.display.set_caption(GAME_TITLE) #Title of the window

#load title screen and background images
title_img = pygame.image.load(os.path.join(IMG_DIR, 'title.png'))
sun_img = pygame.image.load(os.path.join(IMG_DIR, 'sun.png'))
bg_img = pygame.image.load(os.path.join(IMG_DIR, 'sky.png'))

#load button images
restart_img = pygame.image.load(os.path.join(IMG_DIR, 'restart_btn.png'))
load_img = pygame.image.load(os.path.join(IMG_DIR, 'load_btn.png'))
start_img = pygame.image.load(os.path.join(IMG_DIR, 'start_btn.png'))
exit_img = pygame.image.load(os.path.join(IMG_DIR, 'exit_btn.png'))

#load sounds
pygame.mixer.music.load(os.path.join(AUDIO_DIR, 'music.wav'))
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'coin.wav'))
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'jump.wav'))
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'game_over.wav'))
game_over_fx.set_volume(0.5)
btn_click_fx = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'button_click.wav'))
btn_click_fx.set_volume(0.5)
place_block_fx = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'place_block.wav'))
place_block_fx.set_volume(0.5)

def draw_text(text: str, font: pygame.font.Font, text_col, x: int, y: int):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#create dummy coin for showing score
dummy_coin = Coin(TILE_SIZE // 2 - 3, TILE_SIZE // 2 - 6)

#draws the dummy coin and score counter
def draw_score_counter(screen: pygame.Surface):
    dummy_coin.draw(screen)
    draw_text(f'X {score}', score_font, WHITE, TILE_SIZE - 10, 10)

def empty_sprite_groups():
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    coin_group.empty()
    exit_group.empty()

def draw_sprite_groups(screen: pygame.Surface):
    blob_group.draw(screen)
    platform_group.draw(screen)
    lava_group.draw(screen)
    coin_group.draw(screen)
    exit_group.draw(screen)

def place_tile_in_world(tile_id: int, tile_x: int, tile_y: int):
    global world
    empty_sprite_groups()
    world_data[tile_y][tile_x] = tile_id
    world = World(world_data)

#function to reset level
def reset_level(level: int):
    global world_data, score, tile_to_place, tiles_placed
    player.reset(PLAYER_START_X_POS, PLAYER_START_Y_POS)
    empty_sprite_groups()
    score = 0
    tile_to_place = 0
    tiles_placed = [0, 0, 0]
    
    #load in level data and create world
    level_path = os.path.join(ASSETS_DIR, f'level{level}_data')
    if os.path.exists(level_path):
        pickle_in = open(level_path, 'rb')
        world_data = pickle.load(pickle_in)
        pickle_in.close()
    world = World(world_data)

    return world

class Player():
    def __init__(self, x: int, y: int):
        return self.reset(x, y)

    def reset(self, x: int, y: int):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0 
        for num in range(1, 5):
            img_right = pygame.image.load(os.path.join(IMG_DIR, f'guy{num}.png'))
            img_right = pygame.transform.scale(img_right, (35, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load(os.path.join(IMG_DIR, 'ghost.png'))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.in_air = True

    def update(self, game_state: State):
        dx = 0
        dy = 0
        walk_cooldown = 7
        col_threshold = 20

        if game_state == State.GAMEPLAY:
            #get key presses
            key = pygame.key.get_pressed()
            jump_key_pressed = key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]
            #move_left_key_pressed = key[pygame.K_LEFT] or key[pygame.K_a]
            #move_right_key_pressed = key[pygame.K_RIGHT] or key[pygame.K_d]

            dx += 5 * self.direction
            self.counter += 1

            if jump_key_pressed and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not jump_key_pressed:
                self.jumped = False

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10: self.vel_y = 10
            dy += self.vel_y
            
            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = 5 * self.direction
                
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
            
            #check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False): # pyright: ignore[reportArgumentType]
                game_state = State.GAME_OVER
                game_over_fx.play()
            
            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False): # pyright: ignore[reportArgumentType]
                game_state = State.GAME_OVER
                game_over_fx.play()
            
            #stop player from moving too far left
            if self.rect.x + dx < 0:
                self.direction *= -1
                dx = 5 * self.direction
            
            #check for out-of-bounds position
            is_out_of_bounds = self.rect.x < -100 or self.rect.x > GAME_WIDTH + 40 or self.rect.y < -100 or self.rect.y > GAME_HEIGHT + 100
            if is_out_of_bounds:
                game_state = State.GAME_OVER
                game_over_fx.play()
            
            #check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False): # pyright: ignore[reportArgumentType]
                game_state = State.WON_LEVEL
            
            #check for collision with platforms
            for platform in platform_group:
                #collison in x-direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = 5 * self.direction
                
                #collison in y-direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_threshold:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                        #move sideways with platform
                        if platform.move_x != 0:
                            dx += platform.move_direction

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right): self.index = 0
                
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
        
        elif game_state == State.GAME_OVER:
            self.image = self.dead_image
            if self.rect.y > -100: self.rect.y -= 5
        
        #draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2) #draws player's box area (for debugging)

        return game_state

#load tile images
dirt_img = pygame.image.load(os.path.join(IMG_DIR, 'dirt.png'))
grass_img = pygame.image.load(os.path.join(IMG_DIR, 'grass.png'))
green_tile_img = grass_img.copy()
green_tile_img.fill(USER_TILE_COLOR_RGBA, special_flags=pygame.BLEND_RGBA_ADD)
green_x_platform_img = pygame.image.load(os.path.join(IMG_DIR, 'platform_x.png'))
green_x_platform_img.fill(USER_TILE_COLOR_RGBA, special_flags=pygame.BLEND_RGBA_ADD)
green_y_platform_img = pygame.image.load(os.path.join(IMG_DIR, 'platform_y.png'))
green_y_platform_img.fill(USER_TILE_COLOR_RGBA, special_flags=pygame.BLEND_RGBA_ADD)

green_tile_select_img = pygame.transform.scale(green_tile_img, (TILE_SIZE, TILE_SIZE))
green_x_platform_select_img = pygame.transform.scale(green_x_platform_img, (TILE_SIZE, TILE_SIZE // 2))
green_y_platform_select_img = pygame.transform.scale(green_y_platform_img, (TILE_SIZE, TILE_SIZE // 2))

class World():
    def __init__(self, data: list[list[int]]):
        self.tile_list: list[tuple[pygame.Surface, pygame.Rect]] = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                #See dev_info.txt for tile IDs
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    blob = Enemy(col_count * TILE_SIZE + (TILE_SIZE // 8), row_count * TILE_SIZE + 28)
                    blob_group.add(blob)
                elif tile == 4:
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 1, 0)
                    platform_group.add(platform)
                elif tile == 5:
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 0, 1)
                    platform_group.add(platform)
                elif tile == 6:
                    lava = Lava(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2))
                    lava_group.add(lava)
                elif tile == 7:
                    coin = Coin(col_count * TILE_SIZE + (TILE_SIZE // 2), row_count * TILE_SIZE + (TILE_SIZE // 2))
                    coin_group.add(coin)
                elif tile == 8:
                    exit = Exit(col_count * TILE_SIZE, row_count * TILE_SIZE - (TILE_SIZE // 2))
                    exit_group.add(exit)
                elif tile == 10:
                    img = pygame.transform.scale(green_tile_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 11:
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 1, 0, True)
                    platform_group.add(platform)
                elif tile == 12:
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 0, 1, True)
                    platform_group.add(platform)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2) #draws each tile's box area (for debugging)

#load in level data and create world
level_path = os.path.join(ASSETS_DIR, f'level{level}_data')
pickle_in = open(level_path, 'rb')
world_data = pickle.load(pickle_in)
pickle_in.close()

player = Player(PLAYER_START_X_POS, PLAYER_START_Y_POS)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World(world_data)

#create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 50, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 3), restart_img)
load_button = Button(GAME_WIDTH - (TILE_SIZE + 21), GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2) - 10, load_img)
start_button = Button(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2, start_img)
exit_button = Button(526, SCREEN_HEIGHT // 2, exit_img)

#create tile select buttons
green_tile_button = Button(TILE_SIZE, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2) - TILE_SIZE//2, green_tile_select_img)
green_x_platform_button = Button(5*TILE_SIZE, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2), green_x_platform_select_img)
green_y_platform_button = Button(9*TILE_SIZE, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2), green_y_platform_select_img)

mouse_clicked = True
run = True
while run: #Game loop
    clock.tick(FPS) #60fps (60 frames per second)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if game_state == State.MAIN_MENU:
        screen.blit(title_img, (96, 0))
        if exit_button.draw(screen):
            btn_click_fx.play()
            run = False
        if start_button.draw(screen):
            btn_click_fx.play()
            game_state = State.EDITOR
    else:
        world.draw()
        draw_sprite_groups(screen)
        game_state = player.update(game_state)

        draw_text(f'Level {level+1}', score_font, WHITE, SCREEN_WIDTH // 2 - 50, 10)

        if game_state == State.GAMEPLAY:
            blob_group.update()
            platform_group.update()
            #update score
            #check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True): # pyright: ignore[reportArgumentType]
                score += 1
                coin_fx.play()
            draw_score_counter(screen)

            if restart_button.draw(screen):
                btn_click_fx.play()
                world = reset_level(level)
                game_state = State.EDITOR
                score = 0

        elif game_state == State.EDITOR:
            pos = pygame.mouse.get_pos()
            #draw box for tile selection
            pos_tile_x = pos[0] // TILE_SIZE
            pos_tile_y = pos[1] // TILE_SIZE
            if pos_tile_x < TILES_PER_ROW and pos_tile_y < TILES_PER_COL:
                mouse_tile_rect = pygame.Rect(pos_tile_x * TILE_SIZE, pos_tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, MOUSE_TILE_COLOR, mouse_tile_rect, 2)

            if pygame.mouse.get_pressed()[0] == 1 and not mouse_clicked:
                mouse_clicked = True
                if pos_tile_x < TILES_PER_ROW and pos_tile_y < TILES_PER_COL:
                    place_block_fx.play()
                    selected_tile = world_data[pos_tile_y][pos_tile_x]
                    if selected_tile == 0:
                        if tile_to_place == 10 and tiles_placed[0] < MAX_TILES_PLACED[level][0]:
                            place_tile_in_world(10, pos_tile_x, pos_tile_y)
                            tiles_placed[0] += 1
                        elif tile_to_place == 11 and tiles_placed[1] < MAX_TILES_PLACED[level][1]:
                            place_tile_in_world(11, pos_tile_x, pos_tile_y)
                            tiles_placed[1] += 1
                        elif tile_to_place == 12 and tiles_placed[2] < MAX_TILES_PLACED[level][2]:
                            place_tile_in_world(12, pos_tile_x, pos_tile_y)
                            tiles_placed[2] += 1
                    elif selected_tile == 10:
                        place_tile_in_world(0, pos_tile_x, pos_tile_y)
                        tiles_placed[0] -= 1
                    elif selected_tile == 11:
                        place_tile_in_world(0, pos_tile_x, pos_tile_y)
                        tiles_placed[1] -= 1
                    elif selected_tile == 12:
                        place_tile_in_world(0, pos_tile_x, pos_tile_y)
                        tiles_placed[2] -= 1

            #Draws buttons for picking tile to place
            if green_tile_button.draw(screen):
                btn_click_fx.play()
                tile_to_place = 10
            draw_text(f'X {MAX_TILES_PLACED[level][0] - tiles_placed[0]}', score_font, WHITE, 2*TILE_SIZE + 5, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2))
            if green_x_platform_button.draw(screen):
                btn_click_fx.play()
                tile_to_place = 11
            draw_text(f'X {MAX_TILES_PLACED[level][1] - tiles_placed[1]}', score_font, WHITE, 6*TILE_SIZE + 5, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2))
            if green_y_platform_button.draw(screen):
                btn_click_fx.play()
                tile_to_place = 12
            draw_text(f'X {MAX_TILES_PLACED[level][2] - tiles_placed[2]}', score_font, WHITE, 10*TILE_SIZE + 5, GAME_HEIGHT + (OUTER_MARGIN_HEIGHT // 2))

            #Draw border around the tile button based on the tile the user selected to place
            if tile_to_place == 10:
                pygame.draw.rect(screen, MOUSE_TILE_COLOR, green_tile_button.rect, 3)
            elif tile_to_place == 11:
                pygame.draw.rect(screen, MOUSE_TILE_COLOR, green_x_platform_button.rect, 3)
            elif tile_to_place == 12:
                pygame.draw.rect(screen, MOUSE_TILE_COLOR, green_y_platform_button.rect, 3)

            if load_button.draw(screen):
                btn_click_fx.play()
                game_state = State.GAMEPLAY

        #if player has died
        elif game_state == State.GAME_OVER:
            draw_text('GAME OVER!', default_font, BLUE, (SCREEN_WIDTH // 2) - 180, 140)
            draw_score_counter(screen)
            if restart_button.draw(screen):
                btn_click_fx.play()
                world_data = []
                world = reset_level(level)
                game_state = State.EDITOR
                score = 0
        
        #if player has completed the level
        elif game_state == State.WON_LEVEL:
            #reset game and go to next level
            level += 1
            if level < MAX_LEVELS:
                #reset level
                world = reset_level(level)
                game_state = State.EDITOR
            else:
                game_state = State.WON_GAME
        
        #if player has completed the game
        elif game_state == State.WON_GAME:
            level = 9
            draw_text('YOU WIN!', default_font, BLUE, (SCREEN_WIDTH // 2) - 140, 140)
            #restart game
            if restart_button.draw(screen):
                level = 0
                #reset level
                world = reset_level(level)
                game_state = State.EDITOR
                score = 0
        
        #checks if left mouse button has let go
        if pygame.mouse.get_pressed()[0] == 0:
            mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #User clicks X button on the window
            run = False

    pygame.display.update()

pygame.quit()
exit()