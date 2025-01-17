import pygame, random
import sys  # Đừng quên import sys để sử dụng sys.exit()
#create function
def draw_floor():
    screen.blit(floor,(floor_x_pos ,650))
    screen.blit(floor,(floor_x_pos+432 ,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos ))
    toptom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-800))
    return bottom_pipe,toptom_pipe
def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 :
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes :
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >=650:
            return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*4,1)
    return new_bird
def score_display(game_state):

    if game_state == 'main game':
        score_surface = game_font.render(str(int (score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int (score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int (high_score)}',True,(255,255,255))
        high_score_rect =  high_score_surface.get_rect(center = (216,630))
        screen.blit( high_score_surface, high_score_rect)
def update_score(score,high_score):
    if score >high_score:
        high_score=score
    return high_score
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)         
pygame.init()
# Thiết lập cửa sổ game
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\04B_19.ttf', 40)
gravity = 0.25
bird_movement = 0
game_active = True
score=0
high_score=0
# bg
bg = pygame.image.load(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\assets\background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#floor
floor = pygame.image.load(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\assets\floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#create bird
bird = pygame.image.load(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\assets\yellowbird-midflap.png').convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))
#create pipe
pipe_surface = pygame.image.load(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\assets\pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#timer
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1000)
pipe_height = [200,300,400]
#game over
game_over_surface = pygame.image.load(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\assets\message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216,384))
#sound
wing_sound = pygame.mixer.Sound(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\sound\sfx_wing.wav')
hit_sound = pygame.mixer.Sound(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\sound\sfx_hit.wav')
score_sound = pygame.mixer.Sound(r'C:\Users\Admin\AppData\Local\Programs\FileGame\FileGame\sound\sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
               # print("bird")
               bird_movement = 0
               bird_movement =-11
               wing_sound.play() 
            if event.key == pygame.K_SPACE and game_active == False:
                game_active=True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            #print("ong")#
            pipe_list.extend(create_pipe())
            #print(create_pipe)#
    # Hiển thị hình nền
    screen.blit(bg, (0,0))
    if game_active:
        #Bird
        bird_movement += gravity
        rotarted_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotarted_bird,bird_rect)
        game_active=check_collision(pipe_list)
        #pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score +=0.01
        score_display('main game')
        score_sound_countdown -=1
        if score_sound_countdown <= 0 :
            score_sound.play()
            score_sound_countdown=100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos=0
    
    pygame.display.update()

    # Kiểm soát tốc độ khung hình
    clock.tick(87)
