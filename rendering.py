### Rendering ###


import utils
from config import c

import pyglet
from pyglet import shapes

# Initialization

y_offset = 0
x_offset = 0


# Alter offests
def alter_y_offset(negative, amount):
    global y_offset

    if negative:
        y_offset -= amount
    else:
        y_offset += amount

def alter_x_offset(negative, amount):
    global x_offset

    if negative:
        x_offset -= amount
    else:
        x_offset += amount

# Set offsets
def set_x_offset(amount):
    global x_offset
    x_offset = amount

def set_y_offset(amount):
    global y_offset
    y_offset = amount

# Get offsets
def get_x_offset():
    return x_offset

def get_y_offset():
    return y_offset


# Draw everything in the window
def draw(window, s): # s = states (shortened because of already long lines here) 
    font = pyglet.font.load(c.font, c.font_size)
    char_width = font.get_glyphs(" ")[0].advance

    # Clear screen
    window.clear()

    # Set background
    #screen.fill(c.background_color)

    # Find visible lines
    start_index = max(0, (y_offset // c.line_height) - c.buffer_lines)
    end_index = min(len(s.buffer), ((y_offset + c.window_size[1]) // c.line_height) + c.buffer_lines)

    # Highlight current line
    highlight = shapes.Rectangle(0, (s.cursor_location[0] * c.line_height + c.padding_top - y_offset), c.window_size[0], c.line_height, c.current_line_highlight_color)
    highlight.draw()

    # Start text at the top of the screen (+ padding)
    y = c.padding_top + (start_index * c.line_height)

    line_num = 0

    # Render main text
    for line_index in range(start_index, end_index):
        line_chars = s.buffer[line_index]

        # Join text into full lines
        line = "".join(line_chars)

        # Display it
        
        if c.line_numbers:
            text = pyglet.text.Label(line, c.font, c.font_size, c.padding_left - x_offset + c.line_number_width, y - y_offset)
        #else:
        #    screen.blit(c.padding_left - x_offset, y - y_offset)

        text.draw()

        y += c.line_height
    
    # Display cursor @ location * char_width, with a set width of 2, and height being the line height 
    if c.line_numbers: # Improve this if so its only 1 of these cursor lines
        pygame.draw.rect(screen, c.cursor_color, (s.cursor_location[1] * char_width - 1 + c.padding_left - x_offset + c.line_number_width, s.cursor_location[0] * c.line_height + 2 - y_offset, 2, c.font_size+ 1))
    else:
        pygame.draw.rect(screen, c.cursor_color, (s.cursor_location[1] * char_width - 1 + c.padding_left - x_offset, s.cursor_location[0] * c.line_height + 4 - y_offset, 2, c.font_size))

    # Draw line numbers always with background behind them to cover text
    if c.line_numbers:
        # Background
        pygame.draw.rect(screen, c.line_number_background_color, (0, 0, c.line_number_width, c.window_size[1] - c.context_info_size))

        y = c.padding_top + (start_index * c.line_height)

        # Actual line numbers
        for line_index in range(start_index, end_index):
            line_num = line_index + 1

            line_number_surface = line_number_font.render(str(line_num), True, c.line_number_color)
            
            screen.blit(line_number_surface, (c.padding_left , y - y_offset + (c.line_height - line_number_font.get_height()) // 2 + c.vertical_number_offset))

            y += c.line_height

    ##########################

    # Display context menu background at the bottom
    pygame.draw.rect(screen, c.context_background_color, (0, c.window_size[1] - c.line_height - c.context_background_padding_bottom, c.window_size[0], c.line_height + c.context_background_padding_bottom))

    # Draw the text for the menu
    context_text = context_font.render(s.filepath, True, c.context_info_color)
    cursor_location_info = context_font.render("   [ "+str(s.cursor_location[0]+1)+","+str(s.cursor_location[1]+1)+" ]", True, c.context_info_color)

    screen.blit(context_text, (0 + c.context_info_padding, c.window_size[1] - c.line_height - c.context_info_padding))
    screen.blit(cursor_location_info, (c.window_size[0] - cursor_location_info.get_width() - c.unsaved_alert_size - c.context_info_padding - 12, c.window_size[1] - c.line_height - c.context_info_padding))

    # Draw the alert on the context menu if the file has unsaved changes
    if s.changed:
        pygame.draw.circle(screen, c.unsaved_alert_color, (c.window_size[0] - c.unsaved_alert_corner_padding, c.window_size[1] - c.unsaved_alert_corner_padding), c.unsaved_alert_size)
