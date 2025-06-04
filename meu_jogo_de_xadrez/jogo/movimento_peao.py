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
        self.en_passant_ativo = False

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
        """Conclude a drag operation and update the board if the move is valid."""
        if not self.moving:
            return

        nova_pos = (
            round(self.rect.x / self.board.tamanho_quadrado),
            round(self.rect.y / self.board.tamanho_quadrado),
        )

        if nova_pos not in self.board.casas_destacadas:
            # posição inválida, retorna a peça
            self.rect.topleft = self.board.convert_pos_to_coord(self.posicao)
            self.mov_correto = False
            self.board.en_passant_pawn = None
            self.moving = False
            self.board.casas_destacadas = []
            return

        origem = self.posicao

        # verificar se é captura en passant
        capturou = False
        if self.board.en_passant_pawn is not None:
            pawn = self.board.en_passant_pawn
            direcao_inimigo = self.board.direcoes[pawn.cor]
            destino_en_passant = (
                pawn.posicao[0],
                pawn.posicao[1] - direcao_inimigo,
            )
            if nova_pos == destino_en_passant:
                self.board.capturar_peca(pawn.posicao)
                self.board.en_passant_pawn = None
                capturou = True

        if not capturou and not self.board.casa_livre(nova_pos):
            # captura normal
            self.board.capturar_peca(nova_pos)

        self.board.remover_peca(origem)
        self.posicao = nova_pos
        self.board.colocar_peca(self, nova_pos)
        self.rect.topleft = self.board.convert_pos_to_coord(nova_pos)
        self.mov_correto = True

        if abs(nova_pos[1] - origem[1]) == 2:
            self.board.en_passant_pawn = self
            self.en_passant_ativo = True
        else:
            self.board.en_passant_pawn = None
            self.en_passant_ativo = False
        self.contador_mov += 1
        self.moving = False
        self.board.casas_destacadas = []
