### Reed, a minimalistic, customizable text editor ###

# Initial set up 
import sys, os, pygame, pygame.locals, utils, config as c
pygame.init()
pygame.font.init()

cursor_location = [0, 0]

# Default path if none is passed
# This will likely be changed later
filepath = "/home/herohunter/reed_default.txt" 

# Check if a filepath was passed to the script
if len(sys.argv) > 1:
    filepath = sys.argv[1]

# Intial window steup
screen = pygame.display.set_mode(c.window_size)
pygame.display.set_caption("Reed editor")

font = pygame.font.SysFont(c.font, c.font_size)
context_font = pygame.font.SysFont(c.font, c.context_info_size)

# Create new buffer for everything in the file
buffer = [list(line) for line in utils.read_file(filepath).splitlines()]

if not buffer:
    buffer = [[]]

# Keep track of if buffer has changed since last save
changed = False


# Begin update/processing loop
running = True

while running:
    screen.fill(c.background_color)

    # Start text at the top of the screen (+ padding)
    y = c.padding_top

    # Render main text
    for line_chars in buffer:

        # Join into full lines
        line = "".join(line_chars)

        # Display it
        text_surface = font.render(line, True, c.text_color)
        screen.blit(text_surface, (c.padding_left,y))

        y += c.line_height


    # Display cursor @ location * 9 (9 is character width), with a set width of 2, and height being the line height 
    pygame.draw.rect(screen, c.cursor_color, (cursor_location[1] * 9 - 1 + c.padding_left, cursor_location[0] * c.line_height + 4, 2, c.font_size))

    # Display context menu at the bottom
    pygame.draw.rect(screen, c.context_background_color, (0, c.window_size[1] - c.line_height - c.context_background_padding_bottom, c.window_size[0], c.line_height + c.context_background_padding_bottom))

    # Draw the text for the menu
    context_text = context_font.render(filepath, True, c.context_info_color)
    screen.blit(context_text, (0, c.window_size[1] - c.line_height - c.context_info_padding_bottom))

    # Draw the alert on the context menu if the file has unsaved changes
    if changed:
        pygame.draw.circle(screen, c.unsaved_alert_color, (c.window_size[0] - c.unsaved_alert_corner_padding, c.window_size[1] - c.unsaved_alert_corner_padding), c.unsaved_alert_size)


    # Handle all inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keybinds
        if event.type == pygame.KEYDOWN:

            # Navigate cursor with arrow keys
            if event.key == pygame.K_LEFT:
                cursor_location[1] -= 1

                utils.make_cursor_pos_valid(buffer, cursor_location)

            elif event.key == pygame.K_RIGHT:
                cursor_location[1] += 1

                utils.make_cursor_pos_valid(buffer, cursor_location)
            
            elif event.key == pygame.K_DOWN:
                cursor_location[0] += 1

                utils.make_cursor_pos_valid(buffer, cursor_location)
            
            elif event.key == pygame.K_UP:
                cursor_location[0] -= 1
                
                utils.make_cursor_pos_valid(buffer, cursor_location)


            # Allow backspace to delete characters
            elif event.key == pygame.K_BACKSPACE:
                # If in standard usage delete previous character
                if cursor_location[1] > 0:
                    buffer[cursor_location[0]].pop(cursor_location[1] - 1)
                    cursor_location[1] -= 1
                
                # If line is empty then remove the \n before
                elif cursor_location[0] > 0:
                    previous_line_len = len(buffer[cursor_location[0] - 1])
                    
                    # Try-except to prevent index overflow with empty line
                    try:
                        len(buffer[cursor_location[0]])
                        # Move current lines characters to the line above
                        buffer[cursor_location[0] - 1].extend(buffer[cursor_location[0]])
                    
                        # Remove current line
                        buffer.pop(cursor_location[0])
                    except IndexError:
                        pass

                    # Fix cursor location
                    cursor_location[0] -= 1
                    cursor_location[1] = previous_line_len
                
                changed = True
            
            # Allow enter to add new line
            elif event.key == pygame.K_RETURN:
                # Try-except incase the line is empty
                try:
                    len(buffer[cursor_location[0]])

                    # Split line into parts to seperate them
                    current_line = buffer[cursor_location[0]]
                    left = current_line[:cursor_location[1]]
                    right = current_line[cursor_location[1]:]

                    # Split the two onto different lines
                    buffer[cursor_location[0]] = left
                    buffer.insert(cursor_location[0] + 1, right)
                except IndexError:
                    # If the line is empty then create new empty line
                    buffer.append([])

                # Fix cursor location
                cursor_location[0] += 1
                cursor_location[1] = 0

                changed = True

            
            # Save file when control + s is clicked
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                utils.write_buffer(buffer, filepath)

                # Update unsaved alert to be gone
                changed = False
            
            # Insert character
            elif event.unicode:
                buffer[cursor_location[0]].insert(cursor_location[1], event.unicode)
                cursor_location[1] += 1

                changed = True

    # Update screen
    pygame.display.flip()

# Close
pygame.quit()
