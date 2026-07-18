#########################################
### Reed Editor default configuration ###
#########################################

# WARNING:
# If any variables from this file are deleted, the program will not run

# You may modify any values in here - just keep in mind its easy to make it look messed up


import os # This only exists to choose defaults based on OS


#############################
## General Window Settings ##
#############################

background_color = (35, 35, 41)
window_size = (700, 450)


###################
## Text settings ##
###################

# Only monospace fonts will work properly
# Default fonts are selected based on the operating system

if os.name == "posix":
    font = "Monospace" 
elif os.name == "nt":
    font = "Cascadia Code"

text_color = (216, 216, 237)

font_size = 17
line_height = 20


###################
## Text position ##
###################

padding_top = 1
padding_left = 3


#############################
## Status bar/Context menu ## 
#############################

context_info_color = (142, 135, 163) # (text color)
context_background_color = (24, 23, 31)

context_info_size = 17 # (text size)

context_info_padding = 2
context_background_padding_bottom = 2


###############################
## Unsaved changes indicator ##
###############################

unsaved_alert_color = (143, 135, 173)

unsaved_alert_size = 5
unsaved_alert_corner_padding = 11


#####################
## Cursor settings ##
#####################

cursor_color = (255, 255, 255)
large_step = 5 # Distance moved when holding control


####################
## Input settings ##
####################

# Delay when holding keys
# Delay in ms
initial_delay = 430 
repeat_time = 31


############################
## View movement (pixels) ##
############################

view_move_amount = 20
view_padding = 120

# Amount of lines rendered outside of visible range
# This is recommended to be left at default for performance
buffer_lines = 5


##################
## Line numbers ##
##################

line_numbers = True # enabled?

line_number_color = (121, 120, 125)
line_number_background_color = (28, 28, 33)

line_number_text_size = 13
line_number_width = 30

vertical_number_offset = 1


###################
## Miscellaneous ##
###################

# Spaces inserted when pressing tab
tab_spaces = 4

# Set this to the background color if you want to disable highlighting
current_line_highlight_color = (53, 50, 64) 