### Editng functions ###


import pyperclip, utils, cursor_movement
from config import c

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

    s.history.append({"action": "new_line"})

# Delete all text in a selection
def delete_selection(s):
    start = tuple(s.selection_start)
    end = tuple(s.selection_end)

    if start > end:
        start, end = end, start
    
    selection_data = utils.get_selection(s)

    # Delete single line selection
    if start[0] == end[0]:
        del s.buffer[start[0]][start[1] : end[1]]
    # Delete multi-line selection
    else:
        first = s.buffer[start[0]][ : start[1]]
        last = s.buffer[end[0]][end[1] : ]

        s.buffer[start[0]] = first + last

        del s.buffer[start[0] + 1 : end[0] + 1]
    
    # Fix cursor pos
    s.cursor_location = list(start)

    # End selection
    utils.end_selection(s)

    return selection_data

# Handle backspacing cases
def backspace(s, holding_ctrl):
    line_num = s.cursor_location[0]
    line = s.buffer[line_num]

    if s.selecting:
        data = delete_selection(s)
        s.history.append({"action": "backspace", 
                          "type": "selection",
                          "data": data})
        return

    # On first character (& not first line)
    # Runs even if you hit control backspace
    if s.cursor_location[1] == 0 and line_num != 0: 

        previous_line_length = len(s.buffer[line_num - 1])
        
        # Move characters to previous line
        s.buffer[line_num - 1].extend(line)

        # Remove current line
        s.buffer.pop(line_num)
        line_num -= 1

        s.history.append({"action": "backspace",
                          "type": "line", 
                          "data": s.cursor_location})

        # Fix cursor placement
        s.cursor_location[0] -= 1
        s.cursor_location[1] = previous_line_length
    
    # In a normal case delete 1 character
    elif s.cursor_location[1] != 0:
        s.history.append({"action": "backspace",
                          "type": "char",
                          "data": s.buffer[line_num][s.cursor_location[1] - 1]})
        del s.buffer[line_num][s.cursor_location[1] - 1]
        s.cursor_location[1] -= 1
    
    ##########################

    # Runs control backspace even after deleting first char already - This is intended
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
                if char != " " and char != "." and char != "(" and char != ")":
                    count += 1
                else:
                    break

        # Delete word and update buffer & cursor pos
        s.history.append({"action": "backspace", 
                          "type": "word",
                          "data": s.buffer[line_num][s.cursor_location[1] - count : s.cursor_location[1]]})
        del s.buffer[line_num][s.cursor_location[1] - count : s.cursor_location[1]]
        s.cursor_location[1] -= count

# Handle hitting delete key 
def delete(s, holding_ctrl):

    if s.selecting:
        data = delete_selection(s)
        s.history.append({"action": "delete",
                          "type": "selection",
                          "data": data})
        return

    line_num = s.cursor_location[0]
    line = s.buffer[line_num]

    # On last character
    # Runs even if you hit control delete
    if s.cursor_location[1] == len(line) and line_num < len(s.buffer) - 1: 
        
        # Move characters from next line
        s.buffer[line_num].extend(s.buffer[line_num + 1])

        # Remove next line
        s.buffer.pop(line_num + 1)

        s.history.append({"action": "delete",
                          "type": "line",
                          "data": s.cursor_location})
    
    # In a normal case delete 1 character
    elif s.cursor_location[1] < len(s.buffer[s.cursor_location[0]]):
        s.history.append({"action": "delete",
                          "type": "char",
                          "data": s.buffer[line_num][s.cursor_location[1]]})
        del s.buffer[line_num][s.cursor_location[1]]
    
    ##########################

    # Runs control delete even after deleting first char already - This is intended
    if holding_ctrl:
        count = 0
        deleted_spaces = False

        # Delete spaces
        if s.cursor_location[1] < len(line) and s.buffer[line_num][s.cursor_location[1]] == " ":
            for char in line[s.cursor_location[1] : ]:
                if char == " ":
                    count += 1
                else:
                    deleted_spaces = True
                    break

        # Iterate through looking for word
        if not deleted_spaces:
            for char in line[s.cursor_location[1] : ]:
                if char != " ":
                    count += 1
                else:
                    break

        # Delete word and update buffer & cursor pos
        s.history.append({"action": "delete", 
                          "type": "word",
                          "data": s.buffer[line_num][s.cursor_location[1] : s.cursor_location[1] + count]})
        del s.buffer[line_num][s.cursor_location[1] : s.cursor_location[1] + count]

# Insert given unicode character
def insert_character(s, event):

    if s.selecting:
        delete_selection(s)

    s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], event.unicode)
    s.cursor_location[1] += 1

    s.history.append({"action": "insert_character", 
                      "data": event.unicode})

# Insert tab spaces
def tab(s):

    if s.selecting:
        delete_selection(s)
    
    for i in range(c.tab_spaces):   

        s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], " ")
        s.cursor_location[1] += 1
    
    s.history.append({"action": "tab"})

# Paste text from users clipboard
def paste_text(s):

    if s.selecting:
        delete_selection(s)

    data = pyperclip.paste().splitlines()
    line_num = s.cursor_location[0]
    chars = []

    # Find parts of current line
    left = s.buffer[s.cursor_location[0]][ : s.cursor_location[1]]
    right = s.buffer[s.cursor_location[0]][s.cursor_location[1] : ]

    for ind in range(len(data)):
        chars = list(data[ind])

        # Paste text based on cursor location
        if len(data) == 1:
            s.buffer[s.cursor_location[0]] = left + chars + right
        elif ind == 0:
            s.buffer[s.cursor_location[0]] = left + chars
        elif ind == len(data) - 1:
            s.buffer.insert(line_num, chars + right)
        else:
            s.buffer.insert(line_num, chars)
    
        line_num += 1
    
    # Update cursor position
    s.cursor_location[0] = line_num - 1
    s.cursor_location[1] += len(chars)

    s.history.append({"action": "paste_text",
                      "data": data})

# Undo single action
def undo(s):
    history_index = len(s.history) - 1

    if history_index < 0:
        return
    
    # If data is empty then no real action was taken so delete it and exit
    if s.history[history_index]["action"] != "tab" and s.history[history_index]["action"] != "new_line" # Types with no data
        if s.history[history_index]["data"] == []:
            s.history.pop(history_index)
            return
    
    print(s.history)

    # Standard character insert
    if s.history[history_index]["action"] == "insert_character":
        del s.buffer[s.cursor_location[0]][s.cursor_location[1] - 1]

        s.cursor_location[1] -= 1
    
    # All backspace/delete actions
    elif s.history[history_index]["action"] == "backspace" or s.history[history_index]["action"] == "delete":
        # Adding back a character
        if s.history[history_index]["type"] == "char":
            s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], s.history[history_index]["data"])

            # Only move cursor if it was with backspace
            if s.history[history_index]["action"] == "backspace":
                s.cursor_location[1] += 1

        # Adding back a word
        elif s.history[history_index]["type"] == "word":
            # Add first delete back
            if s.history[history_index]["action"] == "delete":
                s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], s.history[history_index - 1]["data"])

            s.cursor_location[1] += 1

            # Loop through adding characters back
            for i in range(len(s.history[history_index]["data"])):
                s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], s.history[history_index]["data"][i])

                s.cursor_location[1] += 1

            # Backspace removes one character then rest of word so restore that one character
            if s.history[history_index]["action"] == "backspace":
                s.buffer[s.cursor_location[0]].insert(s.cursor_location[1], s.history[history_index - 1]["data"])
                s.cursor_location[1] += 1
            
            if s.history[history_index]["action"] == "delete":
                s.cursor_location[1] -= len(s.history[history_index]["data"]) + 1
            
            s.history.pop(history_index - 1)

        # Adding back a line
        elif s.history[history_index]["type"] == "line":
            cursor_history_location = s.history[history_index]["data"]
            left = s.buffer[cursor_history_location[0]][cursor_history_location[1] : ]
            right = s.buffer[cursor_history_location[0]][ : cursor_history_location[1]]

            s.buffer[s.cursor_location[0]] = left
            s.buffer.insert(s.cursor_location[0], right)
 
            if s.history[history_index]["action"] == "backspace":
                s.cursor_location[0] += 1
                s.cursor_location[1] = 0
    
    history_index -= 1
    s.history.pop(history_index)

    cursor_movement.make_cursor_pos_valid(s)

# Redo single action
# Will not be implimented in the current version - it may come later
def redo(s):
    pass
