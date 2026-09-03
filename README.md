# Reed

![image](https://github.com/HeroHunterIguess/reed-editor/blob/main/images/showcase.png)

## General information

Reed is still early in development, but I plan to turn this into a finished (but remaining simple) text editor.
This will not have any advanced editing features or mouse usage, it will remain an extremely simple keyboard-only editor. 

This is made basically just for my personal use. For that reason I'm not trying to make this super optimized, and thats why I chose pygame. I simply wanted an easy to code, easy to use library to assist in my creation of this project.

Currently certain changes in the config.py file may cause unintended visual bugs. Minimal testing has been done on the configuration options. Different fonts may look weird in the editor, I have only tested with Monospace (linux default) and Noto Sans Mono

A more final release will be posted at a later date, right now there are a few pre-releases, but these are early versions that will not completely function as a full seamless editor. 

## Features

- Open any text file
- All basic text modifications
- Displays current column and character
- Line counter
- Full config file within users config directory for full customization
- Keyboard-centric design
- Selecting text
- Unsaved changes indicator
- `Ctrl+Del` or `Ctrl+Backspace` deletes whole word sections
- Fully copy paste function (and `Ctrl+C` with no selection copies all text in file)
- Auto scrolling & off-screen line culling

This editor still has many bugs, and issues that need to be fixed in the future. Some of this will be fixed far sooner than others. 

## Bugs/Issues
- Flickering when resizing window
- When selecting with shift, you cannot hit control to select whole words
- Certain buttons such as escape add a null character
- This may be a font issue, however many characters are null
- Tab is handled badly and tab characters are sometimes null
- Only monospace fonts work
- Pressing Ctrl + Down does not go to the end of the line when on the last line of file

**If you find more bugs or issues that need to be fixed, you can create a GitHub issue for me to review.**
