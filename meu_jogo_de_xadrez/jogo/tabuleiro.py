import pygame
from interface_grafica.cores import BRANCO, PRETO

# Desenha o tabuleiro
class Tabuleiro:
    def __init__(self):
        self.tamanho_quadrado = 75
    
    def convert_pos_to_coord(self, pos):
        x, y = pos
        return x * self.tamanho_quadrado, y * self.tamanho_quadrado
    
    def desenhar_tabuleiro(self, tela):
        for x in range(8):
            for y in range(8):
                cor = BRANCO if (x + y) % 2 == 0 else PRETO
                pygame.draw.rect(tela, cor, (x * self.tamanho_quadrado, y * self.tamanho_quadrado, self.tamanho_quadrado, self.tamanho_quadrado))
                
    def calcular_posicao(self, x,y):
      x, y = self.convert_pos_to_coord((x,y))
      return x, y
    
    def ocupado(self, pos):
        x, y = pos
        return self.desenhar_tabuleiro[x][y] is not None
    
    def casa_livre(self, pos):
        x,y = pos 
        return self.desenhar_tabuleiro[x][y] is None

    def colocar_peca(self, peca, pos):
        x, y = pos
        self.desenhar_tabuleiro[x][y] = peca.tipo_peca
    
    def remover_peca(self, pos):
        x, y = pos
        self.desenhar_tabuleiro[x][y] = None