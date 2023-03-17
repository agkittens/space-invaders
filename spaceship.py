import os
import pygame.sprite

class Ship():
    def __init__(self, x, y, width, height, vel, shipImg):
        self.image = pygame.transform.scale(shipImg, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.maskW, self.maskH = self.mask.get_size()
        self.rect = self.image.get_rect()
        self.laser = None
        self.shipW = width
        self.shipH = height
        self.rect.x = x
        self.rect.y = y
        self.velocity = vel
        self.lasers = pygame.sprite.Group()

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def destroyObject(self, objects, object):
        try:
            del object
        except ValueError:
            return

class Player(Ship):
    def __init__(self):
        self.shipImg = pygame.image.load(os.path.join('assets', 'player.png'))

        super().__init__(500, 600, 200, 200, 3, self.shipImg)
        self.gameLvl = 0
        self.score = 0
        self.hearts = 5
        self.hp = 500
        self.cooldown = 0
        self.laserImg = pygame.image.load(os.path.join('assets', 'main laser.png'))

    def update(self, param):
        self.rect.x += param*self.velocity

    def cooldownFun(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        elif self.cooldown == 0: return True

    def laserInit(self):
        self.lasers.add(Laser(self.rect.x+(self.shipW/2.5), self.rect.y, self.laserImg))
        self.cooldown = 30

    def drawHealthBar(self, window):
        pygame.draw.rect(window, (204, 51, 0), ((self.rect.x +self.shipW/4), self.rect.y+self.shipH-50, 100,10))
        pygame.draw.rect(window, (51, 153, 51), ((self.rect.x +self.shipW/4), self.rect.y+self.shipH-50, 20*self.hp/100,10))

class Invader(Ship):
    def __init__(self, posX, posY):
        self.shipImg = pygame.image.load(os.path.join('assets', 'invader.png'))
        super().__init__(posX, posY, 100, 100, 1, self.shipImg)
        self.laserImg = pygame.image.load(os.path.join('assets', 'inv laser.png'))
        self.moveRight = True

    def update(self):
        if not self.moveRight:
            self.rect.x -= self.velocity
            if self.rect.x <= 100:
                self.moveRight = True

        elif self.moveRight:
            self.rect.x += self.velocity
            if self.rect.x >= 1000:
                self.moveRight = False

    def laserInit(self):
        self.lasers.add(Laser(self.rect.x+(self.shipW/2), self.rect.y, self.laserImg))


class Laser(pygame.sprite.Sprite):
    def __init__(self,x,y,laserImg):
        super(Laser, self).__init__()
        self.image = pygame.transform.scale(laserImg, (100,100))
        self.mask = pygame.mask.from_surface(self.image)
        self.maskW, self.maskH = self.mask.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, param, velocity, window):
        self.rect.y += param*velocity
        if self.rect.y > (window.height-100) or self.rect.y < 0:
            self.kill()

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def checkCollision(self, object, param, objects = None, scoreSprite = None):
        if pygame.sprite.collide_mask(self, object):
            if param == 1:
                if object.hp - 100 == 0:
                    object.hearts -= 1
                    object.hp = 500
                    if object.hearts == 0:
                        del object
                elif object.hp - 100 > 0:
                    object.hp -= 100

                scoreSprite.score -= 50

            if param == -1:
                scoreSprite.score += 100
                try:
                    objects.remove(object)
                except ValueError:
                    return
            self.kill()