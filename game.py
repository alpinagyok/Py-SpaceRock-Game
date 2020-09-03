import pygame
from random import randint
from math import floor

pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Maksimum punkte projekti eest")
pygame.mouse.set_visible(False)
black = (0,0,0)
white = (255,255,255)
purple = (44,4,91)
clock = pygame.time.Clock()

enemyMinSize = 20
enemyMaxSize = 55
enemyMinSpeed = 1
enemyMaxSpeed = 4

##playerImage on 40x40 pixels
playerImage = pygame.image.load('pla.png')
playerRect = playerImage.get_rect()

enemyImage = pygame.image.load('enemy.jpg')


font = pygame.font.SysFont("verdana", 24)
fontSmall = pygame.font.SysFont("verdana", 16)
def writeText(text, font, surface, x, y):
    textObj = font.render(text, 1, white)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)


gameLoop = True
writeText("What gamemode do you prefer?", font, window, 205, 220)
writeText("1) normal (you hit the block - you die)", font, window, 170, 260)
writeText("2) extravaganza (you can destroy small blocks)", font, window, 118, 290)
writeText("Press \"1\" or \"2\"", fontSmall, window, 330, 370)
pygame.display.update()
while gameLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                playerMoveSpeed = 5
                enemyAddRate = 15
                mode = 1
                gameLoop = False
            if event.key == pygame.K_2:
                playerMoveSpeed = 7
                enemyAddRate = 9
                mode = 2
                gameLoop = False


gameLoopLoop = True
while gameLoopLoop:
    gameLoop = True
    window.fill(black)
    writeText("Welcome to the game! Press any key to start.", font, window, 127, 290)
    pygame.display.update()
    while gameLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                gameLoop = False
                

    playerRect.topleft = (380,280)
    moveRight = moveLeft = moveUp = moveDown = False
    enemyNeededToAdd = 0
    enemies = []
    ticks = score = kills = 0
    gameLoop = True                        
    while gameLoop:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                gameLoop = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    moveRight = True
                if event.key == pygame.K_LEFT:
                    moveLeft = True
                if event.key == pygame.K_DOWN:
                    moveDown = True
                if event.key == pygame.K_UP:
                    moveUp = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moveRight = False
                if event.key == pygame.K_LEFT:
                    moveLeft = False
                if event.key == pygame.K_DOWN:
                    moveDown = False
                if event.key == pygame.K_UP:
                    moveUp = False
        
        
        enemyNeededToAdd += 1
        if enemyNeededToAdd == enemyAddRate:
            x = randint(0,3)
            enemyNeededToAdd = 0
            enemySize = randint(enemyMinSize, enemyMaxSize)
            
            ## Parem tähendab, et liikuma peab paremale, seega asub ekraanist vasakul
            posEnemyRight = [0-enemySize, randint(0, 600-enemySize)]
            posEnemyLeft = [800, randint(0, 600-enemySize)]
            posEnemyDown = [randint(0, 800-enemySize), 0-enemySize]
            posEnemyUp = [randint(0, 800-enemySize), 600]
            posEnemy = [posEnemyRight, posEnemyLeft, posEnemyDown, posEnemyUp]
            
            speed = randint(enemyMinSpeed, enemyMaxSpeed)
            
            ## Suund
            moveEnemyRight = [speed, 0]
            moveEnemyLeft = [-speed, 0]
            moveEnemyDown = [0, speed]
            moveEnemyUp = [0, -speed]
            moveEnemy = [moveEnemyRight, moveEnemyLeft, moveEnemyDown, moveEnemyUp]
            
            newEnemy = {"size": enemySize,
                        "rect": pygame.Rect(posEnemy[x][0], posEnemy[x][1], enemySize, enemySize),
                        "surface": pygame.transform.scale(enemyImage, (enemySize, enemySize)),
                        "direction": moveEnemy[x],
                        "x": x}

            enemies.append(newEnemy)
        
        
        if moveRight and playerRect.right < 800:
            playerRect.move_ip(playerMoveSpeed, 0)
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-playerMoveSpeed, 0)
        if moveDown and playerRect.bottom < 600:
            playerRect.move_ip(0, playerMoveSpeed)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -playerMoveSpeed)
        
        
        for enemy in enemies:
            enemy["rect"].move_ip(enemy["direction"][0], enemy["direction"][1])
        for enemy in enemies:
            if enemy["x"] == 0:
                if enemy["rect"].left > 800:
                    enemies.remove(enemy)
            elif enemy["x"] == 1:
                if enemy["rect"].right < 0:
                    enemies.remove(enemy)
            elif enemy["x"] == 2:
                if enemy["rect"].top > 600:
                    enemies.remove(enemy)
            else:
                if enemy["rect"].bottom < 0:
                    enemies.remove(enemy)
                
                
        window.fill(purple)
        
        window.blit(playerImage, playerRect)
        for enemy in enemies:
            window.blit(enemy["surface"], enemy["rect"])
            
        
        ticks += 1
        score = floor(ticks/60)
        if mode == 1:
            writeText("You have survived for " + str(score) + " seconds", font, window, 20, 20)
        else:
            writeText("You have survived for " + str(score) + " seconds and detroyed " + str(kills) + " blocks", font, window, 20, 20)
        
        clock.tick(60)
        pygame.display.flip()
        
        for enemy in enemies:
            if playerRect.colliderect(enemy["rect"]):
                if mode == 1:
                    gameLoop = False
                else:
                    if enemy["size"] < 40:
                        enemies.remove(enemy)
                        kills += 1
                    else:
                        gameLoop = False
        
        
    window.fill(black)
    writeText("What's wrong? Bad at videogames?", font, window, 184, 270)
    if mode == 1:
        writeText("You survived only for " + str(score) + " seconds...", font, window, 197, 300)
    else:
        writeText("You survived only for " + str(score) + " seconds and destroyed " + str(kills) + " blocks...", font, window, 50, 300)
    writeText("Press \"r\" to play again or \"esc\" to quit", fontSmall, window, 241, 350)
    pygame.display.flip()
    gameLoop = True
    while gameLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = gameLoopLoop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameLoop = gameLoopLoop = False
                if event.key == pygame.K_r:
                    gameLoop = False


pygame.quit()