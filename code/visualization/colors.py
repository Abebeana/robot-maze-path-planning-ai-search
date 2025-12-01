"""
Color constants for maze visualization.

Color scheme:
- GREEN: Start cell
- YELLOW: Goal cell
- RED: Explored/visited cells
- BLUE: Frontier cells (to be explored)
- GREY: Final path
- WHITE: Free cells
- BLACK: Wall cells
"""

# RGB tuples (0-1 range for matplotlib)
GREEN = (0.2, 0.8, 0.2)      # Start
YELLOW = (1.0, 0.9, 0.2)     # Goal
RED = (0.9, 0.3, 0.3)        # Explored
BLUE = (0.3, 0.5, 0.9)       # Frontier
GREY = (0.5, 0.5, 0.5)       # Final path
WHITE = (1.0, 1.0, 1.0)      # Free cell
BLACK = (0.1, 0.1, 0.1)      # Wall

# Hex colors (for matplotlib patches)
HEX_GREEN = '#33CC33'
HEX_YELLOW = '#FFEE33'
HEX_RED = '#E64D4D'
HEX_BLUE = '#4D80E6'
HEX_GREY = '#808080'
HEX_WHITE = '#FFFFFF'
HEX_BLACK = '#1A1A1A'

# Color mapping dictionary
COLOR_MAP = {
    'start': GREEN,
    'goal': YELLOW,
    'explored': RED,
    'frontier': BLUE,
    'path': GREY,
    'free': WHITE,
    'wall': BLACK
}

HEX_COLOR_MAP = {
    'start': HEX_GREEN,
    'goal': HEX_YELLOW,
    'explored': HEX_RED,
    'frontier': HEX_BLUE,
    'path': HEX_GREY,
    'free': HEX_WHITE,
    'wall': HEX_BLACK
}
