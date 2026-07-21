### Util functions ###


import pygame, pyperclip, editing, cursor_movement, rendering as r
from config import c

char_width = 0

# Get char_width from the font in main
def initialize(ch_width):
    global char_width
    char_width = ch_width

# Reads the data from the specified file
def read_file(filename):
    try:
        with open(filename, "r") as txt_file:
            return txt_file.read()
    except FileNotFoundError:
        # If the file doesnt exst: create it
        txt_file = open(filename, "x")
        txt_file.close()

        return ""

# Takes in buffer, turns it into standard txt format and writes it to the file
def write_buffer(s):
    with open(s.filepath, "w") as txt_file:
        
        # Turn buffer into standard text
        lines = []
        for line_chars in s.buffer:
            line = "".join(line_chars)

            lines.append(line)

        data = "\n".join(lines)
        
        # Write data
        txt_file.write(data)

# Copy all text in the buffer
def copy_all(buffer):
    lines = []
    # Turn buffer into standard text
    for line_chars in buffer:
        line = "".join(line_chars)

        lines.append(line)

    text = "\n".join(lines)

    pyperclip.copy(text)

def end_selection(s):
    s.selecting = False
    s.selection_start = (-1, -1)
    s.selection_end = (-1, -1)

# Take in lots of info from main.py and process inputs
def take_inputs(s, event):

    # Stop if the event isnt a standard key press
    if event.type != pygame.KEYDOWN:
        return

    # Keep track of if user is holding control
    if pygame.key.get_mods() & pygame.KMOD_CTRL:
        step = c.large_step
        holding_ctrl = True
    else: 
        step = 1
        holding_ctrl = False
    
    # Keep track of if user is holding shift
    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
        holding_shift = True
    else:
        holding_shift = False

    ##########################

    # Control Z & Control Y (undo/redo)
    if event.key == pygame.K_z and holding_ctrl:
        if len(s.history) < 1:
            return 
        
        editing.undo(s)

        return
    elif event.key == pygame.K_y and holding_ctrl:
        
        editing.redo(s)

        return

    # Navigate cursor with arrow keys
    if event.key == pygame.K_LEFT:
        # Check if its moving lines or moving on one line
        if not holding_shift:
            cursor_movement.move_left(s, step)
        else:
            if not holding_ctrl:
                r.alter_x_offset(True, c.view_move_amount)

                if r.get_x_offset() <= 0:
                    r.set_x_offset(0)
            else:
                # Select text
                s.selecting = True
                if s.selection_start == (-1, -1): # (-1,-1) is no selection
                    s.selection_start = s.cursor_location.copy()
                cursor_movement.move_left(s, 1)
                s.selection_end = s.cursor_location.copy()
                print(s.selection_start, s.selection_end)

    elif event.key == pygame.K_RIGHT:
        # Check if its moving lines or moving on one line
        if not holding_shift:
            cursor_movement.move_right(s, step)
        else:
            if not holding_ctrl:
                r.alter_x_offset(False, c.view_move_amount)
                if r.get_x_offset() >= (char_width * len(s.buffer[s.cursor_location[0]]) + c.view_padding) - c.window_size[0]:
                    r.set_x_offset((char_width * len(s.buffer[s.cursor_location[0]]) + c.view_padding) - c.window_size[0])

                    if r.get_x_offset() <= 0:
                        r.set_x_offset(0)
            else:
                # Select text
                s.selecting = True
                if s.selection_start == (-1, -1): # (-1,-1) is no selection
                    s.selection_start = s.cursor_location.copy()
                cursor_movement.move_right(s, 1)
                s.selection_end = s.cursor_location.copy()
                print(s.selection_start, s.selection_end)
        
    elif event.key == pygame.K_DOWN:
        if not holding_shift:
            cursor_movement.move_down(s, step)
        else:
            r.alter_y_offset(False, c.view_move_amount)
            if r.get_y_offset() >= c.line_height * len(s.buffer) - c.window_size[1] + c.view_padding:
                r.set_y_offset(c.line_height * len(s.buffer) - c.window_size[1] + c.view_padding)
                # Limit offset to 0
                if r.get_y_offset() < 0:
                    r.set_y_offset(0)
    
    elif event.key == pygame.K_UP:
        if not holding_shift:
            cursor_movement.move_up(s, step)
        else:
            r.alter_y_offset(True, c.view_move_amount)
            if r.get_y_offset() <= 0:
                r.set_y_offset(0)
                
    ##########################

    # Allow backspace to delete characters
    if event.key == pygame.K_BACKSPACE:
        editing.backspace(s, holding_ctrl)
        
        s.changed = True
    
    # Allow delete key to function properly
    elif event.key == pygame.K_DELETE:
        editing.delete(s, holding_ctrl)

        s.changed = True
    
    # Allow enter to add new line
    elif event.key == pygame.K_RETURN:
        editing.new_line(s)

        s.changed = True
    
    # Insert character
    elif event.unicode and event.key != pygame.K_TAB and not holding_ctrl:
        editing.insert_character(s, event)

        s.changed = True
    
    # Tab character 
    elif event.key == pygame.K_TAB:
        editing.tab(s)

        s.changed = True

def fix_camera_pos(s):
    # If cursor moves -> move camera
    if (s.cursor_location[0]+2) * c.line_height > c.window_size[1] + r.get_y_offset():
        r.alter_y_offset(False, c.line_height)
    elif s.cursor_location[0] * c.line_height - r.get_y_offset() < 0:
        r.alter_y_offset(True, c.line_height)
 