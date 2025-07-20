import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((1920, 1080), vsync = 1)
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(0)
pygame.display.set_caption("Clean Sweep")
pygame.display.toggle_fullscreen()

TOGGLE_CLICKSTART = pygame.USEREVENT + 1
TOGGLE_HIT_TEXT = pygame.USEREVENT + 2
TOGGLE_PLAYER_COUNT = pygame.USEREVENT + 3
TOGGLE_ARROW = pygame.USEREVENT + 4

running = True

gameStarted = False
whichPlayer = 1
mode = "One-player"
clickStartVisible = True
pointsP1 = 0
pointsP2 = 0
drawBall = True
hitTextVisible = False
lostBallsP1 = 1
lostBallsP2 = 1
infiniteLives = False
screenClearP1 = False
screenClearP2 = False
playerCountVisible = True
arrowVisible = True

# ---CZCIONKI---
ramtek = pygame.font.Font("ramtek.otf", 40)
freesansbold = pygame.font.Font("freesansbold.ttf", 25)
ramtekSmall = pygame.font.Font("ramtek.otf", 15)

# ---DZWIEKI---
paddleSound = pygame.mixer.Sound("paddle.mp3")
wallSound = pygame.mixer.Sound("wall.mp3")
dotSound = pygame.mixer.Sound("dot.mp3")
ballOutSound = pygame.mixer.Sound("ballOut.mp3")

# elementy gry
wallLeft = pygame.Rect(250, 0, 10, 1080)
wallRight = pygame.Rect(1660, 0, 10, 1080)
wallTop = pygame.Rect(260, 0, 1400, 10)
dotImg = pygame.image.load("dot.png").convert_alpha()
dot = pygame.Rect(0, 0, 16, 16)
ballImg = pygame.image.load("ball.png").convert_alpha()
ball = pygame.Rect(960, 1000, 18, 18)
paddleImg = pygame.image.load("paddle.png").convert_alpha()
paddle = pygame.Rect(930, 1050, 60, 30)
bar = pygame.Rect(260, 1040, 1400, 10)
arrowP1Img = pygame.image.load("arrowP1.png").convert_alpha()
arrowP1 = pygame.Rect(600, 30, 101, 30)
arrowP2Img = pygame.image.load("arrowP2.png")
arrowP2 = pygame.Rect(815, 30, 101, 30)
ballOutCheck = pygame.Rect(0, 1085, 1920, 30)

# zmienne ball
ballAngle = 148
ballAngleRad = math.radians(ballAngle)

ballSpeed = random.randint(4, 8)

ballVelX = math.cos(ballAngleRad) * ballSpeed
ballVelY = -math.sin(ballAngleRad) * ballSpeed

# zmienne dots
rows = 14
columns = 21
gap = 50
dotX = 290
dotY = 100

def newDotsP1():
    global row, dotsP1, column
    
    dotsP1 = []

    for row in range(rows):
        for column in range(columns):
            x = dotX + column * (16 + gap)
            y = dotY + row * (16 + gap)

            dot = pygame.Rect(x, y, 16, 16)
            dotsP1.append(dot)
    
    return dotsP1

def newDotsP2():
    global row, dotsP2, column

    dotsP2 = []

    for row in range(rows):
        for column in range(columns):
            x = dotX + column * (16 + gap)
            y = dotY + row * (16 + gap)

            dot = pygame.Rect(x, y, 16, 16)
            dotsP2.append(dot)

    return dotsP2

def checkOffset():
    offset = ball.centerx - paddle.centerx
    
    return offset

def dynamicBallRotationAngle():
    maxOffset = paddle.width / 2 # max offset czyli polowa dlugosci paddle

    offset = checkOffset()
    offset = min(offset, maxOffset) # najmniejsza wartosc z offset i maxOffset

    normalizedOffset = offset / maxOffset # teraz offset jest liczba z przedzialu [-1, 1]

    ballAngle = 90 - normalizedOffset * 45 # ustawianie kata w przedziale [45, 135] w zaleznosci od offset. Im blizej srodka tym normalizedOffset blizszy zeru wiec kat bedzie bardziej pionowy bo mniej sie odejmie od 90

    return ballAngle

def startGame():
    global gameStarted, whichPlayer, mode, clickStartVisible, pointsP1, pointsP2, drawBall, lostBallsP1, lostBallsP2, ball, screenClearP1, screenClearP2, dotsP1, dotsP2

    gameStarted = True

    ball = pygame.Rect(960, 1000, 18, 18)
    whichPlayer = 1
    clickStartVisible = True
    pointsP1 = 0
    pointsP2 = 0
    drawBall = False
    lostBallsP1 = 1
    lostBallsP2 = 1
    screenClearP1 = False
    screenClearP2 = False

    dotsP1 = newDotsP1()
    dotsP2 = newDotsP2()
    
def throwBall():
    global drawBall, ball, ballVelX, ballVelY

    drawBall = True

    ball = pygame.Rect(960, 1000, 18, 18)
    ballAngle = 145
    ballAngleRad = math.radians(ballAngle)

    ballSpeed = 10

    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed

def ballOut():
    global drawBall, ball, lostBallsP1, lostBallsP2

    drawBall = False
    ball = pygame.Rect(960, 1000, 18, 18)

    if infiniteLives == False:
        if whichPlayer == 1:
            lostBallsP1 += 1
        
        elif whichPlayer == 2:
            lostBallsP2 += 1
    
    if gameStarted:
        ballOutSound.stop()
        ballOutSound.play()


newDotsP1()
newDotsP2()

pygame.time.set_timer(TOGGLE_CLICKSTART, 2000)
pygame.time.set_timer(TOGGLE_PLAYER_COUNT, 50)
pygame.time.set_timer(TOGGLE_ARROW, 50)

while running:
    pressedKeys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mode == "One-player":
        whichPlayer = 1

    if drawBall:
        arrowVisible = True

    if not dotsP1:
        screenClearP1 = True
    
    if not dotsP2:
        screenClearP2 = True

    # obsluga eventow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if pressedKeys[pygame.K_LCTRL]:
            running = False

        if pressedKeys[pygame.K_m]:
            if mode == "One-player":
                mode = "Two-player"
            
            elif mode == "Two-player":
                mode = "One-player"

        if event.type == TOGGLE_CLICKSTART:
            clickStartVisible = not clickStartVisible
        
        if event.type == TOGGLE_HIT_TEXT:
            hitTextVisible = False
        
        if event.type == TOGGLE_PLAYER_COUNT and gameStarted == False:
            playerCountVisible = not playerCountVisible
        
        if event.type == TOGGLE_ARROW and gameStarted == True and drawBall == False:
            arrowVisible = not arrowVisible

        if event.type == pygame.MOUSEBUTTONDOWN and gameStarted == False:
            startGame()
        
        if gameStarted == True:
            if pressedKeys[pygame.K_g] and drawBall == False:
                throwBall()
        
        if gameStarted == False:
            if pressedKeys[pygame.K_i]:
                infiniteLives = True

        
    
    # ---GRAFIKA---
    screen.fill("black")

    pygame.draw.rect(screen, [0, 204, 204], wallLeft)
    pygame.draw.rect(screen, [0, 204, 204], wallRight)
    pygame.draw.rect(screen, [0, 204, 204], wallTop)
    screen.blit(paddleImg, paddle)
    if drawBall:
        screen.blit(ballImg, ball)

    if whichPlayer == 1:
        for dot in dotsP1:
            screen.blit(dotImg, dot)
    
    elif whichPlayer == 2:
        for dot in dotsP2:
            screen.blit(dotImg, dot)

    # teksty
    clickStartText = freesansbold.render("CLICK START", True, [0, 204, 204])
    freePlayText = freesansbold.render("FREE PLAY", True, [0, 204, 204])

    modeText = freesansbold.render("Mode: {}".format(mode), True, [0, 204, 204])

    hitText = ramtekSmall.render("HIT", True, "black")


    # punkty p1
    P1Hundered = ramtek.render("{}".format(pointsP1 // 100), True, [0, 204, 204])
    P1Ten = ramtek.render("{}".format((pointsP1 // 10) % 10), True, [0, 204, 204])
    P1One = ramtek.render("{}".format(pointsP1 % 10), True, [0, 204, 204])
    P1zero = ramtek.render("00", True, [0, 204, 204])

    screen.blit(P1Hundered, [350, 20])
    screen.blit(P1Ten, [390, 20])
    screen.blit(P1One, [430, 20])
    screen.blit(P1zero, [470, 20])

    # punkty p2
    P2Hundered = ramtek.render("{}".format(pointsP2 // 100), True, [0, 204, 204])
    P2Ten = ramtek.render("{}".format((pointsP2 // 10)% 10), True, [0, 204, 204])
    P2One = ramtek.render("{}".format(pointsP2 % 10), True, [0, 204, 204])
    P2zero = ramtek.render("00", True, [0, 204, 204])

    screen.blit(P2Hundered, [950, 20])
    screen.blit(P2Ten, [990, 20])
    screen.blit(P2One, [1030, 20])
    screen.blit(P2zero, [1070, 20])

    # stracone pilki
    if whichPlayer == 1:
        lostBallsText = ramtek.render("{}".format(lostBallsP1), True, [0, 204, 204])
    
    elif whichPlayer == 2:
        lostBallsText = ramtek.render("{}".format(lostBallsP2), True, [0, 204, 204])
    
    screen.blit(lostBallsText, [740, 20])

    # strzalka graczy
    if arrowVisible:
        if whichPlayer == 1:
            screen.blit(arrowP1Img, arrowP1)
        
        elif whichPlayer == 2:
            screen.blit(arrowP2Img, arrowP2)

    # ilosc graczy na gre
    if mode == "One-player":
        playerCount = ramtek.render("1", True, [0, 204, 204])
    
    elif mode == "Two-player":
        playerCount = ramtek.render("2", True, [0, 204, 204])

    if playerCountVisible:
        screen.blit(playerCount, [1300, 20])

    # ---LOGIKA---
    # ruch ball
    if drawBall:
        ball.centerx += ballVelX
        ball.centery += ballVelY

    # odbijanie ball od scian
    if ball.colliderect(wallLeft):
        ballVelX *= -1

        if gameStarted:
            wallSound.stop()
            wallSound.play()

    if ball.colliderect(wallRight):
        ballVelX *= -1

        if gameStarted:
            wallSound.stop()
            wallSound.play()

    if ball.colliderect(wallTop):
        ballVelY *= -1

        if gameStarted:
            wallSound.stop()
            wallSound.play()

    # poza gra
    if gameStarted == False:
        if ball.colliderect(bar):
            ballAngle = random.randint(58, 148)
            ballAngleRad = math.radians(ballAngle)

            ballSpeed = random.randint(4, 8)

            ballVelX = math.cos(ballAngleRad) * ballSpeed
            ballVelY = -math.sin(ballAngleRad) * ballSpeed
        
        if clickStartVisible:
            screen.blit(clickStartText, [1720, 1000])
        
        elif not clickStartVisible:
            screen.blit(freePlayText, [1735, 1000])

        screen.blit(modeText, [25, 1000])
     # podczas gry
    if gameStarted == True:
        playerCountVisible = True
        
        # ruch paddle
        paddle.centerx = mouse_x

        screen.blit(paddleImg, paddle)

        # odbijanie ball od paddle
        if ball.colliderect(paddle):
            ballAngle = dynamicBallRotationAngle()

            ballAngleRad = math.radians(ballAngle)

            ballSpeed = random.randint(4, 8)

            ballVelX = math.cos(ballAngleRad) * ballSpeed
            ballVelY = -math.sin(ballAngleRad) * ballSpeed

            hitTextVisible = True
            pygame.time.set_timer(TOGGLE_HIT_TEXT, 50, loops = 1)

            if gameStarted:
                paddleSound.stop()
                paddleSound.play()

        # tekst "HIT" na paddle
        if hitTextVisible:
            screen.blit(hitText, (paddle.left + 15, paddle.top + 5))
        
        # pilka wypada
        if ball.colliderect(ballOutCheck):
            ballOut()

        # zbijanie kropek
        if whichPlayer == 1:
            for idx, dot in enumerate(dotsP1):
                if ball.colliderect(dot):
                    del dotsP1[idx]
                    pointsP1 += 1

                    if gameStarted:
                        dotSound.stop()
                        dotSound.play()
        
        if whichPlayer == 2:
            for idx, dot in enumerate(dotsP2):
                if ball.colliderect(dot):
                    del dotsP2[idx]
                    pointsP2 += 1

                    if gameStarted:
                        dotSound.stop()
                        dotSound.play()

        # zakonczenie
        # wygrana
        if mode == "One-player":
            if not dotsP1:
                gameStarted = False
                paddle = pygame.Rect(930, 1050, 60, 30)
        
        if mode == "Two-player":
            if whichPlayer == 1:
                if not dotsP1:
                    drawBall = False
                    ball = pygame.Rect(960, 1000, 18, 18)
                    whichPlayer = 2

            if whichPlayer == 2:
                if not dotsP2:
                    gameStarted = False
                    paddle = pygame.Rect(930, 1050, 60, 30)
        
        # przegrana
        if mode == "One-player":
            if lostBallsP1 == 6:
                gameStarted = False
                paddle = pygame.Rect(930, 1050, 60, 30)
        
        if mode == "Two-player":
            if lostBallsP1 == 6:
                drawBall = False
                ball = pygame.Rect(960, 1000, 18, 18)
                whichPlayer = 6
                lostBallsP1 += 1

            if lostBallsP2 == 6:
                gameStarted = False
                paddle = pygame.Rect(930, 1050, 60, 30)

    pygame.display.flip()

    clock.tick(240)