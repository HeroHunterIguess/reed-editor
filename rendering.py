### Rendering ###


import pygame, utils
from config import c

# Initialization
pygame.font.init()

font = pygame.font.SysFont(c.font, c.font_size)
context_font = pygame.font.SysFont(c.font, c.context_info_size)
line_number_font = pygame.font.SysFont(c.font, c.line_number_text_size)

char_width = font.size(" ")[0]

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

def highlight(screen, width, height, x, y):
    highlight = pygame.Surface((width, height), pygame.SRCALPHA)
    highlight.fill(c.highlight_color)

    screen.blit(highlight, (x - x_offset, y - y_offset))

def draw_selection(screen, s):
    height = c.line_height

    # Normalize start & end 
    start = tuple(s.selection_start)
    end = tuple(s.selection_end)

    if start > end:
        start, end = end, start

    # If selection is on one line
    if start[0] == end[0]:
        x = start[1] * char_width + c.line_number_width + c.padding_left
        y = (start[0]) * c.line_height + c.padding_top
        width = (end[1] - start[1]) * char_width

        highlight(screen, width, height, x, y)
    else:
        # If selection is multiple lines
        amount_of_lines = end[0] - start[0] + 1
        current_line = start[0]

        for i in range(amount_of_lines):
            y = current_line * c.line_height + c.padding_top

            if current_line == start[0]:
                x = start[1] * char_width + c.padding_left + c.line_number_width
                width = len(s.buffer[current_line][start[1] : ]) * char_width

                highlight(screen, width, height, x, y)
            
            elif current_line == end[0]:
                x = c.padding_left + c.line_number_width
                width = end[1] * char_width

                highlight(screen, width, height, x, y)
            
            else: # for all lines in between
                x = c.padding_left + c.line_number_width
                width = len(s.buffer[current_line]) * char_width

                highlight(screen, width, height, x, y)
            
            # Add single space highlight if line is empty
            if len(s.buffer[current_line]) == 0:
                highlight(screen, char_width, c.line_height, c.padding_left + c.line_number_width, y)
            
            current_line += 1

# IMAGE
if c.background_image_location != "":
    image = pygame.image.load(c.background_image_location)
    imagerect = image.get_rect()
    has_image = True
else:
    has_image = False


# Draw everything in the window
def draw(screen, s): # s = states (shortened because of already long lines here) 

    # Set background
    screen.fill(c.background_color)

    # Draw background image if one is set
    if has_image:
        screen.blit(image, imagerect)
        
    # Find visible lines
    start_index = max(0, (y_offset // c.line_height) - c.buffer_lines)
    end_index = min(len(s.buffer), ((y_offset + c.window_size[1]) // c.line_height) + c.buffer_lines)

    # Highlight current line
    pygame.draw.rect(screen, c.current_line_highlight_color, (0, s.cursor_location[0] * c.line_height + c.padding_top - y_offset, c.window_size[0], c.line_height))

    # Highlight selected area
    if s.selecting:
        draw_selection(screen, s)

    # Start text at the top of the screen (+ padding)
    y = c.padding_top + (start_index * c.line_height)

    line_num = 0

    # Render main text
    for line_index in range(start_index, end_index):
        line_chars = s.buffer[line_index]

        # Join text into full lines
        line = "".join(line_chars)

        # Display it
        text_surface = font.render(line, True, c.text_color)
        if c.line_numbers:
            screen.blit(text_surface, (c.padding_left - x_offset + c.line_number_width, y - y_offset))
        else:
            screen.blit(text_surface, (c.padding_left - x_offset, y - y_offset))

        y += c.line_height
    
    # Display cursor @ location * char_width, with a set width of 2, and height being the line height 
    if c.line_numbers: # Improve this if so its only 1 of these cursor lines
        pygame.draw.rect(screen, c.cursor_color, (s.cursor_location[1] * char_width - 1 + c.padding_left - x_offset + c.line_number_width, s.cursor_location[0] * c.line_height - y_offset + 1, 2, c.line_height))
    else:
        pygame.draw.rect(screen, c.cursor_color, (s.cursor_location[1] * char_width - 1 + c.padding_left - x_offset, s.cursor_location[0] * c.line_height + 4 - y_offset, 2, c.line_height))

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
    truncated_name = s.filepath[ : c.max_filename_length]
    if not len(truncated_name) == len(s.filepath):
        truncated_name += "..." 

    context_text = context_font.render(truncated_name, True, c.context_info_color)
    cursor_location_info = context_font.render("   [ "+str(s.cursor_location[0]+1)+","+str(s.cursor_location[1]+1)+" ]", True, c.context_info_color)

    screen.blit(context_text, (0 + c.context_info_padding, c.window_size[1] - c.line_height - c.context_info_padding))
    screen.blit(cursor_location_info, (c.window_size[0] - cursor_location_info.get_width() - c.unsaved_alert_size - c.context_info_padding - 12, c.window_size[1] - c.line_height - c.context_info_padding))

    # Draw the alert on the context menu if the file has unsaved changes
    if s.changed:
        pygame.draw.circle(screen, c.unsaved_alert_color, (c.window_size[0] - c.unsaved_alert_corner_padding, c.window_size[1] - c.unsaved_alert_corner_padding), c.unsaved_alert_size)
