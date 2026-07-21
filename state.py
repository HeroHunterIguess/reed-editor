### Editor states ###


from dataclasses import dataclass
import pygame

@dataclass
class editor_states:
    buffer: list
    cursor_location: list
    filepath: str
    history: list
    history_pos: int = 0
    last_y: int = 0
    changed: bool = False
    held_event: pygame.event.Event | None = None
    hold_time: int = 0
    waiting_for_initial: bool = False
    selecting: bool = False
    selection_start: tuple = (0, 0)
    selection_end: tuple = (0, 0)
