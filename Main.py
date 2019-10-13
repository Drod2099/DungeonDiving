from Map import *
from start_screen import *


clock = pygame.time.Clock()

menu = Start_screen()       # simply the instance of the Start_screen
game_over_menu = Game_Over()
victory = Victory()
game_won = False
game_over = False
menu_screen = True          # this is the boolean that controls if the menu screen is on or not
if not menu_screen:
    my_map = Map("knight")
running = True

pygame.mixer.music.load("SoundEffects/GameMusic.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.5)

while running:

    # UPDATE
    deltaTime = clock.tick()/1000
    # print(clock.get_fps())
    if not menu_screen and not game_won and not game_over:  # only get into the map.update when menu screen is off (false)
        in_battle = my_map.update(deltaTime, deltaTime)

    # INPUT
    evt = pygame.event.poll()
    keys = pygame.key.get_pressed()
    m_pos = pygame.mouse.get_pos()
    if not menu_screen:                 # only gets to map.input if menu and battle screen are False
        if not game_over:
            running,game_over,game_won = my_map.input(evt, keys, running)
    if menu_screen:
        list = menu.input(m_pos, evt)   # list is a tuple with a boolean representing the state of running and character
        running = list[0]
        character = list[1]
        menu_state = list[2]
        if menu_state == "play":
            if character is not None:       # when menu.input returns an actual character menu screen is turned off and the game
                                            # ... initiates with the selected character
                if character != "back":
                    menu_screen = False
                    my_map = Map(character)
                    backup_character = character
                    menu.reset()
    if game_over:
        list = game_over_menu.input(m_pos, evt)
        running = list[0]
        menu_state2 = list[1]
        print(menu_state2)
        if menu_state2 == "mainmenu":
            game_over = False
            menu_screen = True
            game_over_menu.reset()
            my_map.mCharacter = None
        elif menu_state2 == "restart":
            game_over = False
            menu_screen = False
            game_over_menu.reset()
            my_map = Map(backup_character)
    if game_won:
        running, state = victory.input(m_pos, evt)
        if state == "menu":
            game_won = False
            menu_screen = True
            victory.reset()
            my_map.mCharacter = None
        elif state == "quit":
            running = False

    # DRAW
    win.fill((0, 0, 0))
    if game_won:
        victory.draw(win)
    if not menu_screen and not game_won and not game_over:
        my_map.draw(win)
    if menu_screen:
        menu.draw(win)
    if game_over:
        game_over_menu.draw(win)
    pygame.display.flip()
pygame.quit()
