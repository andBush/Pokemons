import pygame
pygame.font.init()

class Text(pygame.sprite.Sprite):
    def __init__(self, tw, x, y, color = (255, 0, 0), size = 96):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.tw = tw
        self.f1 = pygame.font.Font(None, size)
        self.image = self.f1.render(tw, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.image = self.f1.render(self.tw, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


def drawText(surface, text, where, color=(222, 222, 222), font_name="consolas", font_size=16):
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    if type(where) is pygame.Rect:
        text_rect.center = where.center
    else:
        text_rect.topleft = where
    surface.blit(text, text_rect)