### Editng functions ###

import config as c

# States repeatedly references as 's' to shorten code and improve readibility


# Handle hitting enter for a new line
def new_line(s):
    # Try-except incase the line is empty
    try:
        len(s.buffer[s.cursor_location[0]])

        # Split line into parts to seperate them
        current_line = s.buffer[s.cursor_location[0]]
        left = current_line[ : s.cursor_location[1]]
        right = current_line[s.cursor_location[1]:]

        # Split the two onto different lines
        s.buffer[s.cursor_location[0]] = left
        s.buffer.insert(s.cursor_location[0] + 1, right)
    except IndexError:
        # If the line is empty then create new empty line
        s.buffer.append([])

    # Fix cursor location
    s.cursor_location[0] += 1
    s.cursor_location[1] = 0

# Handle backspacing cases
def backspace(s, holding_ctrl):
    line = s.buffer[s.cursor_location[0]]
    removed_space = False

    # Delete whole word if holding control
    if holding_ctrl:
        moves = 0

        # If youre on a space, just delete that space
        try:
            if s.buffer[s.cursor_location[0]][s.cursor_location[1] - 1] == " ":
                spaces = 0

                for char in reversed(s.buffer[s.cursor_location[0]][ : s.cursor_location[1]]):
                    if char == " ": 
                        spaces += 1
                    else:
                        break

                del s.buffer[s.cursor_location[0]][s.cursor_location[1] - spaces : s.cursor_location[1]]
                s.cursor_location[1] -= spaces
                removed_space = True
            
            # Delete whole word
            if not removed_space:
                for char in reversed(line[ : s.cursor_location[1]]):
                    if char != " ":
                        moves += 1
                    else:
                        moves += 1
                        break

                # Delete characters
                start = s.cursor_location[1] - moves
                del line[start:s.cursor_location[1]]

                s.cursor_location[1] = start
        except IndexError:
            pass
    else:
        # Delete previous character in standard usage
        if s.cursor_location[1] > 0:
            s.buffer[s.cursor_location[0]].pop(s.cursor_location[1] - 1)
            s.cursor_location[1] -= 1
        
        # If line is empty then remove the \n before
        elif s.cursor_location[0] > 0:
            previous_line_len = len(s.buffer[s.cursor_location[0] - 1])
            
            # Try-except to prevent index overflow with empty line
            try:
                len(s.buffer[s.cursor_location[0]])
                # Move current lines characters to the line above
                s.buffer[s.cursor_location[0] - 1].extend(s.buffer[s.cursor_location[0]])
            
                # Remove current line
                s.buffer.pop(s.cursor_location[0])
            except IndexError:
                pass

            # Fix cursor location
            s.cursor_location[0] -= 1
            s.cursor_location[1] = previous_line_len

# Handle hitting delete key 
# Currently cannot delete on end of line to merge with next 
def delete(s, holding_ctrl):
    line = s.buffer[s.cursor_location[0]]

    # If holding control delete whole word
    if holding_ctrl:
        moves = 0

        # If youre on a space, delete only that space
        if s.cursor_location[1] < len(line) and line[s.cursor_location[1]] == " ":
            del line[s.cursor_location[1]]
        
        else: 
            for char in line[s.cursor_location[1] : ]:
                if char != " ":
                    moves += 1
                else:
                    break   
            
            # Delete word
            del line[s.cursor_location[1] : s.cursor_location[1] + moves]

    else:
        # Standard single character delete
        if s.cursor_location[1] < len(line):
            s.buffer[s.cursor_location[0]].pop(s.cursor_location[1])

# Insert given unicode character
def insert_character(s, event):
    s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], event.unicode)
    s.cursor_location[1] += 1

# Insert tab spaces
def tab(s):
    for i in range(c.tab_spaces):   

        s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], " ")
        s.cursor_location[1] += 1
