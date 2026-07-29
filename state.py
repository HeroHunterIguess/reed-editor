### Editor states ###


from dataclasses import dataclass
import pygame

@dataclass
class editor_states:
    buffer: list
    cursor_location: list
    filepath: str
    history: list
    #history_pos: int = 0 # Currently unused since ther is no redo action
    last_y: int = 0
    changed: bool = False
    held_event: pygame.event.Event | None = None
    hold_time: int = 0
    waiting_for_initial: bool = False
    selecting: bool = False
    selection_start: tuple = (-1, -1)
    selection_end: tuple = (-1, -1)
