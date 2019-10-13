import pygame

red = (255, 0, 0)
blue = (0, 0, 255)


class Lvl_warp():

    def __init__(self):
        self.mFont = pygame.font.SysFont("Times New Roman", 20)
        self.mTxt0 = self.mFont.render("Level Warp Selection:", True, (255, 255, 0))

        self.mTxt1 = self.mFont.render("Warp to lvl 1", True, red)
        self.mTxt1_1 = self.mFont.render("Warp to lvl 1", True, blue)

        self.mTxt2 = self.mFont.render("Warp to lvl 2", True, red)
        self.mTxt2_1 = self.mFont.render("Warp to lvl 2", True, blue)

        self.mTxt3 = self.mFont.render("Warp to lvl 3", True, red)
        self.mTxt3_1 = self.mFont.render("Warp to lvl 3", True, blue)

        self.mRects = (pygame.Rect(300, 250, 200, 50), pygame.Rect(300, 325, 200, 50), pygame.Rect(300, 400, 200, 50))

        self.mLvl1 = False
        self.mLvl2 = False
        self.mLvl3 = False

    def update(self, dt):
        pass

    def click_test_lvl_select(self, mouse_rect):
        lvl1, lvl2, lvl3 = self.mRects
        if self.mLvl1:
            if mouse_rect.colliderect(lvl1):
                return 1
        if self.mLvl2:
            if mouse_rect.colliderect(lvl2):
                return 2
        if self.mLvl3:
            if mouse_rect.colliderect(lvl3):
                return 3

    def input(self, evt, cur_lvl):
        if cur_lvl > 1:
            self.mLvl1 = True
        if cur_lvl > 2:
            self.mLvl2 = True
        if cur_lvl == 3:
            self.mLvl3 = True
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx, my, 1, 1)

        level_selected = None
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                level_selected = self.click_test_lvl_select(mouse_rect)

        if level_selected is not None:
            return level_selected, False
        return level_selected, True

    def draw(self, win):
        for rect in self.mRects:
            pygame.draw.rect(win, (255, 255, 255), rect, 1)
        win.blit(self.mTxt0, (300, 200))
        if self.mLvl1:
            win.blit(self.mTxt1_1, (300, 250))
        else:
            win.blit(self.mTxt1, (300, 250))
        if self.mLvl2:
            win.blit(self.mTxt2_1, (300, 325))
        else:
            win.blit(self.mTxt2, (300, 325))
        if self.mLvl3:
            win.blit(self.mTxt3_1, (300, 400))
        else:
            win.blit(self.mTxt3, (300, 400))
