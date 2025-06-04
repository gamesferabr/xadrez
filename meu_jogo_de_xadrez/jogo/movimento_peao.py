import pygame


class Peao:
    def __init__(self, cor, posicao_inicial, imagem, tabuleiro):
        self.cor = cor
        self.posicao = posicao_inicial
        self.imagem = imagem
        self.board = tabuleiro
        self.board.colocar_peca(self, self.posicao)
        x, y = self.board.convert_pos_to_coord(self.posicao)
        tamanho = self.board.tamanho_quadrado
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.moving = False
        self.mov_correto = False
        self.contador_mov = 0
        self._offset = (0, 0)

    def iniciar_movimento(self, event):
        if event.button == 1 and self.rect.collidepoint(event.pos):
            self.moving = True
            self._offset = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)

    def mover(self, event):
        if self.moving:
            self.rect.topleft = (
                event.pos[0] - self._offset[0],
                event.pos[1] - self._offset[1],
            )

    def finalizar_movimento(self, event):
        if self.moving:
            nova_pos = (
                round(self.rect.x / self.board.tamanho_quadrado),
                round(self.rect.y / self.board.tamanho_quadrado),
            )
            if nova_pos in self.board.casas_destacadas:
                self.board.remover_peca(self.posicao)
                if not self.board.casa_livre(nova_pos):
                    self.board.remover_peca(nova_pos)
                self.posicao = nova_pos
                self.board.colocar_peca(self, nova_pos)
                self.rect.topleft = self.board.convert_pos_to_coord(nova_pos)
                self.mov_correto = True
                self.contador_mov += 1
            else:
                self.rect.topleft = self.board.convert_pos_to_coord(self.posicao)
                self.mov_correto = False
            self.moving = False
            self.board.casas_destacadas = []
