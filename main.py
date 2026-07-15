# Reed, a minimalistic, customizable text editor

import sys, os, pygame, config as c
pygame.init()

# initial setup
static_file_data = ""

cursor_location = [0, 0]

filepath = "/home/herohunter/reed_default.txt" # default path

# check if a filepath was passed as an argument to the script
if len(sys.argv) > 1:
    filepath = sys.argv[1]

# intial window steup
screen = pygame.display.set_mode(c.window_size)
pygame.display.set_caption("Reed editor")

pygame.font.init()
font = pygame.font.SysFont(c.font, c.font_size)
context_font = pygame.font.SysFont(c.font, c.context_info_size)

running = True

def read_file(filename):
    with open(filename, "r") as txt_file:
        return txt_file.read()

if filepath:
    static_file_data = read_file(filepath)

buffer = [list(line) for line in static_file_data.splitlines()]
if not buffer:
    buffer = [[]]

# check if the cursor is in a valid position and if not then fix it
def make_cursor_pos_valid(buffer, cursor_location):
    if cursor_location[1] > len(buffer[cursor_location[0]]):
        cursor_location[1] = current_line_length
    
    if cursor_location[1] < 0:
        cursor_location[1] = 0
    
    if cursor_location[0] < 0:
        cursor_location[0] = 0
    
    if cursor_location[0]

# begin update loop
while running:
    pygame.time.delay(60)

    screen.fill(c.background_color)

    # start text y at 0
    y = 0

    # render text
    for line_chars in buffer:

        line = "".join(line_chars)

        text_surface = font.render(line, True, c.text_color)
        screen.blit(text_surface, (0,y))

        y += c.line_height

    # display cursor
    pygame.draw.rect(screen, c.cursor_color, (cursor_location[1] * 9 - 1, cursor_location[0] * c.line_height + 4, 2, c.font_size))

    # display context menu
    pygame.draw.rect(screen, c.context_background_color, (0, c.window_size[1] - c.line_height - c.context_background_padding_bottom, c.window_size[0], c.line_height + c.context_background_padding_bottom))

    context_text = context_font.render(filepath, True, c.context_info_color)
    screen.blit(context_text, (0, c.window_size[1] - c.line_height - c.context_info_padding_bottom))

    # allow window to close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # keybinds
        if event.type == pygame.KEYDOWN:

            # navigate cursor with arrows
            if event.key == pygame.K_LEFT:
                cursor_location[1] -= 1

                make_cursor_pos_valid(buffer, cursor_location)

            if event.key == pygame.K_RIGHT:
                cursor_location[1] += 1

                make_cursor_pos_valid(buffer, cursor_location)
            
            if event.key == pygame.K_DOWN:
                cursor_location[0] += 1

                make_cursor_pos_valid(buffer, cursor_location)
            
            if event.key == pygame.K_UP:
                cursor_location[0] -= 1
                
                make_cursor_pos_valid(buffer, cursor_location)

            # backspace
            if event.key == pygame.K_BACKSPACE:
                if cursor_location[1] > 0:
                    buffer[cursor_location[0]].pop(cursor_location[1] - 1)
                    cursor_location[1] -= 1

    # update screen
    pygame.display.flip()

pygame.quit()
