### Util functions ###

import pygame, editing, config as c, rendering as r

char_width = 0

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

# Checks if the cursor is in a valid position in the buffer and if not fix it
def make_cursor_pos_valid(buffer, cursor_location):
    # Vertical checks
    if cursor_location[0] < 0:
        cursor_location[0] = 0
    
    if cursor_location[0] > len(buffer) - 1:
        cursor_location[0] = len(buffer) - 1

    # Horizontal checks
    if cursor_location[1] > len(buffer[cursor_location[0]]):
        cursor_location[1] = len(buffer[cursor_location[0]])
    
    if cursor_location[1] < 0:
        cursor_location[1] = 0

# Takes in buffer, turns it into standard txt format and writes it to the file
def write_buffer(buffer, filename):
    with open(filename, "w") as txt_file:
        
        # Turn buffer into standard text
        lines = []
        for line_chars in buffer:
            line = "".join(line_chars)

            lines.append(line)

        data = "\n".join(lines)
        
        # Write data
        txt_file.write(data)

# Take in lots of info from main.py and process inputs
def take_inputs(event, cursor_location, buffer, last_y, changed):

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

    # Navigate cursor with arrow keys
    if event.key == pygame.K_LEFT:
        # Check if its moving lines or moving on one line
        if not holding_shift:
            if cursor_location[1] == 0 and cursor_location[0] != 0:
                cursor_location[0] -= 1
                cursor_location[1] = len(buffer[cursor_location[0]])
            else:
                cursor_location[1] -= step

                last_y = cursor_location[1]
                make_cursor_pos_valid(buffer, cursor_location)
        else:
            r.alter_x_offset(True, c.view_move_amount)
            if r.get_x_offset() <= 0:
                r.set_x_offset(0)

    elif event.key == pygame.K_RIGHT:
        # Check if its moving lines or moving on one line
        if not holding_shift:
            if cursor_location[1] == len(buffer[cursor_location[0]]): #and cursor_location[0] < len(buffer) - 1:
                cursor_location[0] += 1
                cursor_location[1] = 0
            else: 
                cursor_location[1] += step

                last_y = cursor_location[1]
                make_cursor_pos_valid(buffer, cursor_location)
        else:
            r.alter_x_offset(False, c.view_move_amount)
            if r.get_x_offset() >= (char_width * len(buffer[cursor_location[0]]) + c.view_padding) - c.window_size[0]:
                r.set_x_offset((char_width * len(buffer[cursor_location[0]]) + c.view_padding) - c.window_size[0])

                if r.get_x_offset() <= 0:
                    r.set_x_offset(0)
    
    elif event.key == pygame.K_DOWN:
        if not holding_shift:
            cursor_location[0] += step
            cursor_location[1] = last_y

            # Move to end of line if at the last line
            if cursor_location[0] == len(buffer):
                cursor_location[1] = len(buffer[cursor_location[0] - 1])

            make_cursor_pos_valid(buffer, cursor_location)
        else:
            r.alter_y_offset(False, c.view_move_amount)
            if r.get_y_offset() >= c.line_height * len(buffer) - c.window_size[1] + c.view_padding:
                r.set_y_offset(c.line_height * len(buffer) - c.window_size[1] + c.view_padding)
    
    elif event.key == pygame.K_UP:
        if not holding_shift:
            cursor_location[0] -= step
            cursor_location[1] = last_y

            make_cursor_pos_valid(buffer, cursor_location)

            # Move to start of line if on first line
            if cursor_location[0] <= 0:
                cursor_location[1] = 0
        else:
            r.alter_y_offset(True, c.view_move_amount)
            if r.get_y_offset() <= 0:
                r.set_y_offset(0)
                
    
    ##########################

    # Allow backspace to delete characters
    if event.key == pygame.K_BACKSPACE:
        buffer, cursor_location = editing.backspace(buffer, cursor_location, holding_ctrl)
        
        changed = True
    
    # Allow delete key to function properly
    elif event.key == pygame.K_DELETE:
        buffer, cursor_location = editing.delete(buffer, cursor_location, holding_ctrl)

        changed = True
    
    # Allow enter to add new line
    elif event.key == pygame.K_RETURN:
        buffer, cursor_location = editing.new_line(buffer, cursor_location)

        changed = True
    
    # Insert character
    elif event.unicode:
        buffer, cursor_location = editing.insert_character(buffer, cursor_location, event)

        changed = True
    
    return buffer,cursor_location, last_y, changed
