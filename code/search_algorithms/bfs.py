from collections import deque
from .utils import TrackedGridSearch, SearchResult


class BFS(TrackedGridSearch):
    """
    ---------------------------------------------------------
    BREADTH-FIRST SEARCH (BFS) WITH TRACKING
    ---------------------------------------------------------
    Explores the maze level by level (shortest path in unweighted graph).
    
    Inherits from TrackedGridSearch which provides:
    - Grid navigation utilities (in_bounds, is_free, etc.)
    - Tracking for visualization (visited_order, frontier_history)
    - Execution time measurement
    
    Visualization colors:
    - GREEN: Start cell
    - YELLOW: Goal cell
    - RED: Explored cells
    - BLUE: Frontier (to be explored)
    - GREY: Final path
    """
    
    def search(self, start, goal):
        """
        Perform BFS from start to goal.
        
        Args:
            start: Starting cell (row, col)
            goal: Goal cell (row, col)
            
        Returns:
            SearchResult containing path, visited order, frontier history, etc.
        """
        # Reset tracking for new search
        self.init_tracking()
        self.start_timer()
        
        # BFS data structures
        queue = deque([start])
        visited = set([start])
        parent = {start: None}
        
        while queue:
            # Record frontier BEFORE popping (cells to be explored - BLUE)
            self.record_frontier(queue)
            
            # Pop and explore current cell (will be RED)
            r, c = queue.popleft()
            self.record_explored((r, c))
            
            # Check if goal reached
            if (r, c) == goal:
                self.stop_timer()
                path = self.reconstruct_path(parent, goal)
                return self.create_result(path, success=True)
            
            # Explore neighbors
            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                
                if self.is_valid_move(nr, nc, visited):
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))
        
        # No path found
        self.stop_timer()
        return self.create_result([], success=False)


# Standalone function for backward compatibility
def bfs_search(grid, start, goal):
    """
    Convenience function to run BFS without creating a class instance.
    
    Args:
        grid: 2D grid (0 = free, 1 = wall)
        start: Starting cell (row, col)
        goal: Goal cell (row, col)
        
    Returns:
        SearchResult with path and tracking data
    """
    searcher = BFS(grid)
    return searcher.search(start, goal)
