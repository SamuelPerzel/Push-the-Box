import tkinter as tk
from config import *

root = tk.Tk()

root.title( "Push the Box") # sets the title of the window
canvas = tk.Canvas(root, width = WIDTH, height = HEIGHT) # defines the canvas
canvas.pack() # packs the canvas

walls_coords = [] # empty list where all the wall coords will be stored as tuples after reading from level.txt

level_layout = open("level.txt", "r", encoding = "UTF-8") # the program opens level.txt

# helping variables to calculate the distance of a certain wall tile
x_counter = 0
y_counter = 0

win_text = canvas.create_text(100, 50, text = "", fill = "black", font = "Helvetica 20 bold") # empty text, that will later change to "YOU WIN!" after the player finishes the level

controls_text_title = canvas.create_text(3*TILE_SIZE, HEIGHT - 6*TILE_SIZE, text = "CONTROLS:", fill = "black", font = "Helvetica 20 bold") # title to display controls
controls_text = canvas.create_text(3*TILE_SIZE, HEIGHT - 3*TILE_SIZE, text = "W - up\nA - left\nS - down\nD - right\n\nR - reset", fill = "black", font = "Helvetica 18 bold") # text to display controls

for y_level in level_layout: # reads through the every line in level.txt
    y_level = y_level.strip() # strips it so it's the correct format

    for x_level in y_level: # reads through every character in the specific line
        if x_level == "#": # if the character is "#" -> it is a wall
            x_wall = int(WIDTH/2) + ((x_counter - 5) * TILE_SIZE) # specifies, where the wall should be on the x axis by multiplying the counter value by TILE_SIZE so it would be placed in a grid
            y_wall = int(HEIGHT/2) + ((y_counter - 5) * TILE_SIZE) # and the same for the y axis
            wall = canvas.create_rectangle(x_wall - PLAYER_SIZE, y_wall - PLAYER_SIZE, x_wall + PLAYER_SIZE, y_wall + PLAYER_SIZE, fill = "grey", outline = "") # creates the wall on the position it should appear in the grid

            walls_coords.append((x_wall - PLAYER_SIZE, y_wall - PLAYER_SIZE)) # appends the wall coords as a tuple to a list walls_coords (this is for checking collisions later)
            
        elif x_level == "P": # if the character is "P" -> it is the player
            x_player = int(WIDTH/2) + int(((x_counter- 5) * TILE_SIZE)) # does exactly the same for the player for both x...
            y_player = int(HEIGHT/2) + int(((y_counter - 5) * TILE_SIZE)) # ...and y axes
            player = canvas.create_rectangle(x_player - PLAYER_SIZE, y_player - PLAYER_SIZE, x_player + PLAYER_SIZE, y_player + PLAYER_SIZE, fill = "red3", outline = "") # creates the player

        elif x_level == "B": # if character is "B" -> it is the box
            x_box = int(WIDTH/2) + int(((x_counter- 5) * TILE_SIZE))
            y_box = int(HEIGHT/2) + int(((y_counter - 5) * TILE_SIZE))

            x_box_start = x_box
            y_box_start = y_box

            box = canvas.create_rectangle(x_box - PLAYER_SIZE, y_box - PLAYER_SIZE, x_box + PLAYER_SIZE, y_box + PLAYER_SIZE, fill = "navy", outline = "") # zadefinovanie boxu

        elif x_level == "W": # if the character is "W" -> winning location
            x_win_location = int(WIDTH/2) + int(((x_counter- 5) * TILE_SIZE))
            y_win_location = int(HEIGHT/2) + int(((y_counter - 5) * TILE_SIZE))
            win_location = canvas.create_rectangle(x_win_location - PLAYER_SIZE, y_win_location - PLAYER_SIZE, x_win_location + PLAYER_SIZE, y_win_location + PLAYER_SIZE, fill = "yellow green", outline = "")

        x_counter += 1
    
    x_counter = 0
    y_counter += 1

level_layout.close() # the text file closes so it would not create any further problems

# all x and y values for both player and the box storing how much had player and the box deviated from their starting position
# after reset, player and box will be moved the opposite direction of these values to be at the start again
x_player_change = 0
y_player_change = 0
x_box_change = 0
y_box_change = 0

def actions(event): # function deciding what to do for every coded movement, if a specific key was not coded, the game will do nothing
    global x_player_change
    global y_player_change
    global x_box_change
    global y_box_change

    x, y = 0, 0 # the x and y values to determine how much will the player move, if a key is pressed, but it is not for movement, the player and box will move 0px in x and y direction

    if event.char == "w": # if the pressed key is W
        if ((canvas.coords(player)[0], canvas.coords(player)[1] - TILE_SIZE) in walls_coords) or (canvas.coords(player)[0] == canvas.coords(win_location)[0] and canvas.coords(player)[1] - TILE_SIZE == canvas.coords(win_location)[1]): # checks if player's x1; y1 is equal to any tuple in the walls_list, if the output is True, this means the player is in colision with a wall and cannot move this way, same is done for winning location
            pass # if collision is detected, the player doesn't move and x, y will still be equal to 0
        else: # if the collision is not detected
            y = -TILE_SIZE # the player can move upwards
            y_player_change += y # adds the changed y value to y_player_change to be later used in reset

        if (canvas.coords(player)[1] - canvas.coords(box)[1]) == 40 and (canvas.coords(player)[0] - canvas.coords(box)[0]) == 0: # checks collision with the box, this checks if the box and player are in valid position to be moved
            if (canvas.coords(box)[0], canvas.coords(box)[1] - TILE_SIZE) in walls_coords: # if the box collides with the wall
                y_player_change -= y # it reverts the player movement so it would not count even if the player doesn't move
                y = 0 # neither the player not box move upwards
            else:
                canvas.move(box, x, y) # if no collision is detected, the box will move upwards
                y_box_change += y # box change is counted into the change to be later used in reset

    elif event.char == "a": # if te pressed key is A
        # the program, will do exactly the same process as before, but instead of calculating movement upwards, it will do it for the left side
        if ((canvas.coords(player)[0] - TILE_SIZE, canvas.coords(player)[1]) in walls_coords) or (canvas.coords(player)[0] - TILE_SIZE == canvas.coords(win_location)[0] and canvas.coords(player)[1] == canvas.coords(win_location)[1]): # kolízia so stenou
            pass
        else:
            x = -TILE_SIZE
            x_player_change += x

        if (canvas.coords(player)[0] - canvas.coords(box)[0]) == 40 and (canvas.coords(player)[1] - canvas.coords(box)[1]) == 0: # posúvanie krabice
            if (canvas.coords(box)[0] - TILE_SIZE, canvas.coords(box)[1]) in walls_coords:
                x_player_change -= x
                x = 0
            else:
                canvas.move(box, x, y)
                x_box_change += x

    elif event.char == "s": # if the pressed key is S
        # calculating downward movements
        if ((canvas.coords(player)[0], canvas.coords(player)[1] + TILE_SIZE) in walls_coords) or (canvas.coords(player)[0] == canvas.coords(win_location)[0] and canvas.coords(player)[1] + TILE_SIZE == canvas.coords(win_location)[1]): # kolízia so stenou
            pass
        else:
            y = TILE_SIZE
            y_player_change += y

        if (canvas.coords(player)[1] - canvas.coords(box)[1]) == -40 and (canvas.coords(player)[0] - canvas.coords(box)[0]) == 0: # posúvanie krabice
            if (canvas.coords(box)[0], canvas.coords(box)[1] + TILE_SIZE) in walls_coords:
                y_player_change -= y
                y = 0
            else:
                canvas.move(box, x, y)
                y_box_change += y

    elif event.char == "d": # if the pressed key is Dň
        # movements for the right side
        if ((canvas.coords(player)[0] + TILE_SIZE, canvas.coords(player)[1]) in walls_coords) or (canvas.coords(player)[0] + TILE_SIZE == canvas.coords(win_location)[0] and canvas.coords(player)[1] == canvas.coords(win_location)[1]): # kolízia so stenou
            pass
        else:
            x = TILE_SIZE
            x_player_change += x

        if (canvas.coords(player)[0] - canvas.coords(box)[0]) == -40 and (canvas.coords(player)[1] - canvas.coords(box)[1]) == 0: # posúvanie krabice
            if (canvas.coords(box)[0] + TILE_SIZE, canvas.coords(box)[1]) in walls_coords:
                x_player_change -= x
                x = 0
            else:
                canvas.move(box, x, y)
                x_box_change += x

    elif event.char == "r": # if the player pressed R
        canvas.move(player, -x_player_change, -y_player_change) # the player will be moved in reversed directions of the calculated deviations from starting
        x_player_change = 0 # the x and y changes are then changed back to 0 and the new calculation can begin after the player moves again
        y_player_change = 0

        canvas.move(box, -x_box_change, -y_box_change) # same is done for the box as well
        x_box_change = 0
        y_box_change = 0

        canvas.itemconfig(win_text, text = "") # the win text is changed to empty string, this only has impact when the player already won
        canvas.itemconfig(win_location, fill = "yellow green") # win location color is also changed back to it's original color

    if (canvas.coords(box)[0] == canvas.coords(win_location)[0]) and (canvas.coords(box)[1] == canvas.coords(win_location)[1]): # this checks if the x1; y1 of the box and x1; y1 of the winning location matches, if yes, the palyer has won
        canvas.itemconfig(win_text, text = "YOU WIN!") # empty text will be changed to "YOU WIN!"
        canvas.itemconfig(win_location, fill = "gold") # color of winning location will be changed to gold
    
    canvas.move(player, x, y) # this moves the player in the wanted direction, if W, A, S nor D was pressed, the player will move 0px, which means it will not move

canvas.bind_all("<Key>", actions) # if any key is pressed, the actions function will be called to determine what to do, or if actually do anything at all

root.mainloop() # mainloop for the entire window