### Reed, a minimalistic, customizable text editor ###

### Main logic ###


# Initial set up 
import sys, os, pygame, pygame.locals, utils, state, editing, rendering
from config import c

pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(c.window_size)
pygame.display.set_caption("Reed editor")

# Load char_width into utils
utils.initialize(rendering.char_width)

# Default path if none is passed
# This will likely be changed later
if os.name == "posix":
    filepath = "/home/herohunter/reed_default.txt" 
elif os.name == "nt":
    filepath = os.path.join(os.path.expanduser("~"), "reed_default.txt") # Windows path hasnt been teste

# Check if a filepath was passed to the script
if len(sys.argv) > 1:
    filepath = sys.argv[1]

##########################

# Create new buffer for everything in the file
buffer = [list(line) for line in utils.read_file(filepath).splitlines()]

if not buffer:
    buffer = [[]]

# Initialize states w/ all requires editor states
# Throughout the program states is commonly referred to as s
states = state.editor_states(
    buffer = buffer,
    cursor_location = [0, 0],
    filepath = filepath,
    history = []
)

##########################

# Begin update/processing loop
running = True

while running:

    # Limit fps
    dt = clock.tick(60)

    # Draw screen
    rendering.draw(screen, states)

    ##########################

    keys = pygame.key.get_pressed()

    # Handle main inputs
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        # Clear held key
        if event.type == pygame.KEYUP:
            if states.held_event is not None and event.key == states.held_event.key:
                states.held_event = None

        # Keybinds
        if event.type == pygame.KEYDOWN:

            # Save file when control + s is clicked
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                utils.write_buffer(states)

                # Update unsaved alert to be gone
                states.changed = False
            
            # Allow ctrl+c to copy entire file 
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                utils.copy_all(states.buffer)
            
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                editing.paste_text(states)
            
            # All initial inputs
            else:
                states.hold_time = 0
                states.held_event = event
                states.waiting_for_initial = True

                # Initial move
                utils.take_inputs(states, event)
            
    ##########################

    # Repeat inputs if they are held
    if states.held_event is not None:

        states.hold_time += dt
        
        # First input after intial_delay
        if states.waiting_for_initial and states.hold_time >= c.initial_delay:
            utils.take_inputs(states, states.held_event)
            states.waiting_for_initial = False
            states.hold_time = 0
        # Repeating at a delay of repeat_time 
        elif not states.waiting_for_initial and states.hold_time >= c.repeat_time:
            utils.take_inputs(states, states.held_event)
            states.hold_time = 0

    ##########################

    # Keep cursor on screen
    utils.fix_camera_pos(states)

    # Update screen
    pygame.display.flip()

# Close
pygame.quit()
