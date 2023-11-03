import pygame
import random
from pokemons import *
from trainer import *
from text import *
# недостатки: переменные в родительской и неродительской функции называются одинаково
# не работает когда электрик бьёт водного
"""
Gameplay:

Firstly, you choose the trainer to play with. There are 2 types Smart and Usual. 
Smart Trainer picks pokemons and plays them the best way. Usual Trainer does it by chance.

Then 10 pokemons spawn. You take turns for choosing one, you start.
When picking is finished, the battle starts automatically.

In battle you place the pokemon, then the opponent places his one and starts next round.
"""

def check():
    global fighting, some_more, trainer2, trainer1
    if trainer2.box.sprites().__len__() == 0 or trainer1.box.sprites().__len__() == 0:
        return True

FPS = 60
WIDTH = 1340
HEIGHT = 782
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemons")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

pokemons_g = pygame.sprite.Group()

trainer1 = Trainer(100, 358)
trainer2 = SmartTrainer(1200, 358)
trainers_g = pygame.sprite.Group()
trainers_g.add(trainer1)
trainers_g.add(trainer2)

textik = Text("You attack", WIDTH // 2, 70)
text_g = pygame.sprite.Group()
text_g.add(textik)

bg = pygame.image.load("img/bg.jpg")

# Цикл игры
running = True
picking = True
fighting = False
new_game = True
new_fight = False
some_more = False
who_attacks = 1
who_picks = 1

while running:
    while picking:
        if new_game:
            new_game = False
            bg = pygame.image.load("img/bg.jpg")
            pokemons_g = pygame.sprite.Group()
            for i in range(10):
                x = 317 + i % 5 * 170
                y = 230 + i // 5 * 300
                pokemon_type = random.randint(0, 3)
                if pokemon_type == 0:
                    P = ElectricPokemon(x, y, screen)
                    pokemons_g.add(P)
                if pokemon_type == 1:
                    P = FirePokemon(x, y, screen)
                    pokemons_g.add(P)
                if pokemon_type == 2:
                    P = WaterPokemon(x, y, screen)
                    pokemons_g.add(P)
                if pokemon_type == 3:
                    P = GrassPokemon(x, y, screen)
                    pokemons_g.add(P)
                # screen.blit(P.image, P.rect.center)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                picking = False
                some_more = False
                fighting = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # ловим покемона
                for p in pokemons_g:
                    if p.rect.collidepoint(e.pos[0], e.pos[1]):
                        pokemons_g.remove(p)
                        trainer1.box.add(p)
                        choosed = trainer2.choice(pokemons_g)
                        pokemons_g.remove(choosed)
                        trainer2.box.add(choosed)

                if len(pokemons_g) == 0:
                    picking = False
                    fighting = True
                    new_fight = True
                    who_attacks = 1
                    break
        # Рендеринг
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        pokemons_g.draw(screen)
        trainers_g.draw(screen)
        # Обновление
        pokemons_g.update()
        trainers_g.update()
        text_g.update()
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        clock.tick(FPS)

    while fighting:
        if new_fight:
            bg = pygame.transform.scale(pygame.image.load("img/octagon.jpg"),  (WIDTH, HEIGHT))
            who_attacks = 1
            for i in range(10):
                if i < 5:
                    pok = trainer1.box.sprites()[i]
                    pok.image = pygame.transform.scale(pok.image, (170 * 2 // 3, 200 * 2 // 3))
                    pok.rect.center = (300,  110 + i % 5 * 150)
                    pok.x = 300
                    pok.y = 110 + i % 5 * 150
                else:
                    pok = trainer2.box.sprites()[i-5]
                    pok.image = pygame.transform.scale(pok.image, (170 * 2 // 3, 200 * 2 // 3))
                    pok.rect.center = (1050, 110 + i % 5 * 150)
                    pok.x = 1000
                    pok.y = 110 + i % 5 * 150

            new_fight = False

        for p in range(len(trainer2.box.sprites())):
            trainer2.box.sprites()[p] = trainer2.box.sprites()[p].update()
        for p in range(len(trainer1.box.sprites())):
            trainer1.box.sprites()[p] = trainer1.box.sprites()[p].update()

        for e in pygame.event.get():
            if trainer2.box.sprites().__len__() == 0 or trainer1.box.sprites().__len__() == 0:
                fighting = False
                some_more = True
            if e.type == pygame.QUIT:
                running = False
                picking = False
                fighting = False
                some_more = False
            elif e.type == pygame.MOUSEBUTTONDOWN and who_attacks == 1:
                if who_picks == 1:
                    for p in trainer1.box:
                        if p.rect.collidepoint(e.pos[0], e.pos[1]):
                            oppo_attack = p
                            who_picks = 2
                            break
                else:
                    for p in trainer2.box:
                        if p.rect.collidepoint(e.pos[0], e.pos[1]):
                            terpila = p
                            who_picks = 1
                            while oppo_attack.hp > 0 and terpila.hp > 0:
                                oppo_attack.attack(terpila)
                                terpila.attack(oppo_attack)
                            who_attacks = 2
                            text_g.sprites()[0].tw = "Opponent attacks"
            elif who_attacks == 2:
                if check():
                    fighting = False
                    some_more = True
                    break

                terpila, oppo_attack = trainer2.pick_for_fight(trainer1.box)
                while oppo_attack.hp > 0 and terpila.hp > 0:
                    terpila.attack(oppo_attack)
                    if oppo_attack.hp <= 0:
                        break
                    oppo_attack.attack(terpila)
                who_attacks = 1
                text_g.sprites()[0].tw = "You attack"

                        #trainer2.picking(trainer1.box)

        for p in trainer2.box.sprites():
            if p.hp == 0:
                trainer2.box.remove(p)
        for p in trainer1.box.sprites():
            if p.hp == 0:
                trainer1.box.remove(p)

        # Рендеринг
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        trainer1.box.draw(screen)
        trainer2.box.draw(screen)
        trainers_g.draw(screen)
        text_g.draw(screen)
        # Обновление
        pokemons_g.update()
        trainers_g.update()
        text_g.update()
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        ####if random.randint(0, 2):
            ####text_g.sprites()[0].tw = "Opponent attacks"
        ####else:
            ####text_g.sprites()[0].tw = "You attack"
        #So 'textik' is now another text
        clock.tick(FPS)

    while some_more:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                picking = False
                fighting = False
                some_more = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                trainer2.box.empty()
                trainer1.box.empty()
                some_more = False
                fighting = False
                new_game = True
                new_fight = True
                picking = True
pygame.quit()