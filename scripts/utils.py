### Util functions ###

import pygame, editing, config as c

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

# Checks if the cursor is in a valid position in the buffer and if not fixes it
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
def take_inputs(key, cursor_location, buffer, last_y):

    if pygame.key.get_mods() & pygame.KMOD_CTRL:
        step = c.large_step
    else: 
        step = 1

    # Navigate cursor with arrow keys
    if key == pygame.K_LEFT:
        # Check if its moving lines or moving on one line
        if cursor_location[1] == 0 and cursor_location[0] != 0:
            cursor_location[0] -= 1
            cursor_location[1] = len(buffer[cursor_location[0]])
        else:
            cursor_location[1] -= step

            last_y = cursor_location[1]
            make_cursor_pos_valid(buffer, cursor_location)

    elif key == pygame.K_RIGHT:
        # Check if its moving lines or moving on one line
        if cursor_location[1] == len(buffer[cursor_location[0]]) and cursor_location[0] < len(buffer) - 1:
            cursor_location[0] += 1
            cursor_location[1] = 0
        else: 
            cursor_location[1] += step

            last_y = cursor_location[1]
            make_cursor_pos_valid(buffer, cursor_location)
    
    elif key == pygame.K_DOWN:
        cursor_location[0] += step
        cursor_location[1] = last_y

        # Move to end of line if at the last line
        if cursor_location[0] == len(buffer):
            cursor_location[1] = len(buffer[cursor_location[0] - 1])

        make_cursor_pos_valid(buffer, cursor_location)
    
    elif key == pygame.K_UP:
        cursor_location[0] -= step
        cursor_location[1] = last_y
        
        make_cursor_pos_valid(buffer, cursor_location)
    
    return cursor_location, last_y
