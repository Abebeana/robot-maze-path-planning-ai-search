# Robot Maze Path Planning - Makefile
# ===================================

# Use virtual environment Python if available, otherwise system python3
PYTHON ?= $(shell which python3)
CODE_DIR = code
RESULTS_DIR = results

# Default configuration
export MAZE_ROWS ?= 10
export MAZE_COLS ?= 15
export WALL_PROB ?= 0.3
export OUTPUT_DIR ?= ../results
export SAVE_ANIMATIONS ?= 0
export USE_FALLBACK ?= 0
export RANDOM_SEED ?=

.PHONY: all run run-fallback animate clean help bfs dfs gbfs astar

# Default target - run with fallback maze and animations
all: run-fallback animate
	@echo "✓ Complete! Check results/ for output files."

# Run with randomly generated maze
run:
	@echo "Running with random maze ($(MAZE_ROWS)x$(MAZE_COLS))..."
	cd $(CODE_DIR) && $(PYTHON) main.py

# Run with fallback maze (deterministic)
run-fallback:
	@echo "Running with fallback maze..."
	cd $(CODE_DIR) && USE_FALLBACK=1 $(PYTHON) main.py

# Generate animations with fallback maze
animate:
	@echo "Generating animations..."
	cd $(CODE_DIR) && USE_FALLBACK=1 SAVE_ANIMATIONS=1 $(PYTHON) main.py

# Run with custom 20x20 maze
run-large:
	@echo "Running with 20x20 maze..."
	cd $(CODE_DIR) && MAZE_ROWS=20 MAZE_COLS=20 SAVE_ANIMATIONS=1 $(PYTHON) main.py

# Run with dense walls
run-dense:
	@echo "Running with dense walls (0.4)..."
	cd $(CODE_DIR) && WALL_PROB=0.4 SAVE_ANIMATIONS=1 $(PYTHON) main.py

# Run with seed for reproducibility
run-seeded:
	@echo "Running with seed 42..."
	cd $(CODE_DIR) && RANDOM_SEED=42 $(PYTHON) main.py

# Clean generated files
clean:
	@echo "Cleaning results..."
	rm -f $(RESULTS_DIR)/*.txt
	rm -f $(RESULTS_DIR)/*.csv
	rm -f $(RESULTS_DIR)/*.png
	rm -f $(RESULTS_DIR)/animations/*.gif
	rm -rf $(CODE_DIR)/**/__pycache__
	rm -rf $(CODE_DIR)/__pycache__
	@echo "✓ Cleaned."

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install numpy matplotlib pillow
	@echo "✓ Dependencies installed."

# Help
help:
	@echo "Robot Maze Path Planning - Available targets:"
	@echo ""
	@echo "  make all          - Run with fallback maze and generate animations"
	@echo "  make run          - Run with randomly generated maze"
	@echo "  make run-fallback - Run with deterministic fallback maze"
	@echo "  make animate      - Generate animations with fallback maze"
	@echo "  make run-large    - Run with 20x20 maze + animations"
	@echo "  make run-dense    - Run with higher wall density (0.4)"
	@echo "  make run-seeded   - Run with random seed 42"
	@echo "  make clean        - Remove generated files"
	@echo "  make install      - Install Python dependencies"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Configuration via environment variables:"
	@echo "  MAZE_ROWS=N       - Number of rows (default: 10)"
	@echo "  MAZE_COLS=N       - Number of columns (default: 15)"
	@echo "  WALL_PROB=P       - Wall probability 0.0-1.0 (default: 0.3)"
	@echo "  SAVE_ANIMATIONS=1 - Save GIF animations"
	@echo "  USE_FALLBACK=1    - Use predefined fallback maze"
	@echo "  RANDOM_SEED=N     - Set random seed"
	@echo ""
	@echo "Examples:"
	@echo "  make run MAZE_ROWS=15 MAZE_COLS=20"
	@echo "  make run WALL_PROB=0.4 SAVE_ANIMATIONS=1"
