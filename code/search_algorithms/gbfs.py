import heapq
from typing import override
from .astar import AStar
from .utils import SearchResult


class GBFS(AStar):
    """
    ---------------------------------------------------------
    GREEDY BEST-FIRST SEARCH (GBFS) WITH TRACKING
    ---------------------------------------------------------
    Uses ONLY heuristic to guide search toward the goal.
    f(n) = h(n)  (ignores g-cost)
    
    Does NOT guarantee shortest path.
    
    Inherits from AStar and overrides calculate_priority to ignore g-cost.
    
    Visualization colors:
    - GREEN: Start cell
    - YELLOW: Goal cell
    - RED: Explored cells
    - BLUE: Frontier (to be explored)
    - GREY: Final path
    """
    @override
    def calculate_priority(self, g_cost, cell, goal):
        """
        GBFS priority: f(n) = h(n) only
        Ignores the actual cost (g) - greedy approach.
        """
        return self.heuristic(cell, goal)


# Standalone function for backward compatibility
def gbfs_search(grid, start, goal, heuristic=None):
    """
    Convenience function to run GBFS without creating a class instance.
    
    Args:
        grid: 2D grid (0 = free, 1 = wall)
        start: Starting cell (row, col)
        goal: Goal cell (row, col)
        heuristic: Optional heuristic function
        
    Returns:
        SearchResult with path and tracking data
    """
    searcher = GBFS(grid, heuristic)
    return searcher.search(start, goal)
