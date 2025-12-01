"""
Static grid visualization for maze and search results.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from .colors import COLOR_MAP, HEX_COLOR_MAP


def _draw_maze_on_ax(grid, start, goal, path, explored, title, ax):
    """Draw maze on a given axis."""
    rows, cols = grid.shape
    
    # Draw grid cells
    for r in range(rows):
        for c in range(cols):
            color = HEX_COLOR_MAP['wall'] if grid[r, c] == 1 else HEX_COLOR_MAP['free']
            rect = Rectangle((c, rows - 1 - r), 1, 1, 
                            facecolor=color, edgecolor='gray', linewidth=0.5)
            ax.add_patch(rect)
    
    # Draw explored cells (RED)-
    if explored:
        for cell in explored:
            if cell != start and cell != goal:
                r, c = cell
                rect = Rectangle((c, rows - 1 - r), 1, 1,
                                facecolor=HEX_COLOR_MAP['explored'], 
                                edgecolor='gray', linewidth=0.5)
                ax.add_patch(rect)
    
    # Draw path (GREY)
    if path:
        for cell in path:
            if cell != start and cell != goal:
                r, c = cell
                rect = Rectangle((c, rows - 1 - r), 1, 1,
                                facecolor=HEX_COLOR_MAP['path'], 
                                edgecolor='gray', linewidth=0.5)
                ax.add_patch(rect)
    
    # Draw start (GREEN)
    r, c = start
    rect = Rectangle((c, rows - 1 - r), 1, 1,
                    facecolor=HEX_COLOR_MAP['start'], 
                    edgecolor='darkgreen', linewidth=2)
    ax.add_patch(rect)
    ax.text(c + 0.5, rows - 1 - r + 0.5, 'S', 
           ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Draw goal (YELLOW)
    r, c = goal
    rect = Rectangle((c, rows - 1 - r), 1, 1,
                    facecolor=HEX_COLOR_MAP['goal'], 
                    edgecolor='orange', linewidth=2)
    ax.add_patch(rect)
    ax.text(c + 0.5, rows - 1 - r + 0.5, 'G', 
           ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Configure axes
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.grid(True, linewidth=0.5, color='gray', alpha=0.3)


def draw_comparison(grid, results, start, goal, figsize=(16, 12)):
    """
    Draw comparison of 4 search algorithm results (BFS, DFS, GBFS, A*).
    
    Args:
        grid: 2D numpy array (0=free, 1=wall)
        results: Dict of {algorithm_name: SearchResult}
        start: Start cell (row, col)
        goal: Goal cell (row, col)
        figsize: Figure size tuple
        
    Returns:
        fig: Matplotlib figure
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()
    
    for idx, (name, result) in enumerate(results.items()):
        title = f"{name}\nPath: {result.path_length}, Explored: {result.explored_count}"
        _draw_maze_on_ax(grid, start, goal, 
                        path=result.path if result.success else None,
                        explored=result.visited_order,
                        title=title, ax=axes[idx])
    
    plt.tight_layout()
    return fig


def save_maze_image(grid, start, goal, path=None, explored=None,
                    filename="maze.png", title="Maze", dpi=150):
    """Save maze visualization to an image file."""
    fig, ax = plt.subplots(figsize=(10, 8))
    _draw_maze_on_ax(grid, start, goal, path, explored, title, ax)
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {filename}")
