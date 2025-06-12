from .tela import ALTURA_TELA, LARGURA_TELA
import pygame

def escolher_cor_inicial(tela):
    """Mostra uma tela para o jogador escolher jogar de branco ou preto."""
    font = pygame.font.SysFont(None, 48)
    botao_branco = pygame.Rect(LARGURA_TELA // 4 - 75, ALTURA_TELA // 2 - 50, 150, 100)
    botao_preto = pygame.Rect(3 * LARGURA_TELA // 4 - 75, ALTURA_TELA // 2 - 50, 150, 100)

    while True:
        tela.fill((120, 120, 120))
        titulo = font.render("Escolha sua cor", True, (0, 0, 0))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 150)))

        pygame.draw.rect(tela, (255, 255, 255), botao_branco)
        pygame.draw.rect(tela, (0, 0, 0), botao_preto)
        pygame.draw.rect(tela, (0, 0, 0), botao_branco, 2)
        pygame.draw.rect(tela, (255, 255, 255), botao_preto, 2)

        txt_b = font.render("Branco", True, (0, 0, 0))
        txt_p = font.render("Preto", True, (255, 255, 255))
        tela.blit(txt_b, txt_b.get_rect(center=botao_branco.center))
        tela.blit(txt_p, txt_p.get_rect(center=botao_preto.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_branco.collidepoint(event.pos):
                    return "Branco"
                if botao_preto.collidepoint(event.pos):
                    return "Preto"