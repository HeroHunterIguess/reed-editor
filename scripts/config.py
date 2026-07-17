### Default Reed configuration ###
# If any variables from this file are deleted, the program will not run

import os

# General Window Settings
background_color = [39,40,43]
window_size = (1000, 650)

# Text settings
# Only monospace fonts will work properly
# Default based on operating system defaults
if os.name == "posix":
    font = "Monospace" 
elif os.name == "nt":
    font = "Cascadia Code"

text_color = (255,255,255)
font_size = 17
line_height = 20

# Padding on text position
padding_top = 1
padding_left = 3

# Context menu (default bottom w/ position locked for now)
context_info_color = (111, 110, 115)
context_info_size = 15
context_info_padding_bottom = 2
context_background_color = (22, 22, 28)
context_background_padding_bottom = 2

unsaved_alert_color = (98, 103, 152)
unsaved_alert_size = 5
unsaved_alert_corner_padding = 11

# Cursor settings
cursor_color = (255, 255, 255)
large_step = 5

# Input repeating delay (ms)
initial_delay = 430
repeat_time = 31

# View movement (pixels)
view_move_amount = 20
view_padding = 100
