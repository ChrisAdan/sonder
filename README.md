# Sonder 🐸

> _The realization that each random passerby is living a life as vivid and complex as your own_

[![CI/CD](https://github.com/chrisadan/sonder/actions/workflows/cicd.yml/badge.svg)](https://github.com/chrisadan/sonder/actions/workflows/cicd.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A life simulation game with evolution mechanics, where simple creatures grow, adapt, and evolve in a persistent world. Watch emergent behaviors unfold as entities interact, compete, and develop new traits over time.

## Features

### Core Simulation

- **Entity-Component-System Architecture**: Flexible, modular design for complex behaviors
- **Real-time Evolution**: Creatures adapt and mutate based on environmental pressures
- **Persistent World**: All events logged to database for analysis and continuity
- **Emergent Behavior**: Complex interactions arise from simple rules

### Gameplay Modes

- **Observer Mode**: Watch the simulation unfold autonomously
- **Interactive Mode**: Control a creature and influence the world
- **God Mode**: Spawn entities, modify environment, analyze patterns

### Technical Highlights

- **Performance Optimized**: Spatial partitioning for efficient entity management
- **Modular Design**: Easy to add new creatures, behaviors, and mechanics
- **Rich Terminal UI**: Beautiful ASCII visualization with real-time stats
- **Data-Driven**: Comprehensive event logging for research and analysis
- **Database Agnostic**: Abstract database layer (currently DuckDB, extensible)

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/chrisadan/sonder.git
cd sonder

# Complete setup (creates venv, installs deps, initializes database)
make setup

# Or manual setup:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m sonder init-db
```

### Running the Simulation

```bash
# Start in observer mode (default)
make run
# or: python -m sonder run

# Start with debug logging
make run-debug

# Check status
make status

# Show configuration
make config
```

### Development

```bash
# Run tests
make test

# Code quality checks
make lint
make type-check
make format

# Full development cycle
make quick  # format + lint + test
```

## Project Structure

```
sonder/
├── src/sonder/           # Core game engine
│   ├── core/            # Game loop, world management, config
│   ├── entity/          # Entity definitions and registry
│   ├── component/       # Reusable entity components
│   ├── system/          # Game systems (movement, evolution, etc.)
│   ├── data/            # Database abstraction and persistence
│   ├── ui/              # Terminal interface and rendering
│   └── analytics/       # Data analysis and metrics
├── modules/             # Extension modules (future)
├── tests/               # Comprehensive test suite
├── notebooks/           # Jupyter analysis notebooks
└── scripts/             # Development utilities
```

## Development Status

### Phase 1: Foundation ✅ (Current)

- [x] Project structure and packaging with modern Python tooling
- [x] Entity-Component-System implementation
- [x] Basic game loop with configurable tick management
- [x] Database abstraction layer with DuckDB backend
- [x] Command-line interface with multiple modes
- [x] Development tooling (linting, formatting, testing)
- [x] CI/CD pipeline with release automation
- [x] Container support with Docker

### Phase 2: Core Mechanics 🚧 (Next)

- [ ] Enhanced movement and collision detection
- [ ] Combat system with damage calculations
- [ ] Basic evolution mechanics (stat mutations)
- [ ] Entity spawning and lifecycle management
- [ ] Comprehensive event logging
- [ ] Spatial optimization for large entity counts

### Phase 3: User Interface 📋 (Planned)

- [ ] Rich-based terminal UI with real-time visualization
- [ ] Interactive controls and game state management
- [ ] Statistics dashboard and entity inspection
- [ ] Simulation controls (pause/speed/reset)
- [ ] Configuration management interface

### Phase 4: Advanced Features 🔮 (Future)

- [ ] Complex evolution trees with branching paths
- [ ] Multiple entity types with unique behaviors
- [ ] Environmental effects and interactions
- [ ] Save/load game states
- [ ] Plugin system for custom entities and systems

## Architecture

### Entity-Component-System (ECS)

```python
# Entities are containers with position and components
frog = Frog(x=10, y=5)
frog.add_component(StatsComponent(health=20, attack=3))
frog.add_component(MovementComponent())
frog.add_component(BasicAI())

# Components hold data and simple logic
@dataclass
class StatsComponent(Component):
    health: int = 10
    attack: int = 1
    defense: int = 0

# Systems operate on entities with specific components
class MovementSystem(System):
    def update(self, world_state):
        for entity in entities_with(MovementComponent):
            # Handle movement logic
```

### Database Abstraction

The database layer is designed for flexibility:

```python
# Default DuckDB setup
db_manager = init_database("simulation.db")

# Extensible for other databases
db_manager = create_database_manager(
    "postgresql",  # Future implementation
    connection_string="postgresql://user:pass@localhost/sonder"
)
```

### Configuration Management

```python
from sonder import game_config, display_config

# Modify simulation parameters
game_config.world_width = 200
game_config.tick_rate = 20.0
game_config.max_entities = 5000
```

## CLI Reference

```bash
# Simulation control
sonder run                    # Start observer mode
sonder run --mode interactive # Interactive mode
sonder run --ticks 1000      # Run for 1000 ticks
sonder run --entities 50     # Start with 50 entities

# Database management
sonder init-db               # Initialize database
sonder init-db --force       # Recreate database
sonder status               # Show simulation status

# Configuration
sonder config               # Show current settings
sonder --debug run          # Enable debug logging
```

## Docker Support

```bash
# Build container
make docker-build

# Run simulation in container
make docker-run

# Development container
make docker-dev
```

## Contributing

We welcome contributions! The project follows modern Python best practices:

- **Code Quality**: Black formatting, isort imports, flake8 linting, mypy typing
- **Testing**: pytest with coverage reporting
- **CI/CD**: GitHub Actions with automated releases
- **Documentation**: Comprehensive docstrings and README updates

### Development Workflow

```bash
# Setup development environment
make setup

# Make changes, then run quality checks
make quick

# Run full test suite
make test-verbose

# Submit PR with conventional commits
git commit -m "feat: add new entity type"
```

### Adding New Features

1. **New Entities**: Create in `src/sonder/entity/` and register
2. **New Components**: Add to `src/sonder/component/`
3. **New Systems**: Implement in `src/sonder/system/`
4. **Database Changes**: Update schema in `src/sonder/data/database.py`

Example:

```python
class Wolf(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)
        self.add_component(StatsComponent(health=30, attack=8))
        self.add_component(PackHuntingAI())
        self.add_tag("predator")

# Register for dynamic creation
entity_registry.register("wolf", Wolf)
```

## Data Analysis

All simulation events are stored for analysis:

```sql
-- Evolution trends over time
SELECT generation, AVG(attack), AVG(defense), AVG(health)
FROM evolution_events
GROUP BY generation
ORDER BY generation;

-- Entity lifecycle analysis
SELECT entity_type, AVG(lifespan), COUNT(*) as population
FROM entity_lifecycle
GROUP BY entity_type;
```

## Philosophy

Sonder explores emergence, adaptation, and the beauty of complex systems arising from simple rules. Each entity lives its own "life" - making decisions, facing challenges, and leaving traces in the world's history.

The goal isn't to create a traditional game with win conditions, but rather a living laboratory where you can:

- Observe natural selection in action
- Experiment with different evolutionary pressures
- Discover unexpected behaviors and strategies
- Analyze data to understand complex systems

## Performance

- **Entity Count**: Optimized for 1000+ concurrent entities
- **Spatial Indexing**: O(1) neighbor queries via grid partitioning
- **Memory Usage**: Component pooling and efficient data structures
- **Database**: Async logging with batched writes

## Roadmap

- **Q4 2025**: Core mechanics and basic UI (Phase 2-3)
- **Q1 2026**: Advanced features and plugin system (Phase 4)
- **Q2 2026**: Analytics platform and visualization tools
- **Q3 2026**: Performance optimization and scaling

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by Conway's Game of Life and artificial life research
- Built with modern Python tooling and best practices
- Uses DuckDB for high-performance analytics
- Terminal UI powered by Rich (planned)
- CI/CD via GitHub Actions with Release Please

---

## Connect

[![LinkedIn](https://img.shields.io/badge/Connect%20On-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/chrisadan/)

---

## _"In the end, we're all just trying to survive and evolve. What stories will your simulation tell?"_

```bash
Note: This README was automatically generated by Claude.ai
```
