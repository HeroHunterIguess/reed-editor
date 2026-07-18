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
    line_num = s.cursor_location[0]
    line = s.buffer[line_num]

    # On first character (& not first line)
    # Runs even if you hit control backspace
    if s.cursor_location[1] == 0 and line_num != 0: 

        previous_line_length = len(s.buffer[line_num - 1])
        
        # Move characters to previous line
        s.buffer[line_num - 1].extend(line)

        # Remove current line
        s.buffer.pop(line_num)

        # Fix cursor placement
        s.cursor_location[0] -= 1
        s.cursor_location[1] = previous_line_length
    
    # In a normal case delete 1 character
    elif s.cursor_location[1] != 0:
        del s.buffer[line_num][s.cursor_location[1] - 1]
        s.cursor_location[1] -= 1
    
    ##########################

    # Runs control backspace even after deleting first char already
    if holding_ctrl:
        count = 0
        deleted_spaces = False

        # Delete spaces
        if s.cursor_location[1] > 0 and s.buffer[line_num][s.cursor_location[1] - 1] == " ":
            for char in reversed(line[ : s.cursor_location[1]]):
                if char == " ":
                    count += 1
                else:
                    deleted_spaces = True
                    break

        # Iterate through looking for word
        if not deleted_spaces:
            for char in reversed(line[ : s.cursor_location[1]]):
                if char != " ":
                    count += 1
                else:
                    break

        # Delete word and update buffer & cursor pos
        del s.buffer[line_num][s.cursor_location[1] - count : s.cursor_location[1]]
        s.cursor_location[1] -= count

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
