import pygame
import os

IMG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "interface_grafica", "imagens"
)


def load_image(name, size=(75, 75)):
    """Load an image from the assets directory and resize it."""
    path = os.path.join(IMG_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img
