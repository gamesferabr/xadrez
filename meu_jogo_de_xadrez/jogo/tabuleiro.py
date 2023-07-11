import pygame
from interface_grafica.cores import BRANCO, PRETO, BRANCO_ESCURO,PRETO_CLARO

# Desenha o tabuleiro
class Tabuleiro:
    
    #Construtor
    def __init__(self):
        
        #Tamanho do quadrado do tabuleiro
        self.tamanho_quadrado = 75
        
        #Verifica como estão as casas de cada tabuleiro, se está vazia ou não e cria uma lista através disso.
        self.estado_tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        
        #Verifica e cria uma lista de casas destacadas.
        self.casas_destacadas = []
    

    #Função que converte as coordenadas para se adaptar ao tamanho da tela.
    def convert_pos_to_coord(self, pos):
        
        #Define x e y como um valor de posição ou pos
        x, y = pos
        
        #Retorna cada posição no tamanho certo do quadrado do jogo ou da tela.
        return x * self.tamanho_quadrado, y * self.tamanho_quadrado
    

    #Função que realmente desenha o tabuleiro na tela.
    def desenhar_tabuleiro(self, tela):
      
      #Looping da coordenada x.
      for x in range(8):
        
        #Looping da coordenada y.
        for y in range(8):
            # Verifica se a tupla de x + y é par, se for é a cor branca se não é a cor preta, fazendo o tabuleiro de xadrez.
            cor = BRANCO if (x + y) % 2 == 0 else PRETO
            
            #Essa condição verifica as possíveis casas válidas das peças.
            if (x, y) in self.casas_destacadas:
                 cor = BRANCO_ESCURO if (x + y) % 2 == 0 else PRETO_CLARO  #Destaca a cor das casas válidas de verde.
            
            #Var da própria library que chama o método e desenha o tabuleiro.
            pygame.draw.rect(tela, cor, (x * self.tamanho_quadrado, y * self.tamanho_quadrado, self.tamanho_quadrado, self.tamanho_quadrado))


    def calcular_casas_destacadas(self, peca, turno):
      self.casas_destacadas = []  # limpa qualquer destaque existente
      x, y = peca.posicao
      
      # para este exemplo, vamos apenas destacar as casas diretamente acima, abaixo, à esquerda e à direita da peça
      if turno == "Preto":
       if y > 0:
        
        #Essa condição verifica se é o primeiro movimento
        if peca.contador_mov == 0:
          
          #Se for, a casa destacada é -2 por ser das peças pretas, indicando ao jogador que é possível mover
          self.casas_destacadas.append((x,y - 2))
        
        #Casas destacadas quando o movimento é diferente do movimento inicial, e se for o mesmo, é possível mover um ou duas casas
        self.casas_destacadas.append((x, y - 1))
        
      elif turno == "Branco":
       if y < 7:
        if peca.contador_mov == 0:
          self.casas_destacadas.append((x,y + 2))
        self.casas_destacadas.append((x, y + 1))

    def ocupado(self, pos):
     x, y = pos
     return self.estado_tabuleiro[y][x] is not None


    def casa_livre(self, pos):
     x,y = pos 
     return self.estado_tabuleiro[x][y] is None


    def colocar_peca(self, peca, pos):
     x, y = pos
     self.estado_tabuleiro[x][y] = peca.tipo_peca


    def remover_peca(self, pos):
     x, y = pos
     self.estado_tabuleiro[x][y] = None