from jogo.regras import escolher_promocao, rei_em_cheque, cheque_mate, empate_por_afogamento, movimento_captura_rei
import pygame
from pygame.locals import *
from jogo.tabuleiro import Tabuleiro
from jogo.pecas import load_image
from interface_grafica.tela import ALTURA_TELA, LARGURA_TELA
from jogo.movimento_peao import Peao
from jogo.movimento_rei import Rei
from interface_grafica.interface import escolher_cor_inicial

# Inicializa o Pygame
pygame.init()

# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Xadrez com Reis - Cheque e Cheque Mate")

# Tela inicial de seleção de cor
cor_jogador = escolher_cor_inicial(tela)

# Cria um objeto de tabuleiro
tabuleiro = Tabuleiro(bottom_color=cor_jogador)
tabuleiro.desenhar_tabuleiro(tela)

# Variável do jogo
running = True
turno = "Branco"
jogo_terminado = False
mensagem_final = ""

# Carrega as imagens
white_panw_img = load_image('whitepanw.png')
black_panw_img = load_image('blackpanw.png')
white_king_img = load_image('whiteking.png')
black_king_img = load_image('blackking.png')

# Posições das peças baseadas na cor do jogador
linha_peao_branco = 6 if cor_jogador == "Branco" else 1
linha_peao_preto = 6 if cor_jogador == "Preto" else 1
linha_rei_branco = 7 if cor_jogador == "Branco" else 0
linha_rei_preto = 7 if cor_jogador == "Preto" else 0

# Cria os peões
peao_branco = [Peao("Branco", (i, linha_peao_branco), white_panw_img, tabuleiro) for i in range(8)]
tabuleiro.pecas_brancas.extend(peao_branco)

peao_preto = [Peao("Preto", (i, linha_peao_preto), black_panw_img, tabuleiro) for i in range(8)]
tabuleiro.pecas_pretas.extend(peao_preto)

# Cria os reis
rei_branco = Rei("Branco", (4, linha_rei_branco), white_king_img, tabuleiro)
tabuleiro.pecas_brancas.append(rei_branco)

rei_preto = Rei("Preto", (4, linha_rei_preto), black_king_img, tabuleiro)
tabuleiro.pecas_pretas.append(rei_preto)

# Agrupa todas as peças
todas_pecas_brancas = tabuleiro.pecas_brancas
todas_pecas_pretas = tabuleiro.pecas_pretas

def verificar_fim_de_jogo(cor_atual):
    """Verifica se o jogo terminou (cheque mate ou empate)."""
    global jogo_terminado, mensagem_final
    
    if cheque_mate(tabuleiro, cor_atual):
        cor_vencedora = "Preto" if cor_atual == "Branco" else "Branco"
        mensagem_final = f"Cheque Mate! {cor_vencedora} venceu!"
        jogo_terminado = True
    elif empate_por_afogamento(tabuleiro, cor_atual):
        mensagem_final = "Empate por afogamento!"
        jogo_terminado = True

def desenhar_status(tela):
    """Desenha o status do jogo na tela."""
    font = pygame.font.SysFont(None, 24)
    
    # Verifica se há cheque
    if rei_em_cheque(tabuleiro, turno):
        texto_cheque = font.render(f"Cheque ao rei {turno}!", True, (255, 0, 0))
        tela.blit(texto_cheque, (10, 10))
    
    # Mostra de quem é o turno
    texto_turno = font.render(f"Turno: {turno}", True, (0, 0, 0))
    tela.blit(texto_turno, (10, 40))
    
    # Mostra mensagem final se jogo terminou
    if jogo_terminado:
        texto_final = font.render(mensagem_final, True, (255, 0, 0))
        tela.blit(texto_final, (10, 70))

# Modificação para calcular destacamentos com segurança (evitando captura de reis)
def calcular_destacamentos_seguros(peca):
    """Calcula as casas destacadas, removendo posições onde há um rei."""
    tabuleiro.calcular_casas_destacadas(peca)
    
    # Filtrar movimentos que tentam capturar um rei
    casas_seguras = []
    for pos in tabuleiro.casas_destacadas:
        if not movimento_captura_rei(tabuleiro, peca, pos):
            casas_seguras.append(pos)
    
    tabuleiro.casas_destacadas = casas_seguras

# Looping principal do jogo
while running:
    # Desenha o tabuleiro
    tabuleiro.desenhar_tabuleiro(tela)
    
    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not jogo_terminado:
            # Turno das peças brancas
            if turno == "Branco":
                for peca in todas_pecas_brancas:
                    if peca.rect.collidepoint(event.pos):
                        calcular_destacamentos_seguros(peca)
                        peca.iniciar_movimento(event)
                        
            # Turno das peças pretas
            elif turno == "Preto":
                for peca in todas_pecas_pretas:
                    if peca.rect.collidepoint(event.pos):
                        calcular_destacamentos_seguros(peca)
                        peca.iniciar_movimento(event)
        
        elif event.type == pygame.MOUSEMOTION and not jogo_terminado:
            if turno == "Branco":
                for peca in todas_pecas_brancas:
                    if peca.moving:
                        peca.mover(event)
            elif turno == "Preto":
                for peca in todas_pecas_pretas:
                    if peca.moving:
                        peca.mover(event)
        
        elif event.type == pygame.MOUSEBUTTONUP and not jogo_terminado:
            # Turno das peças brancas
            if turno == "Branco":
                for peca in todas_pecas_brancas:
                    if peca.moving:
                        peca.finalizar_movimento(event)
                        
                        if peca.mov_correto:
                            # Verificar promoção de peão
                            if hasattr(peca, 'en_passant_ativo'):  # É um peão
                                promocao_branco = 7 if tabuleiro.direcoes["Branco"] == 1 else 0
                                if peca.posicao[1] == promocao_branco:
                                    peca.imagem = escolher_promocao(
                                        "white", 
                                        tabuleiro, 
                                        LARGURA_TELA, 
                                        ALTURA_TELA, 
                                        tela)
                            
                            # Trocar turno e verificar fim de jogo
                            turno = "Preto"
                            verificar_fim_de_jogo(turno)
                            
            # Turno das peças pretas
            elif turno == "Preto":
                for peca in todas_pecas_pretas:
                    if peca.moving:
                        peca.finalizar_movimento(event)
                        
                        if peca.mov_correto:
                            # Verificar promoção de peão
                            if hasattr(peca, 'en_passant_ativo'):  # É um peão
                                promocao_preto = 7 if tabuleiro.direcoes["Preto"] == 1 else 0
                                if peca.posicao[1] == promocao_preto:
                                    peca.imagem = escolher_promocao(
                                        "black", 
                                        tabuleiro, 
                                        LARGURA_TELA, 
                                        ALTURA_TELA, 
                                        tela)
                            
                            # Trocar turno e verificar fim de jogo
                            turno = "Branco"
                            verificar_fim_de_jogo(turno)
    
    # Desenha todas as peças
    for peca in todas_pecas_brancas:
        tela.blit(peca.imagem, peca.rect)
    for peca in todas_pecas_pretas:
        tela.blit(peca.imagem, peca.rect)
    
    # Desenha status do jogo
    desenhar_status(tela)
    
    # Atualiza a tela
    pygame.display.update()

pygame.quit() 