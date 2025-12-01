"""
Animation generation for search algorithm visualization.

Colors:
- GREEN: Start cell
- YELLOW: Goal cell
- RED: Explored/visited cells
- BLUE: Frontier cells (to be explored)
- GREY: Final path
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
from .colors import HEX_COLOR_MAP


class SearchAnimator:
    """
    Creates step-by-step animations of search algorithms.
    """
    
    def __init__(self, grid, start, goal, result, algorithm_name="Search"):
        """
        Initialize animator.
        
        Args:
            grid: 2D numpy array (0=free, 1=wall)
            start: Start cell (row, col)
            goal: Goal cell (row, col)
            result: SearchResult from a search algorithm
            algorithm_name: Name of the algorithm for title
        """
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.start = start
        self.goal = goal
        self.result = result
        self.algorithm_name = algorithm_name
        
        # Cell rectangles for animation updates
        self.cell_patches = {}
        
    def _setup_base_grid(self, ax):
        """Draw the initial grid with walls and free cells."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] == 1:
                    color = HEX_COLOR_MAP['wall']
                else:
                    color = HEX_COLOR_MAP['free']
                
                rect = Rectangle((c, self.rows - 1 - r), 1, 1,
                                facecolor=color, edgecolor='gray', 
                                linewidth=0.5)
                ax.add_patch(rect)
                self.cell_patches[(r, c)] = rect
        
        # Draw start (GREEN) - always visible
        r, c = self.start
        self.cell_patches[(r, c)].set_facecolor(HEX_COLOR_MAP['start'])
        ax.text(c + 0.5, self.rows - 1 - r + 0.5, 'S',
               ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw goal (YELLOW) - always visible
        r, c = self.goal
        self.cell_patches[(r, c)].set_facecolor(HEX_COLOR_MAP['goal'])
        ax.text(c + 0.5, self.rows - 1 - r + 0.5, 'G',
               ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.set_aspect('equal')
        ax.set_xticks(range(self.cols + 1))
        ax.set_yticks(range(self.rows + 1))
        ax.grid(True, linewidth=0.3, color='gray', alpha=0.3)
        
    def create_animation(self, interval=100, figsize=(10, 8)):
        """
        Create a step-by-step animation of the search.
        
        Args:
            interval: Time between frames in milliseconds
            figsize: Figure size tuple
            
        Returns:
            FuncAnimation object
        """
        fig, ax = plt.subplots(figsize=figsize)
        self._setup_base_grid(ax)
        
        title = ax.set_title(f"{self.algorithm_name} - Step 0", 
                            fontsize=14, fontweight='bold')
        
        visited_order = self.result.visited_order
        frontier_history = self.result.frontier_history
        path = self.result.path
        
        # Calculate total frames: exploration + path drawing
        n_explore_frames = len(visited_order)
        n_path_frames = len(path) if self.result.success else 0
        total_frames = n_explore_frames + n_path_frames + 10  # +10 for pause at end
        
        # Track explored cells across frames
        explored_so_far = set()
        
        def update(frame):
            if frame < n_explore_frames:
                # Exploration phase
                step = frame
                
                # Reset previous frontier cells to free/explored
                if step > 0 and step - 1 < len(frontier_history):
                    for cell in frontier_history[step - 1]:
                        if cell not in explored_so_far and cell != self.start and cell != self.goal:
                            if self.grid[cell[0], cell[1]] == 0:
                                self.cell_patches[cell].set_facecolor(HEX_COLOR_MAP['free'])
                
                # Mark current explored cell (RED)
                if step < len(visited_order):
                    cell = visited_order[step]
                    explored_so_far.add(cell)
                    if cell != self.start and cell != self.goal:
                        self.cell_patches[cell].set_facecolor(HEX_COLOR_MAP['explored'])
                
                # Mark current frontier (BLUE)
                if step < len(frontier_history):
                    for cell in frontier_history[step]:
                        if cell not in explored_so_far and cell != self.start and cell != self.goal:
                            if self.grid[cell[0], cell[1]] == 0:
                                self.cell_patches[cell].set_facecolor(HEX_COLOR_MAP['frontier'])
                
                title.set_text(f"{self.algorithm_name} - Exploring: Step {step + 1}/{n_explore_frames}")
                
            elif frame < n_explore_frames + n_path_frames:
                # Path drawing phase
                path_step = frame - n_explore_frames
                
                # Clear frontier colors first (only on first path frame)
                if path_step == 0:
                    for cell in explored_so_far:
                        if cell != self.start and cell != self.goal:
                            self.cell_patches[cell].set_facecolor(HEX_COLOR_MAP['explored'])
                
                # Draw path cells (GREY)
                for i in range(path_step + 1):
                    cell = path[i]
                    if cell != self.start and cell != self.goal:
                        self.cell_patches[cell].set_facecolor(HEX_COLOR_MAP['path'])
                
                title.set_text(f"{self.algorithm_name} - Drawing Path: {path_step + 1}/{n_path_frames}")
                
            else:
                # Final state - show complete result
                stats = f"Path: {len(path)}, Explored: {len(visited_order)}"
                title.set_text(f"{self.algorithm_name} - Complete! {stats}")
            
            return list(self.cell_patches.values())
        
        anim = FuncAnimation(fig, update, frames=total_frames,
                           interval=interval, blit=False, repeat=False)
        
        return anim, fig
    
    def save_animation(self, filename, interval=100, figsize=(10, 8), dpi=100):
        """
        Save animation to a GIF file.
        
        Args:
            filename: Output filename (should end in .gif)
            interval: Time between frames in milliseconds
            figsize: Figure size tuple
            dpi: Resolution
        """
        anim, fig = self.create_animation(interval, figsize)
        
        # Save as GIF
        print(f"Saving animation to {filename}...")
        anim.save(filename, writer='pillow', fps=1000//interval, dpi=dpi)
        plt.close(fig)
        print(f"Saved: {filename}")


def animate_search(grid, start, goal, result, algorithm_name="Search",
                   filename=None, interval=100, figsize=(10, 8)):
    """
    Convenience function to create and optionally save a search animation.
    
    Args:
        grid: 2D numpy array (0=free, 1=wall)
        start: Start cell (row, col)
        goal: Goal cell (row, col)
        result: SearchResult from a search algorithm
        algorithm_name: Name of the algorithm
        filename: If provided, saves animation to this file
        interval: Time between frames in milliseconds
        figsize: Figure size tuple
        
    Returns:
        FuncAnimation object if filename is None, otherwise None
    """
    animator = SearchAnimator(grid, start, goal, result, algorithm_name)
    
    if filename:
        animator.save_animation(filename, interval, figsize)
        return None
    else:
        anim, fig = animator.create_animation(interval, figsize)
        return anim
