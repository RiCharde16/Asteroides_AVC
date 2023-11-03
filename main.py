import pygame as pg
import os, sys
from Utilizaveis import *
from random import *
import tkinter as tk
from sys import exit
from pygame.locals import *

# O codigo a seguir ira intermediar o direitorio do arquivo que ira gerar o executavel com Pyinstaller
dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys,'frozen',False):
    os.chdir(sys._MEIPASS)

root = tk.Tk()
pg.init()

largura = 740
altura = 650
# largura = root.winfo_screenwidth()
# altura = root.winfo_screenheight()

screen = pg.display.set_mode((largura,altura-50))
sprite_sheet = pg.image.load('./assets/sprites/Sprites_Personagem.png').convert_alpha()
img = sprite_sheet.subsurface((0,0),(96,96))
# pg.display.set_icon(img)
pg.display.set_caption("Asteroide")
pg.display.set_icon(pg.transform.scale(img,(32,32)))

# musica_background = pg.mixer.music.load('./assets/soundtracks/Used To Say.mp3')
# pg.mixer.music.play(-1)

sound_lazer = pg.mixer.Sound('./assets/soundtracks/Laser Gun Short Silencer 03.mp3')

class Asteroide(pg.sprite.Sprite):
    def __init__(self,pos,group,all_sprites):
        self._layer = 3
        super().__init__(all_sprites,group)
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
        self.rotated_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.math.Vector2(pos)
        self.speed = 2
        self.angle = 0
        self.mask = pg.mask.from_surface(self.rotated_image)
    def update(self):
        self.rotaciona()
        self.movimentacao()
        
    def rotaciona(self):
        self.angle += 2
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        # screen.blit(rotated_image,(self.rect.x - rotated_image.get_width() // 2,self.rect.y - rotated_image.get_height() // 2))
        screen.blit(self.rotated_image,(self.rect.x - self.rotated_image.get_width() // 2,self.rect.y - self.rotated_image.get_height() // 2))
        # screen.blit(rotated_image,(self.rect))
    def movimentacao(self):
        player_pos = pg.math.Vector2(player.rect.center)
        direction = player_pos - self.rect.center
        # if dirty = direction.normalize() * self.speed
        velocity = direction.normalize() * self.speed
        # print(direction)
        self.position += velocity 
        self.rect.center = self.position

class Player(pg.sprite.Sprite):
    def __init__(self,pos,group,all_sprites):
        self._layer= 2
        super().__init__(all_sprites,group)
        self.spritesheet = pg.image.load("./assets/sprites/Sprites_Personagem.png")
        self.image = self.spritesheet.subsurface((0,0),(96,96))
        # group.add(self, layer= self.layer)
        self.image = pg.transform.scale(self.image,(86,86))
        self.rect = self.image.get_rect(center=pos)

        self.angle = 0
        self.rotated = self.image
        self.mask = pg.mask.from_surface(self.rotated)
        self.speed = 6
        

    def update(self):
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
        # if abs(self.angle) == 360:
        #     self.angle = 0
        # if self.angle == -180:
        #     self.angle = 180
        # elif self.angle == 180:
        #     self.angle = -180

    def atirando(self,evento):
        # print(self.angle)
        if evento.key == K_SPACE:
            blaster = Lazer((self.rect.x+32,self.rect.y+32),self.angle,grupo_lazer,all_sprites)
            sound_lazer.play()

class Lazer(pg.sprite.Sprite):
    def __init__(self,pos,angle,group,all_sprites):
        self._layer = 1
        super().__init__(all_sprites,group)
        self.angle =angle
        self.spritesheet = pg.image.load("./assets/sprites/Sprites_Personagem.png")
        self.image = self.spritesheet.subsurface((96,0),(96,96))
        self.image = pg.transform.scale(self.image,(64,64))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.copy = self.image
        self.mask = pg.mask.from_surface(self.copy)

        # Ira criar um Vetor2(x,y) e ira girar o Lazer conforme a rotação do personagem
        # Assim ira ir girando o proprio sprite do lazer e ira em direção conforme o angulo que foi rotacionado 
        self.direct = pg.math.Vector2(0,-self.speed).rotate(-self.angle) 

    def update(self):
        self.copy = pg.transform.rotate(self.image,self.angle) 
        self.rect.center += self.direct
        
        screen.blit(self.copy,(self.rect.x - self.copy.get_width() // 2, self.rect.y - self.copy.get_height() // 2 ))
    
    def outScreen(self,sprite):
        if self.rect.x < 0 or self.rect.x > largura or self.rect.y < 0 or self.rect.y > altura:
            all_sprites.remove(sprite)
            grupo_lazer.remove(sprite)
            # print(all_sprites)

def verificarJanelaMinimizada(event):
    if event.type == ACTIVEEVENT:
        # print(event.__dict__)
        if event.gain == 0 and  event.state == 2:
            # print("janela Fechou")
            pg.mixer.music.pause()
            # pygame.display.
        elif event.gain == 1 and event.state == 2:
            pg.mixer.music.unpause()

def verificarColisao(obj1,group):
    colidiu = pg.sprite.spritecollide(obj1,group,False, pg.sprite.collide_mask)
    return colidiu

grupo_asteroide = pg.sprite.Group()
grupo_lazer = pg.sprite.Group()
all_sprites = pg.sprite.LayeredUpdates()


player = Player((largura//2,altura//2),all_sprites,all_sprites)

def gerarAsteroides():
    for x in range(20): 
        pos_x = randint(-1200,largura+1000)
        pos_y = randint(-1200,altura+1000)
        if pos_x < 0 or pos_x > largura and pos_y < 0 or pos_y > altura: 
            asteroide = Asteroide((pos_x,pos_y),grupo_asteroide,all_sprites)

def reiniciarJogo(goMenu=False):
    # pg.mixer.music.play(-1)
    global all_sprites,player,death, pontos, grupo_asteroide, grupo_lazer,menu
    
    menu = goMenu
    grupo_lazer.empty()
    grupo_asteroide.empty()
    pontos = 0
    death = False
    player = Player((largura//2,altura//2),all_sprites,all_sprites)
    gerarAsteroides()

asteroide = Asteroide((10,100),grupo_asteroide,all_sprites)
clock = pg.time.Clock()

pontos = 0
evento_tempo = pg.USEREVENT + 1
menu = True
Tela.centerX = screen.get_width()/2
Tela.centerY = screen.get_height()/2

pg.time.set_timer(evento_tempo, 12000)

font1 = Texto.novaFonte(Tela.dir_font,32) 
# font_nome = Texto.novaFonte(Tela.dir_font,32)

gerarAsteroides()
# menu = Tela.Menu(menu,screenn)
while True:
    clock.tick(30)
    menu = Tela.Menu(menu,screen)

    # print(Tela.nome_jogador)
    screen.fill((0,0,0))
    name = Texto.DrawTexto(Tela.nome_jogador,(255,255,255),newFont=font1)
    name_rect = name.get_rect(topleft=(10,20))

    txt_pontos = Texto.DrawTexto(f"PONTOS: {pontos}",bold=True,newFont=font1)
    txt_rect = txt_pontos.get_rect(center=(largura-120,40))
    
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:
            player.atirando(event)   
        if event.type == evento_tempo:
            # print("Passou 11 segundos")    
            gerarAsteroides()

        verificarJanelaMinimizada(event)

    # Verifica cada sprite no grupo asteroide e depois faz o mesmo no lazer para remover as sprites que colidiram
    for sprite in grupo_asteroide:
        colisao_tiro = verificarColisao(sprite,grupo_lazer) 
        for lazer in grupo_lazer:
            colisao_meteoro = verificarColisao(lazer,grupo_asteroide)
            if colisao_meteoro and colisao_tiro:
                pontos += 1
                all_sprites.remove(sprite)
                grupo_asteroide.remove(sprite)

                all_sprites.remove(lazer)
                grupo_lazer.remove(lazer)
    
    # Ira verificar se algum sprite do laser saiu da tela e ira exclui-lo do Grupo das sprites principal
    for lazer in grupo_lazer:
        lazer.outScreen(lazer)

    death = verificarColisao(player,grupo_asteroide)

    if death:
        all_sprites.remove(all_sprites)
        death = Tela.GameOver(death,screen,pontos)
        if death[0] == False and death[1] == False:
            reiniciarJogo()
        else:
            reiniciarJogo(death[1])
    

    all_sprites.update()
    screen.blit(txt_pontos,txt_rect)
    screen.blit(name,name_rect)
    # group_camera.custom_draw()

    pg.display.flip()