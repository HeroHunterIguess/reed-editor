### Reed, a minimalistic, customizable text editor ###

### Main logic ###

# Initial set up 
import sys, os, pygame, pygame.locals, utils, rendering, config as c
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Intial window steup
screen = pygame.display.set_mode(c.window_size)
pygame.display.set_caption("Reed editor")

cursor_location = [0, 0]
last_y = 0

# Holding repeats
held_event = None
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
            if held_event is not None and event.key == held_event.key:
                held_event = None

        # Keybinds
        if event.type == pygame.KEYDOWN:

            # Save file when control + s is clicked
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                utils.write_buffer(buffer, filepath)

                # Update unsaved alert to be gone
                changed = False
            else:
                hold_time = 0
                held_event = event
                waiting_for_initial = True

                # Initial move
                buffer, cursor_location, last_y, changed = utils.take_inputs(held_event, cursor_location, buffer, last_y, changed)
            
    ##########################

    if held_event is not None:

        hold_time += dt
        
        if waiting_for_initial and hold_time >= c.initial_delay:
            buffer, cursor_location, last_y, changed = utils.take_inputs(held_event, cursor_location, buffer, last_y, changed)
            waiting_for_initial = False
            hold_time = 0
        elif not waiting_for_initial and hold_time >= c.repeat_time:
            buffer, cursor_location, last_y, changed = utils.take_inputs(held_event, cursor_location, buffer, last_y, changed)
            hold_time = 0

    ##########################

    # Update screen
    pygame.display.flip()

# Close
pygame.quit()
