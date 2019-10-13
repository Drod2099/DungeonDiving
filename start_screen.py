from config import *
color = (200, 85, 6)


class Start_screen():

    def __init__(self):
        self.mStart_screen = pygame.image.load("DungeonDiveMainScreen1.png")
        self.mCharacter_select_image = pygame.image.load("DungeonDiveMainScreen.png")
        wizard_rect = pygame.Rect(313, 517, 183, 80)
        knight_rect = pygame.Rect(100, 442, 185, 80)
        rogue_rect = pygame.Rect(522, 440, 180, 80)
        play = pygame.Rect(318, 318, 180, 75)
        controls = pygame.Rect(318, 405, 180, 75)
        quit = pygame.Rect(318, 492, 180, 75)
        self.mBack = pygame.Rect(703, 556, 97, 44)
        self.mStart_rect_list = (play, controls, quit)
        self.mChar_list = (rogue_rect, knight_rect, wizard_rect)
        self.mCharacter = None
        self.mState = None
        self.mStart = True
        self.mCharacter_select = False
        self.mHelp_screen = False
        self.mKnight_info = False
        self.mWizard_info = False
        self.mRogue_info = False
        self.mouse_pos = []

        self.mHelp_screen_back = pygame.Rect(0, 0, 100, 50)

    def click_test_char_select(self, m_pos):       # the purpose of this method is to test if a player class was clicked
        mouse_rect = pygame.Rect(m_pos[0], m_pos[1], 1, 1)
        rogue, knight, wizard = self.mChar_list
        if mouse_rect.colliderect(rogue):
            print("rogue selected")
            return "rogue"
        if mouse_rect.colliderect(knight):
            print("knight selected")
            return "knight"
        if mouse_rect.colliderect(wizard):
            print("wizard selected")
            return "wizard"
        if self.mCharacter_select:
            if mouse_rect.colliderect(self.mBack):
                return "back"

    def click_test_start_screen(self, m_pos):
        mouse_rect = pygame.Rect(m_pos[0], m_pos[1], 1, 1)
        play, controls, quit = self.mStart_rect_list
        if mouse_rect.colliderect(play):
            return "play"
        if mouse_rect.colliderect(controls):
            return "controls"
        if mouse_rect.colliderect(quit):
            return "quit"

    def click_test_help_screen(self, m_pos):
        mouse_rect = pygame.Rect(m_pos[0], m_pos[1], 1, 1)
        if mouse_rect.colliderect(self.mHelp_screen_back):
            return "back"

    def mouse_hover(self, m_pos):
        mouse_rect = pygame.Rect(m_pos[0], m_pos[1], 1, 1)
        rogue, knight, wizard = self.mChar_list
        if mouse_rect.colliderect(rogue):
            print("rogue selected")
            return "rogue"
        if mouse_rect.colliderect(knight):
            print("knight selected")
            return "knight"
        if mouse_rect.colliderect(wizard):
            print("wizard selected")
            return "wizard"
        return None

    def reset(self):
        self.mCharacter = None
        self.mCharacter_select = False
        self.mStart = True

    def input(self, m_pos, evt):
        self.mouse_pos = m_pos
        hovered_over_character = self.mouse_hover(m_pos)
        if self.mCharacter_select:
            if hovered_over_character is not None:
                if hovered_over_character == "wizard":
                    self.mWizard_info = True
                elif hovered_over_character == "rogue":
                    self.mRogue_info = True
                else:
                    self.mKnight_info = True
            elif hovered_over_character is None:
                self.mKnight_info = False
                self.mWizard_info = False
                self.mRogue_info = False

        if evt.type == pygame.QUIT:
            return False,None,None
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                return False,None,None

        elif evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                pygame.mixer.Sound("SoundEffects/menuclicksoundeffects.wav").play()
                if self.mStart:
                    self.mState = self.click_test_start_screen(m_pos)
                    if self.mState is not None:
                        if self.mState == "play":
                            self.mStart = False
                            self.mCharacter_select = True
                        elif self.mState == "controls":
                            self.mStart = False
                            self.mHelp_screen = True
                        else:
                            return False,None,None
                if self.mCharacter_select:
                    self.mCharacter = self.click_test_char_select(m_pos)    # when left click in menu screen click test gets ran
                    if self.mCharacter == "back":
                        self.mStart = True
                        self.mCharacter_select = False

                if self.mHelp_screen:
                    back = self.click_test_help_screen(m_pos)
                    if back == "back":
                        self.mStart = True
                        self.mCharacter_select = False
                        self.mHelp_screen = False

        return True, self.mCharacter, self.mState        # returns a tuple with state of running in main and a character

    def draw(self, win):
        if self.mStart:
            win.blit(self.mStart_screen, (0, 0))
        elif self.mCharacter_select:
            win.blit(self.mCharacter_select_image, (0, 0))
        if self.mKnight_info:
            win.blit(KnightInfo, (self.mouse_pos[0]-100, self.mouse_pos[1]-100))
        elif self.mWizard_info:
            win.blit(WizardInfo, (self.mouse_pos[0]-100, self.mouse_pos[1]-100))
        elif self.mRogue_info:
            win.blit(RogueInfo, (self.mouse_pos[0]-100, self.mouse_pos[1]-100))
        if self.mHelp_screen:
            win.blit(Help_screen, (0, 0))


########################################################################################################################

class Fight_screen:
    def __init__(self, cur_lvl, sub_lvl):

        # keeps track of level to display the correct screen
        self.cur_lvl = cur_lvl
        self.sub_lvl = sub_lvl

        self.inv_Font = pygame.font.SysFont("Bahnschrift", 40)

        # screens
        self.overworld_background = pygame.image.load("MapAssets/CombatBackgrounds/OverworldDungeonDiveAttackScreen.png")
        self.lava_background = pygame.image.load("MapAssets/CombatBackgrounds/LavaDungeonDiveAttackScreen.png")
        self.green_lava_background = pygame.image.load("MapAssets/CombatBackgrounds/GreenLavaDungeonDiveAttackScreen.png")

        self.overworld_inv = pygame.image.load("MapAssets/CombatBackgrounds/OverworldInventory.png")
        self.lava_inv = pygame.image.load("MapAssets/CombatBackgrounds/LavaInventory.png")
        self.green_inv = pygame.image.load("MapAssets/CombatBackgrounds/GreenLavaInventory.png")

        # rectangles for buttons
        self.attack = (22, 406, 180, 80)
        self.block = (22, 500, 180, 80)
        self.inventory = (220, 406, 180, 80)
        self.flee = (222, 500, 180, 80)

        self.open_inv = False
        self.sheild_potions = 0
        self.health_potions = 0
        self.special_potions = 0

    def update(self, dt, sheilds, healths, specials):
        self.sheild_potions = sheilds
        self.health_potions = healths
        self.special_potions = specials

    def check_pos(self, mpos):
        # checks to see if over attack button
        if self.attack[0] < mpos[0] < self.attack[0] + self.attack[2]:
            if self.attack[1] < mpos[1] < self.attack[1] + self.attack[-1] and not self.open_inv:
                return "attack"
            elif self.attack[1] < mpos[1] < self.attack[1] + self.attack[-1] and self.open_inv:
                return "health"

        # checks to see if over block
        if self.block[0] < mpos[0] < self.block[0] + self.block[2]:
            if self.block[1] < mpos[1] < self.block[1] + self.block[-1] and not self.open_inv:
                return "block"
            elif self.block[1] < mpos[1] < self.block[1] + self.block[-1] and self.open_inv:
                return "sheild"

        # checks to see if over inventory
        if self.inventory[0] < mpos[0] < self.inventory[0] + self.inventory[2]:
            if self.inventory[1] < mpos[1] < self.inventory[1] + self.inventory[-1] and not self.open_inv:
                return "inventory"
            elif self.inventory[1] < mpos[1] < self.inventory[1] + self.inventory[-1] and self.open_inv:
                return "special"

        # checks to see if ober flea
        if self.flee[0] < mpos[0] < self.flee[0] + self.flee[2]:
            if self.flee[1] < mpos[1] < self.flee[1] + self.flee[-1] and not self.open_inv:
                print("flee")
                return "flee"
            elif self.flee[1] < mpos[1] < self.flee[1] + self.flee[-1] and self.open_inv:
                return "back"

    def draw(self, surf):

        # print(self.cur_lvl)
        if self.cur_lvl == 1:
            surf.blit(self.overworld_background,(0,0))
            if self.open_inv:
                surf.blit(self.overworld_inv, (0, 393), (0, 0, 429, 599))
                surf.blit(self.inv_Font.render("x" + str(self.health_potions), True, (255, 255, 255)), (160, 430))
                surf.blit(self.inv_Font.render("x" + str(self.special_potions), True, (255, 255, 255)), (360, 430))
                surf.blit(self.inv_Font.render("x" + str(self.sheild_potions), True, (255, 255, 255)), (160, 525))

        if self.cur_lvl == 2:           # need to make a sublevel check for the green lava background
            surf.blit(self.lava_background, (0, 0))
            if self.open_inv:
                surf.blit(self.lava_inv, (0, 393), (0, 0, 429, 599))
                surf.blit(self.inv_Font.render("x" + str(self.health_potions), True, (255, 255, 255)), (160, 430))
                surf.blit(self.inv_Font.render("x" + str(self.special_potions), True, (255, 255, 255)), (360, 430))
                surf.blit(self.inv_Font.render("x" + str(self.sheild_potions), True, (255, 255, 255)), (160, 525))
            if self.sub_lvl == 2:
                surf.blit(self.green_lava_background, (0, 0))
                if self.open_inv:
                    surf.blit(self.green_inv, (0, 393), (0, 0, 429, 599))
                    surf.blit(self.inv_Font.render("x" + str(self.health_potions), True, (255, 255, 255)), (160, 430))
                    surf.blit(self.inv_Font.render("x" + str(self.special_potions), True, (255, 255, 255)), (360, 430))
                    surf.blit(self.inv_Font.render("x" + str(self.sheild_potions), True, (255, 255, 255)), (160, 525))

        if self.cur_lvl == 3:
            surf.blit(self.boss_background, (0, 0))

#########################################################################################


class Game_Over:
    def __init__(self):
        self.mGame_Over = pygame.image.load("GameOverScreen.png")
        restart = pygame.Rect(90, 413, 180, 80)
        mainMenu = pygame.Rect(310, 490, 180, 80)
        quit = pygame.Rect(530, 410, 180, 80)
        self.mOver_rect_list = (restart, mainMenu, quit)
        self.mState = None
        self.mReturn_state = False
    
    def click_test_game_over(self, m_pos):  
        mouse_rect = pygame.Rect(m_pos[0], m_pos[1], 1, 1)
        restart, mainMenu, quit = self.mOver_rect_list
        if mouse_rect.colliderect(restart):
            return "restart"
        if mouse_rect.colliderect(mainMenu):
            return "mainMenu"
        if mouse_rect.colliderect(quit):
            return "quit"

    def reset(self):
        self.mState = None
        self.mReturn_state = False

    def input(self, m_pos, evt):
        if evt.type == pygame.QUIT:
            return False,None,None
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                return False,None,None
        elif evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                self.mState = self.click_test_game_over(m_pos)
                if self.mState is not None:
                    if self.mState == "restart":
                        self.mReturn_state = "restart"
                    elif self.mState == "mainMenu":
                        self.mReturn_state = "mainmenu"
                    else:
                        return False,None

        return True,self.mReturn_state

    def draw(self, win):
        win.blit(self.mGame_Over, (0, 0))
##############################################################################################################


class Inventory:
    def __init__(self):
        self.Font = pygame.font.SysFont("Times New Roman", 25)
        self.exit_txt = self.Font.render("Close Menu", True, (0, 0, 0))

        self.background_rect = pygame.Rect(300, 100, 200, 400)
        health_rect = pygame.Rect(360, 160, 80, 80)
        sheild_rect = pygame.Rect(360, 250, 80, 80)
        special_rect = pygame.Rect(360, 340, 80, 80)
        self.exit_rect = pygame.Rect(310, 440, 180, 50)
        self.Rect_list = (health_rect, sheild_rect, special_rect)
        self.sheild_potions = 0
        self.health_potions = 0
        self.special_potions = 0

    def update(self, dt, sheilds, healths, specials):
        self.sheild_potions = sheilds
        self.health_potions = healths
        self.special_potions = specials

    def click_test(self, mpos):
        mouse_rec = pygame.Rect(mpos[0], mpos[1], 1, 1)
        health, sheild, special = self.Rect_list
        if mouse_rec.colliderect(health):
            print("healing")
            return "health"
        elif mouse_rec.colliderect(sheild):
            return "sheild"
        elif mouse_rec.colliderect(special):
            return "special"
        elif mouse_rec.colliderect(self.exit_rect):
            print("clicked exit")
            return "exit"

    def input(self, evt, mpos):
        potion_type = None
        inventory_status = True
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                potion_type = self.click_test(mpos)
                pygame.mixer.Sound("SoundEffects/PotionDrink.wav").play()
                # print(potion_type, "potion type in input")
                if potion_type == "exit":
                    inventory_status = False
                    potion_type = None

        return inventory_status, potion_type

    def draw(self, win):
        health_txt = self.Font.render("x" + str(self.health_potions), True, (0, 0, 0))
        h_txt_h = health_txt.get_height()
        h_txt_w = health_txt.get_width()
        sheild_txt = self.Font.render("x" + str(self.sheild_potions), True, (0, 0, 0))
        s_txt_h = sheild_txt.get_height()
        s_txt_w = sheild_txt.get_width()
        special_txt = self.Font.render("x" + str(self.special_potions), True, (0, 0, 0))
        sp_txt_h = special_txt.get_height()
        sp_txt_w = special_txt.get_width()

        win.blit(INVENTORY, (300, 100))
        win.blit(HEALTH_POTION, (360, 160))
        win.blit(SHEILD_POTION, (360, 250))
        win.blit(SPECIAL_POTION, (360, 340))

        win.blit(health_txt, (360 + h_txt_w, 160 + nh_h - h_txt_h))
        win.blit(sheild_txt, (360 + s_txt_w, 250 + ns_h - s_txt_h))
        win.blit(special_txt, (360 + sp_txt_w, 340 + nsp_h - sp_txt_h))


class Victory:
    def __init__(self):
        menu = pygame.Rect(164, 460, 183, 80)
        quit = pygame.Rect(485, 460, 183, 80)
        self.Rect_list = (menu, quit)
        self.mState = None

    def click_test_char_select(self, m_pos):       # the purpose of this method is to test if a player class was clicked
        mouse_rect = pygame.Rect(m_pos[0], m_pos[1], 1, 1)
        menu, quit = self.Rect_list
        if mouse_rect.colliderect(menu):
            return "menu"
        if mouse_rect.colliderect(quit):
            return "quit"

    def input(self, m_pos, evt):
        if evt.type == pygame.QUIT:
            return False, None
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                return False, None

        elif evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                self.mState = self.click_test_char_select(m_pos)    # when left click in menu screen click test gets ran
        return True, self.mState

    def reset(self):
        self.mState = None

    def draw(self, win):
        win.blit(VICTORY, (0, 0))
