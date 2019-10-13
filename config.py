import pygame
import random
from copy import deepcopy

player_opacity = 255
enemy_opacity = 255
pygame.init()
win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
KnightInfo = pygame.image.load("KnightSpecialPopUp.png")
WizardInfo = pygame.image.load("WizardSpecialPopUp.png")
RogueInfo = pygame.image.load("RogueSpecialPopUp.png")
Help_screen = pygame.image.load("ControlsScreen.png")

# knight scaling
KNIGHT = pygame.image.load("SpriteAssets/Golden_Knight.png").convert()
# img_w = oKNIGHT.get_width()
# img_h = oKNIGHT.get_height()
nimg_w = KNIGHT.get_width()   # int(img_w * knight_sf)
nimg_h = KNIGHT.get_height()  # int(img_h * knight_sf)
KNIGHT.set_colorkey((255, 0, 255))
KNIGHT.set_alpha(player_opacity)
knight_directions = {"left": 1, "right": 3, "up": 0, "down": 2, "frameheight": 64, "framewidth": 64, "frames_wide": 8,
                     "x_offset": 15, "y_offset": 5, "player": "knight"}

REDKNIGHT = pygame.image.load("SpriteAssets/RedGolden_Knight_2.0.png").convert()
nimg_w = REDKNIGHT.get_width()   # int(img_w * knight_sf)
nimg_h = REDKNIGHT.get_height()  # int(img_h * knight_sf)
# RED_SF = .7
REDKNIGHT.set_colorkey((255, 0, 255))
REDKNIGHT.set_alpha(player_opacity)
knight_directions = {"left": 1, "right": 3, "up": 0, "down": 2, "frameheight": 64, "framewidth": 64, "frames_wide": 8,
                     "x_offset": 15, "y_offset": 5, "player": "knight"}

# confetti
CONFETTI = pygame.image.load("SpriteAssets/confetti.png")
c_w = CONFETTI.get_width()
c_h = CONFETTI.get_height()
csf = 1.5
c_h = int(c_h * csf)
CONFETTI = pygame.transform.scale(CONFETTI, (c_w, c_h))

# Paladin info
PALADIN = pygame.image.load("SpriteAssets/Paladin.png").convert()
PALADIN.set_colorkey((255, 0, 255))
PALADIN.set_alpha(player_opacity)
pal_w = PALADIN.get_width()
pal_h = PALADIN.get_height()
paladin_height = 57
paladin_width = 33
paladin_directions = {"left": 3, "right": 2, "up": 1, "down": 0, "frameheight": 64, "framewidth": 64, "frames_wide": 5,
                      "x_offset": 15, "y_offset": 5}


# Rogue info
ROGUE = pygame.image.load("SpriteAssets/RogueSprite.png")
rog_w = ROGUE.get_width()
rog_h = ROGUE.get_height()
rogue_sf = 1
rog_w2 = int(rog_w * rogue_sf)
rog_h2 = int(rog_h * rogue_sf)
ROGUE = pygame.transform.scale(ROGUE, (rog_w2, rog_h2)).convert()
ROGUE.set_colorkey((255, 0, 255))
ROGUE.set_alpha(player_opacity)
rogue_directions = {"left": 1, "right": 2, "up": 3, "down": 0, "frameheight": 48, "framewidth": 32, "frames_wide": 4,
                    "x_offset": 15, "y_offset": 0, "player": "rogue"}

WIZARD = pygame.image.load("SpriteAssets/mageattack.png")
wiz_w = WIZARD.get_width()
wiz_h = WIZARD.get_height()
wiz_sf = 1.5
nwiz_w = int(wiz_w * wiz_sf)
nwiz_h = int(wiz_h * wiz_sf)
WIZARD = pygame.transform.scale(WIZARD, (nwiz_w, nwiz_h)).convert()
WIZARD.set_colorkey((255, 0, 255))
WIZARD.set_alpha(player_opacity)
wizard_directions = {"left": 3, "right": 2,"up": 1, "down": 0,"frameheight": 37 * wiz_sf, "framewidth": 36 * wiz_sf,
                     "frames_wide": 6, "x_offset": 5 * wiz_sf, "y_offset": 5 * wiz_sf, "player": "wizard"}

# Goblin scaling
GOBLIN = pygame.image.load("SpriteAssets/goblin_sheet.png")
img_w = GOBLIN.get_width()
img_h = GOBLIN.get_height()
goblin_sf = .8
img_w = int(img_w * goblin_sf)
img_h = int(img_h * goblin_sf)
GOBLIN = pygame.transform.scale(GOBLIN, (img_w, img_h)).convert()
GOBLIN.set_colorkey((255, 0, 255))
GOBLIN.set_alpha(enemy_opacity)
rand = random.randint(1, 100)
if rand <= 15:
    health = 10
    die = 4
    armor = 3
elif 15 < rand <= 45:
    health = 20
    die = 6
    armor = 6
elif 45 < rand <= 75:
    health = 30
    die = 8
    armor = 8
elif 75 < rand <= 90:
    health = 40
    die = 10
    armor = 11
elif 90 < rand <= 100:
    health = 50
    die = 12
    armor = 15
goblin_directions = {"left": 3, "right": 1, "up": 2, "down": 0, "death_row": 4, "death_colum": 4}
goblin_info = {"width": 29, "height": 50, "hitbox_xoffset": 12, "view_radius": 128, "rows": 4, "collums": 11,
               "health": health, "scale": goblin_sf, "speed": 40, "armour": armor, "strength": 3, "frame_w": 52,
               "frame_h": 52, "hitbox_yoffset": 0, "enemy_die": die}

# Zombie scaling
Z = pygame.image.load("SpriteAssets/Zombie_sheet.png")
z_w = Z.get_width()
z_h = Z.get_height()
zombie_sf = 1.4
z_w = int(z_w * zombie_sf)
z_h = int(z_h * zombie_sf)
ZOMBIE = pygame.transform.scale(Z, (z_w, z_h)).convert()
ZOMBIE.set_colorkey((255, 0, 255))
ZOMBIE.set_alpha(enemy_opacity)
rand = random.randint(1, 100)
if rand <= 15:
    health = 6
    die = 2
    armor = 2
elif 15 < rand <= 45:
    health = 14
    die = 4
    armor = 4
elif 45 < rand <= 75:
    health = 26
    die = 6
    armor = 7
elif 75 < rand <= 90:
    health = 34
    die = 8
    armor = 10
elif 90 < rand <= 100:
    health = 44
    die = 10
    armor = 13
zombie_directions = {"left": 1, "right": 2, "up": 3, "down": 0, "death_row": 3, "death_colum": 2}
zombie_info = {"width": 19 * zombie_sf, "height": 28 * zombie_sf, "hitbox_xoffset": 5, "view_radius": 128, "rows": 4,
               "collums": 3, "health": health, "scale": zombie_sf, "speed": 30, "armour": armor, "strength": 3,
               "frame_w": z_w / 3, "frame_h": (z_h / 4), "hitbox_yoffset": 10, "enemy_die": die}

# minotaur scaling
MINOTAUR = pygame.image.load("SpriteAssets/Minotaur/minotaur-red.png")
m_w = MINOTAUR.get_width()
m_h = MINOTAUR.get_height()
minotaur_sf = 1
m_w = int(m_w * minotaur_sf)
m_h = int(m_h * minotaur_sf)
MINOTAUR = pygame.transform.scale(MINOTAUR, (m_w, m_h))
minotaur_directions = {"left": 3, "right": 1, "up": 0, "down": 2}
minotaur_info = {"width": (144//3) * minotaur_sf, "height": 256//4 * minotaur_sf, "hitbox_xoffset": 5, "rows": 4,
                 "collums": 3, "health": 15, "scale": minotaur_sf, "speed": 300, "armour": 10, "strength": 3}

# inventory screen
INVENTORY = pygame.image.load("InventoryScreen.png")
VICTORY = pygame.image.load("WinScreen.png")

chest_win = pygame.image.load("MapAssets/Paper.png")
cw_w = Z.get_width()
cw_h = Z.get_height()
cw_sf = 3
cw_w = int(cw_w * cw_sf)
cw_h = int(cw_h * cw_sf)
chest_win = pygame.transform.scale(chest_win, (cw_w, cw_h))

HEALTH_POTION = pygame.image.load("SpriteAssets/health_potion.png")
h_w = HEALTH_POTION.get_width()
h_h = HEALTH_POTION.get_height()
health_hsf = 5
health_wsf = 5.7
nh_h = int(h_h * health_hsf)
nh_w = int(h_w * health_wsf)
HEALTH_POTION = pygame.transform.scale(HEALTH_POTION, (nh_w, nh_h))

SHEILD_POTION = pygame.image.load("SpriteAssets/sheild_potion.png")
s_w = SHEILD_POTION.get_width()
s_h = SHEILD_POTION.get_height()
ns_h = int(s_h * health_hsf)
ns_w = int(s_w * health_wsf)
SHEILD_POTION = pygame.transform.scale(SHEILD_POTION, (ns_w, ns_h))
# chest_win = pygame.transform.rotate(chest_win, (math.pi/2))

SPECIAL_POTION = pygame.image.load("SpriteAssets/special_potion.png")
s_w = SPECIAL_POTION.get_width()
s_h = SPECIAL_POTION.get_height()
nsp_h = int(s_h * health_hsf)
nsp_w = int(s_w * health_wsf)
SPECIAL_POTION = pygame.transform.scale(SPECIAL_POTION, (nsp_w, nsp_h))

# LVL INFO
# LVL INFO FOR LVL 1'S

enemy_spawn_locations_lvl1_1 = [[300, 300], [500, 500], [600, 735], [1190, 750], [1110, 925], [850, 1230], [1030, 1345],
                                [1189, 1109], [1536, 1130]]
lvl1_1_player_spawn = [50, 20]
lvl1_1_info = {"enemy_spawn_locations": enemy_spawn_locations_lvl1_1,
               "player_spawn_location": lvl1_1_player_spawn,
               "bounds_tilecodes": (61, 64, 62, 15, 63),
               "lvl_warp_rect": pygame.Rect(1491, 1539, 32, 32),
               "chest_tilecode": 2936}
lvl2_1_player_spawn = [13, 865]
enemy_spawn_locations_lvl2_1 = [[152, 1434], [12, 120], [340, 20], [589, 602], [414, 197],
                                [677, 897], [236, 1391], [843, 112], [628, 1461], [1358, 1079], [1524, 1293],
                                [1076, 745], [987, 463], [1343, 348]]
lvl2_1_info = {"enemy_spawn_locations": enemy_spawn_locations_lvl2_1,
               "player_spawn_location": lvl2_1_player_spawn,
               "bounds_tilecodes": (955, 962),
               "lvl_warp_rect": pygame.Rect(1524, 18, 40, 10),
               "chest_tilecode": 2936}

enemy_spawn_locations_lvl3_1 = [[400, 225], [950, 272], [335, 800], [43, 1307], [1096, 796], [923, 1252], [1473, 1033],
                                [1180, 1262]]
lvl3_1_player_spawn = [30,38]
lvl3_1_info = {"enemy_spawn_locations": enemy_spawn_locations_lvl3_1,
               "player_spawn_location": deepcopy(lvl3_1_player_spawn),
               "bounds_tilecodes": (961, 962),
               "lvl_warp_rect": pygame.Rect(1522, 1550, 40, 10),
               "chest_tilecode": 2936}

# LVL INFO FOR LVL 2'S
enemy_spawn_locations_lvl1_2 = [[175, 350], [975, 603], [300, 1075], [495, 1175], [1135, 1308]]
lvl1_2_player_spawn = [90, 95]
lvl1_2_info = {"player_spawn_location": deepcopy(lvl1_2_player_spawn),
               "lvl_warp_rect":  pygame.Rect(1505, 1140, 30, 25),
               "bounds_tilecodes": (814, 2876),
               "enemy_spawn_locations": enemy_spawn_locations_lvl1_2,
               "chest_tilecode": 2936}
# the above values for warp and bounds code appeared to be the same as 2_2 so i copy pasted :)
# the statement above is super wrong so i fixed the copy pastes :)

enemy_spawn_locations_lvl2_2 = [[526, 1387], [425, 797], [848, 940], [848, 606], [507, 550], [80, 112],
                                [921, 90], [1445, 675]]
lvl2_2_player_spawn = [78, 1369]
lvl2_2_info = {"player_spawn_location": deepcopy(lvl2_2_player_spawn),
               "lvl_warp_rect": pygame.Rect(1429, 109, 40, 25),
               "bounds_tilecodes": 855,
               "enemy_spawn_locations": enemy_spawn_locations_lvl2_2,
               "chest_tilecode": 2936}

enemy_spawn_locations_lvl3_2 = [[812, 49], [101, 111], [483, 233], [372, 516], [129, 686], [427, 821], [121, 1358],
                                [407, 1398], [1377, 1400], [1436, 903], [881, 563], [965, 989]]
lvl3_2_player_spawn = [1477, 23]
lvl3_2_info = {"player_spawn_location": deepcopy(lvl3_2_player_spawn),
               "lvl_warp_rect": pygame.Rect(1492, 688, 40, 25),
               "bounds_tilecodes": 810,
               "enemy_spawn_locations": enemy_spawn_locations_lvl3_2,
               "chest_tilecode": 2936}

# LVL INFO FOR LVL 3'S
lvl1_3_player_spawn = [288, 520]
lvl1_3_info = {"enemy_spawn_locations": [[288, 95]],
               "player_spawn_location": deepcopy(lvl1_3_player_spawn),
               "bounds_tilecodes":1093,
               "lvl_warp_rect": pygame.Rect(1429, 110, 10, 10),
               "chest_tilecode": 2936}  # boss map
# enemy spawn may need adjusted for enemy width

lvl2_3_player_spawn = [292, 520]
lvl2_3_info = {"enemy_spawn_locations": [[292, 175]],
               "player_spawn_location": deepcopy(lvl2_3_player_spawn),
               "bounds_tilecodes": 855,
               "lvl_warp_rect": pygame.Rect(1429, 110, 10, 10),
               "chest_tilecode": 2936}

lvl3_3_player_spawn = [290, 522]
lvl3_3_info = {"enemy_spawn_locations": [[290, 255]],
               "player_spawn_location": deepcopy(lvl3_3_player_spawn),
               "bounds_tilecodes": 810,
               "lvl_warp_rect": pygame.Rect(1429, 110, 10, 10),
               "chest_tilecode": 2936}
