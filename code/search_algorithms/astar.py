import heapq
from .utils import TrackedGridSearch, SearchResult


class AStar(TrackedGridSearch):
    """
    ---------------------------------------------------------
    A* SEARCH WITH TRACKING
    ---------------------------------------------------------
    Combines actual cost (g) with heuristic estimate (h).
    f(n) = g(n) + h(n)
    
    GUARANTEES shortest path when heuristic is admissible
    (never overestimates the true cost).
    
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
    
    def __init__(self, grid, heuristic=None):
        """
        Initialize A*.
        
        Args:
            grid: 2D grid (0 = free, 1 = wall)
            heuristic: Function(cell, goal) -> cost. Defaults to Manhattan distance.
        """
        super().__init__(grid)
        self.heuristic = heuristic or self.manhattan_distance
    
    @staticmethod
    def manhattan_distance(cell, goal):
        """Manhattan distance heuristic (admissible for 4-direction movement)."""
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
    
    
    def calculate_priority(self, g_cost, cell, goal):
        """
        Calculate priority for the frontier.
        A*: f(n) = g(n) + h(n)
        
        Override this method in subclasses for different algorithms:
        - GBFS: return only h(n)
        - Dijkstra: return only g(n)
        """
        return g_cost + self.heuristic(cell, goal)
    
    def search(self, start, goal):
        """
        Perform A* Search from start to goal.
        
        Args:
            start: Starting cell (row, col)
            goal: Goal cell (row, col)
            
        Returns:
            SearchResult containing path, visited order, frontier history, etc.
        """
        # Reset tracking for new search
        self.init_tracking()
        self.start_timer()
        
        # Priority queue: (f_cost, counter, cell)
        # f(n) = g(n) + h(n)
        counter = 0
        g_cost = {start: 0}
        f_start = self.calculate_priority(0, start, goal)
        frontier = [(f_start, counter, start)]
        
        visited = set()
        parent = {start: None}
        
        while frontier:
            # Record frontier BEFORE popping (cells to be explored - BLUE)
            frontier_cells = [item[2] for item in frontier]
            self.record_frontier(frontier_cells)
            
            # Pop cell with lowest f-cost (will be RED)
            _, _, (r, c) = heapq.heappop(frontier)
            
            # Skip if already visited (may have been added with higher cost)
            if (r, c) in visited:
                continue
            
            visited.add((r, c))
            self.record_explored((r, c))
            
            # Check if goal reached
            if (r, c) == goal:
                self.stop_timer()
                path = self.reconstruct_path(parent, goal)
                return self.create_result(path, success=True)
            
            # Explore neighbors
            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                
                if not self.in_bounds(nr, nc) or not self.is_free(nr, nc):
                    continue
                
                if (nr, nc) in visited:
                    continue
                
                # Calculate new g cost (cost to reach neighbor through current cell)
                new_g = g_cost[(r, c)] + 1  # Assuming uniform cost of 1
                
                # If we found a better path to this neighbor
                if (nr, nc) not in g_cost or new_g < g_cost[(nr, nc)]:
                    g_cost[(nr, nc)] = new_g
                    f_cost = self.calculate_priority(new_g, (nr, nc), goal)
                    parent[(nr, nc)] = (r, c)
                    counter += 1
                    heapq.heappush(frontier, (f_cost, counter, (nr, nc)))
        
        # No path found
        self.stop_timer()
        return self.create_result([], success=False)


# Standalone function for backward compatibility
def astar_search(grid, start, goal, heuristic=None):
    """
    Convenience function to run A* without creating a class instance.
    
    Args:
        grid: 2D grid (0 = free, 1 = wall)
        start: Starting cell (row, col)
        goal: Goal cell (row, col)
        heuristic: Optional heuristic function
        
    Returns:
        SearchResult with path and tracking data
    """
    searcher = AStar(grid, heuristic)
    return searcher.search(start, goal)
