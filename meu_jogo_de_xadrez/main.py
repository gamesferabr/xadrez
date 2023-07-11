import pygame
from pygame.locals import *
from jogo.tabuleiro import Tabuleiro 
from jogo.pecas import *
from interface_grafica.tela import ALTURA_TELA,LARGURA_TELA
from jogo.movimento_peao import Peao


# Inicializa o Pygame
pygame.init()


# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tabuleiro de Xadrez")


# Cria um objeto de tabuleiro
tabuleiro = Tabuleiro()
tabuleiro.desenhar_tabuleiro(tela)
 

#Essa parte do código cria uma variável onde o jogo começa e a váriável running de True vira false para continuar o loop.
running = True

turno = "Branco"

#Carrega as imagens do peão
white_panw_img = load_image('whitepanw.png')
black_panw_img = load_image('blackpanw.png')


#Fiz um list compreheension para não ter que ficar definindo os 8 peões
# Cria todos os peões brancos
peao_branco = [Peao("Branco",(i,1), white_panw_img) for i in range(0,8)]

# Cria todos os peões pretos
peao_preto = [Peao("Preto",(i,6), black_panw_img) for i in range(0,8)]

#Looping principal que faz o jogo ou engine rodar.
while running:
    #Desenha o tabuleiro do meu jogo de xadrez.
    tabuleiro.desenhar_tabuleiro(tela)
    
    #Para o evento rodando, o pygame irá capturar todas as movimentações do meu game.
    for event in pygame.event.get():
        
        #Se o tipo evento for para sair do jogo, a condição do looping será quebrada e irá fechar a janela do meu jogo atual.
        if event.type == pygame.QUIT:
            running = False

        #Se o botão do mouse for pressionado, a variavel evento irá ser chamada para iterar e executar os movimentos das peças.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            #Se o turno for a vez das peças brancas.
            if turno == "Branco":
                
                #Para iterar em cada peão branco.
                for pb in peao_branco:
                    
                    #O collidepoint é o ponto de colisão das peças, cada imagem tem um ponto de colisão, quando ele é acionado, ele inicia o movimento.
                    if pb.rect.collidepoint(event.pos):
                        
                        #A variavel tabuleiro faz o papel de calcular as casas que podem ser "Preenchidas" pelas peças.
                        tabuleiro.calcular_casas_destacadas(pb,turno)
                        
                        #Inicia a movimentação do peão.
                        pb.iniciar_movimento(event)
                        
           #Vez das peças pretas.
            elif turno == "Preto":
                 
                 #Looping para iterar em cada peça preta.
                 for pb2 in peao_preto:
                    
                    #Ponto de colisão dos peões pretos.
                    if pb2.rect.collidepoint(event.pos):
                        
                        #Calcula as possíveis casas.
                        tabuleiro.calcular_casas_destacadas(pb2,turno)
                        
                        #Inicia o movimento
                        pb2.iniciar_movimento(event)
                       

        
        
        elif event.type == pygame.MOUSEMOTION:
            if turno == "Branco":
                for pb in peao_branco:
                    if pb.moving:
                        pb.mover(event)
                        
            
            elif turno == "Preto":
                 for pb2 in peao_preto:
                    if pb2.moving:
                        pb2.mover(event)
                        

        
        
        elif event.type == pygame.MOUSEBUTTONUP:
           
            #Turno das peças brancas.
            if turno == "Branco":
                
                #looping para iterar em cada peão.
                for pb in peao_branco:
                    
                    if pb.moving:
                        
                        pb.finalizar_movimento(event)
                       
                        # Se o movimento for correto, ele passa na condição e troca de turno
                        if pb.mov_correto:
                          
                          #Variável que troca de turno
                          turno = "Preto"
                       
            
            # Turno das peças pretas.
            elif turno == "Preto":
                
                #Looping para iterar cada peão preto.
                for pb2 in peao_preto:
                    
                    if pb2.moving:
                        
                        #Finaliza o movimento do peão preto
                        pb2.finalizar_movimento(event)
                       
                       #Se o movimento for correto.
                        if pb2.mov_correto:
                          
                          #Variável que troca de turno
                          turno = "Branco"
                        


        #Cria as imagens dentro do jogo do peão branco
        for pb in peao_branco:
         tela.blit(pb.imagem, pb.rect)
        
        #Cria as imagens dentro do jogo do peão preto
        for pb2 in peao_preto:
         tela.blit(pb2.imagem, pb2.rect)
      
        #Atualiza a tela do tabuleiro
        pygame.display.update()      