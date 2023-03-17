import pygame
import random
from interface import *
from spaceship import *

pygame.init()
pygame.font.init()

player = Player()
invaders = []

window = Window()
surface = window.drawScreen()
start = window.startText.render('press any key to start', True, (255, 247, 0))
win = window.startText.render('VICTORY', True, (255, 247, 0))
lost = window.startText.render('DEFEATED', True, (255, 247, 0))

def spawnInvaders():
    if not len(invaders):
        player.gameLvl += 1
        for _ in range(player.gameLvl+5):
                invaders.append(Invader(random.randrange(100,1000), random.randrange(50, 500)))


def invaderShooting():
    invader = random.choice(invaders)
    invader.laserInit()

def invadersUpdate():
    if len(invaders):
        for invader in invaders:
            invader.update()
            invader.draw(surface)
            invader.lasers.update(1, invader.velocity * 2, window)
            invader.lasers.draw(surface)

def playerUpdate():
    player.draw(surface)
    player.lasers.update(-1, player.velocity, window)
    player.drawHealthBar(surface)
    player.lasers.draw(surface)

def gameUpdate():
    playerLives = window.gameText.render(f'Hearts:{player.hearts} ', True, (255, 247, 0))
    playerHp = window.gameText.render(f'HP:{player.hp} ', True, (255, 247, 0))
    gameLvl = window.gameText.render(f'Lvl:{player.gameLvl} ', True, (255, 247, 0))
    playerScore = window.gameText.render(f'Score:{player.score} ', True, (255, 247, 0))


    surface.blit(window.background, (0, 0))
    surface.blit(playerLives, (10,10))
    surface.blit(playerHp, (10,50))
    surface.blit(gameLvl, (window.width-182,10))
    surface.blit(playerScore, (window.width-182,50))

    playerUpdate()
    spawnInvaders()
    invadersUpdate()

def game():
    shootStatus = False
    run = True
    clock = pygame.time.Clock()
    invaderCooldown = pygame.USEREVENT + 5
    pygame.time.set_timer(invaderCooldown, 2400)

    while run:
        clock.tick(window.fps)
        gameUpdate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == invaderCooldown:
                shootStatus = True
                invaderShooting()

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and (player.rect.x - player.velocity) > 0:
            player.update(-1)
        elif key[pygame.K_RIGHT] and (player.rect.x + player.shipW + player.velocity) < window.width:
            player.update(1)
        elif key[pygame.K_SPACE] and player.cooldownFun():
            player.laserInit()

        if shootStatus:
            for invader in invaders[:]:
                for laser in invader.lasers:
                    laser.checkCollision(player, 1, None, player)
                for laser in player.lasers:
                    laser.checkCollision(invader,-1, invaders, player)

        if player.score == 100:
            gameOver(win)

        if player.hearts == 0 and player.hp == 0:
            gameOver(lost)

        pygame.display.update()
    pygame.quit()


def gameOver(endStatus):
    runStatus = True
    surface.blit(window.background, (0, 0))
    surface.blit(endStatus, (500, 380))

    for invader in invaders[:]:
        invader.destroyObject(invaders, invader)
    player.destroyObject(None, player)

    while runStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runStatus = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                runStatus = False

def run():
    runStatus = True
    clock = pygame.time.Clock()
    surface.blit(window.background, (0, 0))
    surface.blit(start, (300, 400))

    while runStatus:
        clock.tick(window.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runStatus = False
            if event.type == pygame.KEYDOWN:
                game()

        pygame.display.update()
    pygame.quit()