import pygame
from pygame.locals import *
from jogo.tabuleiro import Tabuleiro
from jogo.pecas import load_image
from interface_grafica.tela import ALTURA_TELA, LARGURA_TELA
from jogo.movimento_peao import Peao


def escolher_cor_inicial():
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


def escolher_promocao(cor):
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


# Inicializa o Pygame
pygame.init()


# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tabuleiro de Xadrez")

# Tela inicial de seleção de cor
cor_jogador = escolher_cor_inicial()

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
            
            #Se o turno for a vez das peças brancas.
            if turno == "Branco":
                
                #Para iterar em cada peão branco.
                for pb in peao_branco:
                    
                    #O collidepoint é o ponto de colisão das peças, cada imagem tem um ponto de colisão, quando ele é acionado, ele inicia o movimento.
                    if pb.rect.collidepoint(event.pos):
                        
                        #A variavel tabuleiro faz o papel de calcular as casas que podem ser "Preenchidas" pelas peças.
                        tabuleiro.calcular_casas_destacadas(pb)
                        
                        #Inicia a movimentação do peão.
                        pb.iniciar_movimento(event)
                        
            #Vez das peças pretas.
            elif turno == "Preto":

                #Looping para iterar em cada peça preta.
                for pb2 in peao_preto:
                    
                    #Ponto de colisão dos peões pretos.
                    if pb2.rect.collidepoint(event.pos):
                        
                        #Calcula as possíveis casas.
                        tabuleiro.calcular_casas_destacadas(pb2)
                        
                        #Inicia o movimento
                        pb2.iniciar_movimento(event)
                       

        
        
        elif event.type == pygame.MOUSEMOTION:
            if turno == "Branco":
                for pb in peao_branco:
                    if pb.moving:
                        pb.mover(event)
                        
            
            elif turno == "Preto":
                for pb2 in peao_preto:
                    if pb2.moving:
                        pb2.mover(event)
                        

        
        
        elif event.type == pygame.MOUSEBUTTONUP:
           
            #Turno das peças brancas.
            if turno == "Branco":

                #looping para iterar em cada peão.
                for pb in peao_branco:

                    if pb.moving:

                        pb.finalizar_movimento(event)

                        # Se o movimento for correto, ele passa na condição e troca de turno
                        if pb.mov_correto:
                            if pb.posicao[1] == 7:
                                pb.imagem = escolher_promocao("white")

                            #Variável que troca de turno
                            turno = "Preto"
                       
            
            # Turno das peças pretas.
            elif turno == "Preto":

                #Looping para iterar cada peão preto.
                for pb2 in peao_preto:

                    if pb2.moving:

                        #Finaliza o movimento do peão preto
                        pb2.finalizar_movimento(event)

                       #Se o movimento for correto.
                        if pb2.mov_correto:
                            if pb2.posicao[1] == 0:
                                pb2.imagem = escolher_promocao("black")

                            #Variável que troca de turno
                            turno = "Branco"
    #Cria as imagens dentro do jogo do peão branco
    for pb in peao_branco:
        tela.blit(pb.imagem, pb.rect)

    #Cria as imagens dentro do jogo do peão preto
    for pb2 in peao_preto:
        tela.blit(pb2.imagem, pb2.rect)

    #Atualiza a tela do tabuleiro
    pygame.display.update()
