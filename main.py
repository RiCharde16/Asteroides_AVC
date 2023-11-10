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

# O Codigo abaixo usa a biblioteca do Tkinter para
# pegar a largura e a altura da tela do computador que sera usado
root = tk.Tk()
pg.init()

# largura = 740
# altura = 650
largura = root.winfo_screenwidth()
altura = root.winfo_screenheight()

# Codigo do Jogo
screen = pg.display.set_mode((largura,altura-50))
img = pg.image.load('./Assets/Background/asteroide.png').convert_alpha()
pg.display.set_caption("Asteroides")
pg.display.set_icon(img)

musica1 = pg.mixer.music.load('./Assets/soundtracks/Used To Say.mp3')
pg.mixer.music.set_volume(0.55)
pg.mixer.music.play(-1)


sound_lazer = pg.mixer.Sound('./Assets/soundtracks/Laser Gun Short Silencer 03.mp3')
sound_lazer.set_volume(1)

sound_destroyer = pg.mixer.Sound('./Assets/soundtracks/boom.wav')
sound_destroyer.set_volume(0.4)

class Asteroide(pg.sprite.Sprite):
    def __init__(self,pos,group,all_sprites,velocidade=3):
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
        self.speed = velocidade
        self.angle = pos[1]
        self.mask = pg.mask.from_surface(self.rotated_image)
        self.colidiu = False
        self.obj = ""
    def update(self):
        if not(self.colidiu):
            self.rotaciona()
            self.movimentacao()
        else:
            self.rotated_image = self.sprites_asteroide[int(self.index)]
            # all_sprites.remove(obj)
            # print(self.obj)
            if self.index == 12:
                # self.allgroup.remove(obj)
                all_sprites.remove(self.obj)
            self.index += 0.5
            #     return 0
        screen.blit(self.rotated_image,(self.rect.x - self.rotated_image.get_width() // 2,self.rect.y - self.rotated_image.get_height() // 2))
        
    def rotaciona(self):
        self.angle += 2
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        # screen.blit(rotated_image,(self.rect.x - rotated_image.get_width() // 2,self.rect.y - rotated_image.get_height() // 2))
        
        # screen.blit(rotated_image,(self.rect))
    def movimentacao(self):
        player_pos = pg.math.Vector2(player.rect.center)
        direction = player_pos - self.rect.center
        # if dirty = direction.normalize() * self.speed
        velocity = direction.normalize() * self.speed
        # print(direction)
        self.position += velocity 
        self.rect.center = self.position

    def destruir(self,colidiu=False,sprite=""):
        if colidiu:
            self.index = 3
            self.colidiu = colidiu
            self.obj = sprite

class Player(pg.sprite.Sprite):
    def __init__(self,pos,all_sprites,velocidade=6):
        self._layer= 2
        super().__init__(all_sprites)
        self.spritesheet = pg.image.load("./assets/sprites/Sprites_Personagem.png").convert_alpha()
        self.image = self.spritesheet.subsurface((0,0),(96,96))
        # group.add(self, layer= self.layer)
        self.image = pg.transform.scale(self.image,(86,86))
        self.rect = self.image.get_rect(center=pos)

        self.angle = 0
        self.rotated = self.image
        self.speed = velocidade
        

    def update(self):
        self.movimentacao()
        self.direct = pg.math.Vector2(0,-self.speed).rotate(self.angle)
        self.mask = pg.mask.from_surface(self.rotated)
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
        self.spritesheet = pg.image.load("./Assets/sprites/Sprites_Personagem.png").convert_alpha()
        self.image = self.spritesheet.subsurface((96,0),(96,96))
        self.image = pg.transform.scale(self.image,(64,64))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 20
        self.copy = self.image
        

        # Ira criar um Vetor2(x,y) e ira girar o Lazer conforme a rotação do personagem
        # Assim ira ir girando o proprio sprite do lazer e ira em direção conforme o angulo que foi rotacionado 
        self.direct = pg.math.Vector2(0,-self.speed).rotate(-self.angle) 

    def update(self):
        self.copy = pg.transform.rotate(self.image,self.angle) 
        self.mask = pg.mask.from_surface(self.copy)
        self.rect.center += self.direct
        
        screen.blit(self.copy,(self.rect.x - self.copy.get_width() // 2, self.rect.y - self.copy.get_height() // 2 ))
    
    def outScreen(self,sprite):
        if self.rect.x < 0 or self.rect.x > largura-10 or self.rect.y < 0 or self.rect.y > altura-10:
            all_sprites.remove(sprite)
            grupo_lazer.remove(sprite)
            # print(all_sprites)

def verificarColisao(obj1,sprite_group):
    colidiu = pg.sprite.spritecollide(obj1,sprite_group,False, pg.sprite.collide_mask)
    return colidiu

grupo_asteroide = pg.sprite.Group()
grupo_lazer = pg.sprite.Group()
all_sprites = pg.sprite.LayeredUpdates()


player = Player((largura//2,altura//2),all_sprites)

def gerarAsteroides(speed=3):
    for x in range(20): 
        pos_x = randint(-1200,largura+1000)
        pos_y = randint(-1200,altura+1000)
        if pos_x < 0 or pos_x > largura and pos_y < 0 or pos_y > altura: 
            Asteroide((pos_x,pos_y),grupo_asteroide,all_sprites,speed)

def reiniciarJogo(goMenu=False):
    # pg.mixer.music.play(-1)
    global all_sprites,player,death, pontos, grupo_asteroide, grupo_lazer,menu,load,speed_asteroide

    pg.mixer.music.play(-1)
    load = Save.lerArquivo()
    menu = goMenu
    grupo_lazer.empty()
    grupo_asteroide.empty()
    pontos = 0
    death = False
    player = Player((largura//2,altura//2),all_sprites)
    speed_asteroide = 3
    gerarAsteroides(speed_asteroide)

clock = pg.time.Clock()

pontos = 0
# Criação de Eventos para o timer do pygame
evento_tempo = pg.USEREVENT + 1
evento_tempo2 = pg.USEREVENT + 2

menu = True
Tela.centerX = screen.get_width()/2
Tela.centerY = screen.get_height()/2

pg.time.set_timer(evento_tempo, 12000)
pg.time.set_timer(evento_tempo2, 1000)

font1 = Texto.novaFonte(Tela.dir_font,32) 

# Carrega o arquivo e os Salva em uma lista
load = Save.lerArquivo()
FPS = 30

speed_asteroide = 3
gerarAsteroides(speed_asteroide)
apagar = False
while True:
    clock.tick(FPS)
    # Tela.GameOver(True,screen,pontos,load)
    menu = Tela.Menu(menu,screen)
    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
    screen.fill((0,0,0))
    # pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
    name = Texto.DrawTexto(Tela.nome_jogador,(255,255,255),newFont=font1)
    
    name_rect = name.get_rect(topleft=(10,20))

    txt_pontos = Texto.DrawTexto(f"PONTOS: {pontos}",bold=True,newFont=font1)
    txt_rect = txt_pontos.get_rect(bottomright=(largura-10,60))

    # pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
    
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            player.atirando(event)  

        elif event.type == evento_tempo:
            gerarAsteroides(speed_asteroide)
        elif event.type == evento_tempo2:
            if pontos%10 == 0 and pontos > 40 and speed_asteroide < 7 and pontos != 0:
                speed_asteroide += 1
                player.speed += 1
        
        Tela.verificarJanelaMinimizada(event)

    # Verifica cada sprite no grupo asteroide e depois faz o mesmo no lazer para remover as sprites que colidiram
    for sprite in grupo_asteroide:
        colisao_tiro = verificarColisao(sprite,grupo_lazer) 
        for lazer in grupo_lazer:
            colisao_meteoro = verificarColisao(lazer,grupo_asteroide)
            if colisao_meteoro and colisao_tiro:
                pontos += 1
                sound_destroyer.play()
                grupo_asteroide.remove(sprite)
                sprite.destruir(colisao_tiro,sprite)
                all_sprites.remove(lazer)
                grupo_lazer.remove(lazer)
                
    for lazer in grupo_lazer:
        lazer.outScreen(lazer)

    death = verificarColisao(player,grupo_asteroide)

    if death:
        all_sprites.remove(all_sprites)
        sound_lazer.stop()
        sound_destroyer.stop()
        death = Tela.GameOver(death,screen,pontos,load)
        if death[0] == False and death[1] == False:
            reiniciarJogo()
        else:
            reiniciarJogo(death[1])
    

    all_sprites.update()
    # print(all_sprites)
    screen.blit(txt_pontos,txt_rect)
    screen.blit(name,name_rect)
    # group_camera.custom_draw()

    pg.display.flip()