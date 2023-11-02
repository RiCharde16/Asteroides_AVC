import pygame as pg
from pygame.locals import *

class Tela:
    dir_font = './assets/Fonts/pixeloid-font/PixeloidSansBold.ttf'
    centerX = 0
    centerY = 0
    def Menu(inicial,tela):
        
        background_img = pg.image.load('./assets/Background/Space_wallapaper.gif')
        background_img = pg.transform.scale(background_img,(tela.get_width(),tela.get_height()))

        font_titulo = Texto.novaFonte(Tela.dir_font,90)
        font_txt = Texto.novaFonte(Tela.dir_font)

        titulo = Texto.DrawTexto("Asteroide",(255,255,255),newFont=font_titulo,bold=True)
        titulo_rect = Texto.posRect(titulo,(Tela.centerX,Tela.centerY-100))

        txt1 = Texto.DrawTexto("Aperte a Tecla ENTER para começar o jogo",(255,255,255),newFont=font_txt)
        txt1_rect = Texto.posRect(txt1,(Tela.centerX,Tela.centerY+50))

        while inicial:
            tela.fill((0,0,0))

            # Imagem de Fundo
            tela.blit(background_img,(0,0))

            # Textos
            tela.blit(titulo,titulo_rect)
            tela.blit(txt1,txt1_rect)
            for event in pg.event.get():    
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return False
            pg.display.flip()
    
    def GameOver(morte,tela,score):
        font_gameover = Texto.novaFonte(Tela.dir_font,50) 
        Texto_GameOver = Texto.DrawTexto("GAME OVER",color=(255,0,0),bold=True,newFont=font_gameover)
        texto_rect = Texto.posRect(Texto_GameOver,(Tela.centerX, 100))

        font_txt = Texto.novaFonte(Tela.dir_font)
        txt_ponto = Texto.DrawTexto(f"Pontuação Atual: {score}",color=(255,255,255),newFont=font_txt)
        txt_ponto_rect = Texto.posRect(txt_ponto,(Tela.centerX,170))

        txt1 = Texto.DrawTexto("Aperte a Tecla R para Reiniciar o Jogo",(255,255,255),newFont=font_txt)
        txt1_pos = Texto.posRect(txt1,(Tela.centerX,300))

        txt2 = Texto.DrawTexto("Ou aperte a Tecla M para ir para o Menu",(255,255,255),newFont=font_txt)
        txt2_pos = Texto.posRect(txt1,(Tela.centerX,350))
        menu = True
        while morte:
            tela.fill((0,0,0))
            pg.mixer.music.stop()
            pg.draw.rect(tela,((0,0,0)),(0,0,tela.get_width(),tela.get_height()))
            
            # texto_rect = Texto_GameOver.get_rect(center=(tela.get_width()//2, 100))
            tela.blit(Texto_GameOver,texto_rect)
            tela.blit(txt_ponto,txt_ponto_rect)
            tela.blit(txt1,txt1_pos)
            tela.blit(txt2,txt2_pos)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        menu = False
                        return False,menu
                    if event.key == K_m:
                        return False,menu
                        # break

            pg.display.flip()
class Texto:
    def DrawTexto(mensagem,color=(255,255,255),size=32,fontType="Arial",bold=False,Italic=False, antialias=True,newFont=""):
        if newFont == "":
            font = pg.font.SysFont(fontType,size,bold,Italic)
            texto_formatado = font.render(mensagem,antialias,color)
        else:
            texto_formatado = newFont.render(mensagem,antialias,color)
        return texto_formatado
    def novaFonte(dirFile="./assets/Fonts",size=20):
        return pg.font.Font(dirFile,size)
    def posRect(texto,pos):
        return texto.get_rect(center=pos)