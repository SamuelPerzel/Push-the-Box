import tkinter as tk
from config import *

root = tk.Tk()

root.title( "Push the Box") # sets the title of the window
canvas = tk.Canvas(root, width = WIDTH, height = HEIGHT) # defines the canvas
canvas.pack() # packs the canvas

class Game:
    def __init__(self):
        self.walls_coords = [] # empty list where all the wall coords will be stored as tuples after reading from level.txt

        # variables for all images
        self.img_wall = tk.PhotoImage(file = "textures\wall.png")
        self.img_player_neutral = tk.PhotoImage(file = "textures\player_neutral.png")
        self.img_player_up = tk.PhotoImage(file = "textures\player_up.png")
        self.img_player_down = tk.PhotoImage(file = "textures\player_down.png")
        self.img_player_left = tk.PhotoImage(file = "textures\player_left.png")
        self.img_player_right = tk.PhotoImage(file = "textures\player_right.png")
        self.img_box = tk.PhotoImage(file = "textures\\box.png")
        self.img_win_location_off = tk.PhotoImage(file = "textures\win_location_off.png")
        self.img_win_location_on = tk.PhotoImage(file = "textures\win_location_on.png")

        # all x and y values for both player and the box storing how much had player and the box deviated from their starting position
        # after reset, player and box will be moved the opposite direction of these values to be at the start again
        self.x_player_change = 0
        self.y_player_change = 0
        self.x_box_change = 0
        self.y_box_change = 0

    def process_level(self): # this function will read through level.txt, process the information and draw walls, player, box and winning location on the spot where they belong
        self.level_layout = open("level.txt", "r", encoding = "UTF-8") # the program opens level.txt

        # helping variables to calculate the distance of a certain wall tile
        self.x_counter = 0
        self.y_counter = 0

        for self.y_level in self.level_layout: # reads through the every line in level.txt
            self.y_level = self.y_level.strip() # strips it so it's the correct format

            for self.x_level in self.y_level: # reads through every character in the specific line
                
                if self.x_level == "#": # if the character is "#" -> it is a wall
                    self.x_wall = int(WIDTH/2) + ((self.x_counter - 7) * TILE_SIZE) # specifies, where the wall should be on the x axis by multiplying the counter value by TILE_SIZE so it would be placed in a grid
                    self.y_wall = int(HEIGHT/2) + ((self.y_counter - 7) * TILE_SIZE) # and the same for the y axis
                    self.wall = canvas.create_image(self.x_wall - PLAYER_SIZE, self.y_wall - PLAYER_SIZE,anchor = tk.NW, image = self.img_wall) # creates the wall on the position it should appear in the grid

                    self.walls_coords.append((self.x_wall - PLAYER_SIZE, self.y_wall - PLAYER_SIZE)) # appends the wall coords as a tuple to a list walls_coords (this is for checking collisions later)
                    
                elif self.x_level == "P": # if the character is "P" -> it is the player
                    self.x_player = int(WIDTH/2) + int(((self.x_counter - 7) * TILE_SIZE)) # does exactly the same for the player for both x...
                    self.y_player = int(HEIGHT/2) + int(((self.y_counter - 7) * TILE_SIZE)) # ...and y axes
                    self.player = canvas.create_image(self.x_player - PLAYER_SIZE, self.y_player - PLAYER_SIZE, anchor = tk.NW, image = self.img_player_neutral) # creates the player

                elif self.x_level == "B": # if character is "B" -> it is the box
                    self.x_box = int(WIDTH/2) + int(((self.x_counter - 7) * TILE_SIZE))
                    self.y_box = int(HEIGHT/2) + int(((self.y_counter - 7) * TILE_SIZE))

                    self.x_box_start = self.x_box
                    self.y_box_start = self.y_box

                    self.box = canvas.create_image(self.x_box - PLAYER_SIZE, self.y_box - PLAYER_SIZE, anchor = tk.NW, image = self.img_box) # creates the box

                elif self.x_level == "W": # if the character is "W" -> winning location
                    self.x_win_location = int(WIDTH/2) + int(((self.x_counter - 7) * TILE_SIZE))
                    self.y_win_location = int(HEIGHT/2) + int(((self.y_counter - 7) * TILE_SIZE))
                    self.win_location = canvas.create_image(self.x_win_location - PLAYER_SIZE, self.y_win_location - PLAYER_SIZE, anchor = tk.NW, image = self.img_win_location_off)

                self.x_counter += 1
            
            self.x_counter = 0
            self.y_counter += 1

        self.level_layout.close() # the text file closes so it would not create any further problems

    def draw_controls(self): # this function will draw controls
        self.win_text = canvas.create_text(100, 50, text = "", fill = "black", font = "Helvetica 20 bold") # empty text, that will later change to "YOU WIN!" after the player finishes the level

        self.controls_text_title = canvas.create_text(TILE_SIZE, HEIGHT - 6*TILE_SIZE, text = "CONTROLS:", anchor = tk.NW, fill = "black", font = "Helvetica 20 bold") # title to display controls
        self.controls_text = canvas.create_text(TILE_SIZE, HEIGHT - 5*TILE_SIZE, text = "W - up\nA - left\nS - down\nD - right\n\nR - reset", anchor = tk.NW, fill = "black", font = "Helvetica 18 bold") # text to display controls

    def actions(self, event): # this function stores all the actions, that are bound
        self.x, self.y = 0, 0 # the x and y values to determine how much will the player move, if a key is pressed, but it is not for movement, the player and box will move 0px in x and y direction

        if event.char == "w": # if the pressed key is W
            if ((canvas.coords(self.player)[0], canvas.coords(self.player)[1] - TILE_SIZE) in self.walls_coords) or (canvas.coords(self.player)[0] == canvas.coords(self.win_location)[0] and canvas.coords(self.player)[1] - TILE_SIZE == canvas.coords(self.win_location)[1]): # checks if player's x1; y1 is equal to any tuple in the walls_list, if the output is True, this means the player is in colision with a wall and cannot move this way, same is done for winning location
                pass # if collision is detected, the player doesn't move and x, y will still be equal to 0
            else: # if the collision is not detected
                self.y = -TILE_SIZE # the player can move upwards
                self.y_player_change += self.y # adds the changed y value to y_player_change to be later used in reset

            if (canvas.coords(self.player)[1] - canvas.coords(self.box)[1]) == 40 and (canvas.coords(self.player)[0] - canvas.coords(self.box)[0]) == 0: # checks collision with the box, this checks if the box and player are in valid position to be moved
                if (canvas.coords(self.box)[0], canvas.coords(self.box)[1] - TILE_SIZE) in self.walls_coords: # if the box collides with the wall
                    self.y_player_change -= self.y # it reverts the player movement so it would not count even if the player doesn't move
                    self.y = 0 # neither the player not box move upwards
                else:
                    canvas.move(self.box, self.x, self.y) # if no collision is detected, the box will move upwards
                    self.y_box_change += self.y # box change is counted into the change to be later used in reset
            
            canvas.itemconfig(self.player, image = self.img_player_up)

        elif event.char == "a": # if te pressed key is A
            # the program, will do exactly the same process as before, but instead of calculating movement upwards, it will do it for the left side
            if ((canvas.coords(self.player)[0] - TILE_SIZE, canvas.coords(self.player)[1]) in self.walls_coords) or (canvas.coords(self.player)[0] - TILE_SIZE == canvas.coords(self.win_location)[0] and canvas.coords(self.player)[1] == canvas.coords(self.win_location)[1]): # wall collision
                pass
            else:
                self.x = -TILE_SIZE
                self.x_player_change +=self.x

            if (canvas.coords(self.player)[0] - canvas.coords(self.box)[0]) == 40 and (canvas.coords(self.player)[1] - canvas.coords(self.box)[1]) == 0: # box movement
                if (canvas.coords(self.box)[0] - TILE_SIZE, canvas.coords(self.box)[1]) in self.walls_coords:
                    self.x_player_change -= self.x
                    self.x = 0
                else:
                    canvas.move(self.box, self.x, self.y)
                    self.x_box_change += self.x

            canvas.itemconfig(self.player, image = self.img_player_left)

        elif event.char == "s": # if the pressed key is S
            # calculating downward movements
            if ((canvas.coords(self.player)[0], canvas.coords(self.player)[1] + TILE_SIZE) in self.walls_coords) or (canvas.coords(self.player)[0] == canvas.coords(self.win_location)[0] and canvas.coords(self.player)[1] + TILE_SIZE == canvas.coords(self.win_location)[1]): # wall collision
                pass
            else:
                self.y = TILE_SIZE
                self.y_player_change += self.y

            if (canvas.coords(self.player)[1] - canvas.coords(self.box)[1]) == -40 and (canvas.coords(self.player)[0] - canvas.coords(self.box)[0]) == 0: # box movement
                if (canvas.coords(self.box)[0], canvas.coords(self.box)[1] + TILE_SIZE) in self.walls_coords:
                    self.y_player_change -= self.y
                    self.y = 0
                else:
                    canvas.move(self.box, self.x, self.y)
                    self.y_box_change += self.y

            canvas.itemconfig(self.player, image = self.img_player_down)

        elif event.char == "d": # if the pressed key is D
            # movements for the right side
            if ((canvas.coords(self.player)[0] + TILE_SIZE, canvas.coords(self.player)[1]) in self.walls_coords) or (canvas.coords(self.player)[0] + TILE_SIZE == canvas.coords(self.win_location)[0] and canvas.coords(self.player)[1] == canvas.coords(self.win_location)[1]): # wall collision
                pass
            else:
                self.x = TILE_SIZE
                self.x_player_change += self.x

            if (canvas.coords(self.player)[0] - canvas.coords(self.box)[0]) == -40 and (canvas.coords(self.player)[1] - canvas.coords(self.box)[1]) == 0: # box movement
                if (canvas.coords(self.box)[0] + TILE_SIZE, canvas.coords(self.box)[1]) in self.walls_coords:
                    self.x_player_change -= self.x
                    self.x = 0
                else:
                    canvas.move(self.box, self.x, self.y)
                    self.x_box_change += self.x

            canvas.itemconfig(self.player, image = self.img_player_right)

        elif event.char == "r": # if the player pressed R
            canvas.move(self.player, -self.x_player_change, -self.y_player_change) # the player will be moved in reversed directions of the calculated deviations from starting
            self.x_player_change = 0 # the x and y changes are then changed back to 0 and the new calculation can begin after the player moves again
            self.y_player_change = 0
            canvas.itemconfig(self.player, image = self.img_player_neutral)

            canvas.move(self.box, -self.x_box_change, -self.y_box_change) # same is done for the box as well
            self.x_box_change = 0
            self.y_box_change = 0

            canvas.itemconfig(self.win_text, text = "") # the win text is changed to empty string, this only has impact when the player already won
            canvas.itemconfig(self.win_location, image = self.img_win_location_off) # win location image is changed to it's off variant

        if (canvas.coords(self.box)[0] == canvas.coords(self.win_location)[0]) and (canvas.coords(self.box)[1] == canvas.coords(self.win_location)[1]): # this checks if the x1; y1 of the box and x1; y1 of the winning location matches, if yes, the palyer has won
            canvas.itemconfig(self.win_text, text = "YOU WIN!") # empty text will be changed to "YOU WIN!"
            canvas.itemconfig(self.win_location, image = self.img_win_location_on) # image of win location is changed to fit the box outline, meaning, the level victory
        
        canvas.move(self.player, self.x, self.y) # this moves the player in the wanted direction, if W, A, S nor D was pressed, the player will move 0px, which means it will not move

game = Game() # stores Game() into an object

game.process_level() # processes the text file and draws the level
game.draw_controls() # displays the controls on the screen

canvas.bind_all("<Key>", game.actions) # if any key is pressed, the actions function will be called to determine what to do, or if actually do anything at all

root.mainloop() # mainloop for the entire window