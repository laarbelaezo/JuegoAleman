import pygame
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen_path):
        super().__init__()
        try:
            self.image = pygame.image.load(resource_path(imagen_path)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 60))
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.gravedad = 0.8
        self.en_suelo = False
        self.game_over = False

    def update(self, plataformas, sonidos):
        keys = pygame.key.get_pressed()
        moviendo = False
        if keys[pygame.K_LEFT]: self.rect.x -= 7; moviendo = True
        if keys[pygame.K_RIGHT]: self.rect.x += 7; moviendo = True
            
        if moviendo and self.en_suelo and sonidos and not sonidos['walk'].get_num_channels():
            sonidos['walk'].play()
        
        if keys[pygame.K_UP]: self.saltar(sonidos['jump'] if sonidos else None)

        self.vel_y += self.gravedad
        self.rect.y += int(self.vel_y)
        self.en_suelo = False
        
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        for hit in hits:
            if self.vel_y > 0:
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.en_suelo = True
        if self.rect.y > 600: self.game_over = True

    def saltar(self, sonido_jump):
        if self.en_suelo and sonido_jump: 
            self.vel_y = -18
            sonido_jump.play()

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, imagen_path):
        super().__init__()
        self.rect = pygame.Rect(x, y, ancho, alto)
        try:
            tex = pygame.image.load(resource_path(imagen_path)).convert_alpha()
            self.image = pygame.transform.scale(tex, (ancho, alto))
        except:
            self.image = pygame.Surface((ancho, alto))
            self.image.fill((139, 69, 19))

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y