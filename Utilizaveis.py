import pygame as pg
from pygame.locals import *

class Tela:
    def Menu(inicial,tela):
        while inicial:
            tela.fill((0,0,0))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
            pg.display.flip()
    
    # def reiniciarJogo(sprites,):
        # global 
    def GameOver(morte,tela):
        while morte:
            tela.fill((0,0,0))
            pg.mixer.music.stop()
            pg.draw.rect(tela,((0,0,0)),(0,0,tela.get_width(),tela.get_height()))
            Texto_GameOver = Texto.DrawTexto("GAME OVER",color=(255,0,0),bold=True)
            # texto_rect = Texto_GameOver.get_rect(center=(tela.get_width()//2, tela.get_height()//2))
            texto_rect = Texto_GameOver.get_rect(center=(tela.get_width()//2, 100))
            tela.blit(Texto_GameOver,texto_rect)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()

            pg.display.flip()
class Texto:
    def DrawTexto(mensagem,color=(255,255,255),size=32,fontType="Arial",bold=False,Italic=False, antialias=True):
        font = pg.font.SysFont(fontType,size,bold,Italic)
        texto_formatado = font.render(mensagem,antialias,color)

        return texto_formatado