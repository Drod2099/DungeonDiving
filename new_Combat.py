from start_screen import *
from parent_enemy import *


class BattleScreen:

    win_width = 800
    win_height = 600
    surf = pygame.display.set_mode((win_width, win_height))

    def __init__(self, enemy_type, player_type, player, enemy, font, cur_lvl, sub_lvl):
        """Creates a BattleScreen object"""
        self.fight_screen = Fight_screen(cur_lvl, sub_lvl)
        self.inventory = Inventory()
        self.open_inv = False
        self.button = None

        if enemy_type is not None:
            if enemy_type == "goblin":
                self.mEnemy_type = GOBLIN
            elif enemy_type == "zombie":
                self.mEnemy_type = ZOMBIE

        if player_type == "knight":
            self.mPlayer_type = KNIGHT
        if player_type == "wizard":
            self.mPlayer_type = WIZARD
        if player_type == "rogue":
            self.mPlayer_type = ROGUE
        self.player = player
        self.enemy = enemy
        self.font = font
        self.damage = 0

        self.player_miss = False
        self.enemy_miss = False
        self.player_hit = False
        self.enemy_hit = False
        self.mWinner = None
        self.mTaking_damage = False
        self.mTimer = 0.5
        self.enemy_dt = 0

        self.turn = ""
        self.what_happened = ""

        self.hp_gradient_img = pygame.image.load("MapAssets/CombatBackgrounds/hp_gradient.png")

        # dice rolls for combat
        # roll for initiative
        self.player_init = 0
        self.enemy_init = 0
        self.damage_die = 0
        self.strength_mod = self.player.mStrength // 5
        self.stealth_mod = self.player.mStealth // 5
        self.player_block = 0
        self.player_accuracy = 0
        self.enemy_accuracy = 0
        self.player_attack = 0
        self.enemy_attack = 0
        self.enemy_block = 0
        self.enemyX_OFFSET = 0
        self.playerX_OFFSET = 0
        self.mTimer = 1

        self.end_of_turn_txt1 = str(self.player.mHealth) + " player health"
        self.end_of_turn_txt2 = str(self.enemy.mHealth) + " enemy health"

    def initiative(self):
        self.player_init = random.randint(1, 20)
        self.enemy_init = random.randint(1, 20)

        while self.player_init == self.enemy_init:
            self.player_init = random.randint(1, 20)
            self.enemy_init = random.randint(1, 20)

        if self.player_init > self.enemy_init:
            self.turn = "player"
            print("Player turn")
        elif self.player_init < self.enemy_init:
            self.turn = "enemy"
            print("Enemy turn")

    def combat_update(self, mpos, dt, potions, in_battle):
        self.mWinner = self.check_for_winner()

        self.player_attack = 0
        self.enemy_attack = 0

        if not self.open_inv:
            self.button = self.fight_screen.check_pos(mpos)
        elif self.open_inv:
            self.inventory.update(dt, len(potions[1]), len(potions[0]), len(potions[2]))

        self.fight_screen.update(dt, len(potions[1]), len(potions[0]), len(potions[2]))

        # DEALS WITH THE PLAYER/ENEMY JIGGLE WHEN HIT
        if self.mTaking_damage:
            self.mTimer -= dt
        if self.mTimer < 0:
            self.mTimer = 0.5
            self.mTaking_damage = False
            self.enemy_hit = False
            self.player_hit = False
            self.mPlayer_type.set_alpha(255)
            self.mEnemy_type.set_alpha(255)
            print("hello world")
        if self.enemy_hit:
            self.enemyX_OFFSET = random.randint(-3, 3)
            self.mEnemy_type.set_alpha(100)
        elif self.player_hit:
            self.playerX_OFFSET = random.randint(-3, 3)
            self.mPlayer_type.set_alpha(100)

        if in_battle:
            if self.turn == "enemy":
                self.enemy_dt += dt
                print(self.enemy_dt)
                if self.enemy_dt >= 1:
                    enemy_rand = random.randint(0, 20)
                    if enemy_rand <= 15:
                        self.fight()
                        self.turn = "player"
                        print("Player turn")
                        self.enemy_dt = 0
                    elif 15 < enemy_rand <= 20:
                        self.block()
                        self.turn = "player"
                        print("Player turn")
                        self.enemy_dt = 0

        if self.mWinner is not None:
            if self.mWinner == "enemy":
                self.mPlayer_type.set_alpha(255)
                return False, True
                # replace with game over screen?
            else:
                self.mEnemy_type.set_alpha(255)
                return False, False
        return True, False

    def combat_input(self, evt, keys, potions):
        m_pos = pygame.mouse.get_pos()
        if not self.mTaking_damage:
            battle = True
            flee = False
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if self.turn == "player":
                    if evt.button == 1:
                        if self.button == "attack":
                            self.fight()
                            self.turn = "enemy"
                            print("Enemy turn")
                            print("clicked on fight")
                        elif self.button == "flee":
                            battle, flee = self.flee()
                            self.turn = "enemy"
                            print("Enemy turn")
                        elif self.button == "block":
                            self.block()
                            print("block")
                            self.turn = "enemy"
                            print("Enemy turn")
                        elif self.button == "inventory":
                            self.fight_screen.open_inv = True
                            self.open_inventory = True
                        elif self.button == "health":
                            self.heal(potions)
                            self.open_inventory = False
                        elif self.button == "sheild":
                            self.defense(potions)
                            self.open_inventory = False
                        elif self.button == "special":
                            self.special(potions)
                            self.open_inventory = False
                        elif self.button == "back":
                            self.open_inventory = False
                            self.fight_screen.open_inv = False

            if evt.type == pygame.KEYDOWN:
                if self.turn == "player":
                    if evt.key == pygame.K_h:
                        self.heal(potions)
                    if evt.key == pygame.K_d:
                        self.defense(potions)
                    if evt.key == pygame.K_b:
                        self.block()
                    if evt.key == pygame.K_SPACE:
                        self.fight()
                        self.turn = "enemy"
                        print("Enemy turn")
                    elif evt.key == pygame.K_b:
                        self.block()
                        self.turn = "enemy"
                        print("Enemy turn")
                    elif evt.key == pygame.K_r:
                        battle, flee = self.flee()
                        self.turn = "enemy"
                        print("Enemy turn")
            return battle, flee
        return True, False

    def heal(self, potions):
        if len(potions[0]) >= 1:
            print("drink")
            pygame.mixer.Sound("SoundEffects/PotionDrink.wav").play()
            if self.player.mHealth + 10 > self.player.mMax_health:
                self.player.mHealth = self.player.mMax_health
            else:
                self.player.mHealth += 10
            print(self.player.mHealth)
            del potions[0][-1]
        else:
            print("There are no potions in your inventory")

    def defense(self, potions):
        if len(potions[1]) >= 1:
            print("drink")
            pygame.mixer.Sound("SoundEffects/PotionDrink.wav").play()
            self.player.armor_class += 10
            print(self.player.armor_class)
            del potions[1][-1]
        else:
            print("There are no potions in your inventory")

    def special(self, potions):
        if len(potions[-1]) > 0:
            print("special potion drank")
            pygame.mixer.Sound("SoundEffects/PotionDrink.wav").play()
            self.player.special = True
            del potions[-1][-1]
        else:
            print("there are no special potions in your inventory")

    def fight(self):
        self.damage = 0
        if self.turn == "player":
            self.player_accuracy = random.randint(1, 20)
            if self.player_accuracy >= self.enemy.armor_class:
                if self.player.mSprite == KNIGHT:
                    self.player_attack = random.randint(1, 8) + self.strength_mod - self.enemy_block
                elif self.player.mSprite == WIZARD:
                    self.player_attack = random.randint(1, 6) + self.strength_mod - self.enemy_block
                elif self.player.mSprite == ROGUE:
                    self.player_attack = random.randint(1, 4) + self.strength_mod - self.enemy_block
                self.damage = self.player_attack
                if self.player_attack > 0:
                    self.enemy.mHealth -= self.player_attack
                    self.enemy_hit = True
                    self.mTaking_damage = True
                    pygame.mixer.Sound("SoundEffects/swordclashsoundeffect.wav").play()
                    if self.enemy.mHealth < 0:
                        self.enemy.mHealth = 0
                    self.enemy_block = 0
                    self.player_hit_txt = "PLAYER HIT FOR " + str(self.player_attack) + " POINTS OF DAMAGE"
                    self.what_happened = "player hit"
                elif self.player_attack <= 0:
                    self.enemy.mHealth -= self.player_attack
                    self.player_attack = 0
                    if self.enemy.mHealth < 0:
                        self.enemy.mHealth = 0
                    self.enemy_block = 0
                    self.player_blocked_txt = "PLAYER HIT, BUT IT WAS BLOCKED"
                    self.what_happened = "player hit blocked"
            else:
                self.player_missed_txt = "PLAYER MISSED"
                self.what_happened = "player miss"
        if self.turn == "enemy":
            self.enemy_accuracy = random.randint(1, 20)
            if self.enemy_accuracy >= self.player.armor_class:
                if self.enemy.mSprite == ZOMBIE:
                    self.enemy_attack = random.randint(1, self.enemy.mDamage) - self.player_block
                elif self.enemy.mSprite == GOBLIN:
                    self.enemy_attack = random.randint(1, self.enemy.mDamage) - self.player_block
                self.damage = self.enemy_attack
                if self.enemy_attack > 0:
                    self.player.mHealth -= self.enemy_attack
                    self.player_hit = True
                    self.mTaking_damage = True
                    pygame.mixer.Sound("SoundEffects/swordclashsoundeffect.wav").play()
                    if self.player.mHealth < 0:
                        self.player.mHealth = 0
                    self.player_block = 0
                    self.enemy_hit_txt = "ENEMY HIT FOR " + str(self.enemy_attack) + " POINTS OF DAMAGE"
                    self.what_happened = "enemy hit"
                elif self.enemy_attack <= 0:
                    self.player.mHealth -= self.enemy_attack
                    self.enemy_attack = 0
                    if self.player.mHealth < 0:
                        self.player.mHealth = 0
                    self.player_block = 0
                    self.enemy_hit_blocked_txt = "ENEMY HIT, BUT IT WAS BLOCKED"
                    self.what_happened = "enemy hit blocked"
            else:
                self.enemy_missed_txt = "ENEMY MISSED"
                self.what_happened = "enemy miss"

        self.end_of_turn_txt1 = str(self.player.mHealth) + " player health"
        self.end_of_turn_txt2 = str(self.enemy.mHealth) + " enemy health"

    def block(self):
        if self.turn == "player":
            if self.player.mSprite == KNIGHT:
                self.player_block = random.randint(1, 8)
            elif self.player.mSprite == WIZARD:
                self.player_block = random.randint(1, 6)
            elif self.player.mSprite == ROGUE:
                self.player_block = random.randint(1, 4)
            self.player_block_txt = "YOU BLOCKED FOR " + str(self.player_block) + " POINTS OF DAMAGE"
            self.what_happened = "player blocked"

        elif self.turn == "enemy":
            if self.enemy.mSprite == ZOMBIE:
                self.enemy_block = random.randint(1, 2)
            elif self.enemy.mSprite == GOBLIN:
                self.enemy_block = random.randint(1, 4)
            self.enemy_block_txt = "THE ENEMY BLOCKED FOR " + str(self.enemy_block) + " POINTS OF DAMAGE"
            self.what_happened = "enemy blocked"

        self.end_of_turn_txt1 = str(self.player.mHealth) + " player health"
        self.end_of_turn_txt2 = str(self.enemy.mHealth) + " enemy health"

    def flee(self):
        chance = random.randint(1, 20)
        if self.turn == "player":
            if chance >= 20 - self.stealth_mod:
                self.good_flee_txt = "YOU HAVE SUCCESSFULLY FLED FROM BATTLE."
                self.what_happened = "player flee"
                flee = True
                battle = False
            else:
                self.bad_flee_txt = "YOU FAILED TO FLEE FROM BATTLE."
                self.what_happened = "player no flee"
                flee = False
                battle = True

        self.end_of_turn_txt1 = str(self.player.mHealth) + " player health"
        self.end_of_turn_txt2 = str(self.enemy.mHealth) + " enemy health"

        return battle, flee

    def check_for_winner(self):
        """
        method ran every frame in input to check healths
        :return: returns the name of the winner or None of the battle is still in progress
        """
        if self.player.mHealth <= 0:
            pygame.mixer.Sound("SoundEffect/Death.wav").play()
            return "enemy"
        elif self.enemy.mHealth <= 0:
            pygame.mixer.Sound("SoundEffects/Death.wav").play()
            return "player"
        return None

    def draw(self, surf):
        BattleScreen.surf.fill((0, 0, 0))
        self.fight_screen.draw(surf)
        # check isinstance and customize each blit for the player type
        if self.player.mSprite == KNIGHT:
            BattleScreen.surf.blit(self.player.mSprite, (BattleScreen.win_width * (1 / 6) + 40 + self.playerX_OFFSET,
                                                         BattleScreen.win_height * (1 / 2) - 40), (329, 0, 65, 65))
        elif self.player.mSprite == WIZARD:
            BattleScreen.surf.blit(self.player.mSprite, (BattleScreen.win_width * (1 / 6) + 45 + self.playerX_OFFSET,
                                                         BattleScreen.win_height * (1 / 2) - 30), (160, 55, 50, 57))
        elif self.player.mSprite == ROGUE:
            BattleScreen.surf.blit(self.player.mSprite, (BattleScreen.win_width * (1 / 6) + 50 + self.playerX_OFFSET,
                                                         BattleScreen.win_height * (1 / 2) - 20), (0, 144, 32, 65))

        if self.enemy.mSprite == GOBLIN:
            BattleScreen.surf.blit(self.enemy.mSprite, (BattleScreen.win_width * (2 / 3) + 40 + self.enemyX_OFFSET,
                                                        BattleScreen.win_height * (1 / 6) + 20), (403, 0, 65, 50))
        elif self.enemy.mSprite == ZOMBIE:
            BattleScreen.surf.blit(self.enemy.mSprite, (BattleScreen.win_width * (2 / 3) + 70 + self.enemyX_OFFSET,
                                                        BattleScreen.win_height * (1 / 6) + 25), (40, 10, 26, 35))

        # Player health bar
        player_pcent = self.player.mHealth / self.player.mMax_health
        player_color = self.hp_gradient_img.get_at((int((self.hp_gradient_img.get_width() - 1) * player_pcent), 0))
        pwidth = 229 * player_pcent
        pygame.draw.rect(BattleScreen.surf, player_color, (549, 449, pwidth, 12))

        # Enemy health bar
        enemy_pcent = self.enemy.mHealth / self.enemy.mMax_health
        enemy_color = self.hp_gradient_img.get_at((int((self.hp_gradient_img.get_width() - 1) * enemy_pcent), 0))
        ewidth = 229 * enemy_pcent
        pygame.draw.rect(BattleScreen.surf, enemy_color, (549, 481, ewidth, 12))

        # Roll
        textFont = pygame.font.SysFont("Bahnschrift", 48)
        dirFont = pygame.font.SysFont("Bahnschrift", 20)
        if self.turn == "player":
            BattleScreen.surf.blit(textFont.render(str(self.enemy_accuracy), True, (255, 255, 255)), (549, 510))
            BattleScreen.surf.blit(textFont.render(str(self.damage), True, (255, 255, 255)), (730, 510))
        elif self.turn == "enemy":
            BattleScreen.surf.blit(textFont.render(str(self.player_accuracy), True, (255, 255, 255)), (549, 510))
            BattleScreen.surf.blit(textFont.render(str(self.damage), True, (255, 255, 255)), (730, 510))

        # Directions Box
        BattleScreen.surf.blit(dirFont.render("Attack = SpaceBar", True, (255, 255, 255)), (440, 290))
        BattleScreen.surf.blit(dirFont.render("Block = B", True, (255, 255, 255)), (440, 315))
        BattleScreen.surf.blit(dirFont.render("Flee = R", True, (255, 255, 255)), (440, 340))
        BattleScreen.surf.blit(dirFont.render("To play enemy turn, press Space Bar", True, (255, 255, 255)), (440, 365))

        # Text Box
        textBoxFont = pygame.font.SysFont("Bahnschrift", 20)
        pygame.draw.rect(surf, (255, 255, 255), (10, 10, 440, 130))
        pygame.draw.rect(surf, (0, 0, 0), (8, 8, 443, 133), 3)
        if self.turn == "player":
            BattleScreen.surf.blit(textBoxFont.render("Player Turn", True, (0, 0, 0)), (12, 12))
        elif self.turn == "enemy":
            BattleScreen.surf.blit(textBoxFont.render("Enemy Turn", True, (0, 0, 0)), (12, 12))

        if self.what_happened == "player hit":
            BattleScreen.surf.blit(textBoxFont.render(self.player_hit_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "player miss":
            BattleScreen.surf.blit(textBoxFont.render(self.player_missed_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "enemy hit":
            BattleScreen.surf.blit(textBoxFont.render(self.enemy_hit_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "enemy hit blocked":
            BattleScreen.surf.blit(textBoxFont.render(self.enemy_hit_blocked_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "player hit blocked":
            BattleScreen.surf.blit(textBoxFont.render(self.player_blocked_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "enemy miss":
            BattleScreen.surf.blit(textBoxFont.render(self.enemy_missed_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "player blocked":
            BattleScreen.surf.blit(textBoxFont.render(self.player_block_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "enemy blocked":
            BattleScreen.surf.blit(textBoxFont.render(self.enemy_block_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "player flee":
            BattleScreen.surf.blit(textBoxFont.render(self.good_flee_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "player no flee":
            BattleScreen.surf.blit(textBoxFont.render(self.bad_flee_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "enemy flee":
            BattleScreen.surf.blit(textBoxFont.render(self.enemy_good_flee_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))
        elif self.what_happened == "enemy no flee":
            BattleScreen.surf.blit(textBoxFont.render(self.enemy_bad_flee_txt, True, (0, 0, 0)), (12, 45))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt1), True, (0, 0, 0)), (12, 78))
            BattleScreen.surf.blit(textBoxFont.render(str(self.end_of_turn_txt2), True, (0, 0, 0)), (12, 101))

        if self.open_inv:
            self.inventory.draw(win)
