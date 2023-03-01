import pygame
import os

IMG_DIR = os.path.join('meu_jogo_de_xadrez\interface_grafica\imagens')

def load_image(name, size= (75,75)):
    path = os.path.join(IMG_DIR, name)
    imagens = []
    for i in range(0,7):
        img = pygame.image.load(path).convert_alpha() 
        img = pygame.transform.scale(img, size)
        imagens.append(img)
    return img
