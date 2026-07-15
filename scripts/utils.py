### Util functions ###

import pygame

# Reads the data from the specified file
def read_file(filename):
    with open(filename, "r") as txt_file:
        return txt_file.read()

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

# Take in lots of info from main.py and process movement
def move_cursor(key, cursor_location, step, buffer, last_y):
    # Navigate cursor with arrow keys
    if key == pygame.K_LEFT:
        cursor_location[1] -= step

        last_y = cursor_location[1]
        make_cursor_pos_valid(buffer, cursor_location)

    elif key == pygame.K_RIGHT:
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
