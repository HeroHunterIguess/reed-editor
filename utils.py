### Util functions ###


import pygame, pyperclip, editing, cursor_movement, os, subprocess, shutil, rendering as r
from config import c

char_width = 0

# Check if user has wl-clipboard
if os.name == "posix":
    has_wl_clipboard = shutil.which("wl-copy") is not None

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

def get_selection(s):
    lines = []

    # Normalize
    start = tuple(s.selection_start)
    end = tuple(s.selection_end)

    if start > end:
        start, end = end, start

    # Single line 
    if start[0] == end[0]:
        line = s.buffer[start[0]][start[1] : end[1]]

        lines.append(line)

        # Copy
        return lines
    
    # Multiline
    else:
        # First line
        lines.append(s.buffer[start[0]][start[1] : ])

        # Middle lines
        for line_num in range(start[0] + 1, end[0]):
            lines.append(s.buffer[line_num])

        # Last line
        lines.append(s.buffer[end[0]][ : end[1]])
    
        # Return all lines in the selection
        return lines

# Copy text from buffer or selection
def copy_text(s):
    lines = []

    # Copy whole file
    if not s.selecting:
        # Turn buffer into standard text
        for line_chars in s.buffer:
            line = "".join(line_chars)

            lines.append(line)

        text = "\n".join(lines)

        pyperclip.copy(text)
    
    # Copy selection
    else:
        # Turn into standard text to copy

        for line in get_selection(s):
            lines.append("".join(line))
            print(line)
        
        final = "\n".join(lines)

        # If on linux and single character then use script to fix weird wl-copy behavior
        if os.name == "posix" and len(final) == 1 and has_wl_clipboard:
            subprocess.run(f"/bin/bash -c \"wl-copy {final}\"", shell = True)
        else:
            pyperclip.copy(final)

def end_selection(s):
    s.selecting = False
    s.selection_start = (-1, -1)
    s.selection_end = (-1, -1)

def selection(s, dir):
    s.selecting = True
    if s.selection_start == (-1, -1): # (-1,-1) is no selection
        s.selection_start = s.cursor_location.copy()
    if dir == "right":
        cursor_movement.move_right(s, 1, False)
    elif dir == "left":
        cursor_movement.move_left(s, 1, False)
    elif dir == "down":
        cursor_movement.move_down(s, 1, False)
    elif dir == "up":
        cursor_movement.move_up(s, 1, False)
    s.selection_end = s.cursor_location.copy()

# Select all text in the file
def select_all(s):
    s.selecting = True
    s.selection_start = [0,0]
    s.selection_end = [len(s.buffer) - 1, len(s.buffer[len(s.buffer) - 1])]
    s.cursor_location = s.selection_end

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
            cursor_movement.move_left(s, step, True)
        else:
            # Select text
            selection(s, "left")

    elif event.key == pygame.K_RIGHT:
        # Check if its moving lines or moving on one line
        if not holding_shift:
            cursor_movement.move_right(s, step, True)
        else:
            # Select text
            selection(s, "right")
        
    elif event.key == pygame.K_DOWN:
        if not holding_shift:
            cursor_movement.move_down(s, step, True)
        else:
            # Select text
            selection(s, "down")
        
    elif event.key == pygame.K_UP:
        if not holding_shift:
            cursor_movement.move_up(s, step, True)
        else:
            # Select text
            selection(s, "up")

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

        s.last_y = s.cursor_location[1]

        s.changed = True
    
    # Tab character 
    elif event.key == pygame.K_TAB:
        editing.tab(s)

        s.changed = True
    
    print(s.history)

def fix_camera_pos(s):
    # If cursor moves -> move camera
    if (s.cursor_location[0]+2) * c.line_height > c.window_size[1] + r.get_y_offset():
        r.set_y_offset(((s.cursor_location[0] + 1) * c.line_height + c.padding_top + 3) - (c.window_size[1] - c.line_height))
    elif s.cursor_location[0] * c.line_height - r.get_y_offset() < 0:
        r.set_y_offset(c.line_height * s.cursor_location[0])
 
    # Fix horizontal position

    # is this if statement stupid or okay? i really dont know
    if (s.cursor_location[1] * char_width) + c.padding_left + c.line_number_width - r.get_x_offset() > c.window_size[0]:
        r.set_x_offset(s.cursor_location[1] * char_width + c.padding_left + c.line_number_width - c.window_size[0])
    if s.cursor_location[1] * char_width < r.get_x_offset():
        r.set_x_offset(s.cursor_location[1] * char_width)
