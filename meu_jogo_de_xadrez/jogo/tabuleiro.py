import pygame
from interface_grafica.cores import BRANCO, PRETO, BRANCO_ESCURO, PRETO_CLARO


class Tabuleiro:
    def __init__(self):
        self.tamanho_quadrado = 75
        self.estado_tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.casas_destacadas = []

    def convert_pos_to_coord(self, pos):
        x, y = pos
        return x * self.tamanho_quadrado, y * self.tamanho_quadrado

    def desenhar_tabuleiro(self, tela):
        for x in range(8):
            for y in range(8):
                cor = BRANCO if (x + y) % 2 == 0 else PRETO
                if (x, y) in self.casas_destacadas:
                    cor = BRANCO_ESCURO if (x + y) % 2 == 0 else PRETO_CLARO
                pygame.draw.rect(
                    tela,
                    cor,
                    (
                        x * self.tamanho_quadrado,
                        y * self.tamanho_quadrado,
                        self.tamanho_quadrado,
                        self.tamanho_quadrado,
                    ),
                )

    def calcular_casas_destacadas(self, peca):
        self.casas_destacadas = []
        x, y = peca.posicao
        direcao = 1 if peca.cor == "Branco" else -1
        proxima = (x, y + direcao)
        if 0 <= proxima[1] < 8 and self.casa_livre(proxima):
            self.casas_destacadas.append(proxima)
            duas = (x, y + 2 * direcao)
            if peca.contador_mov == 0 and 0 <= duas[1] < 8 and self.casa_livre(duas):
                self.casas_destacadas.append(duas)
        for dx in (-1, 1):
            captura = (x + dx, y + direcao)
            if 0 <= captura[0] < 8 and 0 <= captura[1] < 8:
                alvo = self.estado_tabuleiro[captura[1]][captura[0]]
                if alvo is not None and alvo.cor != peca.cor:
                    self.casas_destacadas.append(captura)

    def ocupado(self, pos):
        x, y = pos
        return self.estado_tabuleiro[y][x] is not None

    def casa_livre(self, pos):
        x, y = pos
        return self.estado_tabuleiro[y][x] is None

    def colocar_peca(self, peca, pos):
        x, y = pos
        self.estado_tabuleiro[y][x] = peca

    def remover_peca(self, pos):
        x, y = pos
        self.estado_tabuleiro[y][x] = None
