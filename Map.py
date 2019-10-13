from new_Combat import *
from transition_screen import *
from chest import *
from lvl_warp_screen import *
from parent_enemy import *
from parent_player import *
from config import *
from File_Parsing import *
from start_screen import *


class Map:

    def __init__(self, character):

        self.mCamera = [0, 0]

        self.enemy_list = []

        # potion STUFF
        self.chests = []  # list of chest objects
        self.acquired_potions = [[1], [1], [1,1]]
        self.take_items = False   # bool that shows true if you are colliding with the chest and able to take its items
        self.selected_chest = None  # keeps track of the last chest you collided with so it deletes the right one
        self.inventory = False
        self.mInventory_inst = Inventory()

        self.mNext = False
        self.mCur_lvl = 1
        self.mSub_lvl = random.randint(1, 3)
        self.mLvl_sets = [(self.mCur_lvl, self.mSub_lvl)]
        self.mLvl_info = self.get_lvl_info(self.mCur_lvl, self.mSub_lvl)
        self.mLvlwarp = self.mLvl_info["lvl_warp_rect"]
        self.create_enemys(self.mLvl_info["enemy_spawn_locations"])

        self.mPlayer_type = character

        if character == "knight":              # If selected character is a knight then the knight object is created
            self.mPlayer = Knight(self.mCamera, self.mLvl_info["player_spawn_location"], KNIGHT, self.mLvlwarp)
            self.mDirections = knight_directions
        elif character == "wizard":
            self.mPlayer = Wizard(self.mCamera, self.mLvl_info["player_spawn_location"], WIZARD, self.mLvlwarp)
            self.mDirections = wizard_directions
        else:
            self.mPlayer = Rogue(self.mCamera, self.mLvl_info["player_spawn_location"], ROGUE, self.mLvl_info)
            self.mDirections = rogue_directions

        self.mLoad_screen = Loading()
        self.mLoading = True
        self.mWarp_screen = False
        self.mWarp = Lvl_warp()
        self.mSpawn_point = self.mLvl_info["player_spawn_location"]

        self.mSection = None
        self.mBounds = []

        data = map_data(self.mCur_lvl, self.mSub_lvl)  # map data is a method elsewhere that returns a tuple of map data
        self.mHeader_data = data[0]
        self.mMap_layers = data[1]
        self.mTileset_img = data[2]
        self.mNum_tiles_wide = data[3]

        if isinstance(self.mLvl_info["bounds_tilecodes"], int):
            self.load_boundries(self.mLvl_info["bounds_tilecodes"])
        else:
            self.load_boundries(*self.mLvl_info["bounds_tilecodes"])

        # loading in the chests?
        if isinstance(self.mLvl_info["chest_tilecode"], int):
            self.find_chests(self.mLvl_info["chest_tilecode"])

        # combat attributes
        self.in_battle = False
        self.mode = "init start"
        self.has_enemies = True
        self.font = pygame.font.SysFont("Times New Roman", 24)          # can probably be moved to config ?
        self.selected_enemy = None
        self.in_battle = None
        self.mCreate_battle = False
        self.flee = False
        self.counter = 0
        self.mPlayer_dead = False
        self.mPlayer_won = False
        self.lvl2warp = False
        self.lvl3warp = False

        # special attribure
        self.attack_avalible = False
        self.special_enemy = None

        self.x = 0
        self.confetti_timer = 5

    def get_lvl_info(self, cur_lvl, cur_sub_lvl):
        if cur_lvl == 1:
            if cur_sub_lvl == 1:
                return deepcopy(lvl1_1_info)
            elif cur_sub_lvl == 2:
                return deepcopy(lvl2_1_info)
            else:
                return deepcopy(lvl3_1_info)
        elif cur_lvl == 2:
            if cur_sub_lvl == 1:
                return deepcopy(lvl1_2_info)
            elif cur_sub_lvl == 2:
                return deepcopy(lvl2_2_info)
            else:
                return deepcopy(lvl3_2_info)
        elif cur_lvl == 3:
            if cur_sub_lvl == 1:
                return deepcopy(lvl1_3_info)
            elif cur_sub_lvl == 2:
                return deepcopy(lvl2_3_info)
            else:
                return deepcopy(lvl3_3_info)

    def use_potion(self, potions, potion_type):
        if potion_type == "health":
            if len(potions[0]) >= 1:
                print("drink")
                if self.mPlayer.mHealth + 10 > self.mPlayer.mMax_health:
                    self.mPlayer.mHealth = self.mPlayer.mMax_health
                else:
                    self.mPlayer.mHealth += 10
                print(self.mPlayer.mHealth)
                del potions[0][-1]
            else:
                print("There are no health potions in your inventory")
        elif potion_type == "sheild":
            if len(potions[1]) >= 1:
                print("drink")
                self.mPlayer.armor_class += 2
                print(self.mPlayer.armor_class)
                del potions[1][-1]
            else:
                print("There are no defense potions in your inventory")
        elif potion_type == "special":
            if len(potions[-1]) >= 1:
                print("drink")
                self.mPlayer.special = True
                del potions[-1][-1]
            else:
                print("There are no special potions in your inventory")

    def create_enemys(self, position_list):
        cur_set_of_enemys = []
        num_of_enemies = len(position_list)
        for i in range(num_of_enemies):
            num = random.randint(0, 1)
            if num == 0:
                enemy = Parent_enemy(GOBLIN, self.mCamera, position_list[i])
                cur_set_of_enemys.append(enemy)
            elif num == 1:
                enemy = Parent_enemy(ZOMBIE, self.mCamera, position_list[i])
                cur_set_of_enemys.append(enemy)
        self.enemy_list.append(cur_set_of_enemys)

    def load_boundries(self, *args):
        # print(args, "bound codes given")
        bound_codes = []
        if isinstance(args, list):
            for i in args:
                for code in i:
                    bound_codes.append(code)
        else:
            for i in args:
                bound_codes.append(i)
        # print(bound_codes)
        for layer in self.mMap_layers:
            y = 0
            for row in layer:
                x = 0
                for code in row:
                    for block in bound_codes:
                        if block == code:
                            block = [x, y, self.mHeader_data["tilewidth"], self.mHeader_data["tileheight"]]
                            self.mBounds.append(block)

                    x += self.mHeader_data["tilewidth"]
                y += self.mHeader_data["tileheight"]

    def find_chests(self, chest_block):
        # print(args, "bound codes given")
        bound_codes = chest_block
        # print(bound_codes)
        for layer in self.mMap_layers:
            y = 0
            for row in layer:
                x = 0
                for code in row:
                    # print(code)
                    # print(row)

                    if code == bound_codes:
                        chest = Chest([x, y])  # [x, y, self.mHeader_data["tilewidth"], self.mHeader_data["tileheight"]]
                        self.chests.append(chest)

                    x += self.mHeader_data["tilewidth"]
                y += self.mHeader_data["tileheight"]

    def update(self, dt, combat_dt):
        self.mCamera = self.mPlayer.mCam
        self.dt = dt
        if len(self.acquired_potions[-1]) == 0:
            self.attack_avalible = False

        mpos = pygame.mouse.get_pos()
        if not self.in_battle:
            if self.mWarp_screen:
                self.mWarp.update(dt)

        # PAUSES THE GAME COMPLETELY WHILE IN COMBAT AND IN THE INVENTORY
        if self.in_battle is True or self.inventory is True:
            if self.mLoading:
                self.mLoading = self.mLoad_screen.update(dt)
            self.dt = 0.0

        # UPDATES THE ENEMIES
        mpos_rect = pygame.Rect(mpos[0], mpos[1], 1, 1)
        if self.mCur_lvl != 3:
            cur_lvl_enemies = self.enemy_list[self.mCur_lvl-1]
            for e in cur_lvl_enemies:
                if isinstance(self.mPlayer, Rogue):
                    if not self.mPlayer.special_ability:            # WHAT HAPPENS WHEN THE ROGUE ISNT USING HIS ABILITY
                        e.update(self.dt, combat_dt, self.mPlayer.mPoss, self.mCamera, True)
                        # checks to see if cursor is over any enemies
                        if e.mBounding_rect[0] < mpos[0] < e.mBounding_rect[2] and e.mBounding_rect[1] < mpos[1] < e.mBounding_rect[3]:
                            self.special_enemy = e
                        else:
                            self.special_enemy = None
                        # refine this
                    else:
                        e.update(self.dt, combat_dt, self.mPlayer.mPoss, self.mCamera, False)
                        if e.mBounding_rect[0] < mpos[0] < e.mBounding_rect[2] and e.mBounding_rect[1] < mpos[1] < e.mBounding_rect[3]:
                            self.special_enemy = e
                        else:
                            print("no special enemy")
                            self.special_enemy = None
                else:                                   # WHAT HAPPENS IF THE ROGUE ISN'T SELECTED
                    e.update(self.dt, combat_dt, self.mPlayer.mPoss, self.mCamera, True)
                    # checks to see if cursor is over any enemies
                    if e.mBounding_rect.colliderect(mpos_rect):
                        self.special_enemy = e

            # PLAYER UPDATE
            self.mPlayer.update(self.dt, self.special_enemy, self.mBounds, self.mDirections["frames_wide"],
                                self.mDirections)

        else:
            # print("update")
            self.boss.Update(self.dt, combat_dt, self.mPlayer, self.mCamera, self.mBounds)
            if self.boss.mHealth <= 0:
                self.x += dt
                if self.x > self.confetti_timer:
                    self.mPlayer_won = True
            self.special_enemy = self.boss
            self.mPlayer.update(self.dt, self.special_enemy, self.mBounds, self.mDirections["frames_wide"],
                                self.mDirections)

        # UPDATES LEVEL JUMPING STUFF
        if self.mNext:                      # when end lvl rect is reached reset and update needed variables
            self.warp()

        self.take_items = False
        self.selected_chest = None
        if len(self.chests) > 0:
            for c in self.chests:
                c.update(self.mCamera)
                if c.Bounding_rect.colliderect(self.mPlayer.Bounding_rect):
                    self.take_items = True
                    self.selected_chest = c
                    # making the text box stuff for chest contents
                    # self.chest_window = pygame.Surface((200,300))
                    self.info_health = "Health Potions: " + str(self.selected_chest.health_potions)
                    self.info_def = "Defense Potions: " + str(self.selected_chest.def_potions)
                    self.info_spec = "Special Potions: " + str(self.selected_chest.special_potion)
                    self.chest_text = (self.info_health, self.info_def, self.info_spec)

        if self.inventory:
            self.mInventory_inst.update(self.dt, len(self.acquired_potions[1]), len(self.acquired_potions[0]),
                                        len(self.acquired_potions[2]))

    ### COMBAT ###

        # CHECKING FOR COLLISION
        if self.mCur_lvl != 3:
            enemy_type = None
            if self.has_enemies and self.flee is False:
                for e in cur_lvl_enemies:
                    if not self.in_battle and e.mBounding_rect.colliderect(self.mPlayer.Bounding_rect):
                        self.selected_enemy = e     # makes one enemy to focus on for battle sequence
                        #############################################
                        if isinstance(self.mPlayer, Knight):        #
                            if self.mPlayer.rage_mode is True:      # this section is for the rage mode for the knight class
                                self.selected_enemy.mHealth = 0     #
                        #############################################
                        if self.selected_enemy.mHealth <= 0:
                            self.in_battle = False
                        else:
                            self.in_battle = True
                            self.mCreate_battle = True
                            self.mLoading = True
                            self.mLoad_screen.mWidth = 1
                            if e.mSprite == GOBLIN:
                                enemy_type = "goblin"
                            elif e.mSprite == ZOMBIE:
                                enemy_type = "zombie"
            # print(self.selected_enemy)

                # RETURN IN BATTLE TO MAIN AND IF IN BATTLE IN MAIN IS TRUE THEN RUN THE BATTLE METHOD IN MAP

            if self.mCreate_battle:
                battlescreen_num = 1
                self.battle = BattleScreen(enemy_type, self.mPlayer_type, self.mPlayer, self.selected_enemy, self.font,
                                           self.mCur_lvl, self.mSub_lvl)
                self.battle.initiative()
                self.mCreate_battle = False

        if self.flee:
            self.selected_enemy.mRad = 0
            timer = 1
            self.counter += combat_dt
            if self.counter >= timer:
                # print("reset")
                self.flee = False
                self.selected_enemy.mRad = 128
                self.counter = 0

        if self.in_battle:
            self.in_battle, self.mPlayer_dead = self.battle.combat_update(mpos, combat_dt, self.acquired_potions,
                                                                          self.in_battle)

    def warp(self, specific_lvl=None):
        if specific_lvl is not None:
            self.mCur_lvl = specific_lvl
            self.mSub_lvl = self.mLvl_sets[specific_lvl-1][1]
        else:
            self.mCur_lvl += 1
            self.mSub_lvl = random.randint(1, 3)
            self.mLvl_sets.append((self.mCur_lvl, self.mSub_lvl))
        self.mLvl_info = self.get_lvl_info(self.mCur_lvl, self.mSub_lvl)
        self.mCamera = [0, 0]
        self.mPlayer.mPoss = self.mLvl_info["player_spawn_location"]
        data = map_data(self.mCur_lvl, self.mSub_lvl)  # new instance of the map is made with new map
        self.mHeader_data = data[0]
        self.mMap_layers = data[1]
        self.mTileset_img = data[2]
        self.mNum_tiles_wide = data[3]
        self.mBounds = []
        self.chests = []

        if self.mCur_lvl != 3:
            if isinstance(self.mLvl_info["bounds_tilecodes"], int):
                self.load_boundries(self.mLvl_info["bounds_tilecodes"])
                self.find_chests(self.mLvl_info["chest_tilecode"])
            else:
                self.load_boundries(*self.mLvl_info["bounds_tilecodes"])
                self.find_chests(self.mLvl_info["chest_tilecode"])
            self.create_enemys(self.mLvl_info["enemy_spawn_locations"])
            self.mLvlwarp = self.mLvl_info["lvl_warp_rect"]
        else:
            self.load_boundries(self.mLvl_info["bounds_tilecodes"])
            self.find_chests(self.mLvl_info["chest_tilecode"])
            self.mLvlwarp = self.mLvl_info["lvl_warp_rect"]
            self.boss = Boss(self.mCamera, [250, 250], self.mPlayer, MINOTAUR)

    def input(self, evt, keys, running):
        mpos = pygame.mouse.get_pos()
        if self.in_battle:
            self.in_battle, self.flee = self.battle.combat_input(evt, keys, self.acquired_potions)
        if not self.in_battle:
            if self.inventory:
                self.inventory, potion_type = self.mInventory_inst.input(evt, mpos)
                if potion_type == "exit":
                    self.inventory = False
                elif potion_type == "health":
                    self.use_potion(self.acquired_potions, potion_type)
                elif potion_type == "sheild":
                    self.use_potion(self.acquired_potions, potion_type)
                elif potion_type == "special":
                    self.mPlayer.special = True
                    self.use_potion(self.acquired_potions, potion_type)

            if self.mWarp_screen:
                lvl_selected, self.mWarp_screen = self.mWarp.input(evt, self.mCur_lvl)
                if lvl_selected is not None:
                    self.warp(lvl_selected)
        if evt.type == pygame.QUIT:
            running = False
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                running = False
            elif evt.key == pygame.K_q:
                self.mWarp_screen = not self.mWarp_screen
            elif evt.key == pygame.K_e:
                self.inventory = not self.inventory

        if not self.in_battle:
            self.mNext = self.mPlayer.input(evt, self.attack_avalible, self.mBounds, keys, self.mLvlwarp, self.mDirections)
            # print(self.mNext, "next being returned from player input")
            #  self.attack_abalible is true if the cursor is over
            # an enemy and false if not

            # the chest stuff
            if self.take_items is True:
                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_SPACE:
                            self.selected_chest.take_items(self.acquired_potions)
                            self.chests.remove(self.selected_chest)
                            # print("remove")
                            pygame.mixer.Sound("SoundEffects/ChestOpen.wav").play()
        if self.mPlayer.mHealth <= 0:
            self.mPlayer_dead = True

        return running, self.mPlayer_dead, self.mPlayer_won

    def draw(self, surf):
        if not self.in_battle:
            if self.mTileset_img is not None:
                tile_x = int(self.mPlayer.mCam[0] / self.mHeader_data["tilewidth"])
                tile_y = int(self.mPlayer.mCam[1] / self.mHeader_data["tileheight"])
                num_x = surf.get_width() // self.mHeader_data["tilewidth"]
                num_y = surf.get_height() // self.mHeader_data["tileheight"]
                offset_x = int(self.mPlayer.mCam[0] % self.mHeader_data["tilewidth"])
                offset_y = int(self.mPlayer.mCam[1] % self.mHeader_data["tileheight"])

                for layer in self.mMap_layers:
                    y = -offset_y
                    for i in range(tile_y, num_y + tile_y + 2):
                        if 0 <= i < self.mHeader_data["height"]:
                            row = layer[i]
                            x = -offset_x
                            for j in range(tile_x, num_x + tile_x + 2):
                                if 0 <= j < self.mHeader_data["width"]:
                                    code = row[j]
                                    if code != 0:
                                        src_row = code // self.mNum_tiles_wide
                                        src_col = (code - 1) % self.mNum_tiles_wide
                                        src_rect = (src_col * 32, src_row * 32, 32, 32)
                                        surf.blit(self.mTileset_img, (x, y), src_rect)

                                x += self.mHeader_data["tilewidth"]
                            y += self.mHeader_data["tileheight"]

                for b in range(len(self.mBounds)):
                    x = self.mBounds[b][0] - self.mCamera[0]
                    y = self.mBounds[b][1] - self.mCamera[1]
                    # pygame.draw.rect(surf, (255, 255, 255), (x, y, 32, 32), 1)

            if self.mCur_lvl == 3:
                self.boss.Draw(surf)
                self.mPlayer.draw(surf)

            else:
                cur_enemy_list = self.enemy_list[self.mCur_lvl-1]
                for e in cur_enemy_list:
                    e.draw(surf)
                self.mPlayer.draw(surf)

            if self.inventory:
                self.mInventory_inst.draw(win)

        for c in self.chests:
            if self.take_items is True:
                c.draw(surf, self.take_items, self.chest_text)
                # print("should be showing text")
            else:
                c.draw(surf, self.take_items)

        if self.in_battle:
            if not self.mLoading:
                self.battle.draw(surf)
            if self.mLoading:
                self.mLoad_screen.draw(surf)
        if not self.in_battle:
            if self.mWarp_screen:
                self.mWarp.draw(surf)
