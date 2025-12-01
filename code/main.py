#!/usr/bin/env python3
"""
Robot Maze Path Planning using AI Search Algorithms

This project demonstrates four search algorithms:
1. BFS (Breadth-First Search) - Guarantees shortest path
2. DFS (Depth-First Search) - Does not guarantee shortest path
3. GBFS (Greedy Best-First Search) - Uses heuristic only
4. A* (A-Star Search) - Optimal, uses g(n) + h(n)

Configuration is done via environment variables (set by Makefile):
    MAZE_ROWS, MAZE_COLS, WALL_PROB, SAVE_ANIMATIONS, USE_FALLBACK, RANDOM_SEED
"""

import os
import sys
import csv

import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from search_algorithms import (
    bfs_search, dfs_search, gbfs_search, astar_search,
    generate_maze, FALLBACK_MAZE
)
from visualization import draw_comparison, save_maze_image, animate_search


# Configuration from environment variables (set by Makefile)
ROWS = int(os.environ.get('MAZE_ROWS', 10))
COLS = int(os.environ.get('MAZE_COLS', 15))
WALL_PROB = float(os.environ.get('WALL_PROB', 0.3))
SAVE_ANIMATIONS = os.environ.get('SAVE_ANIMATIONS', '0') == '1'
USE_FALLBACK = os.environ.get('USE_FALLBACK', '0') == '1'
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '../results')
_seed = os.environ.get('RANDOM_SEED', '')
RANDOM_SEED = int(_seed) if _seed else None


def run_all_algorithms(grid, start, goal):
    """
    Run all search algorithms on the given maze.
    
    Args:
        grid: 2D numpy array (0=free, 1=wall)
        start: Start cell (row, col)
        goal: Goal cell (row, col)
        
    Returns:
        Dict of {algorithm_name: SearchResult}
    """
    algorithms = {
        'BFS': bfs_search,
        'DFS': dfs_search,
        'GBFS': gbfs_search,
        'A*': astar_search
    }
    
    results = {}
    
    print("\n" + "=" * 60)
    print("RUNNING SEARCH ALGORITHMS")
    print("=" * 60)
    
    for name, search_func in algorithms.items():
        print(f"\nRunning {name}...")
        result = search_func(grid, start, goal)
        results[name] = result
        
        if result.success:
            print(f"  ✓ Path found!")
            print(f"    - Path length: {result.path_length}")
            print(f"    - Cells explored: {result.explored_count}")
            print(f"    - Execution time: {result.execution_time * 1000:.2f} ms")
        else:
            print(f"  ✗ No path found")
            print(f"    - Cells explored: {result.explored_count}")
    
    return results


def print_comparison_table(results):
    """Print a comparison table of all algorithm results."""
    print("\n" + "=" * 60)
    print("ALGORITHM COMPARISON")
    print("=" * 60)
    
    # Header
    print(f"\n{'Algorithm':<12} {'Path Length':<12} {'Explored':<12} {'Time (ms)':<12} {'Optimal?':<10}")
    print("-" * 58)
    
    # Find shortest path for optimality comparison
    successful = {k: v for k, v in results.items() if v.success}
    if successful:
        min_path = min(r.path_length for r in successful.values())
    else:
        min_path = 0
    
    for name, result in results.items():
        if result.success:
            is_optimal = "Yes" if result.path_length == min_path else "No"
            print(f"{name:<12} {result.path_length:<12} {result.explored_count:<12} "
                  f"{result.execution_time * 1000:<12.2f} {is_optimal:<10}")
        else:
            print(f"{name:<12} {'N/A':<12} {result.explored_count:<12} "
                  f"{result.execution_time * 1000:<12.2f} {'N/A':<10}")
    
    print("\n" + "-" * 58)
    print("Note: BFS and A* guarantee optimal (shortest) paths.")
    print("      DFS and GBFS do not guarantee optimal paths.")


def save_results(results, output_dir, grid, start, goal):
    """Save results to files."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'animations'), exist_ok=True)
    
    # Save paths to text files
    for name, result in results.items():
        if result.success:
            filename = os.path.join(output_dir, f"{name.lower().replace('*', 'star')}_path.txt")
            with open(filename, 'w') as f:
                f.write(f"Algorithm: {name}\n")
                f.write(f"Path Length: {result.path_length}\n")
                f.write(f"Cells Explored: {result.explored_count}\n")
                f.write(f"Execution Time: {result.execution_time * 1000:.2f} ms\n")
                f.write(f"\nPath:\n")
                for cell in result.path:
                    f.write(f"  {cell}\n")
            print(f"Saved: {filename}")
    
    # Save performance metrics to CSV
    csv_filename = os.path.join(output_dir, 'performance_metrics.csv')
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Algorithm', 'Path Length', 'Cells Explored', 
                        'Execution Time (ms)', 'Success'])
        for name, result in results.items():
            writer.writerow([
                name,
                result.path_length if result.success else 'N/A',
                result.explored_count,
                f"{result.execution_time * 1000:.2f}",
                result.success
            ])
    print(f"Saved: {csv_filename}")
    
    # Save comparison image
    comparison_filename = os.path.join(output_dir, 'algorithm_comparison.png')
    fig = draw_comparison(grid, results, start, goal)
    fig.savefig(comparison_filename, dpi=150, bbox_inches='tight')
    print(f"Saved: {comparison_filename}")


def save_animations(results, output_dir, grid, start, goal):
    """Save animations for all algorithms."""
    animations_dir = os.path.join(output_dir, 'animations')
    os.makedirs(animations_dir, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("SAVING ANIMATIONS")
    print("=" * 60)
    
    for name, result in results.items():
        if result.success:
            safe_name = name.lower().replace('*', 'star')
            filename = os.path.join(animations_dir, f"{safe_name}_animation.gif")
            print(f"\nGenerating {name} animation...")
            animate_search(grid, start, goal, result, name, 
                          filename=filename, interval=100)


def print_maze(grid, start, goal):
    """Print ASCII representation of the maze."""
    rows, cols = grid.shape
    print("\nMaze Layout:")
    print("  " + "".join(f"{c:2}" for c in range(cols)))
    print("  " + "-" * (cols * 2 + 1))
    
    for r in range(rows):
        row_str = f"{r:2}|"
        for c in range(cols):
            if (r, c) == start:
                row_str += "S "
            elif (r, c) == goal:
                row_str += "G "
            elif grid[r, c] == 1:
                row_str += "# "
            else:
                row_str += ". "
        print(row_str)
    
    print("\nLegend: S=Start, G=Goal, #=Wall, .=Free")


def main():
    """Main entry point."""
    # Set random seed if provided
    if RANDOM_SEED is not None:
        np.random.seed(RANDOM_SEED)
    
    print("=" * 60)
    print("ROBOT MAZE PATH PLANNING - AI SEARCH ALGORITHMS")
    print("=" * 60)
    
    # Generate or load maze
    if USE_FALLBACK:
        print("\nUsing fallback maze (10x15)...")
        grid = FALLBACK_MAZE.copy()
        rows, cols = grid.shape
    else:
        rows, cols = ROWS, COLS
        print(f"\nGenerating {rows}x{cols} maze (wall probability: {WALL_PROB})...")
        grid = generate_maze(rows, cols, wall_prob=WALL_PROB)
    
    # Define start and goal
    start = (0, 0)
    goal = (rows - 1, cols - 1)
    
    print(f"\nMaze size: {rows} x {cols}")
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    
    # Print ASCII maze
    print_maze(grid, start, goal)
    
    # Run all algorithms
    results = run_all_algorithms(grid, start, goal)
    
    # Print comparison
    print_comparison_table(results)
    
    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), OUTPUT_DIR)
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60 + "\n")
    
    save_results(results, output_dir, grid, start, goal)
    
    # Save animations if requested
    if SAVE_ANIMATIONS:
        save_animations(results, output_dir, grid, start, goal)
    
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
