from config import *
import pygame
import random


class ParentPlayer:

    def __init__(self, camera, pos, image=None, health=1, strength=10, stealth=10):
        """class constructor requires the image file for all player frames"""
        # self explained attributes
        self.mSprite_sht = image
        self.mPoss = pos
        self.mSpd = 350
        self.mDist = None
        self.mCam = camera
        self.mMax_health = 1
        self.mHealth = health
        self.mStrength = strength
        self.mStealth = stealth

        # Describes in boolean if the camera is touching the right side
        self.mRight_lock = False
        self.mLeft_lock = False
        self.mTop_lock = False
        self.mBottom_lock = False

        # animation attributes
        self.mRow = 0
        print(self.mSprite_sht)
        if self.mSprite_sht == KNIGHT:
            self.mRow = 3
        self.mColumn = 0
        self.mFrame_timer = 0.05
        self.mDirection = None

        # special attributes
        self.special = False    # means that you drank the potion and your ability can be used
        self.x = 0
        self.wizard_timer = 5
        self.rogue_timer = 5
        self.knight_timer = 5
        self.special_enemy = None

        #special meter
        self.sx = 0
        self.special_timer = 5
        self.percent = 1

        #text init
        self.dirFont = pygame.font.SysFont("Bahnschrift", 20)


    def update(self, dt, special_enemy,bounds, frms_wide, directions):
        """
        :param dt: deltaTime
        :param bounds: list of rects where the player cannot move
        :param frms_wide: how many frames of animation wide is the sprite sheet
        :return: Nothing
        """
        self.special_enemy = special_enemy
        self.mDist = self.mSpd * dt

        if self.mDirection is not None:
            self.mFrame_timer -= dt
            if self.mFrame_timer < 0:
                if self.mDirection == "right":
                    self.mColumn = (self.mColumn + 1) % frms_wide
                    self.mRow = directions["right"]
                if self.mDirection == "left":
                    self.mColumn = (self.mColumn + 1) % frms_wide
                    self.mRow = directions["left"]
                if self.mDirection == "up":
                    self.mColumn = (self.mColumn + 1) % frms_wide
                    self.mRow = directions["up"]
                if self.mDirection == "down":
                    self.mColumn = (self.mColumn + 1) % frms_wide
                    self.mRow = directions["down"]

                self.mFrame_timer = 0.05
            else:
                self.mDirection = None

        if not self.mLeft_lock:
            if self.mCam[0] <= 0:
                self.mCam[0] = 0
                self.mLeft_lock = True
        if not self.mTop_lock:
            if self.mCam[1] <= 0:
                self.mCam[1] = 0
                self.mTop_lock = True
        if not self.mRight_lock:
            if self.mCam[0] >= 800:
                self.mCam[0] = 800
                self.mRight_lock = True
        if not self.mBottom_lock:
            if self.mCam[1] >= 1000:
                self.mCam[1] = 1000
                self.mBottom_lock = True

        if self.mTop_lock:
            if self.mPoss[1] >= 300:
                self.mTop_lock = False
        if self.mLeft_lock:
            if self.mPoss[0] >= 400:
                self.mLeft_lock = False
        if self.mRight_lock:
            if self.mPoss[0] <= 1200:
                self.mRight_lock = False
        if self.mBottom_lock:
            if self.mPoss[1] <= 1300:
                self.mBottom_lock = False

        # timer for the special power
        if directions["player"] == "wizard":
            if self.special is True:
                self.x += dt
                if self.x >= self.wizard_timer:
                    self.special = False
                    self.x = 0

        elif directions["player"] == "rogue":
            if self.special_ability:
                if self.special:
                    self.x += dt
                    if self.x > self.rogue_timer:
                        self.special_ability = False
                        self.special = False
                        self.x = 0

        elif directions["player"] == "knight":
            if self.special is True:
                self.x += dt
                if self.x > self.knight_timer:
                    self.special = False
                    self.x = 0

        if directions["player"] != "rogue":
            if self.special == True:
                self.sx += dt
                self.percent = 1 - self.sx/self.special_timer
            else:
                self.sx = 0
                self.percent = 1

        else:
            if self.special_ability == True and self.special == True:
                self.sx += dt
                self.percent = 1 - self.sx/self.special_timer
            else:
                self.percent = 1
                self.sx = 0



    def input(self, evt, attack_avalible, bounds, keys, lvlwarp, directions):
        """ this chunk of input only determines the direction of movement the player needs to go
        :param evt: Nothing (this may change
        :param keys: for device polling
        :return: Nothing
        """
        self.mCur_pos = self.mPoss.copy()
        self.mPoss = self.mPoss.copy()
        self.mCur_cam = self.mCam.copy()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.mDirection = "left"
            self.mPoss[0] -= self.mDist
            if not self.mRight_lock and not self.mLeft_lock:
                self.mCam[0] -= self.mDist
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.mDirection = "right"
            self.mPoss[0] += self.mDist
            if not self.mLeft_lock and not self.mRight_lock:
                self.mCam[0] += self.mDist
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.mDirection = "up"
            self.mPoss[1] -= self.mDist
            if not self.mBottom_lock and not self.mTop_lock:
                self.mCam[1] -= self.mDist
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.mDirection = "down"
            self.mPoss[1] += self.mDist
            if not self.mTop_lock and not self.mBottom_lock:
                self.mCam[1] += self.mDist

        x_offset = directions["x_offset"]
        y_offset = directions["y_offset"]
        next_pos = pygame.Rect(self.mPoss[0] + x_offset, self.mPoss[1] + y_offset, 37, 55)  # directions["framewidth"], directions["frameheight"])
        for rect in bounds:
            rec = pygame.Rect(rect)
            # print(rec)
            if rec.colliderect(next_pos):
                self.mPoss = self.mCur_pos

        self.mCam[0] = self.mPoss[0] - 400
        self.mCam[1] = self.mPoss[1] - 300
        if self.mCam[0] <= 0:
            self.mCam[0] = 0
        if self.mCam[1] <= 0:
            self.mCam[1] = 0

        cur_pos = pygame.Rect(self.mPoss[0] + x_offset, self.mPoss[1] + y_offset, directions["framewidth"], directions["frameheight"])
        # print(self.mLvl2warp)
        # print(cur_pos, "pos")
        if lvlwarp.colliderect(cur_pos):
            print("colliding with lvl warp")
            return True

    def draw(self,win):
        if self.special == True:
            width = 120 * self.percent
            pygame.draw.rect(win,(200,200,200),(650,70,width, 20))
            pygame.draw.rect(win, (255,255,255), (650,70,120,20),1)

        win.blit(self.dirFont.render("Health : " + str(self.mHealth) + "/" + str(self.mMax_health),False, (255,255,255)), (650,30))



class Knight(ParentPlayer):

    def __init__(self, camera, pos, sprite, Lvl2warp):
        """Creates a Knight object"""
        ParentPlayer.__init__(self, camera, pos, sprite)
        self.mSprite = sprite
        self.armor_class = 15
        self.mLvl2warp = Lvl2warp
        self.Bounding_rect = None
        self.rage_mode = False
        self.mMax_health = 100
        self.mHealth = 100

    def update(self, dt, special_enemy, bounds, frms_wide, paladin_directions):
        super().update(dt, special_enemy, bounds, frms_wide, paladin_directions)
        self.Bounding_rect = pygame.Rect(int(self.mPoss[0] + 12 - self.mCam[0]), int(self.mPoss[1] + 8 - self.mCam[1]),
                                         37, 55)
        # print(self.mSprite)
        if self.special is True:
            self.rage_mode = True
        else:
            self.rage_mode = False

    def draw(self, win):
        super().draw(win)
        width = knight_directions["framewidth"]
        height = knight_directions["frameheight"]
        rect = (self.mColumn * width, self.mRow * height, width, height)  # Visualizeing the rect the player uses for collision
        # pygame.draw.rect(win, (255, 255, 255), (int(self.mPoss[0] + 12 - self.mCam[0]),
        #                                         int(self.mPoss[1] + 8 - self.mCam[1]), 37, 55), 2)
        if self.rage_mode is False:
            win.blit(self.mSprite, (self.mPoss[0] - self.mCam[0], self.mPoss[1] - self.mCam[1]), rect)
        if self.rage_mode is True:
            win.blit(REDKNIGHT, (self.mPoss[0] - self.mCam[0], self.mPoss[1] - self.mCam[1]), rect)


class Wizard(ParentPlayer):

    def __init__(self, camera, pos, sprite, Lvl2warp):
        """Creates a Knight object"""
        ParentPlayer.__init__(self, camera, pos, sprite)
        self.mSprite = sprite
        self.armor_class = 12
        self.mLvl2warp = Lvl2warp
        self.Bounding_rect = None
        self.special_attack = False
        self.mouse_pos = None
        self.mMax_health = 75
        self.mHealth = 75

    def update(self, dt, special_enemy, bounds, frms_wide, paladin_directions):
        super().update(dt, special_enemy, bounds, frms_wide, paladin_directions)
        self.g, self.b = random.randint(0, 255), random.randint(0, 255)
        self.Bounding_rect = pygame.Rect(int(self.mPoss[0] + 15 - self.mCam[0]), int(self.mPoss[1] + 5 - self.mCam[1]),
                                         37, 55)
        self.mouse_pos = pygame.mouse.get_pos()

    def input(self, evt, attack_avalible, bounds, keys, lvlwarp, directions):
        next = super().input(evt, attack_avalible, bounds, keys, lvlwarp, directions)

        if self.special is True:
            # probably going to be mousebutton events
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_SPACE:
                    self.special_attack = True
                    if self.special_enemy is not None:
                        self.special_enemy.mHealth -= 3
            if evt.type == pygame.KEYUP:
                if evt.key == pygame.K_SPACE:
                    self.special_attack = False

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    self.special_attack = True
                    if self.special_enemy is not None:
                        self.special_enemy.mHealth -= 3
            elif evt.type == pygame.MOUSEBUTTONUP:
                if evt.button == 1:
                    self.special_attack = False

        return next

    def draw(self, win):
        # print(self.mPoss)
        super().draw(win)
        width = wizard_directions["framewidth"]
        height = wizard_directions["frameheight"]
        rect = (self.mColumn * width, self.mRow * height, width, height)          # Visualizeing the rect the player uses for collision
        # pygame.draw.rect(win, (255, 255, 255), (int(self.mPoss[0] + 15 - self.mCam[0]),
        #                                         int(self.mPoss[1] + 5 - self.mCam[1]), paladin_width,
        #                                         paladin_height), 1)
        # pygame.draw.rect(win, (255, 255, 255), (int(self.mPoss[0] + 12 - self.mCam[0]), int(self.mPoss[1] + 8 - self.mCam[1]), 37, 55), 2)
        win.blit(self.mSprite, (self.mPoss[0] - self.mCam[0], self.mPoss[1] - self.mCam[1]), rect)

        if self.special_enemy is not None and self.special is True:
            b = self.special_enemy
            rect = b.mBounding_rect  # (b.mPos[0],b.mPos[1],20,20)
            pygame.draw.rect(win, (255, 0, 0), rect, 1)

        # draws the lazer
        if self.special_attack is True and self.special is True:
            pxy = (int(self.mPoss[0] + 40 - self.mCam[0]), int(self.mPoss[1] + 15 - self.mCam[1]))
            if self.special_enemy is not None:
                exy = (int(self.special_enemy.mPos[0] - self.mCam[0]+(self.special_enemy.mFrame_w//2)),
                       int(self.special_enemy.mPos[1] - self.mCam[1]+(self.special_enemy.mFrame_h//2)))
            else:
                exy = (int(self.mouse_pos[0]),
                       int(self.mouse_pos[1]))
            pygame.draw.line(win, (0, self.g, self.b), pxy, exy, 2)


class Rogue(ParentPlayer):

    def __init__(self, camera, pos, sprite, Lvl2warp):
        """Creates a Knight object"""
        ParentPlayer.__init__(self, camera, pos, sprite)
        self.mSprite = sprite
        self.armor_class = 9
        self.mLvl2warp = Lvl2warp
        self.Bounding_rect = None
        self.special_ability = False
        self.mMax_health = 50
        self.mHealth = 50

    def update(self, dt, special_enemy, bounds, frms_wide, paladin_directions):
        super().update(dt, special_enemy, bounds, frms_wide, paladin_directions)
        self.Bounding_rect = pygame.Rect(int(self.mPoss[0] + 15 - self.mCam[0]), int(self.mPoss[1] - self.mCam[1]+3),
                                         30, 45)

    def input(self, evt, attack_avalible, bounds, keys, lvlwarp, directions):
        next = super().input(evt, attack_avalible, bounds, keys, lvlwarp, directions)

        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                if self.special:
                    self.special_ability = True

        return next

    def draw(self, win):
        # print(self.mPoss)
        super().draw(win)
        width = rogue_directions["framewidth"]
        height = rogue_directions["frameheight"]
        rect = (self.mColumn * width, self.mRow * height, width, height)
        # pygame.draw.rect(win, (255, 255, 255), (int(self.mPoss[0] + 15 - self.mCam[0]),
                                                # int(self.mPoss[1] - self.mCam[1] + 3), 30, 45), 1)
        if self.special and self.special_ability:
            self.mSprite.set_alpha(100)
        else:
            self.mSprite.set_alpha(255)
        win.blit(self.mSprite, (self.mPoss[0] - self.mCam[0] + 13, self.mPoss[1] - self.mCam[1] + 5), rect)
