from config import *
import random


class Chest:
    def __init__(self, chest_pos, sprite=None):
        self.chest_screen = pygame.Surface((200, 120))
        self.health_potions = random.randint(0, 2)
        self.def_potions = random.randint(0, 2)
        self.special_potion_chance = random.randint(0, 2)
        if self.special_potion_chance == 1:
            self.special_potion = 1
        else:
            self.special_potion = 0
        self.sprite = sprite
        self.chest_pos = chest_pos[0], chest_pos[1]
        self.take = False
        self.Bounding_rect = None
        self.camera = [0, 0]

        self.font = pygame.font.SysFont("Bahnschrift", 16)
        """self.hp_text = "Health Potions: " + str(self.health_potions)
        self.def_text = "Defense Potions: " + str(self.def_potions)
        self.spec_text = "Special Potions ;): " + str(self.special_potion)"""

    def update(self,camera):
        self.camera = camera
        # print(self.camera)
        self.Bounding_rect = pygame.Rect(int(self.chest_pos[0]-self.camera[0]), int(self.chest_pos[1]-self.camera[1]),
                                         32, 32)
        # print(self.Bounding_rect)

    def take_items(self,your_potions):
        # print("we made it this far")
        # if self.take == True:
        if self.special_potion_chance != 1:
            self.special_potion = 0
        if self.special_potion_chance == 1:
            your_potions[-1].append(0)
        for i in range(self.health_potions ):
            your_potions[0].append(0)
        for i in range(self.def_potions ):
            your_potions[1].append(0)
                # print('took')

    def draw(self, surf, take, text=None):
        # pygame.draw.rect(surf, (255, 255, 255), (int(self.chest_pos[0]-self.camera[0]),
        #                                          int(self.chest_pos[1]-self.camera[1]), 32, 32), 1)
        if take:
            surf.blit(self.chest_screen, (500, 400))
            self.chest_screen.blit(chest_win, (0, 0))
            self.chest_screen.blit(self.font.render(str(text[0]), True, (0, 0, 0)), (35, 10))
            self.chest_screen.blit(self.font.render(str(text[1]), True, (0, 0, 0)), (30, 50))
            self.chest_screen.blit(self.font.render(str(text[2]), True, (0, 0, 0)), (32, 90))
            # use the tuple passed in text

#######################################################################################################################
