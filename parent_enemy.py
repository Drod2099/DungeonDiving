import parent_player
from config import *
from vector import *


class Parent_enemy:
    def __init__(self, img, cam, pos, damage=None, defense=None):
        self.mSprite = img
        # print(self.mSprite)
        self.mCam = cam
        self.mPos = pos

        if img == GOBLIN:
            self.mEnemy_info = goblin_info
            self.mDirections = goblin_directions
        elif img == ZOMBIE:
            self.mEnemy_info = zombie_info
            self.mDirections = zombie_directions
        self.mSf = self.mEnemy_info["scale"]
        self.mNum_rows = self.mEnemy_info["rows"]
        self.mNum_columns = self.mEnemy_info["collums"]
        self.mFrame_w = self.mEnemy_info["frame_w"]  # self.mSprite.get_width() // self.mNum_columns
        self.mFrame_h = self.mEnemy_info["frame_h"]
        self.mFrame_timer = .1
        self.mDirection = None

        self.mRow = 0
        self.mColumn = 0
        self.mPoi = pos
        self.mDist = 0
        self.mRad = self.mEnemy_info["view_radius"]

        self.mDamage = self.mEnemy_info["enemy_die"]
        self.mMax_health = self.mEnemy_info["health"]
        self.mHealth = self.mEnemy_info["health"]
        self.mDefense = defense
        self.mSpeed = self.mEnemy_info["speed"]
        self.armor_class = self.mEnemy_info["armour"]
        self.mStrength = self.mEnemy_info["strength"]
        self.rogue_invisable = False

    def update(self, dt, combat_dt, p_pos, cam, bool_for_not_moving):
        # print("enemy update")
        self.mCam = cam
        self.mBounding_rect = pygame.Rect(int(self.mPos[0] - self.mCam[0]) + self.mEnemy_info["hitbox_xoffset"],
                                          int(self.mPos[1] - self.mCam[1]), self.mEnemy_info["width"],
                                          self.mEnemy_info["height"])
        buffer = 7
        # print(str(self.mPos[0]))
        x = [p_pos[0]-self.mPos[0], p_pos[1]-self.mPos[1]]
        for i in range(len(x)):
            self.mDist = self.mDist + (x[i]) ** 2   # finding length
        self.mDist = self.mDist ** (1/2)
        # print(self.mDist)
        # setting direction bassed on point of interest
        if bool_for_not_moving:
            if int(self.mDist) <= self.mRad:
                self.mPoi = p_pos
                if self.mPoi[0] < self.mPos[0] - buffer:  # left
                    self.mPos[0] -= self.mSpeed * dt
                    self.mDirection = "left"
                if self.mPoi[0] > self.mPos[0] - buffer:  # right
                    self.mPos[0] += self.mSpeed * dt
                    self.mDirection = "right"
                if self.mPoi[1] < self.mPos[1] - buffer:  # up
                    self.mPos[1] -= self.mSpeed * dt
                    # self.mDirection = "up"
                if self.mPoi[1] > self.mPos[1] - buffer:  # down
                    self.mPos[1] += self.mSpeed * dt
                    # self.mDirection = "down"
            else:
                self.mDirection = None
                # timer using direction for the frames so that the timer doesnt effect the enemy speed
            self.mFrame_timer -= dt
            if self.mFrame_timer < 0:
                if self.mDirection == "left":
                    self.mColumn = (self.mColumn + 1) % self.mNum_columns
                    self.mRow = self.mDirections["left"]
                if self.mDirection == "right":
                    self.mColumn = (self.mColumn + 1) % self.mNum_columns
                    self.mRow = self.mDirections["right"]
                if self.mDirection == "up":
                    self.mColumn = (self.mColumn + 1) % self.mNum_columns
                    self.mRow = self.mDirections["up"]
                if self.mDirection == "down":
                    self.mColumn = (self.mColumn + 1) % self.mNum_columns
                    self.mRow = self.mDirections["down"]
                self.mFrame_timer = .2
            if self.mHealth <= 0:
                self.mRad = 0
                self.mColumn = self.mDirections["death_colum"]
                self.mRow = self.mDirections["death_row"]

    def draw(self, win):
        # print(self.mColumn)
        rect = (self.mColumn * self.mFrame_w, self.mRow * self.mFrame_h, self.mEnemy_info["frame_w"], self.mEnemy_info["frame_h"])
        win.blit(self.mSprite, (int(self.mPos[0] - self.mCam[0]), int(self.mPos[1] - self.mCam[1])), rect)
        # pygame.draw.rect(win, (255, 255, 255), (int(self.mPos[0] - self.mCam[0]) + self.mEnemy_info["hitbox_xoffset"],
        #                                         int(self.mPos[1] - self.mCam[1]), self.mEnemy_info["width"],
        #                                         self.mEnemy_info["height"]), 1)

########################################################################################################################


class Boss:
    def __init__(self, cam, pos, player, img=None):
        self.img = img
        self.confetti = CONFETTI
        self.camera = cam
        self.mPos = Vector(pos[0], pos[1])
        self.speed = minotaur_info["speed"]
        self.damage = 10
        self.max_heatlth = 30
        self.mHealth = 30

        # other lolz
        self.frame_timer = .1
        self.bounding_rect = 0

        # timer/mode stuff
        self.x = 0
        self.px = 0
        self.ex = 0
        self.charge_timer = 1
        self.attack = "rest"
        self.vulnerable = "False"

        # movement stuff
        self.row = 0
        self.column = 0
        self.movement = Vector(0,0)
        self.velocity = Vector(0,0)
        self.p_pos = Vector(0,0)
        self.mFrame_w = minotaur_info["width"]
        self.mFrame_h = minotaur_info["height"]

        # health stuff
        self.hp_gradient_img = pygame.image.load("MapAssets/CombatBackgrounds/hp_gradient.png")
        self.player = player
        self.health_timer = 1
        self.player_hurt = False
        self.enemy_hurt = False

        # confetti stuff
        self.con_midx = 0
        self.conx = -120
        self.cony = 0
        self.amp = 12
        self.fall_speed = 100

    def Update(self, dt, combat_dt, player, cam, bounds):
        self.camera = cam
        self.p_pos = Vector(player.mPoss[0], player.mPoss[1])
        old_pos = self.mPos.copy()

        self.mBounding_rect = pygame.Rect(self.mPos.x - self.camera[0], self.mPos.y - self.camera[1], minotaur_info["width"], minotaur_info["height"])    #will need to be replaced by real values

        self.x += dt
        if self.x > self.charge_timer:
            if self.attack == "rest":
                self.attack = "charge"
                self.x = 0
            else:
                self.attack = "rest"
                self.x = 0

        # after the timer goes off the vector will be used to charge toward the plater
        self.distance_vect = Vector(self.p_pos.x - self.mPos.x, self.p_pos.y - self.mPos.y)

        # freezes the boss when dead
        if self.mHealth > 0:
            if self.attack == "charge":
                self.movement += (self.speed * self.distance_vect.normalize)
                self.velocity += self.movement
                self.mPos += self.velocity * dt
                self.column = (self.column + 1) % 3
                self.movement = Vector(0, 0)
                self.velocity = Vector(0, 0)
                self.vulnerable = "False"

        if self.attack == "rest":
            self.velocity += self.movement  # Vector(0,0)
            self.mPos += self.velocity * dt
            self.movement = Vector(0, 0)
            self.vulnerable = "True"

        # player and boss collision
        if self.mBounding_rect.colliderect(player.Bounding_rect):
            if self.vulnerable == "True" and self.enemy_hurt is False:
                # knight rampage stuff
                if isinstance(self.player, parent_player.Knight):
                    if self.player.rage_mode is True:
                        self.mHealth -= 15
                        pygame.mixer.Sound("SoundEffects/BossHit.wav").play()
                    else:
                        self.mHealth -= 10
                        pygame.mixer.Sound("SoundEffects/BossHit.wav").play()
                else:
                    self.mHealth -= 10
                    pygame.mixer.Sound("SoundEffects/BossHit.wav").play()

                # movement for if the boss is vulnerable
                self.movement += (self.speed * -self.distance_vect.normalize)
                self.movement += Vector(0, 0)
                self.enemy_hurt = True

            if self.vulnerable == "False" and self.player_hurt is False:
                # print("player takes damage")
                self.player.mHealth -= self.damage
                self.player_hurt = True

        if self.player_hurt is True:
            self.px += dt
            if self.px >= self.health_timer:
                # print("timer has gone off")
                self.player_hurt = False
                self.px = 0
        if self.enemy_hurt is True:
            self.ex += dt
            if self.ex >= self.health_timer:
                # print("timer has gone off")
                self.enemy_hurt = False
                self.ex = 0

        # boundries for the boss
        next_pos = pygame.Rect(self.mPos.x, self.mPos.y, minotaur_info["width"], minotaur_info["height"]) # will need to be replaced by real values
        for b in bounds:
            b = pygame.Rect(b)
            if next_pos.colliderect(b):
                self.mPos = old_pos

        if self.mHealth > 0:
            # frame change stuff
            if -(2 **(1/2) / 2)< self.distance_vect.normalize.x < (2 **(1/2) / 2):    # up
                if self.distance_vect.normalize.y < 0:
                    self.row = 0  # minotaur_info["up"]
            if -(2 ** (1 / 2) / 2) < self.distance_vect.normalize.x < (2 ** (1 / 2) / 2):  # down
                if self.distance_vect.normalize.y > 0:
                        self.row = 2  # minotaur_info["down"]
            if -(2 ** (1 / 2) / 2) < self.distance_vect.normalize.y < (2 ** (1 / 2) / 2):  # left
                if self.distance_vect.normalize.x < 0:
                    self.row = 3  # minotaur_info["left"]
            if -(2 ** (1 / 2) / 2) < self.distance_vect.normalize.y < (2 ** (1 / 2) / 2):  # right
                if self.distance_vect.normalize.x > 0:
                    self.row = 1  # minotaur_info["right"]

    ####################################################################################################################
        # updates the confetti#
        ######################
        if self.mHealth <= 0:
            self.cony += self.fall_speed * dt
            self.conx = self.amp * (math.sin(self.cony * .1)) + self.con_midx

    def Draw(self, surf):
        # pygame.draw.rect(surf, (255, 0, 0), (self.mPos.x - self.camera[0], self.mPos.y - self.camera[1],
        #                                      minotaur_info["width"], minotaur_info["height"]), 1)
        rect = (minotaur_info["width"] * self.column, minotaur_info["height"] * self.row, minotaur_info["width"],
                minotaur_info["height"])
        surf.blit(self.img, (int(self.mPos.x - self.camera[0]), int(self.mPos.y - self.camera[1])), rect)

        # health bar stuff
        player_pcent = self.player.mHealth / self.player.mMax_health
        if player_pcent < 0:
            player_pcent = 0
        player_color = self.hp_gradient_img.get_at((int((self.hp_gradient_img.get_width() - 1) * player_pcent), 0))
        width = 100 * player_pcent
        pygame.draw.rect(surf, player_color, (self.player.mPoss[0] - 10 - self.camera[0],
                                              self.player.mPoss[1] - 40 - self.camera[1], width, 12))

        # boss health bar stuff
        boss_pcent = self.mHealth / self.max_heatlth
        if boss_pcent < 0:
            boss_pcent = 0
        boss_color = self.hp_gradient_img.get_at((int((self.hp_gradient_img.get_width() - 1) * boss_pcent), 0))
        width = 100 * boss_pcent
        pygame.draw.rect(surf, boss_color, (self.mPos.x - 10 - self.camera[0], self.mPos.y - 40 - self.camera[1], width,
                                            12))

        # confetti
        if self.mHealth <= 0:
            surf.blit(CONFETTI, (self.conx, self.cony))



