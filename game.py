import pygame

pygame.init()
mixer = pygame.mixer.init()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.playerx = player_x
        self.playery = player_y
        self.size_x = size_x
        self.size_y = size_y
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        main_window.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        self.player_image = player_image
        self.image = pygame.transform.scale(pygame.image.load(self.player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.direction = "right"
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        pygame.sprite.Sprite.__init__(self)

    def fire(self):
        bullet = Bullet('images/bullets.png', self.rect.centerx, self.rect.top, 64, 64, 20)
        bullets.add(bullet)
    def reset(self):
        main_window.blit(self.image, (self.rect.x, self.rect.y))

    def load_animation(self):
        sheet_right = pygame.image.load(self.player_image).convert_alpha()
        frame_width = 24
        frame_height = 24
        self.frames_right = [
            pygame.transform.scale(sheet_right.subsurface((i * frame_width, 0, frame_width, frame_height)), (64, 64))
            for i in range(4)
        ]
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]
        self.animation_frames = self.frames_right
    
    def update_animation(self):
        if self.direction == "right":
            self.animation_frames = self.frames_right
        elif self.direction == "left":
            self.animation_frames = self.frames_left
        self.frame_index += 0.25
        if self.frame_index >= len(self.animation_frames):
            self.frame_index = 0
        self.image = self.animation_frames[int(self.frame_index)]
    


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.bullet = pygame.transform.scale(pygame.image.load("images/bullets.png"), (320, 64))
        self.direction = "right"
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()

    def load_animation(self):
        sheet_right = pygame.image.load("images/bullets.png").convert_alpha()
        frame_width = 64
        frame_height = 64
        self.frames_right = [
            pygame.transform.scale(sheet_right.subsurface((i * frame_width, 0, frame_width, frame_height)), (64, 64))
            for i in range(5)
        ]
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]
        self.animation_frames = self.frames_right
    
    def update_animation(self):
        if self.direction == "right":
            self.animation_frames = self.frames_right
        elif self.direction == "left":
            self.animation_frames = self.frames_left
        self.frame_index += 0.1
        if self.frame_index >= len(self.animation_frames):
            self.frame_index = 0
        self.image = self.animation_frames[int(self.frame_index)]

    def update(self):
        if game_level == 1:
            if rozumnik.direction == "right":
                self.direction = "right"
                self.rect.x += self.speed
                if self.rect.x > window_width+10:
                    self.kill()
            elif rozumnik.direction == "left":
                self.direction = "left"
                self.rect.x -= self.speed
                if self.rect.x < -10:
                    self.kill()
        self.update_animation()
class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 = x1
        self.x2 = x2

    def update(self):
        if self.rect.x <= self.x1: 
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 =y1
        self.y2 =y2

    def update(self):
        if self.rect.y <= self.y1: 
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

back = (224, 224, 224)
menu_rect_color = (255, 25, 255)

recty_offset = 100
window_width = 1280
window_height = 720
pygame.display.set_icon(pygame.image.load("images/icons/gameico.png"))
main_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Яблуко Долі: Порятунок Білосніжки")
main_window.fill(back)
pygame.display.update()
clock = pygame.time.Clock()
clock.tick(60)
music_state = True
        
def fade(screen, width, height):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

rect_y = 300
rect_x = 580
rect_y_offset = 100

x = 96
y = 616

xspeed = 0
yspeed = 0
############################ menu ############################ 
pygame.mixer.music.load("sounds/bg_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

menu_bg = pygame.transform.scale(pygame.image.load("images/menubg.png"), (window_width, window_height))
menu_bg_color = (79,173, 245)
sound_on_img = pygame.transform.scale(pygame.image.load("images/icons/soundon.png"), (64, 64))
sound_on_hover = pygame.transform.scale(pygame.image.load("images/icons/soundon_hover.png"), (64, 64))
sound_off_img = pygame.transform.scale(pygame.image.load("images/icons/soundoff.png"), (64, 64))
sound_off_hover = pygame.transform.scale(pygame.image.load("images/icons/soundoff_hover.png"), (64, 64))
start = pygame.transform.scale(pygame.image.load("images/icons/start.png"),(188,91))
start_hover = pygame.transform.scale(pygame.image.load("images/icons/start_hover.png"),(188,91))
quit = pygame.transform.scale(pygame.image.load("images/icons/quit.png"),(188,91))
quit_hover = pygame.transform.scale(pygame.image.load("images/icons/quit_hover.png"),(188,91))
font = pygame.font.SysFont("Arial", 30)
start_text = font.render("Грати", True, (0, 0, 0))
quit_text = font.render("Вийти", True, (0, 0, 0))
logo1 = pygame.transform.scale(pygame.image.load("images/logo1.png"), (500,500))

monsters = pygame.sprite.Group()
monster1 = Enemy_h('images/icons/gameico.png', 0, 300, 64, 64, 5, 0, 150)
monster2 = Enemy_h('images/icons/gameico.png', 150, 110, 64, 64, 5, 120, 290)
monsters.add(monster1)
monsters.add(monster2)
coin1 = GameSprite('images/icons/hint.png', 220, 126, 64, 64)
coin2 = GameSprite('images/icons/hint.png', 60, 300, 64, 64)
coin3 = GameSprite('images/icons/hint.png', 585, 310, 64, 64)
coin4 = GameSprite('images/icons/hint.png', 840, 100, 64, 64)
coin5 = GameSprite('images/icons/hint.png', 1000, 410, 64, 64)
coins = pygame.sprite.Group()
bullets = pygame.sprite.Group()
coins.add(coin1)   
coins.add(coin2)
coins.add(coin3)
coins.add(coin4)
coins.add(coin5)
coin_counter = 0
colide = True              
fall = False
key_rect = False
down = False
key = pygame.transform.scale(pygame.image.load("images/icons/key.png"), (64, 64))
platform = pygame.transform.scale(pygame.image.load("images/platforms_lvl1.png"),(window_width,window_height))
rozumnik = Player("images/gnomi/rozumnik.png", x, y, 64, 64, 5, 5)
rozumnik.load_animation()
bg = pygame.transform.scale(pygame.image.load("images/bg.png"), (window_width, window_height))

sonko = Player("images/gnomi/sonko.png", 21, 156, 64, 64, 5, 5)
sonko.load_animation()
lvl2_bg = pygame.transform.scale(pygame.image.load("images/lvl2_bg.png"), (window_width, window_height))
xspeedsonko = 0
yspeedsonko =0
door = pygame.transform.scale(pygame.image.load('images/door.png'),(128,128))

lost_screen = False
game = True
menurunning = True
game_end = False
game_level = 1
jumpreload = 0


# menurunning = False
# game_level = 2
# up_collide = (252, 186, 3) #yellow
# down_collide = (38, 255, 0) #green
# right_collide = (17, 0, 255)
# left_collide = (255, 13, 0)
while game:
    if menurunning:
        start_rect = pygame.draw.rect(main_window, menu_rect_color, (window_width/2-188/2, rect_y, 188, 91), 5)
        quit_rect = pygame.draw.rect(main_window, menu_rect_color, (window_width/2-188/2, rect_y+rect_y_offset, 188, 91), 5)
        main_window.blit(menu_bg, (0,0))
        main_window.blit(logo1, (window_width/2-500/2, -150))
        main_window.blit(start, (window_width/2-188/2, rect_y))
        if start_rect.collidepoint(pygame.mouse.get_pos()):
            main_window.blit(start_hover, (window_width/2-188/2, rect_y))
        main_window.blit(quit, (window_width/2-188/2, rect_y+rect_y_offset))
        if quit_rect.collidepoint(pygame.mouse.get_pos()):
            main_window.blit(quit_hover, (window_width/2-188/2, rect_y+rect_y_offset))
        sound_rect = pygame.draw.rect(main_window, menu_bg_color, (window_width-64, window_height - 64, 64, 64), 1)
        if music_state:
            sound_on = main_window.blit(sound_on_img, (window_width-64, window_height - 64))
            if sound_rect.collidepoint(pygame.mouse.get_pos()):
                sound_on = main_window.blit(sound_on_hover, (window_width-64, window_height - 64))
        elif music_state == False:
            sound_off = main_window.blit(sound_off_img, (window_width-64, window_height - 64))
            if sound_rect.collidepoint(pygame.mouse.get_pos()):
                sound_off = main_window.blit(sound_off_hover, (window_width-64, window_height - 64))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(pygame.mouse.get_pos()):
                    menurunning = False
                    pygame.quit()
                    exit()
                elif start_rect.collidepoint(pygame.mouse.get_pos()):
                    main_window.fill(back)
                    pygame.display.update()
                    fade(main_window, window_width, window_height)
                    game_controls = False
                    menurunning = False
                    main_window.blit(bg, (0,0))
                    if game_level == 1:
                        pygame.mixer.music.load("sounds/lvl1.wav")
                    elif game_level == 2:
                        pygame.mixer.music.load("sounds/lvl2.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)

                elif sound_rect.collidepoint(pygame.mouse.get_pos()):
                    if music_state:
                        music_state = False
                        pygame.mixer.music.pause()
                    else:                            
                        music_state = True
                        pygame.mixer.music.unpause()
    if menurunning == False:
        if game_level == 1:
            key_rect = pygame.Rect(1170, -10, 64, 64)
            if coin_counter == 5:
                pygame.draw.rect(main_window, (0,0,0), key_rect, 1)
            block_rect = pygame.draw.rect(main_window, (0,0,0), (0, 640, 1280, 400), 1)
            platform1 = pygame.draw.rect(main_window, (0,0,0), (150,190,200,50),5)
            platform2 = pygame.draw.rect(main_window, (0,0,0), (450,70,200,50),5)
            platform3 = pygame.draw.rect(main_window, (0,0,0), (1100,48,200,50),5)
            platform4 = pygame.draw.rect(main_window,(0,0,0), (0,360,190,50),5)
            platform5 = pygame.draw.rect(main_window,(0,0,0), (330,510,200,50),5)
            platform6 = pygame.draw.rect(main_window,(0,0,0), (520,360,200,50),5)
            platform7 = pygame.draw.rect(main_window,(0,0,0), (770,160,200,50),5)
            platform8 = pygame.draw.rect(main_window,(0,0,0), (1020,270,200,50),5)
            platform9 = pygame.draw.rect(main_window,(0,0,0), (930,475,200,50),5)
            main_window.blit(bg, (0,0))
            main_window.blit(platform, (0,0))
            rozumnik.update_animation()
            rozumnik.reset()
            coins.draw(main_window)
            bullets.draw(main_window)
            bullets.update()
            monsters.update()
            monsters.draw(main_window)
            if monster1 in monsters:
                monster1.reset()
            else:
                monster1.rect.x -= 10000
            if monster2 in monsters:
                monster2.reset()
            else:
                monster2.rect.x -= 10000
            for bullet in bullets:
                for monster in monsters:
                    if bullet.rect.colliderect(monster.rect):
                        bullet.kill()
                        monster.kill()
            if monster2.rect.colliderect(rozumnik.rect) or monster1.rect.colliderect(rozumnik.rect):
                fade(main_window, window_width, window_height)
                rozumnik.rect.x, rozumnik.rect.y = x, y
                bullets.empty()
                for coin in coins:
                    coin.add(coins)
                menurunning = True
                pygame.mixer.music.stop()
                if music_state:
                    pygame.mixer.music.load("sounds/bg_music.wav")
                    pygame.mixer.music.play(-1)
            if coin1.alive() and coin1.rect.colliderect(rozumnik.rect):
                coin1.kill()
                coin_counter += 1
            elif coin2.alive() and coin2.rect.colliderect(rozumnik.rect):
                coin2.kill()
                coin_counter += 1
            elif coin3.alive() and coin3.rect.colliderect(rozumnik.rect):
                coin3.kill()
                coin_counter += 1
            elif coin4.alive() and coin4.rect.colliderect(rozumnik.rect):
                coin4.kill()
                coin_counter += 1
            elif coin5.alive() and coin5.rect.colliderect(rozumnik.rect):
                coin5.kill()
                coin_counter += 1
            if coin_counter == 5:
                main_window.blit(key, (1170,-10))
                if key_rect.colliderect(rozumnik.rect):
                    fade(main_window,window_width, window_height)
                    game_level = 2
                    pygame.mixer.music.stop()
                    coin_counter = 0
                    menurunning = True
                    main_window.fill(back)
                    if music_state:
                        pygame.mixer.music.load("sounds/bg_music.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_w:
                        if jumpreload == 1:
                            yspeed -= rozumnik.y_speed
                            jumpreload = 0
                    if e.key == pygame.K_a: 
                        rozumnik.direction = "left"
                        xspeed -= rozumnik.x_speed
                    if e.key == pygame.K_s:
                        if down:
                            yspeed += rozumnik.y_speed
                    if e.key == pygame.K_d:
                        rozumnik.direction = "right"
                        xspeed += rozumnik.x_speed
                    if e.key == pygame.K_SPACE:
                        rozumnik.fire()
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_w or e.key == pygame.K_s:
                        yspeed = 0
                        jumpreload = 0
                        fall = True
                        if colide:
                            fall = False
                        else:
                            fall = True
                    if e.key == pygame.K_a or e.key == pygame.K_d:
                        xspeed = 0
                        if colide:
                            fall = False
                        else:
                            fall = True
            if rozumnik.rect.colliderect(block_rect) or rozumnik.rect.colliderect(platform1) or rozumnik.rect.colliderect(platform2) or rozumnik.rect.colliderect(platform3) or rozumnik.rect.colliderect(platform4) or rozumnik.rect.colliderect(platform5) or rozumnik.rect.colliderect(platform6) or rozumnik.rect.colliderect(platform7) or rozumnik.rect.colliderect(platform8) or rozumnik.rect.colliderect(platform9):
                colide = True
            else:
                colide = False
            if colide:
                jumpreload = 1
                fall = False
                down = False
            else:
                if fall == True:
                    rozumnik.rect.y += rozumnik.y_speed
                down = True
            rozumnik.rect.x += xspeed
            rozumnik.rect.y += yspeed
            if rozumnik.rect.y < -32:
                rozumnik.rect.y += 5
            elif rozumnik.rect.y-64 > window_height:
                rozumnik.rect.y -= 5
            if rozumnik.rect.x < 0:
                rozumnik.rect.x += 5
            elif rozumnik.rect.x > window_width:
                rozumnik.rect.x -= 5
        if game_level == 2:
            wallh1 = pygame.draw.rect(main_window, back, (0, 120, 510, 15), 15)
            wallh2 = pygame.draw.rect(main_window, back, (0, 250, 420, 15), 15)
            wallh3 = pygame.draw.rect(main_window, back, (120, 450, 300, 15), 15)
            wallh4 = pygame.draw.rect(main_window, back, (200, 630, 300, 15), 15)
            wallh5 = pygame.draw.rect(main_window, back, (500, 270, 345, 15), 15)
            wallh6 = pygame.draw.rect(main_window, back, (500, 400, 180, 15), 15)
            wallh7 = pygame.draw.rect(main_window, back, (780, 400, 160, 15), 15)
            wallh8 = pygame.draw.rect(main_window, back, (830, 120, 500, 15), 15)
            wallh9 = pygame.draw.rect(main_window, back, (940, 240, 640, 15), 15)
            wallh10 = pygame.draw.rect(main_window, back, (780, 580, 290, 15), 15)
            wallh11 = pygame.draw.rect(main_window, back, (1060, 440, 640, 15), 15)
            wallv1 = pygame.draw.rect(main_window, back, (405, 250, 15, 200), 15)
            wallv2 = pygame.draw.rect(main_window, back, (120, 450, 15, 550), 15)
            wallv3 = pygame.draw.rect(main_window, back, (500, 120, 15, 160), 15)
            wallv4 = pygame.draw.rect(main_window, back, (500, 400, 15, 240), 15)
            wallv5 = pygame.draw.rect(main_window, back, (200, 630, 15, 500), 15)
            wallv6 = pygame.draw.rect(main_window, back, (680, 400, 15, 600), 15)
            wallv7 = pygame.draw.rect(main_window, back, (780, 400, 15, 190), 15)
            wallv8 = pygame.draw.rect(main_window, back, (830, 120, 15, 165), 15)
            wallv9 = pygame.draw.rect(main_window, back, (940, 240, 15, 170), 15)
            wallv10 = pygame.draw.rect(main_window, back, (1050, 440, 15, 160), 15)
            main_window.blit(lvl2_bg, (0,0))
            main_window.blit(door, (1100,130))
            sonko.update_animation()
            sonko.reset()
            if sonko.rect.colliderect(wallh1) or sonko.rect.colliderect(wallh3) or sonko.rect.colliderect(wallh5) or sonko.rect.colliderect(wallh8) or sonko.rect.colliderect(wallh11) or sonko.rect.colliderect(wallh10):
                sonko.rect.y += 5
            if sonko.rect.colliderect(wallh2) or sonko.rect.colliderect(wallh4) or sonko.rect.colliderect(wallh6) or sonko.rect.colliderect(wallh7) or sonko.rect.colliderect(wallh9) or sonko.rect.y > window_height-64:
                sonko.rect.y -= 5
            if sonko.rect.colliderect(wallv1) or sonko.rect.colliderect(wallv2) or sonko.rect.colliderect(wallv6) or sonko.rect.colliderect(wallv8) or sonko.rect.colliderect(wallv10) or sonko.rect.x < 0:
                sonko.rect.x += 5
            if sonko.rect.colliderect(wallv3) or sonko.rect.colliderect(wallv4) or sonko.rect.colliderect(wallv5) or sonko.rect.colliderect(wallv7) or sonko.rect.colliderect(wallv9) or sonko.rect.x > window_width-64:
                sonko.rect.x -= 5
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_w:
                        yspeedsonko -= sonko.y_speed
                    if e.key == pygame.K_s:
                        yspeedsonko += sonko.y_speed
                    if e.key == pygame.K_a:
                        sonko.direction = 'left'
                        xspeedsonko -= sonko.x_speed
                    if e.key == pygame.K_d:
                        sonko.direction = "right"
                        xspeedsonko += sonko.x_speed
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_w or e.key == pygame.K_s:
                        yspeedsonko = 0
                    if e.key == pygame.K_a or e.key == pygame.K_d:
                        xspeedsonko = 0
            sonko.rect.x += xspeedsonko
            sonko.rect.y += yspeedsonko
    clock.tick(60)
    pygame.display.update()
pygame.quit()
exit()