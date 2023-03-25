import sys, pygame, pygame.freetype, random
pygame.init()

#ALL GLOBAL VARIABLES USED TO CERATE GAME AND SCREEN
global dx, dy, player_1_score, player_2_score, paused_music
paused_music = False
dx = 0
dy = 0
player_1_score = 0
player_2_score = 0
black = 0, 0, 0
white = (255, 255, 255)
size = width, height = 1280, 720
clock = pygame.time.Clock()
line_list = [(width / 2 - 3.5, 0), (width / 2 - 3.5, height / 2), (width / 2 - 3.5, height)]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
ball = pygame.Rect(width / 2 - 10, height / 2 - 5 , 10, 10)
player_1 = pygame.Rect(15, ((height / 2) - 55), 10, 110)
player_2 = pygame.Rect(width - 25, ((height / 2) - 55), 10, 110)
running = True

#---------------------------------------------------------------------------------------------
# These are methods that we will use in the game engine loop----------------------------------

def scoreboard_update():
    font = pygame.font.Font('freesansbold.ttf', 55)

    #Player_1 Scoreboard
    player_1_scoreboard = font.render(str(player_1_score), True, white, None)
    player_1_scoreboard_rect = player_1_scoreboard.get_rect()
    player_1_scoreboard_rect.topleft = ((width / 4) - (player_1_scoreboard_rect.width / 2), 25)
    screen.blit(player_1_scoreboard, player_1_scoreboard_rect)

    #Player_2 Scoreboard
    player_2_scoreboard = font.render(str(player_2_score), True, white, None)
    player_2_scoreboard_rect = player_2_scoreboard.get_rect()
    player_2_scoreboard_rect.topleft = ((width) - (width / 4), 25)
    screen.blit(player_2_scoreboard, player_2_scoreboard_rect)

#This will capture keyboard input and move the player paddles accordingly
def keyboard_check():
    global keys
    if keys[pygame.K_w] and player_1.top > -1:
        player_1.top-=4
    if keys[pygame.K_s] and player_1.bottom < height + 1:
        player_1.top+=4
    if keys[pygame.K_UP] and player_2.top > -1:
        player_2.top-=4
    if keys[pygame.K_DOWN] and player_2.bottom < height + 1:
        player_2.top+=4

def has_won():
    global dx, dy, player_1_score, player_2_score
    if player_1_score == 5:
        dx = 0
        dy = 0
        font = pygame.font.Font('freesansbold.ttf', 60)
        player1_winner = font.render('Player 1 Won!', True, (0, 0, 255), None)
        player1_winner_rect = player1_winner.get_rect()
        player1_winner_rect.center = (width / 2, height / 4)
        play_again = font.render('Press \'r\' to play again', True, (0,0,255), None)
        play_again_rect = play_again.get_rect()
        play_again_rect.center = (width / 2, height / 2)
        screen.blit(player1_winner, player1_winner_rect)
        screen.blit(play_again, play_again_rect)
        return True
    elif player_2_score == 5:
        dx = 0
        dy = 0
        font = pygame.font.Font('freesansbold.ttf', 60)
        player2_winner = font.render('Player 2 Won!', True, (0, 0, 255), None)
        player2_winner_rect = player2_winner.get_rect()
        player2_winner_rect.center = (width / 2, height / 4)
        play_again = font.render('Press \'r\' to play again', True, (0,0,255), None)
        play_again_rect = play_again.get_rect()
        play_again_rect.center = (width / 2, height / 2)
        screen.blit(player2_winner, player2_winner_rect)
        screen.blit(play_again, play_again_rect)
        return True

#This will check collisions and also update score and reset the ball
def collision_check():
    global dx, dy, player_1_score, player_2_score

    if ball.colliderect(player_1) or ball.colliderect(player_2): #CHECKS IF BALL COLLIDES WITH PLAYER 1 OR 2 PADDLES
        if dx < 0 and dx > -13:
            dx *= -1
            dx += 1
        elif dx > 0 and dx < 13:
            dx *= -1
            dx -= 1
        else:
            dx*=-1
    elif ball.right > width + 1: #CHECKS IS PLAYER 1 SCORES AND UPDATES SCORE
        player_1_score += 1
        dx = 0
        dy = 0
        ball.x = width / 2 - 8.5
        ball.y = height / 2 - 5
    elif ball.left < -1: #CHECKS IF PLAYER 2 SCORES AND UPDATES SCORE
        player_2_score += 1
        dx = 0
        dy = 0
        ball.x = width / 2 - 8.5
        ball.y = height / 2 - 5
    elif ball.top <= -1 or ball.bottom >= height + 1: #CHECKS IF BALL HITS EITHER TOP OR BOTTOM OF SCREEN AND INVERTS THE VELOCITY
        dy *= -1

#Playing music
pygame.mixer.music.load('retro music.wav')
pygame.mixer.music.play(-1)

def music_pause():
    pygame.mixer.music.pause()

def music_unpause():
    global paused_music
    pygame.mixer.music.unpause()
    paused_music = False

#-------------------------------------------------------------------------------------------------------------------
# This is the game engine that will run in the background 60 frames per second
while running:
    global keys

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #CREATES A LIST OF PRESSED KEYS
    keys = pygame.key.get_pressed()

    #Keeps running to see if user presses 'p' to pause or play music
    if keys[pygame.K_p] and paused_music == False:
        music_pause()
        paused_music = True
    elif keys[pygame.K_p] and paused_music == True:
        music_unpause()

    #CREATES THE SCREEN
    screen.fill(black)
    scoreboard_update()
    pygame.draw.lines(screen, white, True, line_list, 7)
    pygame.draw.rect(screen, white, player_1)
    pygame.draw.rect(screen, white, player_2)
    pygame.draw.rect(screen, (255, 0, 0), ball)

    #CHECKS KEYBOARD AND COLLISION DETECTION
    collision_check()
    keyboard_check()

    #Tells the user to press 'p' to pause the music
    font = pygame.font.Font('freesansbold.ttf', 15)
    pause_text = font.render('Press \'p\' to pause and resume music', True, white, None)
    pause_text_rect = pause_text.get_rect()
    pause_text_rect.topleft = (5, 15)
    screen.blit(pause_text, pause_text_rect)
    
    #ONLY EXECUTED WHEN GAME IS LAUNCHED OR SOMEONE SCORES
    if (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_w] or keys[pygame.K_s]) and dx == 0 and dy == 0:
        left_or_right = random.choice([-1, 1])
        dx = 4 * left_or_right
        dy = 4 * left_or_right
        ball.right+=dx
        ball.top-=dy

    #KEEPS THE BALL MOVING AFTER IT HAS BEEN GIVEN AN INITIAL VELOCITY
    ball.right+=dx
    ball.top-=dy


    #RUNS WHEN PLAYER HAS WON
    if has_won():
        while True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                player_1_score = 0
                player_2_score = 0
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            screen.fill(black)
            #Tells the user to press 'p' to pause the music
            font = pygame.font.Font('freesansbold.ttf', 15)
            pause_text = font.render('Press \'p\' to pause and resume music', True, white, None)
            pause_text_rect = pause_text.get_rect()
            pause_text_rect.topleft = (15, 15)
            screen.blit(pause_text, pause_text_rect)
            if keys[pygame.K_p] and paused_music == False:
                music_pause()
                paused_music = True
            elif keys[pygame.K_p] and paused_music == True:
                music_unpause()
            has_won()
            scoreboard_update()
            pygame.draw.lines(screen, white, True, line_list, 7)
            pygame.draw.rect(screen, white, player_1)
            pygame.draw.rect(screen, white, player_2)
            pygame.draw.rect(screen, (255, 0, 0), ball)
            pygame.display.flip()
            clock.tick(60)

    pygame.display.flip()
    clock.tick(60)