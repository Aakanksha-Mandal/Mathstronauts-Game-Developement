# Intro to GameDev - main game file

import pgzrun
import random

WIDTH = 1000
HEIGHT = 600

# """ define some colours
# Red = (255, 0, 0)

# def draw():
#   screen.fill(Red) """

#creating images
BACKGROUND_TITLE = "game_logo1"
BACKGROUND_LEVEL1 = "background1"
BACKGROUND_LEVEL2 = "background2"
BACKGROUND_LEVEL3 = "background3"

PLAYER_IMG = "spaceship"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris3"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"

SCOREBOX_HEIGHT = 52

#start game with title screen
BACKGROUND_IMG = BACKGROUND_TITLE

#initialize title screen buttons
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 500)

instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 560)

#keep track of score
score = 0
level = 0
level_screen = 0

junk_collect = 0
lvl2_LIMIT = 5 #collect 5 junk to move to Leve 2
lvl3_LIMIT = 10

#initializing speeds
junk_speed = 5
satellite_speed = 3
debris_speed = 2
laser_speed = -5
satellite_speed = 3

def on_mouse_down(pos):
    global level, level_screen

    #check start button
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1

     #check instructions button
    if instructions_button.collidepoint(pos):
        level = -1

def init():
    global player, junks, satellite, debris, lasers
    #initializing spacheship
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH - 15, HEIGHT / 2)

    #initializing junks
    junk = Actor(JUNK_IMG)
    junk.pos = (0, HEIGHT / 2)
    
    junks = []
    for i in range(5):
        junk = Actor(JUNK_IMG)
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
        junk.topleft = (x_pos, y_pos)
        junks.append(junk)

    #initializing satellite
    satellite = Actor(SATELLITE_IMG)
    x_sat = random.randint(-500, -50)
    y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)

    #initializing debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500, -50)
    y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

    #background music
    music.play("spacelife")


#game loop
init()

def update():
    global level, level_screen, BACKGROUND_IMG, junk_collect, score
    if junk_collect == lvl2_LIMIT: #Level 2
        level = 2

    if junk_collect == lvl3_LIMIT: #Level 3
        level = 3

    if level == -2: #Game Over
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            level = 0
            init()

    if level == -1: #Instructions Screen
        BACKGROUND_IMG = BACKGROUND_LEVEL1
    
    if score >= 0 and level >= 1: #Gameplay
        if level_screen == 1: #Level 1 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1:
                level_screen = 2

        if level_screen == 2: #Level 1 Gameplay Screen
            playerUpdate()
            junkUpdate()
        
        if level == 2 and level_screen <= 3: #Level 2 Transition Screen
            level_screen = 3
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            #background music
            music.play("space_mysterious")
            if keyboard.RETURN == 1:
                level_screen = 4
        
        if level_screen == 4: #Level 2 Gameplay Screen
            #background music
            music.play("space_mysterious")
            playerUpdate()
            junkUpdate()
            satelliteUpdate()
        
        if level == 3 and level_screen <= 5: #Level 3 Transition Screen
            level_screen = 5
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            #background music
            music.play("space_suspense")
            if keyboard.RETURN == 1:
                level_screen = 6

        if level_screen == 6: #Level 3 Gameplay Screen
            #background music
            music.play("space_suspense")
            playerUpdate()
            junkUpdate()
            satelliteUpdate()
            debrisUpdate()
            updateLasers()
        
    if score < 0 or level == -2:  # Game Over
        music.stop()
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            level = 0
            init()

def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))

    if level == 0:
        start_button.draw()
        instructions_button.draw()
    
    if level == -1:
        start_button.draw()

    if (score >= 0  and level >= 1):
        player.draw() #draw player sprite on screen
    
        for junk in junks:
            junk.draw() #draw junk sprite on screen
    
    if level >= 2:
        satellite.draw() #draw satellite sprite on screen
        
    if level == 3:
        debris.draw() #draw debris satellite sprite on screen
        
        for laser in lasers:
            laser.draw() #draw laser sprite on screen

    if level == -1: #instructions screen
        start_button.draw()
        show_instructions = ("Use UP and DOWN arrow keys to move your player.\n\nPress SPACEBAR to fire lasers.\n\nCollect the debris.\n\n Avoid shooting the good spaceships.\n\nShoot the bad spaceships to gain points.")
        screen.draw.text(show_instructions, midtop = (WIDTH/2, 200), fontsize = 35, color = "white")
    
    #draw score on the screen
    show_score = "Score: " + str(score) #remember to convert score to a string
    screen.draw.text(show_score, topleft = (850,15), fontsize = 35, color = "white")
    
    #draw number of junk on the screen
    show_collect_value = "Junk: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft = (650, 15), fontsize = 35, color = "white")

    if level >= 1:
        show_level = "Level " + str(level)
        screen.draw.text(show_level, topright = (550, 15), fontsize = 35, color = "white")
    
    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_level_title = "Level " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_level_title, center = (WIDTH/2, HEIGHT/2), fontsize = 70, color = "white")

    # game over screen
    if score < 0:
        game_over = "YOU LOST!\nPress ENTER to play again!"
        screen.draw.text(game_over, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="white")


def playerUpdate():
    if (keyboard.up == 1 or keyboard.w == 1):
        player.y += -5
    
    elif (keyboard.down == 1 or keyboard.s == 1):
        player.y += 5

    if (player.top < 52):
        player.top =  52

    if (player.bottom > HEIGHT):
        player.bottom = HEIGHT

    #initializing laser
    if (keyboard.space == 1) and (level == 3):
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

def junkUpdate():
    #make junk move left to right
    global score, junk_collect
    
    for junk in junks:
        junk.x += junk_speed

        collision = player.colliderect(junk)

        if (junk.left > WIDTH or collision == 1):
            #junk_speed = random.randint(2, 10)
            x_pos = random.randint(-500, -50)
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if (junk.left >= WIDTH):
            junk.right = 0

        if (collision == 1):
            score += 1
            junk_collect += 1 #increase by 1 every time collision occurs
            sounds.collect_pep.play()
            

def satelliteUpdate():
    global score, satellite_speed
    satellite.x += satellite_speed

    collision = player.colliderect(satellite)

    if (satellite.right > 850 or collision == 1):
        x_sat = random.randint(-500, -50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score += -10
        sounds.explosion.play()

def debrisUpdate():
    global score, debris_speed
    debris.x += debris_speed

    collision = player.colliderect(debris)

    if (debris.left > WIDTH or collision == 1):
        x_deb = random.randint(-500, -50)
        y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score -= 5
        sounds.collect_pep.play()

def updateLasers():
    global score
    for laser in lasers:
        laser.x += laser_speed
        collision_sat = satellite.colliderect(laser)
        collision_deb = debris.colliderect(laser)
        
        if laser.right < 0 or collision_sat ==1 or collision_deb == 1:
            lasers.remove(laser)
        
        #checking for collison with satellite
        if collision_sat == 1:
            x_sat = random.randint(-500, -50)
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score -= 5

        #checking for collision with debris
        if collision_deb == 1:
            x_deb = random.randint(-500, -50)
            y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5

#intializing laser
lasers = []
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list

pgzrun.go()