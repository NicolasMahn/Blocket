import arcade
import random
import math
import os
import time
from datetime import datetime

#Autor: Nicolas Mahn

# Set constants for the screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Blocket"

MOVEMENT_SPEED = 10

class Text_Button:
    """ Text-based button """

    def __init__(self, center_x, center_y, width, height, text, font_size=18, font_face="Arial", font_color=arcade.color.WHITE, color=arcade.color.BLACK, button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.font_color = font_color
        self.pressed = False
        self.color = color
        self.button_height = button_height
        pass

    def draw(self):        
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.color)
        
        x = self.center_x
        y = self.center_y
       
        arcade.draw_text(self.text, x, y, self.font_color, font_size=self.font_size, width=self.width, align="center", anchor_x="center", anchor_y="center")

        pass

    def on_press(self):
        self.pressed = True
        pass

    def on_release(self):
        self.pressed = False
        pass

def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()
    pass

def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()
    pass

class Pause_Text_Button(Text_Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Pause", 18, "Arial", arcade.color.WHITE, arcade.color.GRAY)
        self.action_function = action_function
        pass

    def on_release(self):
        super().on_release()
        self.action_function()
        pass

class Highscore_Text_Button(Text_Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Highscores", 18, "Arial", arcade.color.WHITE, arcade.color.GRAY)
        self.action_function = action_function
        pass

    def on_release(self):
        super().on_release()
        self.action_function()
        pass

class Play_Text_Button(Text_Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 200, 80, "Play", 72, "Arial")
        self.action_function = action_function
        pass

    def on_release(self):
        super().on_release()
        self.action_function()
        pass

class Exit_Text_Button(Text_Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 80, "Exit", 34, "Arial", arcade.color.RED)
        self.action_function = action_function
        pass

    def on_release(self):
        super().on_release()
        self.action_function()
        pass

class Back_Text_Button(Text_Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Back", 18, "Arial", arcade.color.WHITE, arcade.color.GRAY)
        self.action_function = action_function
        pass

    def on_release(self):
        super().on_release()
        self.action_function()
        pass

class Mute_Button(Text_Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "", 18, "Arial", arcade.color.WHITE, arcade.color.GRAY)
        self.action_function = action_function
        pass

    def on_release(self):
        super().on_release()
        self.action_function()
        pass

class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
        pass

class Blocket(arcade.View):

    def __init__(self):
        super().__init__()

        #booleans
        self.pause = False
        self.playing_music = True

        # Set up the player info
        self.player_sprite = None
        self.score = 0     

        #lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()
        self.image_list_1 = arcade.SpriteList()
        self.image_list_2 = arcade.SpriteList()
        self.partical_list = arcade.SpriteList()
        self.button_list = []
        self.music_list = []

        #music
        self.current_song = 0
        self.music = None
        self.music_list = ["music/playing.mp3"]
        self.play_song()

        #images
        self.mute_image_1 = arcade.Sprite("textures/mute_1.png")
        self.mute_image_1.center_x = 240 #Starting position
        self.mute_image_1.center_y = 980
        self.image_list_1.append(self.mute_image_1)

        self.mute_image_2 = arcade.Sprite("textures/mute_2.png")
        self.mute_image_2.center_x = 240 #Starting position
        self.mute_image_2.center_y = 980
        self.image_list_2.append(self.mute_image_2)

        #particals
        self.background_partical = arcade.Sprite("textures/background_partical.png")
        self.background_partical.center_x = -25 #Starting position
        self.background_partical.center_y = 1000
        self.partical_list.append(self.background_partical)

        self.blocket_partical = arcade.Sprite("textures/blocket_partical.png")
        self.blocket_partical.center_x = -25 #Starting position
        self.blocket_partical.center_y = 1000
        self.partical_list.append(self.blocket_partical)
       
        #score
        self.score = 0

        #button
        pause_button = Pause_Text_Button(450, 980, self.pause_program)
        self.button_list.append(pause_button)
        mute_button = Mute_Button(240, 980, self.mute_program)
        self.button_list.append(mute_button)

        #setup player
        self.player_sprite = arcade.Sprite("textures/blocket.png")
        self.player_sprite.center_x = 245 #Starting position
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)       

        #blocks
        #normal_blocks
        self.normal_block_1 = arcade.Sprite("textures/normal_block.png")
        self.normal_block_1.center_x = -25
        self.normal_block_1.center_y = 1000
        self.block_list.append(self.normal_block_1)

        self.normal_block_2 = arcade.Sprite("textures/normal_block.png")
        self.normal_block_2.center_x = -25
        self.normal_block_2.center_y = 1000
        self.block_list.append(self.normal_block_2)

        self.normal_block_3 = arcade.Sprite("textures/normal_block.png")
        self.normal_block_3.center_x = -25
        self.normal_block_3.center_y = 1000
        self.block_list.append(self.normal_block_3)
        
        #quick_blocks
        self.quick_block = arcade.Sprite("textures/quick_block.png")
        self.quick_block.center_x = -25
        self.quick_block.center_y = 1200
        self.block_list.append(self.quick_block)

        #position_list          0     1     2     3     4     5     6     7     8     9
        self.position_list = [False, False, False, False, False, False, False, False, False, False]
        #                     0 1 2 3 4 5 6 7 8 9
        self.duration_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.amount=0

        #setup walls
        self.invis_wall_1 = arcade.Sprite("textures/invis_wall_1.png")
        self.invis_wall_1.center_x = -25
        self.invis_wall_1.center_y = 100
        self.wall_list.append(self.invis_wall_1)

        self.invis_wall_1 = arcade.Sprite("textures/invis_wall_1.png")
        self.invis_wall_1.center_x = 525
        self.invis_wall_1.center_y = 100
        self.wall_list.append(self.invis_wall_1)

        self.invis_wall_2 = arcade.Sprite("textures/invis_wall_2.png")
        self.invis_wall_2.center_x = 250
        self.invis_wall_2.center_y = -100
        self.wall_list.append(self.invis_wall_2)
        
        #physicsengine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        pass

    def on_show(self):

        #background
        arcade.set_background_color(arcade.color.BLACK)
        pass

    #@window.event
    def on_draw(self):

        arcade.start_render()

       
        # draw all sprites
        self.partical_list.draw()
        self.block_list.draw()
        self.player_list.draw()
        

        # forground
        arcade.draw_rectangle_filled(250, 980, 500,
                                     40, arcade.color.GRAY) 
          
        # score
        arcade.draw_text(f"Score: {int(self.score)}", 0, 969, arcade.color.WHITE, 17, 100, "center", "Arial")

        # button
        for button in self.button_list:
            button.draw()

        # images
        if Music.volume > 0:
            self.image_list_2.draw()
        elif Music.volume == 0:
            self.image_list_1.draw()
        

        # forground
        arcade.draw_rectangle_filled(250, 960, 500,
                                     2, arcade.color.WHITE) 
        arcade.draw_rectangle_filled(250, 1000, 500,
                                     2, arcade.color.WHITE) 
        pass

    def update(self, delta_time):

        # pause
        if self.pause:
            return

        self.physics_engine.update()
        self.block_list.update()
        self.partical_list.update()

        # Neue partical
        self.blocket_partical = arcade.Sprite("textures/blocket_partical.png")
        self.blocket_partical.center_x =  self.player_sprite.center_x + random.randint(-5,5) # Starting position
        self.blocket_partical.center_y =  self.player_sprite.center_y - 20
        self.partical_list.append(self.blocket_partical)


        if random.randint(0,5) == 0:
            self.background_partical = arcade.Sprite("textures/background_partical.png")
            self.background_partical.center_x = random.randint(0,500)
            self.background_partical.center_y = 1000
            self.partical_list.append(self.background_partical)

        # Neue Bloecke generieren
        if random.randint(0,30-int(self.score/10)) == 0:
            x = Block.position(self, 10)
            self.normal_block_1 = arcade.Sprite("textures/normal_block.png")
            self.normal_block_1.center_x = x
            self.normal_block_1.center_y = 1000
            self.block_list.append(self.normal_block_1)
            x = Block.position_specific(self, 10, x)
            if x%25 != 0: print(x)
            if x != -25 and random.randint(0,4) == 0:
                self.normal_block_2 = arcade.Sprite("textures/normal_block.png")
                self.normal_block_2.center_x = x
                self.normal_block_2.center_y = 1000
                self.block_list.append(self.normal_block_2)
                x = Block.position_specific(self, 10, x)
                if x%25 != 0: print(x)
                if x != -25 and random.randint(0,4) == 0:
                    self.normal_block_3 = arcade.Sprite("textures/normal_block.png")
                    self.normal_block_3.center_x = x
                    self.normal_block_3.center_y = 1000
                    self.block_list.append(self.normal_block_3)

        if random.randint(0,100) == 0:
            self.quick_block = arcade.Sprite("textures/quick_block.png")
            self.quick_block.center_x = Block.position(self, 100)
            self.quick_block.center_y = 2000
            self.block_list.append(self.quick_block)

        Block.update(self)

        #block_movement
        self.normal_block_1.change_y = -5-(self.score/20) 
        self.normal_block_2.change_y = -5-(self.score/20)
        self.normal_block_3.change_y = -5-(self.score/20)  
        self.quick_block.change_y = -10-(self.score/20) 

        #partical_movment
        self.background_partical.change_y = -3-(self.score/20)-random.randint(0,2)
        self.blocket_partical.change_y = -3-(self.score/20)-random.randint(0,2)

        #death_blocks
        wall_hit_list = arcade.check_for_collision_with_list(self.invis_wall_2, self.block_list)
        for normal_block in wall_hit_list:
            normal_block.remove_from_sprite_lists()
        for quick_block in wall_hit_list:
            quick_block.remove_from_sprite_lists()

        #death_particals
        wall_hit_list = arcade.check_for_collision_with_list(self.invis_wall_2, self.partical_list)
        for background_partical in wall_hit_list:
            background_partical.remove_from_sprite_lists()
        for blocket_partical in wall_hit_list:
            blocket_partical.remove_from_sprite_lists()


        #death_player
        block_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.block_list)
        for self.player_sprite in block_hit_list:
            menu_view = Menu()
            #gebe menue score uns speichere es
            menu_view.score = int(self.score)
            Highscore.save(int(self.score))
            #stop music
            self.music.stop()
            self.playing_music = False
            self.window.show_view(menu_view)           

        #score
        self.score += 1/60

        #music
        time = self.music.get_stream_position()
        if time == 0.0:
            self.play_song()
        pass
    
    def play_song(self):

        if self.playing_music == False:
            return
    
        if self.music:
            self.music.stop()

        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(Music.volume, 0)
        time.sleep(0.03)
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            #print("left")
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
            #print("right")
        pass

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        pass

    #buttons
    def on_mouse_press(self, x, y, button, key_modifiers):
        #Called when the user presses a mouse button.
        check_mouse_press_for_buttons(x, y, self.button_list)
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        #Called when a user releases a mouse button.
        check_mouse_release_for_buttons(x, y, self.button_list)
        pass

    def pause_program(self):
        if self.pause == True:
            self.pause = False
            self.music.stop()
            #Music.change_volume()          
        else:
            self.pause = True
            self.music.stop()
            #Music.change_volume()
        pass   
    
    def mute_program(self):
        self.music.stop()
        Music.change_volume(self)

#x position of blocks
class Block:

    def position(self, speed):

        available = False
        value = -1

        while available == False & self.amount < 8:
            value = random.randint(0,9)
            if self.position_list[value] == False:
                self.position_list[value] = True
                self.duration_list[value] = speed
                available = True
                self.amount += 1
                return (-25 + (value+1)*50)
            else:
                return -25

    def position_specific(self, speed, neighbour):

        if self.amount < 8:
            value = int(((neighbour-25)/50)+1)
            if value != 10:
                if self.position_list[value] == False:
                    self.position_list[value] = True
                    self.duration_list[value] = speed
                    self.amount += 1
                    return (-25 + (value+1)*50)
            if value > 0:
                if self.position_list[value-2] == False and value != -2:
                    value -=2
                    self.position_list[value] = True
                    self.duration_list[value] = speed
                    self.amount += 1
                    return (-25 + (value+1)*50)
                else:
                    return -25
            else:
                return -25

    def update(self):
        
        i = 0
        while i != 10:
            if self.duration_list[i] > 0:
                self.duration_list[i] -= 1
            else:
                self.amount =-1
                self.position_list[i] = False
            i += 1
        pass

class Menu(arcade.View):

    def __init__(self):
        super().__init__()

        #score
        self.score = 0

        #images
        self.image_list_1 = arcade.SpriteList()
        self.mute_image_1 = arcade.Sprite("textures/mute_1.png")
        self.mute_image_1.center_x = 240 #Starting position
        self.mute_image_1.center_y = 980
        self.image_list_1.append(self.mute_image_1)

        self.image_list_2 = arcade.SpriteList()
        self.mute_image_2 = arcade.Sprite("textures/mute_2.png")
        self.mute_image_2.center_x = 240 #Starting position
        self.mute_image_2.center_y = 980
        self.image_list_2.append(self.mute_image_2)

        self.partical_list = arcade.SpriteList()
        self.background_partical = arcade.Sprite("textures/background_partical.png")
        self.background_partical.center_x = -25 #Starting position
        self.background_partical.center_y = 1000
        self.partical_list.append(self.mute_image_2)

        #wall    
        self.wall_list = arcade.SpriteList()
        self.invis_wall_2 = arcade.Sprite("textures/invis_wall_2.png")
        self.invis_wall_2.center_x = 250
        self.invis_wall_2.center_y = -100
        self.wall_list.append(self.invis_wall_2)

        #button
        self.button_list = []
        highscore_button = Highscore_Text_Button(440, 980, self.highscore_program)
        self.button_list.append(highscore_button)
        play_button = Play_Text_Button(250, 400, self.play_program)
        self.button_list.append(play_button)
        exit_button = Exit_Text_Button(250, 300, self.exit_program)
        self.button_list.append(exit_button)
        mute_button = Mute_Button(240, 980, self.mute_program)
        self.button_list.append(mute_button)
        pass

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        pass

    def on_draw(self):

        arcade.start_render()
        
        #background
        self.partical_list.draw()

        #forground
        arcade.draw_rectangle_filled(250, 980, 500, 40, arcade.color.GRAY) 

        #button
        for button in self.button_list:
            button.draw()

        #images
        if Music.volume > 0:
            self.image_list_2.draw()
        elif Music.volume == 0:
            self.image_list_1.draw()
          
        #score
        if self.score != 0:
            arcade.draw_text(f"Score: {int(self.score)}", 0, 969, arcade.color.WHITE, 17, 100, "center", "Arial")

        #forground
        arcade.draw_rectangle_filled(250, 960, 500,
                                     2, arcade.color.WHITE) 

        arcade.draw_rectangle_filled(250, 1000, 500,
                                     2, arcade.color.WHITE)
        pass
    
    def on_update(self, delta_time):

        self.partical_list.update()

        #Neue background partical
        if random.randint(0,5) == 0:
            self.background_partical = arcade.Sprite("textures/background_partical.png")
            self.background_partical.center_x = random.randint(0,500)
            self.background_partical.center_y = 1000
            self.partical_list.append(self.background_partical)

        #partical_movment
        self.background_partical.change_y = -3-(self.score/20)-random.randint(0,2)

        #partical death
        wall_hit_list = arcade.check_for_collision_with_list(self.invis_wall_2, self.partical_list)
        for background_partical in wall_hit_list:
            background_partical.remove_from_sprite_lists()

        pass

    def on_mouse_press(self, x, y, button, modifiers):
        #button
        check_mouse_press_for_buttons(x, y, self.button_list)
        pass
        

    def on_mouse_release(self, x, y, button, key_modifiers):
        #Called when a user releases a mouse button.
        check_mouse_release_for_buttons(x, y, self.button_list)
        pass
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            game_view = Blocket()
            self.window.show_view(game_view)
        pass

    def highscore_program(self):
        highscore_view = Highscore_View()
        highscore_view.score = self.score
        self.window.show_view(highscore_view)
        pass

    def play_program(self):
        game_view = Blocket()
        self.window.show_view(game_view)
        pass

    def exit_program(self):
        os._exit(0)
        pass

    def mute_program(self):
        Music.change_volume(self)
        pass

class Highscore_View(arcade.View):

    def __init__(self):
        super().__init__()

        #highscores list
        self.highscores = []

        #score
        self.score = 0

        #images
        self.image_list_1 = arcade.SpriteList()
        self.mute_image_1 = arcade.Sprite("textures/mute_1.png")
        self.mute_image_1.center_x = 240 #Starting position
        self.mute_image_1.center_y = 980
        self.image_list_1.append(self.mute_image_1)

        self.image_list_2 = arcade.SpriteList()
        self.mute_image_2 = arcade.Sprite("textures/mute_2.png")
        self.mute_image_2.center_x = 240 #Starting position
        self.mute_image_2.center_y = 980
        self.image_list_2.append(self.mute_image_2)

        #button
        self.button_list = []
        back_button = Back_Text_Button(440, 980, self.back_program)
        self.button_list.append(back_button)
        mute_button = Mute_Button(240, 980, self.mute_program)
        self.button_list.append(mute_button)
        pass


    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.highscores = Highscore.read(self)
        pass

    def on_draw(self):
        arcade.start_render()

        #title     
        arcade.draw_text("Highscores", 110, 800, arcade.color.WHITE, 54)

        #highscores
        x_1 = 50
        x_2 = 350
        y = 650
        i = 1
        arcade.draw_text(f"Date", x_1, y+50, arcade.color.WHITE, 19, 100, "center", "Arial")
        arcade.draw_text(f"Score", x_2, y+50, arcade.color.WHITE, 19, 100, "center", "Arial")

        while i < 21:
            arcade.draw_text(f"{self.highscores[i-1]}", x_1, y, arcade.color.WHITE, 17, 200, "center", "Arial")
            arcade.draw_text(f"{int(self.highscores[i])}", x_2, y, arcade.color.WHITE, 17, 100, "center", "Arial")
            i += 2
            y -= 50

        #forground
        arcade.draw_rectangle_filled(250, 980, 500,
                                     40, arcade.color.GRAY) 

        #button
        for button in self.button_list:
            button.draw()

        #images
        if Music.volume > 0:
            self.image_list_2.draw()
        elif Music.volume == 0:
            self.image_list_1.draw()
          
        #score
        if self.score != 0:
            arcade.draw_text(f"Score: {int(self.score)}", 0, 969, arcade.color.WHITE, 17, 100, "center", "Arial")

        #forground          
        arcade.draw_rectangle_filled(250, 960, 500,
                                     2, arcade.color.WHITE) 
        arcade.draw_rectangle_filled(250, 1000, 500,
                                     2, arcade.color.WHITE)
        pass     

    def on_mouse_press(self, x, y, button, modifiers):
        #button
        check_mouse_press_for_buttons(x, y, self.button_list)
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        #Called when a user releases a mouse button.
        check_mouse_release_for_buttons(x, y, self.button_list)
        pass

    def back_program(self):
        menu_view = Menu()
        menu_view.score = self.score
        self.window.show_view(menu_view)
        pass

    def mute_program(self):
        Music.change_volume(self)
        pass

#Highscores in Datei speicher bzw. auslesen lassen
class Highscore:
    
    def save(score):
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")

        highscore = [20]

        with open('highscore.txt', 'r') as f:
            temp_highscore = f.read()
            temp_highscore = temp_highscore.split(',')
            highscore = [x for x in temp_highscore if x.strip()]
        #print(highscore)

        i = 1
        while i < 21:
            #print(i)
            if int(highscore[i]) < score:
                temp_highscore = highscore[i]
                temp_time = highscore[i-1]
                highscore[i] = score
                highscore[i-1] = now
                i += 2
                while i != 21:
                    temp = highscore[i]
                    highscore[i] = temp_highscore
                    temp_highscore = temp
                    temp = highscore[i-1]
                    highscore[i-1] = temp_time
                    temp_time = temp
                    i += 2
            i += 2
        #print(highscore)

        with open('highscore.txt', 'w') as f:
            for highscore in highscore:
                f.write(str(highscore) + ',')
        pass

    def read(self):

        with open('highscore.txt', 'r') as f:
            temp_highscore = f.read()
            temp_highscore = temp_highscore.split(',')
            highscore = [x for x in temp_highscore if x.strip()]
        #print(highscore)
        return highscore

class Music:

    volume = 0.125

    def change_volume(self):
        if Music.volume == 0.125:
            Music.volume = 0
        elif Music.volume == 0:
            Music.volume = 0.125
        pass

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = Menu()
    window.show_view(menu)
    arcade.run()
    pass

if __name__ == "__main__":
    main()