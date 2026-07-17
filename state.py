### Editor states ###

from dataclasses import dataclass
import pygame

@dataclass
class editor_states:
    buffer: list
    cursor_location: list
    filepath: str
    last_y: int = 0
    changed: bool = False
    held_event: pygame.event.Event | None = None
    hold_time: int = 0
    waiting_for_initial: bool = False
