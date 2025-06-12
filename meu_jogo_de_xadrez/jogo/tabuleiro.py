import pygame
from interface_grafica.cores import BRANCO, PRETO, BRANCO_ESCURO, PRETO_CLARO


class Tabuleiro:
    def __init__(self, bottom_color="Preto"):
        self.tamanho_quadrado = 75
        self.estado_tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.casas_destacadas = []
        self.pecas_brancas = []
        self.pecas_pretas = []
        self.en_passant_pawn = None
        
        if bottom_color == "Preto":
            self.direcoes = {"Branco": 1, "Preto": -1}
        else:
            self.direcoes = {"Branco": -1, "Preto": 1}
        
        self.bottom_color = bottom_color

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
        
        # Verificar se é um rei (tem atributo 'ja_moveu')
        if hasattr(peca, 'ja_moveu'):
            self.calcular_movimentos_rei(peca)
        # Verificar se é um peão (tem atributo 'en_passant_ativo')
        elif hasattr(peca, 'en_passant_ativo'):
            self.calcular_movimentos_peao(peca)
    
    def calcular_movimentos_rei(self, rei):
        """Calcula os movimentos válidos do rei."""
        from jogo.regras import obter_movimentos_validos
        movimentos_validos = obter_movimentos_validos(self, rei)
        self.casas_destacadas = movimentos_validos
    
    def calcular_movimentos_peao(self, peca):
        """Calcula os movimentos válidos do peão (lógica original)."""
        x, y = peca.posicao
        direcao = self.direcoes[peca.cor]
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
                    # Verificar se o alvo não é um rei
                    if not hasattr(alvo, 'ja_moveu'):  # Se não for rei
                        self.casas_destacadas.append(captura)
                elif (
                    self.en_passant_pawn is not None
                    and self.en_passant_pawn.posicao == (x + dx, y)
                    and self.en_passant_pawn.cor != peca.cor
                ):
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

    def capturar_peca(self, pos):
        x, y = pos
        peca = self.estado_tabuleiro[y][x]
        
        # Verificar se a peça é um rei - não permitir captura de reis
        if peca is not None and hasattr(peca, 'ja_moveu'):  # Se for rei
            # Não permitir a captura, só retornar a peça
            return peca
        
        # Para peças que não são reis, proceder normalmente
        self.estado_tabuleiro[y][x] = None
        
        if peca is not None:
            if peca.cor == "Branco" and peca in self.pecas_brancas:
                self.pecas_brancas.remove(peca)
            elif peca.cor == "Preto" and peca in self.pecas_pretas:
                self.pecas_pretas.remove(peca)
        
        return peca
