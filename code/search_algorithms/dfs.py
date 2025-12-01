from collections import deque
from .utils import TrackedGridSearch, SearchResult


class DFS(TrackedGridSearch):
    """
    ---------------------------------------------------------
    DEPTH-FIRST SEARCH (DFS) WITH TRACKING
    ---------------------------------------------------------
    Explores the maze by going as deep as possible before backtracking.
    Does NOT guarantee shortest path.
    
    Inherits from TrackedGridSearch which provides:
    - Grid navigation utilities (in_bounds, is_free, etc.)
    - Tracking for visualization (visited_order, frontier_history)
    - Execution time measurement
    
    Visualization colors:
    - GREEN: Start cell
    - YELLOW: Goal cell
    - RED: Explored cells
    - BLUE: Frontier/Stack (to be explored)
    - GREY: Final path
    """
    
    def search(self, start, goal):
        """
        Perform DFS from start to goal.
        
        Args:
            start: Starting cell (row, col)
            goal: Goal cell (row, col)
            
        Returns:
            SearchResult containing path, visited order, frontier history, etc.
        """
        # Reset tracking for new search
        self.init_tracking()
        self.start_timer()
        
        # DFS data structures (using stack instead of queue)
        stack = [start]
        visited = set([start])
        parent = {start: None}
        
        while stack:
            # Record frontier/stack BEFORE popping (cells to be explored - BLUE)
            self.record_frontier(stack)
            
            # Pop and explore current cell (will be RED)
            r, c = stack.pop()
            self.record_explored((r, c))
            
            # Check if goal reached
            if (r, c) == goal:
                self.stop_timer()
                path = self.reconstruct_path(parent, goal)
                return self.create_result(path, success=True)
            
            # Explore neighbors (reversed to maintain left-to-right order)
            for dr, dc in reversed(self.directions):
                nr, nc = r + dr, c + dc
                
                if self.is_valid_move(nr, nc, visited):
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))
        
        # No path found
        self.stop_timer()
        return self.create_result([], success=False)


# Standalone function for backward compatibility
def dfs_search(grid, start, goal):
    """
    Convenience function to run DFS without creating a class instance.
    
    Args:
        grid: 2D grid (0 = free, 1 = wall)
        start: Starting cell (row, col)
        goal: Goal cell (row, col)
        
    Returns:
        SearchResult with path and tracking data
    """
    searcher = DFS(grid)
    return searcher.search(start, goal)
