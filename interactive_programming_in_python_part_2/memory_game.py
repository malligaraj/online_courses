# implementation of card game - Memory
# Execute in http://www.codeskulptor.org/ to view output

import simplegui
import random

WIDTH = 800
HEIGHT = 100
BOX_WIDTH = 50

game_list = []
exposed = []
turns = 0
state = 0
open1, open2 = 0, 0

# helper function to initialize globals
def new_game():
    global game_list, exposed, state, turns
    game_list = []
    for i in range(2):
        for j in range(0, 8):
            game_list.append(j)    
    random.shuffle(game_list)
    print(game_list)
    exposed = [False] * len(game_list)
    state = 0
    turns = 0

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, turns, game_list, state, open1, open2
    
    x, y = pos
    idx = x / BOX_WIDTH
    
    if state == 0:
        open1 = idx
        if exposed[open1] == False:
            exposed[open1] = True
            state = 1        
            turns = turns + 1
    elif state == 1:
        open2 = idx
        if exposed[open2] == False:
            exposed[open2] = True
            state = 2
            turns = turns + 1
    elif state == 2:
        if game_list[open1] != game_list[open2]:
            exposed[open1] = False
            exposed[open2] = False
        open1 = idx
        if exposed[open1] == False:
            exposed[open1] = True
            state = 1
            turns = turns + 1
    else:
        pass
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global game_list, exposed
    TEXT_SIZE = 100
    TEXT_PADDING = 15
    TEXT_COLOR = 'White'
    FILL_COLOR = 'Green'        
    LINE_COLOR = 'Yellow'
    LINE_WIDTH = 1
    
    label.set_text("Turns = " + str(turns))
    
    for i in range(0, WIDTH, BOX_WIDTH):
        text_pos = [i, HEIGHT - TEXT_PADDING]
        canvas.draw_text(str(game_list[i/BOX_WIDTH]), text_pos, TEXT_SIZE, TEXT_COLOR)
        
        screen_points = [[i, 0], [i + BOX_WIDTH, 0], [i + BOX_WIDTH, HEIGHT], [i, HEIGHT]]
        if exposed[i/BOX_WIDTH]:
            canvas.draw_polygon(screen_points, LINE_WIDTH, LINE_COLOR, None)
        else:
            canvas.draw_polygon(screen_points, LINE_WIDTH, LINE_COLOR, FILL_COLOR)
    
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric