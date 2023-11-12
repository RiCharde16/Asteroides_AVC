import pygame as pg
from pygame.locals import *
import re, os


diretorio = os.getcwd()
class Tela:
    dir_font = './Assets/Fonts/pixeloid-font/PixeloidSansBold.ttf'
    centerX = 0
    centerY = 0
    nome_jogador = ""
    def verificarJanelaMinimizada(event):
        if event.type == ACTIVEEVENT:
            # print(event.__dict__)
            if event.gain == 0 and  event.state == 2:
                # print("janela Fechou")
                pg.mixer.music.pause()
                # pygame.display.
            elif event.gain == 1 and event.state == 2:
                pg.mixer.music.unpause()
            
    def Menu(inicial,tela):
        
        background_img = pg.image.load('./assets/Background/Space_wallapaper.gif')
        background_img = pg.transform.scale(background_img,(tela.get_width(),tela.get_height()))
        
        input = Input(tela,(Tela.centerX-80,Tela.centerY+100),(0,0,255))
        texto = "Digite o Nome para o Jogador"

        amarelo = (255,255,0)
        colortxt = (255,255,255)

        font_titulo = Texto.novaFonte(Tela.dir_font,90)
        font_txt = Texto.novaFonte(Tela.dir_font)

        titulo = Texto.DrawTexto("Asteroides",(amarelo),newFont=font_titulo,bold=True)
        titulo_rect = Texto.posRect(titulo,(Tela.centerX,Tela.centerY-100))

        while inicial:
            tela.fill((0,0,0))

            txt1 = Texto.DrawTexto(texto,colortxt,newFont=font_txt)
            txt1_rect = Texto.posRect(txt1,(Tela.centerX,Tela.centerY+50))

            # Imagem de Fundo
            tela.blit(background_img,(0,0))

            # Textos
            input.renderInput()
            tela.blit(titulo,titulo_rect)
            tela.blit(txt1,txt1_rect)

            for event in pg.event.get():    
                if event.type == QUIT:
                    pg.quit()
                    exit()
                input.InputBox(event)
                if event.type == KEYDOWN :
                    if event.key == K_RETURN and len(input.texto) == 6:
                        # print("Começando")
                        Tela.nome_jogador = input.texto
                        return False
                Tela.verificarJanelaMinimizada(event)

            if len(input.texto) == 6:
                texto = "Aperte a Telca Enter para começar"
                colortxt = (0,255,0)
                input.color = (0,255,0)
            else:
                texto = "Digite o Nome para o Jogador"
                colortxt = amarelo
                input.color = amarelo
                # return input.enter
            pg.display.flip()
    
    def GameOver(morte,tela,score,load):
        
        font_gameover = Texto.novaFonte(Tela.dir_font,50) 
        Texto_GameOver = Texto.DrawTexto("GAME OVER",color=(255,0,0),bold=True,newFont=font_gameover)
        texto_rect = Texto.posRect(Texto_GameOver,(Tela.centerX, 100))
        
        font_txt = Texto.novaFonte(Tela.dir_font)
        nome_player = Texto.DrawTexto(f"Nome Jogador: {Tela.nome_jogador}",(255,255,255),newFont=font_txt)
        nome_rect = Texto.posRect(nome_player,(Tela.centerX,200))

        txt_ponto = Texto.DrawTexto(f"Pontuação Atual: {score}",color=(255,255,255),newFont=font_txt)
        txt_ponto_rect = Texto.posRect(txt_ponto,(Tela.centerX,240))

        menu = True
        
        dados = Save.salvarJogador(score,Tela.nome_jogador,load)
        dados_jogador = Save.mediaJogador(dados[1],Tela.nome_jogador)
        # Save.mediaJogador(dados[1],Tela.nome_jogador)
        
        txt_partidas_jogador = Texto.DrawTexto(f"Partidas do Jogador: {dados_jogador[1]}",(255,255,255),newFont=font_txt)
        txt_pos2 = Texto.posRect(txt_partidas_jogador,(Tela.centerX,280))

        txt_media_jogador = Texto.DrawTexto(f"Media de Pontos do Jogador: {dados_jogador[0]}",(255,255,255),newFont=font_txt)
        txt_pos1 = Texto.posRect(txt_media_jogador,(Tela.centerX,320))

        txt_media_g = Texto.DrawTexto(f"Media Geral de Pontos: {dados[0]}",(255,255,255),newFont=font_txt)
        txt_media_rect = Texto.posRect(txt_media_g,(Tela.centerX,360))

        txt1 = Texto.DrawTexto("Aperte a Tecla R para Reiniciar o Jogo",(255,255,255),newFont=font_txt)
        txt1_pos = Texto.posRect(txt1,(Tela.centerX,tela.get_height()-250))

        txt2 = Texto.DrawTexto("Ou aperte a Tecla M para ir para o Menu",(255,255,255),newFont=font_txt)
        txt2_pos = Texto.posRect(txt1,(Tela.centerX,tela.get_height()-200))
        # print(dados)
        # pg.mouse.set_visible(True)
        # pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        game_over_sound = pg.mixer.Sound('./Assets/soundtracks/Game Over.mp3')
        game_over_sound.set_volume(0.9)
        game_over_sound.play()

        while morte:
            tela.fill((0,0,0))
            pg.mixer.music.stop()
            pg.draw.rect(tela,((0,0,0)),(0,0,tela.get_width(),tela.get_height()))
            
            # texto_rect = Texto_GameOver.get_rect(center=(tela.get_width()//2, 100))

            # Titulo
            tela.blit(Texto_GameOver,texto_rect)

            # Dados
            tela.blit(nome_player,nome_rect)
            tela.blit(txt_ponto,txt_ponto_rect)

            tela.blit(txt_partidas_jogador,txt_pos2)
            tela.blit(txt_media_jogador,txt_pos1)
            tela.blit(txt_media_g,txt_media_rect)


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
    def novaFonte(dirFile="./Assets/Fonts",size=20):
        return pg.font.Font(dirFile,size)
    def posRect(texto,pos):
        return texto.get_rect(center=pos)
    
class Input:
    def __init__(self,tela,pos=(10,20),color=(255,255,255)):
        self.pos = pos
        self.tela = tela
        self.color = color
        # self.boxInput = 
        self.clicked = False
        self.texto = "" 
        self.font = Texto.novaFonte(Tela.dir_font,20)
        self.border = 1
    def InputBox(self,evento):
        mouse_pos = pg.mouse.get_pos()
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        if self.boxInput.collidepoint(mouse_pos):
            if pg.mouse.get_focused():
                # print("Focou")
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                # self.border = 5
            if pg.mouse.get_pressed()[0] == True and self.clicked == False:
                # print("Click")    
                self.border = 3
                self.clicked = True

            if self.clicked:
                # print("Digite")
                if evento.type == KEYDOWN and evento.key and self.clicked == True:
                    if evento.key == K_BACKSPACE:
                        # self.active = False
                        self.texto = self.texto[:-1]
                    elif evento.key != K_BACKSPACE and len(self.texto) <= 5 and evento.key != K_RETURN:
                        # self.active = False
                        self.texto += str(evento.unicode).upper()
                        self.texto = re.sub('[^a-zA-Z0-9 \\\]','',self.texto)
        else:
            self.border =1
            self.clicked = False
                
    def renderInput(self):
        self.boxInput = pg.draw.rect(self.tela,(self.color),(self.pos[0],self.pos[1],150,30),self.border,5)

        nome = Texto.DrawTexto(self.texto,(255,255,255),newFont=self.font)
        self.tela.blit(nome,(self.pos[0]+20,self.pos[1]))  

class Save:
    def lerArquivo():
        try:
            Dados = open(diretorio+'\Save.txt','x')
        except:
            pass
        Dados = open(diretorio+"\Save.txt","r")
        save = []
        texto = Dados.read().split("\n")
        if texto != ['']:
            for x in range(0,len(texto)-1):
                    save.append(texto[x].split("\t\t"))
            
        save.sort()
        Dados.close()
        return save

    def salvarJogador(pontos,nome, load=[]):
        save = open(diretorio+'\Save.txt','w+')
        soma_total = 0
        load.append([nome,str(pontos)])
        load.sort()
        
        for item in load:
            save.write(f'{item[0]}\t\t{item[1]}\n')
            soma_total += int(item[1])

        media_g = f"{round(soma_total/len(load))}"

        save.write(f'Media Geral de Pontos:\t\t{media_g}')
        save.close()
        return media_g,load
    
    def mediaJogador(dados,player_name):
        p,soma = 0,0  
        jogador_pontos = []
        for player in dados:
            if player[0] == player_name:
                jogador_pontos.append(player[1])
                p += 1

        for pontos in jogador_pontos: 
            soma += int(pontos)
        if soma != 0:
            media_jogador = round(soma/p)
        else: 
            media_jogador = 0
        return media_jogador,p