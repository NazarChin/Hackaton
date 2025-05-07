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
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed, bullet_image):
        self.player_image = player_image
        self.image = pygame.transform.scale(pygame.image.load(self.player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.bullet = bullet_image
        self.bullet_image = bullet_image
        self.direction = "right"
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        pygame.sprite.Sprite.__init__(self)

    def fire(self):
        bullet = Bullet('images/bullet.png', self.rect.centerx, self.rect.top, 64, 64, 20)
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
    

class Rozumnik(Player):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed, bullet_image):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed, bullet_image)

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
logo2 = pygame.transform.scale(pygame.image.load("images/logo2.png"), (500,500))

############################ game controls ############################
game_controls_shown = False
game_controls = False
controls = pygame.transform.scale(pygame.image.load("images/controls.png"), (window_width, window_height))
close = pygame.transform.scale(pygame.image.load("images/icons/close.png"), (64,64))
close_hover = pygame.transform.scale(pygame.image.load("images/icons/close_hover.png"), (64,64))

############################ lvl 1 ############################
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
key = pygame.transform.scale(pygame.image.load("images/icons/key.png"), (64, 64))
platform = pygame.transform.scale(pygame.image.load("images/platforms_lvl1.png"),(1280,720))
rozumnik = Rozumnik("images/gnomi/rozumnik.png", x, y, 64, 64, 5, 5, "images/gnomi/rozumnik_ghost.png")
rozumnik.load_animation()
bg = pygame.transform.scale(pygame.image.load("images/bg.png"), (window_width, window_height))

i = 0

game = True
menurunning = True
game_end = False
game_level = 0
jumpreload = 0

while game:
    if menurunning:
        start_rect = pygame.draw.rect(main_window, menu_rect_color, (window_width/2-188/2, rect_y, 188, 91), 5)
        quit_rect = pygame.draw.rect(main_window, menu_rect_color, (window_width/2-188/2, rect_y+rect_y_offset, 188, 91), 5)
        main_window.blit(menu_bg, (0,0))
        main_window.blit(logo1, (window_width/2-500/2, -150))
        main_window.blit(start, (window_width/2-188/2, rect_y)) #play text
        if start_rect.collidepoint(pygame.mouse.get_pos()):
            main_window.blit(start_hover, (window_width/2-188/2, rect_y)) #play text
        main_window.blit(quit, (window_width/2-188/2, rect_y+rect_y_offset)) #quit text
        if quit_rect.collidepoint(pygame.mouse.get_pos()):
            main_window.blit(quit_hover, (window_width/2-188/2, rect_y+rect_y_offset))
        sound_rect = pygame.draw.rect(main_window, menu_bg_color, (window_width-64, window_height - 64, 64, 64), 1)
        if music_state:
            sound_on = main_window.blit(sound_on_img, (window_width-64, window_height - 64)) #sound on icon
            if sound_rect.collidepoint(pygame.mouse.get_pos()):
                sound_on = main_window.blit(sound_on_hover, (window_width-64, window_height - 64))
        elif music_state == False:
            sound_off = main_window.blit(sound_off_img, (window_width-64, window_height - 64)) #sound off icon
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
                    fade(main_window, window_width, window_height)
                    game_controls = True
                    menurunning = False
                    pygame.mixer.music.stop()
                elif sound_rect.collidepoint(pygame.mouse.get_pos()):
                    if music_state:
                        music_state = False
                        pygame.mixer.music.pause()
                    else:                            
                        music_state = True
                        pygame.mixer.music.unpause()

    elif menurunning == False:
        if game_controls:
            i += 1
            close_game_controls = pygame.draw.rect(main_window, back, (window_width-64, 0, 64, 64), 5)
            main_window.blit(menu_bg,(0,0))
            main_window.blit(controls, (0,0))
            if close_game_controls.collidepoint(pygame.mouse.get_pos()):
                main_window.blit(close_hover, (window_width-64, 0))
            else:
                main_window.blit(close, (window_width-64, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if close_game_controls.collidepoint(pygame.mouse.get_pos()):
                        fade(main_window, window_width, window_height)
                        game_controls = False
                        menurunning = False
                        game_level = 1
                        main_window.blit(bg, (0,0))
                        pygame.mixer.music.load("sounds/lvl1.wav")
                        if music_state:
                            pygame.mixer.music.set_volume(0.5)
                            pygame.mixer.music.play(-1)
            if i/60 == 5:
                fade(main_window, window_width, window_height)
                game_controls = False
                menurunning = False
                game_level = 1
                main_window.blit(bg, (0,0))
                pygame.mixer.music.load("sounds/lvl1.wav")
                if music_state:
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                i = 0
        elif game_level == 1:
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
                jumpreload = 1
                fall = False
            else:
                if fall == True:
                    rozumnik.rect.y += rozumnik.y_speed
            rozumnik.rect.x += xspeed
            rozumnik.rect.y += yspeed
            if rozumnik.rect.colliderect(block_rect) or rozumnik.rect.colliderect(platform1) or rozumnik.rect.colliderect(platform2) or rozumnik.rect.colliderect(platform3) or rozumnik.rect.colliderect(platform4) or rozumnik.rect.colliderect(platform5) or rozumnik.rect.colliderect(platform6) or rozumnik.rect.colliderect(platform7) or rozumnik.rect.colliderect(platform8) or rozumnik.rect.colliderect(platform9):
                colide = True
            else:
                colide = False
        if game_level == 2:
            main_window.blit(menu_bg, (50,50))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
    clock.tick(60)
    pygame.display.update()
pygame.quit()
exit()