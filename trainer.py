import pygame
from pokemons import *


class Trainer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.box = pygame.sprite.Group()
        self.wins = 0
        self.x = x
        self.y = y
        num = random.randint(1, 5)
        image = pygame.image.load(f"img/train/{num}.webp")
        self.image = pygame.transform.scale(image, (179, 500))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def add(self, other: Pokemon):
        self.box.append(other)


    def update(self):
        return
        #self.x += 1
        #self.y += 1
        #self.rect.center = (self.x, self.y)
        #self.image.blit(self.image, (self.x, self.y))


class SmartTrainer(Trainer):
    def imagine_fight(self, pok1: 'mine and attacking', pok2):
        damage_to_2 = 0
        damage_to_1 = 0
        while damage_to_2 < pok2.hp and damage_to_1 < pok2.hp:
            damage_to_2 += pok1.attack(pok2, imagine=True)
            if damage_to_2 < pok2.hp:
                damage_to_1 += pok1.attack(pok2, imagine=True)
            else:
                break
        return pok1.hp - damage_to_1

    def choice(self, pokemons_g):
        best = 0
        best_pok = None
        for i in pokemons_g:
            if i.get_atk() + i.get_def() > best:
                best_pok = i
                best = i.get_atk() + i.get_def()
        return best_pok

    def pick_for_fight(self, opbox):
        best = 10000000000000
        #pok.elem
        dic = {"Water": ["Fire", 3, 1], "Grass": ["Fire", 1, 0.5], "Electric": ["Water", 0, 1], "Fire": [None, None, None]}
        # лучший для меня выбор это когда после боя мой покемон выигрывает и у него остается минимальное здоровье,
        # для этого нужно написать аттакк без изменений здоровья, затем возвращаем результаты боя и мутим кулнесс
        my_fighter = self.box.sprites()[0]
        oppo_fighter = opbox.sprites()[0]
        for pok1 in self.box:
            for pok2 in opbox:
                if dic[pok1.elem][0] == pok2.elem:
                    cool = self.imagine_fight(pok1, pok2)
                    if cool > 0 and cool < best:
                        best = cool
                        my_fighter = pok1
                        oppo_fighter = pok2
        return (my_fighter, oppo_fighter)