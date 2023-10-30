import pygame as pg
import math
# import Classe_Player as obj
from random import *
from random import *
import tkinter as tk
from sys import exit
from pygame.locals import *

root = tk.Tk()
pg.init()

largura = 740
altura = 650
largura = root.winfo_screenwidth()
altura = root.winfo_screenheight()

screen = pg.display.set_mode((largura,altura-50))


class Asteroide(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.sprites_asteroide = []
        valor = randint(0,2)
        self.index = valor
        self.spritesheet = pg.image.load('./assets/sprites/Asteroides_Sprite.png').convert_alpha()
        for y in range(2):
            for x in range(7):
                img = self.spritesheet.subsurface((x*96,y*96),(96,96))
                # img = pg.transform.scale(img,(64,64))
                self.sprites_asteroide.append(img)
        self.image = self.sprites_asteroide[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pg.math.Vector2()
        self.speed = 2
        self.angle = 0
    def update(self):
        # self.direction.x = 1
        self.rotaciona()
        
        # self.index += 0.5
        # if self.index >= 14:
        #     self.index = 0
        # self.image = self.sprites_asteroide[int(self.index)]
        # print(int(self.index))
        
    def rotaciona(self):
        self.angle -= 2
        rotated_image = pg.transform.rotate(self.image, self.angle)
        # print(self.angle)
        # self.image = rotated_image
        # self.rect.x += self.speed
        # screen.blit(rotated_image,(self.rect.x - rotated_image.get_width() // 2,self.rect.y - rotated_image.get_height() // 2))
        self.mask = pg.mask.from_surface(rotated_image)
        # rotated_image.fill((255,255,0))
        screen.blit(rotated_image,(self.rect.x - rotated_image.get_width() // 2,self.rect.y - rotated_image.get_height() // 2))
        # screen.blit(rotated_image,(self.rect))

class Player(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.spritesheet = pg.image.load("./assets/sprites/Sprites_Personagem.png")
        self.image = self.spritesheet.subsurface((0,0),(96,96))
        self.rect = self.image.get_rect(center=pos)

        self.angle = 0
        self.rotated = self.image
        self.speed = 5


    def update(self):
        self.mask = pg.mask.from_surface(self.image)
        self.movimentacao()
        self.direct = pg.math.Vector2(0,-self.speed).rotate(self.angle)
        screen.blit(self.rotated,(self.rect.x - self.rotated.get_width()//2, self.rect.y - self.rotated.get_height() //2))
        # screen.blit(self.rotated,(self.rect.x - self.rotated.get_width()//2, self.rect.y - self.rotated.get_height() //2))
    
    def movimentacao(self):
        key = pg.key.get_pressed()

        if key[K_LEFT]:
            self.angle = self.angle + self.speed
            self.rotated = pg.transform.rotate(self.image,self.angle)
        elif key[K_RIGHT]:
            self.angle = self.angle - self.speed
            self.rotated = pg.transform.rotate(self.image,self.angle)
        if abs(self.angle) == 360:
            self.angle = 0
        if self.angle == -180:
            self.angle = 180
        elif self.angle == 180:
            self.angle = -180
    def atirando(self,evento):
        # print(self.angle)
        if evento.key == K_SPACE:
            # print("Apertou Spaço")'
            # tiro = Lazer((self.rect.x-20,self.rect.y-20),self.angle,group_camera)
            blaster = Lazer((self.rect.x+32,self.rect.y+32),self.angle,group_camera)
            # blaster = Lazer((self.rect.center),self.angle,group_camera)
            # print(self.angle)
            # print(blaster.direct)

class Lazer(pg.sprite.Sprite):
    def __init__(self,pos,angle,group):
        super().__init__(group)
        self.angle =angle
        self.spritesheet = pg.image.load("./assets/sprites/Sprites_Personagem.png")
        self.image = self.spritesheet.subsurface((96,0),(96,96))
        self.image = pg.transform.scale(self.image,(64,64))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.copy = self.image

        # Ira criar um Vetor2(x,y) e ira girar o Lazer conforme a rotação do personagem
        # Assim ira ir girando o proprio sprite do lazer e ira em direção conforme o angulo que foi rotacionado 
        self.direct = pg.math.Vector2(0,-self.speed).rotate(-self.angle) 

    def update(self):
        self.copy = pg.transform.rotate(self.image,self.angle)  

        self.rect.center += self.direct
        screen.blit(self.copy,(self.rect.x - self.copy.get_width() // 2, self.rect.y - self.copy.get_height() // 2 ))
         
class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

grupo_asteroide = pg.sprite.Group()
# grupo_nave = pg.sprite.Group()
group_camera = CameraGroup()

def verificarColisao(obj1,obj2):
    colidiu = pg.sprite.spritecollide(obj1,obj2,False, pg.sprite.collide_mask)
    # if colidiu:
        # print("Colidiu")
player = Player((largura//2,altura//2),group_camera)
asteroides = []
for x in range(15):
    asteroide = Asteroide((randint(30,largura-50),randint(20,altura-50)),group_camera)
    grupo_asteroide.add(asteroide)

clock = pg.time.Clock()
while True:
    screen.fill((0,0,0))
    clock.tick(30)
    group_camera.update()
    verificarColisao(player,grupo_asteroide)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:
            player.atirando(event)
            # pass

    
    
    # group_camera.custom_draw()

    pg.display.flip()