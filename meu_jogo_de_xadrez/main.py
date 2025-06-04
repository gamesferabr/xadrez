def confirmar_voltar():
    """Pergunta ao jogador se ele deseja voltar para a tela inicial."""
    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render("Voltar para a tela inicial?", True, (0, 0, 0))
    rect_sim = pygame.Rect(LARGURA_TELA // 2 - 120, ALTURA_TELA // 2, 100, 50)
    rect_nao = pygame.Rect(LARGURA_TELA // 2 + 20, ALTURA_TELA // 2, 100, 50)
    while True:
        tela.fill((180, 180, 180))
        tela.blit(texto, texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40)))
        pygame.draw.rect(tela, (0, 200, 0), rect_sim)
        pygame.draw.rect(tela, (200, 0, 0), rect_nao)
        txt_sim = fonte.render("Sim", True, (0, 0, 0))
        txt_nao = fonte.render("Não", True, (0, 0, 0))
        tela.blit(txt_sim, txt_sim.get_rect(center=rect_sim.center))
        tela.blit(txt_nao, txt_nao.get_rect(center=rect_nao.center))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_sim.collidepoint(event.pos):
                    return True
                if rect_nao.collidepoint(event.pos):
                    return False


from jogo.regras import escolher_promocao
import pygame
from pygame.locals import *
from jogo.tabuleiro import Tabuleiro
from jogo.pecas import load_image
from interface_grafica.tela import ALTURA_TELA, LARGURA_TELA
from jogo.movimento_peao import Peao
from interface_grafica.interface import escolher_cor_inicial

# Inicializa o Pygame
pygame.init()

# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tabuleiro de Xadrez")

# Tela inicial de seleção de cor
cor_jogador = escolher_cor_inicial(tela)

# Cria um objeto de tabuleiro
tabuleiro = Tabuleiro(bottom_color=cor_jogador)
tabuleiro.desenhar_tabuleiro(tela)
 

#Essa parte do código cria uma variável onde o jogo começa e a váriável running de True vira false para continuar o loop.
running = True

turno = "Branco"

#Carrega as imagens do peão
white_panw_img = load_image('whitepanw.png')
black_panw_img = load_image('blackpanw.png')


# Cria todos os peões de acordo com a cor que ficou na parte inferior
linha_branco = 6 if cor_jogador == "Branco" else 1
linha_preto = 6 if cor_jogador == "Preto" else 1

peao_branco = [Peao("Branco", (i, linha_branco), white_panw_img, tabuleiro) for i in range(8)]
tabuleiro.pecas_brancas.extend(peao_branco)
peao_branco = tabuleiro.pecas_brancas

peao_preto = [Peao("Preto", (i, linha_preto), black_panw_img, tabuleiro) for i in range(8)]
tabuleiro.pecas_pretas.extend(peao_preto)

peao_preto = tabuleiro.pecas_pretas

#Looping principal que faz o jogo ou engine rodar.
while running:
    #Desenha o tabuleiro do meu jogo de xadrez.
    tabuleiro.desenhar_tabuleiro(tela)
    
    #Para o evento rodando, o pygame irá capturar todas as movimentações do meu game.
    for event in pygame.event.get():
        
        #Se o tipo evento for para sair do jogo, a condição do looping será quebrada e irá fechar a janela do meu jogo atual.
        if event.type == pygame.QUIT:
            running = False

        #Se o botão do mouse for pressionado, a variavel evento irá ser chamada para iterar e executar os movimentos das peças.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
fonte_botao = pygame.font.SysFont(None, 24)
while True:
    cor_jogador = escolher_cor_inicial()
    tabuleiro = Tabuleiro(bottom_color=cor_jogador)
    white_panw_img = load_image("whitepanw.png")
    black_panw_img = load_image("blackpanw.png")
    linha_branco = 6 if cor_jogador == "Branco" else 1
    linha_preto = 6 if cor_jogador == "Preto" else 1
    peao_branco = [Peao("Branco", (i, linha_branco), white_panw_img, tabuleiro) for i in range(8)]
    tabuleiro.pecas_brancas.extend(peao_branco)
    peao_branco = tabuleiro.pecas_brancas
    peao_preto = [Peao("Preto", (i, linha_preto), black_panw_img, tabuleiro) for i in range(8)]
    tabuleiro.pecas_pretas.extend(peao_preto)
    peao_preto = tabuleiro.pecas_pretas
    botao_voltar = pygame.Rect(LARGURA_TELA - 90, 10, 80, 30)
    turno = "Branco"
    running = True
    while running:
        tabuleiro.desenhar_tabuleiro(tela)
        tabuleiro.desenhar_contador(tela)
        pygame.draw.rect(tela, (100, 0, 0), botao_voltar)
        txt_voltar = fonte_botao.render("Voltar", True, (255, 255, 255))
        tela.blit(txt_voltar, txt_voltar.get_rect(center=botao_voltar.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    if confirmar_voltar():
                        running = False
                        break
                else:
                    if turno == "Branco":
                        for pb in peao_branco:
                            if pb.rect.collidepoint(event.pos):
                                tabuleiro.calcular_casas_destacadas(pb)
                                pb.iniciar_movimento(event)
                    else:
                        for pb2 in peao_preto:
                            if pb2.rect.collidepoint(event.pos):
                                tabuleiro.calcular_casas_destacadas(pb2)
                                pb2.iniciar_movimento(event)
            elif event.type == pygame.MOUSEMOTION:
                if turno == "Branco":
                    for pb in peao_branco:
                        if pb.moving:
                            pb.mover(event)
                else:
                    for pb2 in peao_preto:
                        if pb2.moving:
                            pb2.mover(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if turno == "Branco":
                    for pb in peao_branco:
                        if pb.moving:
                            pb.finalizar_movimento(event)
                            if pb.mov_correto:
                                promocao_branco = 7 if tabuleiro.direcoes["Branco"] == 1 else 0
                                if pb.posicao[1] == promocao_branco:
                                    pb.imagem = escolher_promocao("white")
                                turno = "Preto"
                else:
                    for pb2 in peao_preto:
                        if pb2.moving:
                            pb2.finalizar_movimento(event)
                            if pb2.mov_correto:
                                promocao_preto = 7 if tabuleiro.direcoes["Preto"] == 1 else 0
                                if pb2.posicao[1] == promocao_preto:
                                    pb2.imagem = escolher_promocao("black")
                                turno = "Branco"

        for pb in peao_branco:
            tela.blit(pb.imagem, pb.rect)
        for pb2 in peao_preto:
            tela.blit(pb2.imagem, pb2.rect)
        pygame.display.update()

