### Rendering ###

import pygame, config as c

pygame.font.init()

font = pygame.font.SysFont(c.font, c.font_size)
context_font = pygame.font.SysFont(c.font, c.context_info_size)

char_width = font.size(" ")[0]

def draw(screen, buffer, cursor_location, filepath, changed):

    # Set background
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

    ##########################

    # Display cursor @ location * char_width, with a set width of 2, and height being the line height 
    pygame.draw.rect(screen, c.cursor_color, (cursor_location[1] * char_width - 1 + c.padding_left, cursor_location[0] * c.line_height + 4, 2, c.font_size))

    # Display context menu at the bottom
    pygame.draw.rect(screen, c.context_background_color, (0, c.window_size[1] - c.line_height - c.context_background_padding_bottom, c.window_size[0], c.line_height + c.context_background_padding_bottom))

    # Draw the text for the menu
    context_text = context_font.render(filepath, True, c.context_info_color)
    screen.blit(context_text, (0, c.window_size[1] - c.line_height - c.context_info_padding_bottom))

    # Draw the alert on the context menu if the file has unsaved changes
    if changed:
        pygame.draw.circle(screen, c.unsaved_alert_color, (c.window_size[0] - c.unsaved_alert_corner_padding, c.window_size[1] - c.unsaved_alert_corner_padding), c.unsaved_alert_size)
    
    pygame.display.flip()
