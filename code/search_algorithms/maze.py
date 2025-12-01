"""
Maze Generator - generates random solvable mazes.
Uses BFS to validate paths.
"""

import numpy as np
from .bfs import bfs_search


# Fallback maze (10x15, known solvable)
FALLBACK_MAZE = np.array([
    [0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])


def has_valid_path(grid, start, goal):
    """Check if path exists using BFS."""
    return bfs_search(grid, start, goal).success


def generate_maze(rows, cols, start=None, goal=None, wall_prob=0.3):
    """
    Generate a random solvable maze.
    
    Args:
        rows, cols: Maze dimensions
        start: Start cell, defaults to (0, 0)
        goal: Goal cell, defaults to (rows-1, cols-1)
        wall_prob: Wall probability (0.0-1.0)
    
    Returns:
        numpy array (0=free, 1=wall)
    """
    start = start or (0, 0)
    goal = goal or (rows - 1, cols - 1)
    
    for attempt in range(100):
        grid = (np.random.random((rows, cols)) < wall_prob).astype(int)
        grid[start[0], start[1]] = 0
        grid[goal[0], goal[1]] = 0
        
        if has_valid_path(grid, start, goal):
            print(f"Maze generated after {attempt + 1} attempt(s)")
            return grid
    
    # Fallback
    print("Using fallback maze...")
    if rows == 10 and cols == 15:
        return FALLBACK_MAZE.copy()
    
    # Create L-shaped path
    grid = (np.random.random((rows, cols)) < wall_prob).astype(int)
    grid[start[0], start[1]] = 0
    grid[goal[0], goal[1]] = 0
    for i in range(rows):
        grid[i, 0] = 0
    for j in range(cols):
        grid[rows - 1, j] = 0
    return grid
