import pygame as pg
from pygame.locals import *
from sys import exit

pg.init()

largura = 760 
altura =  600
screen = pg.display.set_mode((largura,altura))

class Circulo:
    # def __init__(self,color,x,y,width,height):
    def __init__(self,color,position,radius,fill=0):
        # pass
        self.color = color
        self.radius = radius
        self.fill = fill
        self.pos = pg.math.Vector2(position)
        self.circle = pg.draw.circle(screen,color,(self.pos),self.radius,self.fill)

        # elf.circle
        # print(position)
        self.angle = 0
        # self.rect = (x,y)]
    def rotated(self):
        # self.circle = pg.transform.rotate(self.circle,self.angle)
        self.pos.x += 10
        self.pos.y += 10
        self.circle = pg.draw.circle(screen,self.color,(self.pos),self.radius,self.fill)
        # self.circle.center = pg.Vector2(self.pos.rotate(self.angle))
        # self.angle += 1
        # pg.draw.rect(screen,color,(x,y,self.width,self.height))
        # pg.draw.circle(screen,color,(x,y,radius))
        # pg.draw.rect(screen,color,(self
        # self.direction.x =
        # self.degree += 1
        # self.pos = pg.math.Vector2(self.pos).rotate_rad(self.degree)
        # print(self.pos)
        # print(self.degree)
        # pass
# for x in range(10):


# circulo = 
 
for x in range(10):
    circulo2 = Circulo((0,255,0),(largura//2,altura//2),3)
    circulo2.rotated()
    print(circulo2.pos)

circulo = Circulo((255,0,0),(largura//2,altura//2),3)
while True:
    # screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()

    # pg.draw(circulo)
    # circulo.rotated()
    # circulo
    # pg.draw.circle(screen,(255,0,0),(100,200),20,1) # sem preenchimento na forma 
    # pg.draw.circle(screen,(255,0,0),(largura//2,altura//2),5,0)
    # circulo = Circulo((255,0,0),(largura//2,altura//2),3;)
    

    # for x in range(10):  
    # for x in range(10):
    #     circulo2 = Circulo((0,255,0),((largura//2+20),altura//2+20),2)
    #     circulo2 = Circulo((0,255,0),((largura//2+20),altura//2-20),2)
    #     circulo2 = Circulo((0,255,0),((largura//2+10),altura//2-20),2)
    #     circulo2 = Circulo((0,255,0),((largura//2-10),altura//2-20),2)
        # circulo2.rotated()
   
    # pg.draw.rect(screen,(255,255,0),(100,200,10,20))
    pg.display.flip()