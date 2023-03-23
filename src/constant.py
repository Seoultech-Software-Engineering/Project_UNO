import pygame
from pathlib import Path

RESOURCE_PATH = Path.cwd() / 'resources'

EVENT_QUIT_GAME = pygame.event.custom_type()
EVENT_START_SINGLE = pygame.event.custom_type()
EVENT_OPEN_OPTION = pygame.event.custom_type()