### Util functions ###

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
