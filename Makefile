# Sonder Development Makefile
# =============================================================================

# Project configuration
PROJECT_NAME := sonder
PROJECT_ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PYTHON := python3
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip
SRC_DIR := src
TEST_DIR := tests
SCRIPTS_DIR := scripts

# Colors for output
BOLD := \033[1m
GREEN := \033[32m
BLUE := \033[34m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := help

# Phony targets
.PHONY: help install dev test test-verbose lint format type-check clean run setup check-deps init-db docker-build docker-run profile benchmark docs serve-docs

# =============================================================================
# Help and Information
# =============================================================================

help:  ## Show this help message with available commands
	@echo "$(BOLD)$(PROJECT_NAME) Development Commands$(RESET)"
	@echo "======================================"
	@echo ""
	@echo "$(BOLD)Setup & Installation:$(RESET)"
	@grep -E '^(setup|install|dev|init-db):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Development:$(RESET)"
	@grep -E '^(run|test|lint|format|type-check):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Maintenance:$(RESET)"
	@grep -E '^(clean|check-deps|profile|benchmark):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Documentation:$(RESET)"
	@grep -E '^(docs|serve-docs):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Docker:$(RESET)"
	@grep -E '^(docker-build|docker-run):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-18s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Setup & Installation
# =============================================================================

setup: check-deps install dev init-db  ## Complete initial project setup
	@echo "$(GREEN)✅ $(PROJECT_NAME) setup completed successfully!$(RESET)"
	@echo ""
	@echo "$(BOLD)Next steps:$(RESET)"
	@echo "  • Run '$(BLUE)make run$(RESET)' to start the simulation"
	@echo "  • Run '$(BLUE)make test$(RESET)' to verify everything works"
	@echo "  • Check out the notebooks/ directory for analysis tools"

check-deps:  ## Check for required system dependencies
	@echo "$(YELLOW)🔍 Checking system dependencies...$(RESET)"
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "$(RED)❌ Python 3.9+ required but not found$(RESET)"; exit 1; }
	@$(PYTHON) -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" || { echo "$(RED)❌ Python 3.9+ required$(RESET)"; exit 1; }
	@echo "$(GREEN)✅ System dependencies OK$(RESET)"

check-venv:  ## Check if virtual environment exists and is active
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Virtual environment not found. Run 'make install' first$(RESET)"; \
		exit 1; \
	fi

install:  ## Install the package in development mode
	@echo "$(YELLOW)🐍 Creating virtual environment @ .venv...$(RESET)"
	@$(PYTHON) -m venv .venv
	@echo "$(GREEN)✅ Virtual environment created$(RESET)"
	@echo "$(YELLOW)📦 Installing $(PROJECT_NAME) package...$(RESET)"
	@.venv/bin/python -m pip install --upgrade pip
	@.venv/bin/pip install -e .
	@echo "$(GREEN)✅ Package installed$(RESET)"
	@echo "$(BLUE)ℹ️  To activate: source .venv/bin/activate$(RESET)"

dev:  ## Install development and analytics dependencies
	@echo "$(YELLOW)🔧 Installing development dependencies...$(RESET)"
	@if [ ! -d ".venv" ]; then \
		echo "$(RED)❌ Virtual environment not found. Run 'make install' first$(RESET)"; \
		exit 1; \
	fi
	@.venv/bin/pip install -e ".[dev,analytics]"
	@echo "$(GREEN)✅ Development environment ready$(RESET)"

init-db: check-venv  ## Initialize the game database
	@echo "$(YELLOW)🗄️  Initializing game database...$(RESET)"
	@$(VENV_PYTHON) -c "from $(SRC_DIR).$(PROJECT_NAME).data.database import init_database; init_database()"
	@echo "$(GREEN)✅ Database initialized$(RESET)"

# =============================================================================
# Development Commands
# =============================================================================

run: check-venv  ## Start the game simulation
	@echo "$(YELLOW)🎮 Starting $(PROJECT_NAME) simulation...$(RESET)"
	@$(VENV_PYTHON) -m $(PROJECT_NAME)

run-observer: check-venv  ## Start in observer mode (watch-only)
	@echo "$(YELLOW)👁️  Starting $(PROJECT_NAME) in observer mode...$(RESET)"
	@$(VENV_PYTHON) -m $(PROJECT_NAME) --mode observer

run-interactive: check-venv  ## Start in interactive mode (player control)
	@echo "$(YELLOW)🕹️  Starting $(PROJECT_NAME) in interactive mode...$(RESET)"
	@$(VENV_PYTHON) -m $(PROJECT_NAME) --mode interactive

run-debug: check-venv  ## Start with debug output enabled
	@echo "$(YELLOW)🐛 Starting $(PROJECT_NAME) with debug logging...$(RESET)"
	@$(VENV_PYTHON) -m $(PROJECT_NAME) --debug

# =============================================================================
# Testing
# =============================================================================

test: check-venv  ## Run the test suite
	@echo "$(YELLOW)🧪 Running test suite...$(RESET)"
	@$(VENV_PYTHON) -m pytest $(TEST_DIR)/ -v --tb=short
	@echo "$(GREEN)✅ Tests completed$(RESET)"

test-verbose: check-venv  ## Run tests with verbose output and coverage
	@echo "$(YELLOW)🧪 Running comprehensive test suite...$(RESET)"
	@$(VENV_PYTHON) -m pytest $(TEST_DIR)/ -v --tb=long --cov=$(SRC_DIR)/$(PROJECT_NAME) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Tests completed with coverage report$(RESET)"
	@echo "📊 Coverage report: htmlcov/index.html"

test-watch: check-venv  ## Run tests in watch mode (requires pytest-watch)
	@echo "$(YELLOW)👀 Starting test watcher...$(RESET)"
	@$(VENV_PYTHON) -m pytest_watch -- $(TEST_DIR)/ -v

benchmark: check-venv  ## Run performance benchmarks
	@echo "$(YELLOW)⚡ Running performance benchmarks...$(RESET)"
	@$(VENV_PYTHON) -m pytest $(TEST_DIR)/benchmarks/ -v --benchmark-only
	@echo "$(GREEN)✅ Benchmarks completed$(RESET)"

# =============================================================================
# Code Quality
# =============================================================================

lint:  ## Run all linting checks
	@echo "$(YELLOW)🔍 Running linting checks...$(RESET)"
	@echo "  → flake8..."
	@$(PYTHON) -m flake8 $(SRC_DIR) $(TEST_DIR) --count --statistics
	@echo "  → isort check..."
	@$(PYTHON) -m isort --check-only --diff $(SRC_DIR) $(TEST_DIR)
	@echo "  → black check..."
	@$(PYTHON) -m black --check --diff $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Linting passed$(RESET)"

format:  ## Auto-format code with black and isort
	@echo "$(YELLOW)🎨 Formatting code...$(RESET)"
	@echo "  → Running black..."
	@$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR)
	@echo "  → Running isort..."
	@$(PYTHON) -m isort $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Code formatted$(RESET)"

type-check:  ## Run type checking with mypy
	@echo "$(YELLOW)🔍 Running type checking...$(RESET)"
	@$(PYTHON) -m mypy $(SRC_DIR)/$(PROJECT_NAME) --pretty
	@echo "$(GREEN)✅ Type checking passed$(RESET)"

quality: lint type-check  ## Run all code quality checks
	@echo "$(GREEN)✅ All quality checks passed$(RESET)"

# =============================================================================
# Maintenance
# =============================================================================

clean:  ## Clean build artifacts and cache files
	@echo "$(YELLOW)🧹 Cleaning build artifacts...$(RESET)"
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf htmlcov/ .coverage .pytest_cache/ .mypy_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@echo "$(GREEN)✅ Cleanup completed$(RESET)"

clean-db:  ## Clean database files (destructive!)
	@echo "$(RED)⚠️  WARNING: This will delete all game data!$(RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo ""; \
		echo "$(YELLOW)🗑️  Removing database files...$(RESET)"; \
		rm -f *.db *.db-wal *.db-shm; \
		echo "$(GREEN)✅ Database files removed$(RESET)"; \
	else \
		echo ""; \
		echo "$(BLUE)ℹ️  Database cleanup cancelled$(RESET)"; \
	fi

reset: clean clean-db init-db  ## Complete project reset (destructive!)
	@echo "$(GREEN)✅ Project reset completed$(RESET)"

profile:  ## Run performance profiling
	@echo "$(YELLOW)📊 Running performance profiling...$(RESET)"
	@$(PYTHON) -m cProfile -o profile.stats -m $(PROJECT_NAME) --mode observer --ticks 1000
	@$(PYTHON) -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
	@echo "$(GREEN)✅ Profiling completed$(RESET)"
	@echo "📈 Full profile saved to: profile.stats"

# =============================================================================
# Documentation
# =============================================================================

docs:  ## Build documentation
	@echo "$(YELLOW)📚 Building documentation...$(RESET)"
	@$(PYTHON) -m sphinx-build -b html docs/ docs/_build/html/
	@echo "$(GREEN)✅ Documentation built$(RESET)"
	@echo "📖 Documentation: docs/_build/html/index.html"

serve-docs:  ## Serve documentation locally
	@echo "$(YELLOW)🌐 Serving documentation at http://localhost:8000$(RESET)"
	@cd docs/_build/html && $(PYTHON) -m http.server 8000

# =============================================================================
# Docker Support
# =============================================================================

docker-build:  ## Build Docker container
	@echo "$(YELLOW)🐳 Building Docker container...$(RESET)"
	@docker build -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✅ Docker container built$(RESET)"

docker-run:  ## Run simulation in Docker container
	@echo "$(YELLOW)🐳 Running $(PROJECT_NAME) in Docker...$(RESET)"
	@docker run -it --rm $(PROJECT_NAME):latest

docker-dev:  ## Run development environment in Docker
	@echo "$(YELLOW)🐳 Starting development container...$(RESET)"
	@docker run -it --rm -v $(PWD):/app -w /app $(PROJECT_NAME):dev /bin/bash

# =============================================================================
# Advanced Development
# =============================================================================

notebook:  ## Start Jupyter notebook server
	@echo "$(YELLOW)📓 Starting Jupyter notebook server...$(RESET)"
	@$(PYTHON) -m jupyter notebook notebooks/

install-hooks:  ## Install git pre-commit hooks
	@echo "$(YELLOW)🔗 Installing pre-commit hooks...$(RESET)"
	@$(PYTHON) -m pre_commit install
	@echo "$(GREEN)✅ Pre-commit hooks installed$(RESET)"

release-check: quality test  ## Check if ready for release
	@echo "$(GREEN)✅ Release checks passed$(RESET)"
	@echo "$(BOLD)Ready for release!$(RESET)"

# =============================================================================
# Utility Functions
# =============================================================================

show-config:  ## Show current project configuration
	@echo "$(BOLD)Project Configuration:$(RESET)"
	@echo "  Project Name: $(PROJECT_NAME)"
	@echo "  Project Root: $(PROJECT_ROOT)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  Pip: $(shell $(PIP) --version)"
	@echo "  Source Dir: $(SRC_DIR)"
	@echo "  Test Dir: $(TEST_DIR)"

show-deps:  ## Show installed package dependencies
	@echo "$(YELLOW)📋 Installed packages:$(RESET)"
	@$(PIP) list --format=columns

# =============================================================================
# Development Shortcuts
# =============================================================================

quick: format lint test  ## Quick development cycle (format, lint, test)
	@echo "$(GREEN)✅ Quick development cycle completed$(RESET)"

full-check: clean quality test-verbose benchmark  ## Full quality and performance check
	@echo "$(GREEN)✅ Full project check completed$(RESET)"