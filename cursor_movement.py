### Cursor movement ###


# Checks if the cursor is in a valid position in the buffer and if not fix it
def make_cursor_pos_valid(s):
    # Vertical checks
    if s.cursor_location[0] < 0:
        s.cursor_location[0] = 0
    
    if s.cursor_location[0] > len(s.buffer) - 1:
        s.cursor_location[0] = len(s.buffer) - 1

    # Horizontal checks
    if s.cursor_location[1] > len(s.buffer[s.cursor_location[0]]):
        s.cursor_location[1] = len(s.buffer[s.cursor_location[0]])
    
    if s.cursor_location[1] < 0:
        s.cursor_location[1] = 0


def move_left(s, step):
    if s.cursor_location[1] == 0 and s.cursor_location[0] != 0:
        s.cursor_location[0] -= 1
        s.cursor_location[1] = len(s.buffer[s.cursor_location[0]])
    else:
        s.cursor_location[1] -= step

        s.last_y = s.cursor_location[1]
        make_cursor_pos_valid(s)

def move_right(s, step):
    if s.cursor_location[1] == len(s.buffer[s.cursor_location[0]]) and s.cursor_location[0] < len(s.buffer) - 1:
        s.cursor_location[0] += 1
        s.cursor_location[1] = 0
    else: 
        s.cursor_location[1] += step

        s.last_y = s.cursor_location[1]
        make_cursor_pos_valid(s)

def move_down(s, step):
    s.cursor_location[0] += step
    s.cursor_location[1] = s.last_y

    # Move to end of line if at the last line
    if s.cursor_location[0] == len(s.buffer):
        s.cursor_location[1] = len(s.buffer[s.cursor_location[0] - 1])

    make_cursor_pos_valid(s)

def move_up(s, step):
    s.cursor_location[0] -= step
    s.cursor_location[1] = s.last_y

    make_cursor_pos_valid(s)

    # Move to start of line if on first line
    if s.cursor_location[0] <= 0:
        s.cursor_location[1] = 0
