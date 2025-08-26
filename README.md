# Sonder 🐸

> _The realization that each random passerby is living a life as vivid and complex as your own_

A life simulation game with evolution mechanics, where simple creatures grow, adapt, and evolve in a persistent world. Watch emergent behaviors unfold as entities interact, compete, and develop new traits over time.

## Features

### Core Simulation

- **Entity-Component-System Architecture**: Flexible, modular design for complex behaviors
- **Real-time Evolution**: Creatures adapt and mutate based on environmental pressures
- **Persistent World**: All events logged to DuckDB for analysis and continuity
- **Emergent Behavior**: Complex interactions arise from simple rules

### Gameplay Modes

- **Observer Mode**: Watch the simulation unfold autonomously
- **Interactive Mode**: Control a creature and influence the world
- **God Mode**: Spawn entities, modify environment, analyze patterns
- **Analytics Mode**: Deep dive into evolution patterns and statistics

### Technical Highlights

- **Performance Optimized**: Spatial partitioning for thousands of entities
- **Modular Design**: Easy to add new creatures, behaviors, and mechanics
- **Rich Terminal UI**: Beautiful ASCII visualization with real-time stats
- **Data-Driven**: Comprehensive event logging for research and analysis

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/sonder.git
cd sonder
make setup

# Run the simulation
make run

# Or start in observer mode
python -m sonder --mode observer

# Run tests
make test
```

## Project Structure

```
sonder/
├── src/sonder/           # Core game engine
│   ├── core/            # Game loop, world management, config
│   ├── entity/          # Entity definitions and registry
│   ├── component/       # Reusable entity components
│   ├── system/          # Game systems (movement, combat, etc.)
│   ├── ui/              # Terminal interface and rendering
│   ├── data/            # Database models and persistence
│   └── analytics/       # Data analysis and metrics
├── modules/             # Extension modules
│   ├── fantasy/         # Dragons, wizards, magic systems
│   └── scifi/           # Robots, aliens, technology
├── tests/               # Comprehensive test suite
├── notebooks/           # Jupyter analysis notebooks
└── scripts/             # Development utilities
```

## Development Roadmap

### Phase 1: Core Foundation ✅

- [x] Project structure and packaging
- [x] Entity-Component-System implementation
- [x] Basic game loop with tick management
- [x] DuckDB integration and schema
- [x] Simple terminal display

### Phase 2: Game Mechanics 🚧

- [ ] Movement and collision detection
- [ ] Combat system (attack/defense calculations)
- [ ] Basic evolution mechanics (stat increases)
- [ ] Entity spawning system
- [ ] Event logging to DuckDB

### Phase 3: User Interface 📋

- [ ] Rich-based TUI with game visualization
- [ ] Player controls implementation
- [ ] Real-time statistics display
- [ ] Game mode switching
- [ ] Simulation controls (pause/speed/reset)

### Phase 4: Advanced Features 🔮

- [ ] Complex evolution trees with branching paths
- [ ] Different entity types with unique behaviors
- [ ] Environmental effects and power-ups
- [ ] Configurable game parameters
- [ ] Save/load game states

### Phase 5: Analytics Layer 📊

- [ ] Comprehensive event tracking
- [ ] Performance metrics collection
- [ ] Analysis notebooks and visualizations
- [ ] Data export for external tools
- [ ] Evolution pattern analysis

## Architecture Deep Dive

### Entity-Component-System (ECS)

**Entities** are unique identifiers with position and components:

```python
frog = Frog(x=10, y=5)
frog.add_component(StatsComponent(health=20, attack=3))
frog.add_component(MovementComponent())
frog.add_component(BasicAI())
```

**Components** hold data and simple logic:

```python
@dataclass
class StatsComponent(Component):
    health: int = 10
    attack: int = 1
    defense: int = 0
```

**Systems** operate on entities with specific components:

```python
class MovementSystem(System):
    def update(self, world_state):
        for entity in entities_with(MovementComponent):
            # Handle movement logic
```

### Performance Considerations

- **Spatial Partitioning**: O(1) neighbor queries for large entity counts
- **Batch Processing**: Systems process entities in batches for cache efficiency
- **Component Pooling**: Reuse component instances to reduce GC pressure
- **Configurable Complexity**: Scale simulation detail based on performance needs

### Data Persistence

All game events flow into DuckDB for analysis:

```sql
-- Track entity evolution over time
SELECT generation, AVG(attack), AVG(defense), AVG(health)
FROM evolution_events
GROUP BY generation
ORDER BY generation;

-- Analyze survival patterns
SELECT entity_type, AVG(lifespan), COUNT(*) as population
FROM entity_lifecycle
GROUP BY entity_type;
```

## Contributing

Thoughts and contributions are welcome! Feel free to fork or star

### Development Setup

```bash
# Install development dependencies
make dev

# Run the full test suite
make test

# Format code
make format

# Run linting
make lint

# Clean build artifacts
make clean
```

### Adding New Entities

1. Create entity class in `src/sonder/entity/`
2. Define required components
3. Register in `entity_registry`
4. Add tests in `tests/entity/`

```python
class Wolf(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)
        self.add_component(StatsComponent(health=30, attack=8))
        self.add_component(PackHuntingAI())
        self.add_tag("predator")
```

### Creating Custom Systems

```python
class PackHuntingSystem(System):
    def update(self, world_state):
        # Find wolves near each other
        # Coordinate hunting behavior
        # Apply pack bonuses
```

## Philosophy

Sonder explores emergence, adaptation, and the beauty of complex systems arising from simple rules. Each entity lives its own "life" - making decisions, facing challenges, and leaving traces in the world's history.

The goal isn't to create a traditional game with win conditions, but rather a living laboratory where you can:

- Observe natural selection in action
- Experiment with different evolutionary pressures
- Discover unexpected behaviors and strategies
- Analyze the data to understand complex systems

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by Conway's Game of Life and artificial life research
- Built with modern Python tooling and best practices
- Uses DuckDB for high-performance analytics
- Terminal UI powered by Rich

---

## Stay Connected

[![Read On](https://img.shields.io/badge/Read%20On-Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://www.linkedin.com/in/chrisadan/)
[![Connect On](https://img.shields.io/badge/Connect%20On-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/chrisadan/)

---

_"In the end, we're all just trying to survive and evolve. What stories will your simulation tell?"_

---

```bash
Note: This README was automatically generated by Claude.ai
```
