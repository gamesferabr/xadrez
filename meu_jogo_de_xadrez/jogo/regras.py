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
