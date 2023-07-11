import pygame
from jogo.tabuleiro import Tabuleiro

class Peao:
    
    #Construtor
    def __init__(self, cor, posicao_inicial, imagem):
     self.cor = cor
     self.posicao = posicao_inicial
     self.imagem = imagem
     self.moving = False
     self.mov_correto = False
     self.tabuleiro = Tabuleiro()  # Mova isso para cima
     x, y = self.tabuleiro.convert_pos_to_coord(self.posicao)
     largura = altura = self.tabuleiro.tamanho_quadrado
     self.rect = pygame.Rect(x, y, largura, altura)
     
     #Condição ELPASSANT
     self.contador_mov = 0
    
    #Função que move através do ponto de colisão das peças    
    def mover(self, event):
        if self.moving:
            self.rect.move_ip(event.rel)


    #Função que inicia o movimento
    def iniciar_movimento(self, event):
        
        if event.button == 1 and self.rect.collidepoint(event.pos):
          # obter a posição da casa em que o jogador clicou
          pos_casa_clicada = (event.pos[0] // self.tabuleiro.tamanho_quadrado, event.pos[1] // self.tabuleiro.tamanho_quadrado)
          # verificar se a casa clicada está entre as casas destacadas
          if pos_casa_clicada in self.tabuleiro.casas_destacadas:
            # mover a peça para a casa clicada
            self.posicao = pos_casa_clicada
            self.rect.topleft = self.tabuleiro.convert_pos_to_coord(self.posicao)
          else:
            self.moving = True
    
    #Função que finaliza o movimento das peças.
    def finalizar_movimento(self, event):
        #Verifica se a movimentação é verdadeira, se for, ela finaliza a posição e move a peça.
        if self.moving:
            
            #Define a cor e a posição que a peça irá se mover.
            self.posicao, self.cor = self.mover_peao(self.posicao[0], self.posicao[1], self.rect, self.cor)
            
            #Após a movimentação, a var moving vai ser definida como falsa para continuar o turno.
            self.moving = False


    #Função para movimentar o peão.
    def mover_peao(self, x, y, rect, cor):
        
        #Define a posição atual da peça.
        posicao_atual = [x,y]
        
        #Converte a posição atual para a posição do tabuleiro.
        x,y = self.tabuleiro.convert_pos_to_coord(posicao_atual)
        
        #Define a posição nova da peça.
        posicao_nova = (round(rect.x/self.tabuleiro.tamanho_quadrado), round(rect.y/self.tabuleiro.tamanho_quadrado))            
        
        #Turno das peças brancas.
        if cor == "Branco":
           
           # Toda vez que um movimento for feito, essa var tem que resetar como false para sempre estar comprindo as condições do turno
           self.mov_correto = False
           
           #Lógica do EL PASSANT, essa condição verifica se a movimentação da peça peão está se movendo pela primeira vez.
           if self.contador_mov == 0: 
              if posicao_nova[1] == posicao_atual[1] +2 and posicao_nova[0] == posicao_atual[0]:
                posicao_atual = (posicao_nova[0],posicao_nova[1] if posicao_nova[1] < 8 else posicao_atual[1]) 
            
                #Essa linha aqui faz a casa do tabuleiro atrair a imagem
                rect.topleft = self.tabuleiro.convert_pos_to_coord(posicao_atual)
                self.mov_correto = True
             
                #Condição para fazer o el passant
                self.contador_mov+=1
           
           #Condição de movimentação para o resto dos movimentos.
           if posicao_nova[1] == posicao_atual[1] +1 and posicao_nova[0] == posicao_atual[0]:
              
             #Define a posição atual. 
             posicao_atual = (posicao_nova[0],posicao_nova[1] if posicao_nova[1] < 8 else posicao_atual[1]) 
            
             #Essa linha aqui faz a casa do tabuleiro atrair a imagem.
             rect.topleft = self.tabuleiro.convert_pos_to_coord(posicao_atual)
             self.mov_correto = True
             
             #Condição para fazer o el passant.
             self.contador_mov+=1
           
           # Se o movimento correto for falso ou seja, ele é incorreto, a peça irá voltar para sua casa original
           if self.mov_correto == False:                 
           
              #Isso que faz a peça não poder ir para outras casas se a condição anterior não for cumprida 
              rect.topleft = self.tabuleiro.convert_pos_to_coord(posicao_atual)
             
           
        #Define a movimentação para o peão preto.
        #Lembrando que as peças pretas estão subtraindo casas.
        elif cor == "Preto":
            self.mov_correto = False
            
            #Lógica do EL PASSANT, essa condição verifica se a movimentação da peça peão está se movendo pela primeira vez.
            if self.contador_mov == 0: 
              if posicao_nova[1] == posicao_atual[1] - 2 and posicao_nova[0] == posicao_atual[0]:
                posicao_atual = (posicao_nova[0],posicao_nova[1] if posicao_nova[1] < 8 else posicao_atual[1]) 
            
                #Essa linha aqui faz a casa do tabuleiro atrair a imagem
                rect.topleft = self.tabuleiro.convert_pos_to_coord(posicao_atual)
                self.mov_correto = True
             
                #Condição para fazer o el passant
                self.contador_mov+=1
            
            if posicao_nova[1] == posicao_atual[1] - 1 and posicao_nova[0] == posicao_atual[0]:
              posicao_atual = (posicao_nova[0], posicao_nova[1] if posicao_nova[1] >= 0 else posicao_atual[1])
              
              rect.topleft = self.tabuleiro.convert_pos_to_coord(posicao_atual)
              self.mov_correto = True
              
              #Condição para fazer o el passant
              self.contador_mov+=1

            if self.mov_correto == False: 
               
               rect.topleft = self.tabuleiro.convert_pos_to_coord(posicao_atual)
      
        # Retorna a nova posição atual para atualizar a função
        return posicao_atual, cor
