### Reed, a minimalistic, customizable text editor ###

### Main logic ###

# Initial set up 
import sys, os, pygame, pygame.locals, utils, rendering, editing, config as c
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Intial window steup
screen = pygame.display.set_mode(c.window_size)
pygame.display.set_caption("Reed editor")

cursor_location = [0, 0]
last_y = 0

# Holding repeats
held_key = None
hold_time = 0
waiting_for_initial = False

# Default path if none is passed
# This will likely be changed later
filepath = "/home/herohunter/reed_default.txt" 

# Check if a filepath was passed to the script
if len(sys.argv) > 1:
    filepath = sys.argv[1]

##########################

# Create new buffer for everything in the file
buffer = [list(line) for line in utils.read_file(filepath).splitlines()]

if not buffer:
    buffer = [[]]

# Keep track of if buffer has changed since last save
changed = False

##########################

# Begin update/processing loop
running = True

while running:

    # Limit fps
    dt = clock.tick(60)

    # Draw screen
    rendering.draw(screen, buffer, cursor_location, filepath, changed)

    ##########################

    keys = pygame.key.get_pressed()

    # Handle all inputs
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        # Clear held key
        if event.type == pygame.KEYUP:
            if event.key == held_key:
                held_key = None

        # Keybinds
        if event.type == pygame.KEYDOWN:
            
            # Keep track of held arrow keys
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                held_key = event.key
                hold_time = 0
                waiting_for_initial = True

                # Initial move
                cursor_location, last_y = utils.take_inputs(held_key, cursor_location, buffer, last_y)

            ##########################

            # Allow backspace to delete characters
            if event.key == pygame.K_BACKSPACE:
                editing.backspace(buffer, cursor_location)
                
                changed = True
            
            # Allow delete key to function properly
            elif event.key == pygame.K_DELETE:
                # Delete next character
                editing.delete(buffer, cursor_location)

            # Allow enter to add new line
            elif event.key == pygame.K_RETURN:
                editing.new_line(buffer, cursor_location)
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

    ##########################

    if held_key is not None:

        hold_time += dt
        
        if waiting_for_initial and hold_time >= c.initial_delay:
            cursor_location, last_y = utils.take_inputs(held_key, cursor_location, buffer, last_y)
            waiting_for_initial = False
            hold_time = 0
        elif not waiting_for_initial and hold_time >= c.repeat_time:
            cursor_location, last_y = utils.take_inputs(held_key, cursor_location, buffer, last_y)
            hold_time = 0

    ##########################

    # Update screen
    pygame.display.flip()

# Close
pygame.quit()
