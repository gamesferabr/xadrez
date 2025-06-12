import pygame
from jogo.pecas import load_image

def escolher_promocao(cor, tabuleiro, LARGURA_TELA, ALTURA_TELA, tela):
    """Exibe opções de promoção e retorna a imagem selecionada."""
    nomes = [
        f"{cor.lower()}queen.png",
        f"{cor.lower()}rook.png",
        f"{cor.lower()}bishop.png",
        f"{cor.lower()}knight.png",
    ]
    imagens = [load_image(n) for n in nomes]
    tamanho = tabuleiro.tamanho_quadrado
    inicio_x = (LARGURA_TELA - tamanho * 4) // 2
    y = (ALTURA_TELA - tamanho) // 2
    retangulos = [
        pygame.Rect(inicio_x + i * tamanho, y, tamanho, tamanho)
        for i in range(4)
    ]
    selecionando = True
    while selecionando:
        tabuleiro.desenhar_tabuleiro(tela)
        for pb in tabuleiro.pecas_brancas:
            tela.blit(pb.imagem, pb.rect)
        for pb in tabuleiro.pecas_pretas:
            tela.blit(pb.imagem, pb.rect)
        for img, rect in zip(imagens, retangulos):
            pygame.draw.rect(tela, (200, 200, 200), rect)
            tela.blit(img, rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                for img, rect in zip(imagens, retangulos):
                    if rect.collidepoint(event.pos):
                        return img


def encontrar_rei(tabuleiro, cor):
    """Encontra a posição do rei da cor especificada."""
    for y in range(8):
        for x in range(8):
            peca = tabuleiro.estado_tabuleiro[y][x]
            if peca is not None and hasattr(peca, 'cor') and peca.cor == cor:
                # Verifica se é um rei (tem atributo 'ja_moveu' que é específico do rei)
                if hasattr(peca, 'ja_moveu'):
                    return (x, y)
    return None


def movimento_captura_rei(tabuleiro, peca, nova_posicao):
    """Verifica se um movimento tenta capturar o rei adversário."""
    if tabuleiro.casa_livre(nova_posicao):
        return False
    
    x, y = nova_posicao
    peca_alvo = tabuleiro.estado_tabuleiro[y][x]
    
    # Verifica se a peça alvo é um rei (tem atributo 'ja_moveu')
    return hasattr(peca_alvo, 'ja_moveu')


def casa_atacada_por(tabuleiro, posicao, cor_atacante):
    """Verifica se uma casa está sendo atacada por peças da cor especificada."""
    x, y = posicao
    
    # Verificar ataques de peões
    direcao_peao = tabuleiro.direcoes[cor_atacante]
    for dx in [-1, 1]:
        peao_x, peao_y = x + dx, y - direcao_peao
        if 0 <= peao_x < 8 and 0 <= peao_y < 8:
            peca = tabuleiro.estado_tabuleiro[peao_y][peao_x]
            if (peca is not None and peca.cor == cor_atacante and 
                hasattr(peca, 'en_passant_ativo')):  # É um peão
                return True
    
    # Verificar ataques de rei (uma casa em todas as direções)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            rei_x, rei_y = x + dx, y + dy
            if 0 <= rei_x < 8 and 0 <= rei_y < 8:
                peca = tabuleiro.estado_tabuleiro[rei_y][rei_x]
                if (peca is not None and peca.cor == cor_atacante and 
                    hasattr(peca, 'ja_moveu')):  # É um rei
                    return True
    
    # TODO: Adicionar verificações para outras peças (torre, bispo, cavalo, rainha)
    # quando elas forem implementadas
    
    return False


def rei_em_cheque(tabuleiro, cor):
    """Verifica se o rei da cor especificada está em cheque."""
    posicao_rei = encontrar_rei(tabuleiro, cor)
    if posicao_rei is None:
        return False
    
    cor_inimiga = "Preto" if cor == "Branco" else "Branco"
    return casa_atacada_por(tabuleiro, posicao_rei, cor_inimiga)


def movimento_deixa_rei_em_cheque(tabuleiro, peca, nova_posicao):
    """Simula um movimento e verifica se deixa o próprio rei em cheque."""
    # Salvar estado atual
    posicao_original = peca.posicao
    peca_capturada = None
    
    # Simular movimento
    if not tabuleiro.casa_livre(nova_posicao):
        peca_capturada = tabuleiro.estado_tabuleiro[nova_posicao[1]][nova_posicao[0]]
    
    tabuleiro.remover_peca(posicao_original)
    tabuleiro.colocar_peca(peca, nova_posicao)
    peca.posicao = nova_posicao
    
    # Verificar se rei está em cheque
    em_cheque = rei_em_cheque(tabuleiro, peca.cor)
    
    # Desfazer movimento
    tabuleiro.remover_peca(nova_posicao)
    tabuleiro.colocar_peca(peca, posicao_original)
    peca.posicao = posicao_original
    
    if peca_capturada is not None:
        tabuleiro.colocar_peca(peca_capturada, nova_posicao)
    
    return em_cheque


def obter_movimentos_validos(tabuleiro, peca):
    """Obtém todos os movimentos válidos de uma peça (que não deixam o rei em cheque)."""
    movimentos_possiveis = []
    
    # Obter movimentos baseado no tipo de peça
    if hasattr(peca, 'get_movimentos_possiveis'):
        # Para o rei
        movimentos_possiveis = peca.get_movimentos_possiveis()
    elif hasattr(peca, 'en_passant_ativo'):
        # Para peões - usar a lógica existente do tabuleiro
        tabuleiro.calcular_casas_destacadas(peca)
        movimentos_possiveis = tabuleiro.casas_destacadas.copy()
    
    # Filtrar movimentos que deixam rei em cheque
    movimentos_validos = []
    for movimento in movimentos_possiveis:
        if not movimento_deixa_rei_em_cheque(tabuleiro, peca, movimento):
            movimentos_validos.append(movimento)
    
    return movimentos_validos


def cheque_mate(tabuleiro, cor):
    """Verifica se há cheque mate para a cor especificada."""
    if not rei_em_cheque(tabuleiro, cor):
        return False
    
    # Verificar se alguma peça da cor pode fazer um movimento válido
    pecas = tabuleiro.pecas_brancas if cor == "Branco" else tabuleiro.pecas_pretas
    
    for peca in pecas:
        movimentos_validos = obter_movimentos_validos(tabuleiro, peca)
        if movimentos_validos:
            return False  # Existe pelo menos um movimento válido
    
    return True  # Não há movimentos válidos - é cheque mate


def empate_por_afogamento(tabuleiro, cor):
    """Verifica se há empate por afogamento (rei não está em cheque mas não pode mover)."""
    if rei_em_cheque(tabuleiro, cor):
        return False  # Não é afogamento se está em cheque
    
    # Verificar se alguma peça da cor pode fazer um movimento válido
    pecas = tabuleiro.pecas_brancas if cor == "Branco" else tabuleiro.pecas_pretas
    
    for peca in pecas:
        movimentos_validos = obter_movimentos_validos(tabuleiro, peca)
        if movimentos_validos:
            return False  # Existe pelo menos um movimento válido
    
    return True  # Não há movimentos válidos e não está em cheque - é afogamento
