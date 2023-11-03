import pygame
import random


class Pokemon(pygame.sprite.Sprite):
    def __init__(self, image, elem, atk, df, x, y, screen=None, hp=100, new=True):
        """Creats the Pokemon. It has 100 heat points and
        level of attack and defence set by yourself,
        but they can't be less than 5.
        If Pokemon has 0 heat points, it faints."""
        pygame.font.init()
        super().__init__()
        if new:
            self.default_image = image
        self.elem = elem
        self.x = x
        self.y = y
        self.hp = hp
        self.atk = max(5, atk)
        self.df = max(5, df)
        self.faint = False
        self.image = pygame.transform.scale(image, (170, 200))
        self.rect = self.image.get_rect(bottom=y + 100)
        self.rect.center = (self.x, self.y)
        self.text_array = []
        self.text_array.append(f"Type: {self.elem}")
        self.text_array.append(f"Health: {self.hp}")
        self.text_array.append(f"Defeat: {self.df}")
        self.text_array.append(f"Attack: {self.atk}")

        fontObj = pygame.font.Font(None, 32)
        for i in range(4):
            textSufaceObj = fontObj.render(self.text_array[i], True, (86, 3, 25), None)
            textRectObj = textSufaceObj.get_rect(topleft=(0, 70 + 25 * i))
            self.image.blit(textSufaceObj, textRectObj)

    def attack(self, other, powerUp=1, dfUp=1, imagine=False):
        """This function  makes one Pokemon attacking another one.
         The Pokemon with 0 heat points can not attack or be attacked.
         Dependently on a type of Pokemon his attack and defence levels can be changed"""
        if self.hp == 0 or other.hp == 0:
            return 0
        if dfUp == 0.5:
            damage = self.atk * powerUp - other.df // 2
        else:
            damage = self.atk * powerUp - (other.df * dfUp)
        if damage > 0:
            if imagine:
                return damage
            other.hp -= damage
        else:
            if imagine:
                return 1
            other.hp -= 1
        other.hp = max(0, other.hp)

    def get_name(self):
        """Returns name of the Pokemon"""
        return self.elem

    def get_hp(self):
        """Returns heat points of the Pokemon"""
        return self.hp

    def get_atk(self):
        """Returns attack level of the Pokemon"""
        return self.atk

    def get_def(self):
        """Returns defence level of the Pokemon"""
        return self.df


class WaterPokemon(Pokemon):
    """Hello, I'm WaterPokemon. I have one feature. When
    I attack FirePokemon my power increases 3 times. I don't like them."""
    """ x and y must be given in the main program by formula."""

    def __init__(self, x, y, screen):
        image = pygame.image.load(f"img/pok/wat/{random.randint(0, 3)}.webp")
        self.default_image = image
        elem = "Water"
        atk = random.randint(50, 100)
        df = random.randint(30, 60)
        super().__init__(image, elem, atk, df, x, y, screen)

    def attack(self, other, imagine=False):
        if isinstance(other, FirePokemon):
            return super().attack(other, powerUp=3, imagine=imagine)
        return super().attack(other, imagine=imagine)


class FirePokemon(Pokemon):
    """Hello, I'm just FirePokemon. I hate the rules of this world.
    I don't have any features at all..."""

    def __init__(self, x, y, screen):
        image = pygame.image.load(f"img/pok/fir/{random.randint(0, 3)}.webp")
        self.default_image = image
        elem = "Fire"
        atk = random.randint(50, 100)
        df = random.randint(30, 60)
        super().__init__(image, elem, atk, df, x, y, screen)


class GrassPokemon(Pokemon):
    """Hello, I'm GrassPokemon. I have one feature. When I attack
    FirePokemon his defence decreases in 2 times. I don't like them."""

    def __init__(self, x, y, screen):
        image = pygame.image.load(f"img/pok/gras/{random.randint(0, 3)}.webp")
        self.default_image = image
        elem = "Grass"
        atk = random.randint(50, 100)
        df = random.randint(30, 60)
        super().__init__(image, elem, atk, df, x, y, screen)

    def attack(self, other, imagine=False):
        if isinstance(other, FirePokemon):
            return super().attack(other, dfUp=0.5, imagine=imagine)
        return super().attack(other, imagine=imagine)


class ElectricPokemon(Pokemon):
    """Hello, I'm ElectricPokemon. I have one feature. When I attack
    WaterPokemon his defence decreases goes to 0. I don't like them."""

    def __init__(self, x, y, screen):
        image = pygame.image.load(f"img/pok/elec/{random.randint(0, 3)}.webp")
        self.default_image = image
        elem = "Electric"
        atk = random.randint(50, 100)
        df = random.randint(30, 60)
        super().__init__(image, elem, atk, df, x, y, screen)

    def attack(self, other, imagine=False):
        if isinstance(other, WaterPokemon):
            return super().attack(other, dfUp=0, imagine=imagine)
        return super().attack(other, imagine=imagine)
