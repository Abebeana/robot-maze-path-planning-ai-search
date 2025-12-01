from collections import deque
from dataclasses import dataclass, field
import time


@dataclass
class SearchResult:
    """
    Data class to store all results from a search algorithm.
    Used for visualization and analysis.
    """
    path: list = field(default_factory=list)
    visited_order: list = field(default_factory=list)
    frontier_history: list = field(default_factory=list)
    explored_count: int = 0
    path_length: int = 0
    execution_time: float = 0.0
    success: bool = False
    
    def __post_init__(self):
        self.explored_count = len(self.visited_order)
        self.path_length = len(self.path)


class TrackingMixin:
    """
    -----------------------------------------------------
    MIXIN FOR TRACKING SEARCH PROGRESS
    -----------------------------------------------------
    Provides tracking functionality for:
    - visited_order: cells in the order they were explored (RED)
    - frontier_history: frontier state at each step (BLUE)
    - execution time measurement
    
    Use this mixin with GridSearchBase to enable animation support.
    
    Colors in visualization:
    - GREEN: Start cell
    - YELLOW: Goal cell  
    - RED: Explored/visited cells
    - BLUE: Frontier cells (to be explored)
    - GREY: Final path
    """
    
    def init_tracking(self):
        """Initialize tracking data structures."""
        self.visited_order = []
        self.frontier_history = []
        self._start_time = 0.0
        self._end_time = 0.0
    
    def start_timer(self):
        """Start execution timer."""
        self._start_time = time.perf_counter()
    
    def stop_timer(self):
        """Stop execution timer."""
        self._end_time = time.perf_counter()
    
    def get_execution_time(self):
        """Get execution time in seconds."""
        return self._end_time - self._start_time
    
    def record_explored(self, cell):
        """Record a cell as explored (will be shown in RED)."""
        self.visited_order.append(cell)
    
    def record_frontier(self, frontier):
        """
        Record the current state of the frontier (will be shown in BLUE).
        
        Args:
            frontier: List of cells
        """
        self.frontier_history.append(list(frontier))
    
    def create_result(self, path, success=True):
        """
        Create a SearchResult object with all tracking data.
        
        Args:
            path: The final path from start to goal
            success: Whether the search found a path
            
        Returns:
            SearchResult with all tracking information
        """
        return SearchResult(
            path=path,
            visited_order=self.visited_order.copy(),
            frontier_history=[f.copy() for f in self.frontier_history],
            explored_count=len(self.visited_order),
            path_length=len(path),
            execution_time=self.get_execution_time(),
            success=success
        )


class GridSearchBase:
    """
    ---------------------------------------------------------
    BASE CLASS FOR GRID SEARCH ALGORITHMS
    ---------------------------------------------------------
    This class stores:
    - the grid
    - helper functions (in_bounds, is_free)
    - allowed movement directions

    BFS and DFS will inherit from this class.
    """
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        # 4-direction movement (no diagonals)
        self.directions = [
            (0, 1),   # right
            (0, -1),  # left
            (1, 0),   # down
            (-1, 0)   # up
        ]

    def in_bounds(self, r, c):
        """Check that (r, c) is inside the grid."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, r, c):
        """Check that the cell is not a wall (0 = free, 1 = wall)."""
        return self.grid[r][c] == 0
    
    def is_valid_move(self, r, c, visited):
        """Check if a move to (r, c) is valid."""
        return (self.in_bounds(r, c) and 
                self.is_free(r, c) and 
                (r, c) not in visited)

    def reconstruct_path(self, parent, goal):
        """
        Reconstruct path by following parent pointers
        from the goal → back to the start.
        """
        path = []
        cur = goal

        while cur is not None:
            path.append(cur)
            cur = parent[cur]

        return path[::-1]  # reverse to get start → goal
    
    def get_neighbors(self, r, c):
        """Get all valid neighboring cells."""
        neighbors = []
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.is_free(nr, nc):
                neighbors.append((nr, nc))
        return neighbors


class TrackedGridSearch(GridSearchBase, TrackingMixin):
    """
    ---------------------------------------------------------
    GRID SEARCH WITH FULL TRACKING SUPPORT
    ---------------------------------------------------------
    Combines GridSearchBase with TrackingMixin for algorithms
    that need animation/visualization support.
    
    Usage:
        class BFS(TrackedGridSearch):
            def search(self, start, goal):
                self.init_tracking()
                self.start_timer()
                # ... search logic ...
                self.stop_timer()
                return self.create_result(path)
    """
    
    def __init__(self, grid):
        GridSearchBase.__init__(self, grid)
        self.init_tracking()
