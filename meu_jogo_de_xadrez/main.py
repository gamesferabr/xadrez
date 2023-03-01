import pygame
from pygame.locals import *
#import sys
from jogo.tabuleiro import Tabuleiro 
#from jogo.movimentos import Move
from jogo.pecas import *
from interface_grafica.tela import ALTURA_TELA,LARGURA_TELA
from interface_grafica.cores import BRANCO, PRETO


# Inicializa o Pygame
pygame.init()


# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tabuleiro de Xadrez")


# Cria um objeto de tabuleiro
tabuleiro = Tabuleiro()
tabuleiro.desenhar_tabuleiro(tela)
 

running = True
moving = False
moving2 = False
# Loop principal do jogo
#peca_selecionada = None


#Provavelmente da o movimento da imagem, mas ainda é incerto
largura_celula = LARGURA_TELA // 8
altura_celula = ALTURA_TELA // 8


#Define as posições iniciais
posicao_inicial = (0,1)
posicao_inicial2 = (1,1)


#Define as posições atuais
posicao_atual = posicao_inicial
posicao_atual2 = posicao_inicial2


#Essa variavel ajusta a posição para o tamanho do tabuleiro
x, y = tabuleiro.convert_pos_to_coord(posicao_atual)
x2,y2 = tabuleiro.convert_pos_to_coord(posicao_atual2)


#Essa variavel aqui ajusta a imagem peão.
rect = pygame.Rect(x, y, altura_celula, largura_celula)
#ajusta a imagem do segundo peão branco
rect2 = pygame.Rect(x2,y2,altura_celula,largura_celula)


#Carrega as imagens
white_panw_img = load_image('whitepanw.png')
#white_panw_img2 = load_image('whitepanw.png')

while running:
     tabuleiro.desenhar_tabuleiro(tela)
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False
              
        # Movimenta as peças com o mouse
        elif event.type == pygame.MOUSEBUTTONDOWN: #and not peca_selecionada:
            
            
            if rect.collidepoint(event.pos):
               moving = True  
            
               
            elif rect2.collidepoint(event.pos):
               moving2 = True
        
        
        # Verifica se o jogador moveu a peça selecionada
        elif event.type == pygame.MOUSEBUTTONUP: #and peca_selecionada:
            
            #Movimenta o peão 1
            if moving: 
                 
                 #Define a posição nova no começo da condição
                 posicao_nova = (rect.x//tabuleiro.tamanho_quadrado,rect.y//tabuleiro.tamanho_quadrado)
                                                             #Essa parte aqui da variavel resolve o passant
                 if posicao_nova[1] == posicao_atual[1]+1 or posicao_nova[1] == 3 and max(round(posicao_nova[0]), 0) == posicao_atual[0]:
                     posicao_atual = (max(round(posicao_nova[0]), 0),posicao_nova[1] if posicao_nova[1] < 8 else posicao_atual[1])          
                     print(posicao_atual)
                     #Essa linha aqui faz a casa do tabuleiro atrair a imagem
                     rect.topleft = tabuleiro.convert_pos_to_coord(posicao_atual)
                    
                 else:                 
                    
                    #Isso que faz a peça não poder ir para outras casas se a condição anterior não for cumprida
                    rect.topleft = tabuleiro.convert_pos_to_coord(posicao_atual)
                   
                 #Isso faz com que a peça seja solta do mouse
                 moving = False
               
            elif moving2:
                 posicao_nova2 = (rect2.x//tabuleiro.tamanho_quadrado,rect2.y//tabuleiro.tamanho_quadrado)
                                             #Essa parte aqui da variavel resolve o passant
                 if posicao_nova2[1] == posicao_atual2[1]+1 and max(round(posicao_nova2[0]), 1) == posicao_atual2[0]:
                     
                     #Atualiza a posição
                     posicao_atual2 = (max(round(posicao_nova2[0]), 1),posicao_nova2[1] if posicao_nova2[1] < 8 else posicao_atual2[1])       
                     
                     
                     #Essa linha aqui faz a casa do tabuleiro atrair a imagem
                     rect2.topleft = tabuleiro.convert_pos_to_coord(posicao_atual2)
                    
                 else:                 
                    
                    #Isso que faz a peça não poder ir para outras casas se a condição anterior não for cumprida
                    rect2.topleft = tabuleiro.convert_pos_to_coord(posicao_atual2)
                    
                 #Isso faz com que a peça seja solta do mouse
                 # mover o segundo peão ...
                 moving2 = False
        

        #Move com o mouse
        elif event.type == pygame.MOUSEMOTION:
            
            #Move o peão 1
            if moving:
             rect.move_ip(event.rel)    
            
            #Move o peão 2 
            elif moving2:
             rect2.move_ip(event.rel)
          

        #Desenha as imagens na tela
        #Desenha o peão 1
        tela.blit(white_panw_img, rect)
       
        #Desenha o peão 2
        tela.blit(white_panw_img, rect2)
        pygame.display.update()


   
   
   
   
   
  



  


  



  
  























