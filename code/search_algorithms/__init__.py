"""
Search algorithms module for maze path planning.
"""

from .utils import SearchResult, TrackingMixin, GridSearchBase, TrackedGridSearch
from .bfs import BFS, bfs_search
from .dfs import DFS, dfs_search
from .astar import AStar, astar_search
from .gbfs import GBFS, gbfs_search
from .maze import generate_maze, has_valid_path, FALLBACK_MAZE

__all__ = [
    # Base classes
    'SearchResult',
    'TrackingMixin',
    'GridSearchBase',
    'TrackedGridSearch',
    # BFS
    'BFS',
    'bfs_search',
    # DFS
    'DFS',
    'dfs_search',
    # A*
    'AStar',
    'astar_search',
    # GBFS
    'GBFS',
    'gbfs_search',
    # Maze generation
    'generate_maze',
    'has_valid_path',
    'FALLBACK_MAZE'
]
