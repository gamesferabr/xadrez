import pygame
from jogo.regras import movimento_captura_rei


class Rei:
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
        self.ja_moveu = False

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
        """Conclude o movimento do rei e verifica se é válido."""
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
            self.moving = False
            self.board.casas_destacadas = []
            return

        # Verificar se está tentando capturar um rei
        if movimento_captura_rei(self.board, self, nova_pos):
            # Impedir movimento que captura rei
            self.rect.topleft = self.board.convert_pos_to_coord(self.posicao)
            self.mov_correto = False
            self.moving = False
            self.board.casas_destacadas = []
            return

        origem = self.posicao

        # Verificar se há peça na nova posição para capturar
        if not self.board.casa_livre(nova_pos):
            self.board.capturar_peca(nova_pos)

        # Mover o rei
        self.board.remover_peca(origem)
        self.posicao = nova_pos
        self.board.colocar_peca(self, nova_pos)
        self.rect.topleft = self.board.convert_pos_to_coord(nova_pos)
        self.mov_correto = True
        
        self.contador_mov += 1
        self.ja_moveu = True
        self.moving = False
        self.board.casas_destacadas = []

    def get_movimentos_possiveis(self):
        """Retorna todos os movimentos possíveis do rei (sem validação de cheque)."""
        movimentos = []
        x, y = self.posicao
        
        # Rei pode mover uma casa em qualquer direção
        direcoes = [
            (-1, -1), (-1, 0), (-1, 1),  # linha superior
            (0, -1),           (0, 1),   # lados
            (1, -1),  (1, 0),  (1, 1)    # linha inferior
        ]
        
        for dx, dy in direcoes:
            nova_x, nova_y = x + dx, y + dy
            
            # Verificar se está dentro do tabuleiro
            if 0 <= nova_x < 8 and 0 <= nova_y < 8:
                nova_pos = (nova_x, nova_y)
                
                # Pode mover para casa vazia ou capturar peça inimiga
                if self.board.casa_livre(nova_pos):
                    movimentos.append(nova_pos)
                else:
                    peca_destino = self.board.estado_tabuleiro[nova_y][nova_x]
                    if peca_destino.cor != self.cor:
                        # Verificar se não está tentando capturar um rei
                        if not hasattr(peca_destino, 'ja_moveu'):  # Não é rei
                            movimentos.append(nova_pos)
        
        return movimentos
